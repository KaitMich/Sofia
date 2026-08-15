"""
Passive Fact Extraction System (Pure Extraction - No Storage)

Purpose: Extract structured facts from Wikipedia articles using pattern matching.
Philosophy: Passive, non-intrusive extraction that feeds into corroboration_engine.

IMPORTANT: This module ONLY extracts facts. It does NOT store or validate them.
           Validation happens in corroboration_engine.py through multi-source consensus.

Key Principles:
- Extraction happens in BACKGROUND (Sophia doesn't notice)
- Facts are passed to corroboration_engine for validation
- No duplicate storage systems - single source of truth

Created: 2026-01-04
Author: Claude Code
Modified: 2026-01-04 - Stripped to pure extraction, integrated with corroboration_engine
"""

import re
from bs4 import BeautifulSoup
from typing import List, Dict


class FactExtractor:
    """
    Extracts structured facts from Wikipedia HTML content using pattern matching.

    Extraction Patterns:
    - Definitions: "X is a Y"
    - Properties: "X has Y"
    - Relationships: "X is used in Y", "X relates to Y"
    - Quantities: "X makes up N% of Y"
    - Origins: "X was created/formed in Y"

    NOTE: This is pure extraction. Validation through multi-source consensus
          happens in corroboration_engine.py.
    """

    def extract_facts_from_html(self, html_content: str, url: str, topic: str = None) -> List[Dict]:
        """
        Extract facts from Wikipedia HTML content.

        Args:
            html_content: Raw HTML from Wikipedia page
            url: Source URL (for metadata only)
            topic: Main topic of the page (e.g., "Silicon")

        Returns:
            List of extracted facts with metadata (NOT stored, just returned)
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get main content (Wikipedia article body)
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            return []

        # Extract text from paragraphs (skip infoboxes, navigation)
        paragraphs = content_div.find_all('p', recursive=True)
        text_blocks = []
        for p in paragraphs:
            # Skip empty paragraphs
            text = p.get_text().strip()
            if text and len(text) > 20:  # Minimum length
                text_blocks.append(text)

        # If no topic provided, try to get it from title
        if not topic:
            title_elem = soup.find('h1', {'id': 'firstHeading'})
            if title_elem:
                topic = title_elem.get_text().strip()

        # Extract facts from text
        facts = []
        for text in text_blocks[:10]:  # First 10 paragraphs (most important)
            extracted = self._extract_facts_from_text(text, topic)
            facts.extend(extracted)

        return facts

    def _extract_facts_from_text(self, text: str, topic: str = None) -> List[Dict]:
        """
        Extract facts using pattern matching.

        Patterns:
        - "X is a Y" (definition)
        - "X is an Y" (definition)
        - "X has Y" (property)
        - "X contains Y" (composition)
        - "X makes up N% of Y" (quantity)
        - "X is used in Y" (application)
        """
        facts = []

        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()

        # Split into sentences
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Too short
                continue

            # Pattern 1: "X is a/an Y" (definitions)
            match = re.search(r'^([A-Z][a-zA-Z\s]+?)\s+(?:is|are)\s+(?:a|an)\s+([a-z][a-zA-Z\s,]+?)(?:\.|,|that|which|with)', sentence)
            if match:
                subject = match.group(1).strip()
                definition = match.group(2).strip()
                facts.append({
                    "type": "definition",
                    "subject": subject,
                    "text": f"{subject} is a {definition}",
                    "sentence": sentence,
                    "topic": topic
                })

            # Pattern 2: "X has/have Y" (properties)
            match = re.search(r'([A-Z][a-zA-Z\s]+?)\s+(?:has|have)\s+([a-z][a-zA-Z\s,]+?)(?:\.|,|and|or)', sentence)
            if match:
                subject = match.group(1).strip()
                property_text = match.group(2).strip()
                facts.append({
                    "type": "property",
                    "subject": subject,
                    "text": f"{subject} has {property_text}",
                    "sentence": sentence,
                    "topic": topic
                })

            # Pattern 3: "X contains Y" (composition)
            match = re.search(r'([A-Z][a-zA-Z\s]+?)\s+(?:contains|consists of|comprises)\s+([a-z0-9][a-zA-Z\s,%-]+?)(?:\.|,|and|or)', sentence)
            if match:
                subject = match.group(1).strip()
                composition = match.group(2).strip()
                facts.append({
                    "type": "composition",
                    "subject": subject,
                    "text": f"{subject} contains {composition}",
                    "sentence": sentence,
                    "topic": topic
                })

            # Pattern 4: "makes up N%" (quantities)
            match = re.search(r'([A-Z][a-zA-Z\s]+?)\s+makes up\s+([\d.]+%)\s+of\s+([a-zA-Z\s]+)', sentence)
            if match:
                subject = match.group(1).strip()
                percentage = match.group(2).strip()
                target = match.group(3).strip()
                facts.append({
                    "type": "quantity",
                    "subject": subject,
                    "text": f"{subject} makes up {percentage} of {target}",
                    "sentence": sentence,
                    "topic": topic
                })

            # Pattern 5: "X is used in/for Y" (applications)
            match = re.search(r'([A-Z][a-zA-Z\s]+?)\s+is used\s+(?:in|for)\s+([a-z][a-zA-Z\s,]+?)(?:\.|,|and|or)', sentence)
            if match:
                subject = match.group(1).strip()
                application = match.group(2).strip()
                facts.append({
                    "type": "application",
                    "subject": subject,
                    "text": f"{subject} is used in {application}",
                    "sentence": sentence,
                    "topic": topic
                })

        return facts


def extract_facts_passive(html_content: str, url: str, topic: str = None) -> List[Dict]:
    """
    Convenience function for passive fact extraction.
    Call this during saturation learning - it returns extracted facts.

    Args:
        html_content: HTML from Wikipedia page
        url: Source URL
        topic: Main topic (optional)

    Returns:
        List of extracted facts (caller should feed to corroboration_engine)
    """
    extractor = FactExtractor()
    facts = extractor.extract_facts_from_html(html_content, url, topic)
    return facts
