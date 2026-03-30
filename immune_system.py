#!/usr/bin/env python3
"""
Immune System - Page-Level Threat Detection Through Passive Observation

REFACTORED: Focuses ONLY on unique page-level analysis, does NOT duplicate
AlphaWall or linguistic_warfare functionality.

Unique capabilities:
- HTML structure analysis (hidden elements, suspicious scripts, redirects)
- Content quality metrics (ad density, code ratio, paywall detection)
- Source/domain-level signals (TLD reputation, URL patterns)
- Integration with trust_database for domain reputation

What this does NOT do (delegated to existing systems):
- Text-based threat detection → AlphaWall
- Linguistic manipulation detection → linguistic_warfare
- Chunk-level quarantine → quarantine_layer

Key principle: Accepts existing security results as input, focuses on page structure.
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import numpy as np


@dataclass
class ThreatSignal:
    """Individual threat signal detected in content."""
    signal_type: str          # 'structure', 'quality', 'source', 'security'
    severity: float           # 0.0 to 1.0
    confidence: float         # How confident in this signal
    description: str          # Human-readable description
    evidence: List[str]       # Specific evidence found
    pattern_id: str          # Which pattern triggered this


@dataclass
class ThreatAssessment:
    """Complete threat assessment for a page."""
    url: str
    overall_threat_score: float    # 0.0 (safe) to 1.0 (dangerous)
    confidence: float              # Confidence in this assessment
    threat_signals: List[ThreatSignal]
    recommendation: str            # 'ALLOW', 'REVIEW', 'BLOCK'
    reasoning: List[str]           # Step-by-step reasoning
    timestamp: str
    domain_trust: Optional[float] = None  # From trust_database

    def to_dict(self) -> Dict:
        """Convert to dictionary for logging."""
        return {
            'url': self.url,
            'overall_threat_score': self.overall_threat_score,
            'confidence': self.confidence,
            'threat_signals': [asdict(sig) for sig in self.threat_signals],
            'recommendation': self.recommendation,
            'reasoning': self.reasoning,
            'timestamp': self.timestamp,
            'domain_trust': self.domain_trust
        }


@dataclass
class FactRisk:
    """Risk assessment for a specific fact before memory commit."""
    fact_text: str
    risk_score: float             # 0.0 (safe) to 1.0 (risky)
    confidence: float
    risk_factors: List[str]       # What makes this risky
    contradictions: List[str]     # Contradicts existing knowledge
    corroboration_needed: bool    # Needs more sources
    recommendation: str           # 'COMMIT', 'DEFER', 'REJECT'
    timestamp: str

    def to_dict(self) -> Dict:
        """Convert to dictionary for logging."""
        return asdict(self)


class ImmuneSystem:
    """
    Page-level immune system analyzing HTML structure, content quality, and source reputation.

    DOES NOT duplicate AlphaWall/linguistic_warfare - focuses on page-level concerns.
    """

    def __init__(self, data_dir: str = "data", trust_database=None):
        print("🛡️ Initializing Page-Level Immune System...")

        self.data_dir = Path(data_dir)
        self.immune_dir = self.data_dir / "immune"
        self.immune_dir.mkdir(parents=True, exist_ok=True)

        # Trust database integration (optional)
        self.trust_db = trust_database

        # Load pattern weights (for self-correction)
        self.pattern_weights_file = self.immune_dir / "pattern_weights.json"
        self.pattern_weights = self._load_pattern_weights()

        # Initialize ONLY page-level threat patterns (no text analysis)
        self._init_threat_patterns()

        print("✅ Page-Level Immune System initialized (structure, quality, source analysis)")

    def _load_pattern_weights(self) -> Dict[str, float]:
        """Load pattern weights (adjusted by self-correction)."""
        if self.pattern_weights_file.exists():
            try:
                with open(self.pattern_weights_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load pattern weights: {e}")

        # Default weights (1.0 = normal strength)
        return {
            'hidden_elements': 1.0,
            'suspicious_scripts': 1.0,
            'redirects': 1.0,
            'ad_density': 1.0,
            'paywall': 1.0,
            'code_ratio': 1.0,
            'low_content_quality': 1.0,
            'suspicious_domain': 1.0
        }

    def _save_pattern_weights(self):
        """Save updated pattern weights."""
        try:
            with open(self.pattern_weights_file, 'w') as f:
                json.dump(self.pattern_weights, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save pattern weights: {e}")

    def _init_threat_patterns(self):
        """Initialize ONLY page-level threat patterns (HTML structure, not text content)."""

        # HTML structure patterns (UNIQUE to immune system)
        self.structure_patterns = {
            'hidden_elements': {
                'patterns': [
                    r'display:\s*none',
                    r'visibility:\s*hidden',
                    r'opacity:\s*0',
                    r'position:\s*absolute.*left:\s*-\d+',
                ],
                'severity': 0.4
            },
            'suspicious_scripts': {
                'patterns': [
                    r'eval\s*\(',
                    r'document\.write\s*\(',
                    r'window\.location\s*=',
                    r'<iframe[^>]*hidden',
                    r'<script[^>]*src=["\']data:',
                ],
                'severity': 0.7
            },
            'redirects': {
                'patterns': [
                    r'<meta[^>]*http-equiv=["\']refresh',
                    r'window\.location\.replace',
                    r'window\.location\.href\s*=',
                ],
                'severity': 0.5
            }
        }

        # Content quality indicators (UNIQUE to immune system)
        self.quality_patterns = {
            'ad_indicators': [
                'advertisement', 'sponsored', 'promoted', 'ad-container',
                'google_ads', 'adsense', 'ad-slot', 'adsbygoogle'
            ],
            'paywall_indicators': [
                'paywall', 'subscribe to read', 'subscription required', 'members only',
                'premium content', 'sign in to continue', 'login to view'
            ],
            'low_quality_indicators': [
                'click here', 'you won\'t believe', 'shocking discovery',
                'doctors hate', 'one weird trick', 'what happens next'
            ]
        }

        # REMOVED: linguistic_patterns - this is AlphaWall/warfare's job!
        # REMOVED: manipulation detection - AlphaWall handles this!
        # REMOVED: emotional manipulation - linguistic_warfare handles this!

    def analyze_page(self, url: str, html_content: str, extracted_text: str,
                     alphawall_result: Optional[Dict] = None,
                     warfare_result: Optional[Dict] = None) -> ThreatAssessment:
        """
        Analyze a web page for PAGE-LEVEL threats through passive observation.

        Focus: HTML structure, content quality, source reputation
        Does NOT analyze text content (that's AlphaWall's job)

        Args:
            url: The URL of the page
            html_content: Raw HTML content
            extracted_text: Cleaned text (for quality metrics only, not threat detection)
            alphawall_result: Optional result from AlphaWall (threat_score, threat_type)
            warfare_result: Optional result from linguistic_warfare

        Returns:
            ThreatAssessment with page-level threat analysis
        """
        threat_signals = []
        reasoning = []

        # Get domain trust score if available
        domain_trust = None
        if self.trust_db:
            try:
                domain = urlparse(url).netloc
                domain_trust = self.trust_db.get_trust(domain)
                reasoning.append(f"Domain trust score: {domain_trust:.2f}")
            except Exception as e:
                print(f"⚠️ Error getting domain trust: {e}")

        # 1. HTML structure analysis (UNIQUE to immune system)
        structure_signals = self._analyze_structure(url, html_content)
        threat_signals.extend(structure_signals)
        if structure_signals:
            reasoning.append(f"Found {len(structure_signals)} HTML structure concerns")

        # 2. Content quality analysis (UNIQUE to immune system)
        quality_signals = self._analyze_content_quality(url, html_content, extracted_text)
        threat_signals.extend(quality_signals)
        if quality_signals:
            reasoning.append(f"Detected {len(quality_signals)} content quality issues")

        # 3. Source/domain signals (UNIQUE to immune system)
        source_signals = self._analyze_source_signals(url)
        threat_signals.extend(source_signals)
        if source_signals:
            reasoning.append(f"Detected {len(source_signals)} source reputation concerns")

        # 4. Incorporate existing security system results (if provided)
        if alphawall_result:
            threat_signals.append(ThreatSignal(
                signal_type='security',
                severity=alphawall_result.get('threat_score', 0.0),
                confidence=0.9,
                description=f"AlphaWall threat detected: {alphawall_result.get('threat_type', 'unknown')}",
                evidence=[f"AlphaWall score: {alphawall_result.get('threat_score', 0.0):.2f}"],
                pattern_id='alphawall_integration'
            ))
            reasoning.append(f"AlphaWall detected threats: {alphawall_result.get('threat_type', 'unknown')}")

        if warfare_result:
            threat_signals.append(ThreatSignal(
                signal_type='security',
                severity=warfare_result.get('threat_score', 0.0),
                confidence=0.9,
                description="Linguistic warfare patterns detected",
                evidence=warfare_result.get('threats_detected', [])[:3],
                pattern_id='warfare_integration'
            ))
            reasoning.append(f"Linguistic warfare score: {warfare_result.get('threat_score', 0.0):.2f}")

        # Calculate overall threat score
        if threat_signals:
            # Weight each signal by pattern weight and severity
            weighted_scores = []
            for signal in threat_signals:
                pattern_weight = self.pattern_weights.get(signal.pattern_id, 1.0)
                weighted_score = signal.severity * signal.confidence * pattern_weight
                weighted_scores.append(weighted_score)

            overall_threat_score = min(1.0, sum(weighted_scores) / len(weighted_scores) * 1.5)
            confidence = sum(sig.confidence for sig in threat_signals) / len(threat_signals)
        else:
            overall_threat_score = 0.0
            confidence = 0.8  # High confidence when nothing found
            reasoning.append("No page-level threats detected - HTML structure and quality appear safe")

        # Factor in domain trust (low trust increases threat score)
        if domain_trust is not None and domain_trust < 0.5:
            trust_penalty = (0.5 - domain_trust) * 0.3  # Max 0.15 penalty
            overall_threat_score = min(1.0, overall_threat_score + trust_penalty)
            reasoning.append(f"Low domain trust ({domain_trust:.2f}) increases caution")

        # Determine recommendation
        if overall_threat_score >= 0.7:
            recommendation = 'BLOCK'
            reasoning.append(f"HIGH RISK: Threat score {overall_threat_score:.2f} - blocking page")
        elif overall_threat_score >= 0.4:
            recommendation = 'REVIEW'
            reasoning.append(f"MEDIUM RISK: Threat score {overall_threat_score:.2f} - flagging for review")
        else:
            recommendation = 'ALLOW'
            reasoning.append(f"LOW RISK: Threat score {overall_threat_score:.2f} - allowing page")

        return ThreatAssessment(
            url=url,
            overall_threat_score=overall_threat_score,
            confidence=confidence,
            threat_signals=threat_signals,
            recommendation=recommendation,
            reasoning=reasoning,
            timestamp=datetime.utcnow().isoformat(),
            domain_trust=domain_trust
        )

    def _analyze_structure(self, url: str, html_content: str) -> List[ThreatSignal]:
        """Analyze HTML structure for suspicious patterns (UNIQUE capability)."""
        signals = []

        for pattern_id, pattern_info in self.structure_patterns.items():
            evidence = []

            for pattern in pattern_info['patterns']:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    evidence.extend([str(m)[:50] for m in matches[:3]])  # Keep first 3 examples, truncate

            if evidence:
                pattern_weight = self.pattern_weights.get(pattern_id, 1.0)
                adjusted_severity = pattern_info['severity'] * pattern_weight

                signals.append(ThreatSignal(
                    signal_type='structure',
                    severity=adjusted_severity,
                    confidence=0.8,
                    description=f"Detected {pattern_id.replace('_', ' ')} in HTML structure",
                    evidence=evidence,
                    pattern_id=pattern_id
                ))

        return signals

    def _analyze_content_quality(self, url: str, html_content: str, extracted_text: str) -> List[ThreatSignal]:
        """Analyze content quality indicators (UNIQUE capability)."""
        signals = []

        # Ad density analysis
        ad_count = sum(1 for indicator in self.quality_patterns['ad_indicators']
                      if indicator.lower() in html_content.lower())

        if ad_count > 5:
            pattern_weight = self.pattern_weights.get('ad_density', 1.0)
            signals.append(ThreatSignal(
                signal_type='quality',
                severity=min(0.6, ad_count / 20) * pattern_weight,
                confidence=0.7,
                description=f"High ad density detected ({ad_count} ad indicators)",
                evidence=[f"{ad_count} advertising elements found"],
                pattern_id='ad_density'
            ))

        # Paywall detection (informational, low severity)
        paywall_matches = [indicator for indicator in self.quality_patterns['paywall_indicators']
                          if indicator.lower() in extracted_text.lower()]

        if paywall_matches:
            pattern_weight = self.pattern_weights.get('paywall', 1.0)
            signals.append(ThreatSignal(
                signal_type='quality',
                severity=0.3 * pattern_weight,  # Paywalls not dangerous, just limiting
                confidence=0.8,
                description="Paywall detected - content may be incomplete",
                evidence=paywall_matches[:3],
                pattern_id='paywall'
            ))

        # Content/code ratio (high code = suspicious)
        if html_content and extracted_text:
            code_length = len(html_content)
            text_length = len(extracted_text)

            if text_length > 0:
                code_ratio = code_length / text_length

                if code_ratio > 20:  # 20:1 code to content is suspicious
                    pattern_weight = self.pattern_weights.get('code_ratio', 1.0)
                    signals.append(ThreatSignal(
                        signal_type='quality',
                        severity=min(0.7, code_ratio / 50) * pattern_weight,
                        confidence=0.6,
                        description=f"Very high code-to-content ratio ({code_ratio:.1f}:1)",
                        evidence=[f"HTML: {code_length} chars, Text: {text_length} chars"],
                        pattern_id='code_ratio'
                    ))

        # Low quality content indicators (clickbait patterns)
        low_quality_matches = [indicator for indicator in self.quality_patterns['low_quality_indicators']
                               if indicator.lower() in extracted_text.lower()]

        if len(low_quality_matches) >= 2:
            pattern_weight = self.pattern_weights.get('low_content_quality', 1.0)
            signals.append(ThreatSignal(
                signal_type='quality',
                severity=0.5 * pattern_weight,
                confidence=0.7,
                description="Low-quality content patterns detected (clickbait)",
                evidence=low_quality_matches[:3],
                pattern_id='low_content_quality'
            ))

        return signals

    def _analyze_source_signals(self, url: str) -> List[ThreatSignal]:
        """Analyze source-level signals (domain, TLD, etc.) (UNIQUE capability)."""
        signals = []

        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Suspicious TLDs (not blocked, just flagged)
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click']

            for tld in suspicious_tlds:
                if domain.endswith(tld):
                    pattern_weight = self.pattern_weights.get('suspicious_domain', 1.0)
                    signals.append(ThreatSignal(
                        signal_type='source',
                        severity=0.3 * pattern_weight,
                        confidence=0.6,
                        description=f"Domain uses potentially suspicious TLD: {tld}",
                        evidence=[domain],
                        pattern_id='suspicious_domain'
                    ))
                    break

            # Very long domains (often used in phishing)
            if len(domain) > 50:
                pattern_weight = self.pattern_weights.get('suspicious_domain', 1.0)
                signals.append(ThreatSignal(
                    signal_type='source',
                    severity=0.4 * pattern_weight,
                    confidence=0.7,
                    description=f"Unusually long domain name ({len(domain)} chars)",
                    evidence=[domain],
                    pattern_id='suspicious_domain'
                ))

            # Excessive subdomains (possible subdomain takeover or obfuscation)
            subdomain_count = domain.count('.')
            if subdomain_count > 4:
                pattern_weight = self.pattern_weights.get('suspicious_domain', 1.0)
                signals.append(ThreatSignal(
                    signal_type='source',
                    severity=0.3 * pattern_weight,
                    confidence=0.6,
                    description=f"Excessive subdomains ({subdomain_count})",
                    evidence=[domain],
                    pattern_id='suspicious_domain'
                ))

            # IP address instead of domain (suspicious for web content)
            ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
            if re.match(ip_pattern, domain):
                pattern_weight = self.pattern_weights.get('suspicious_domain', 1.0)
                signals.append(ThreatSignal(
                    signal_type='source',
                    severity=0.5 * pattern_weight,
                    confidence=0.8,
                    description="Using IP address instead of domain name",
                    evidence=[domain],
                    pattern_id='suspicious_domain'
                ))

        except Exception as e:
            print(f"⚠️ Error analyzing source signals: {e}")

        return signals

    def analyze_fact(self, fact_text: str, embedding: np.ndarray, source_url: str,
                     domain_trust: Optional[float] = None) -> FactRisk:
        """
        Evaluate a specific fact before committing to memory.

        Args:
            fact_text: The text of the fact
            embedding: Vector embedding of the fact (for similarity checks)
            source_url: URL where fact was found
            domain_trust: Optional trust score from trust_database

        Returns:
            FactRisk assessment with recommendation
        """
        risk_factors = []
        contradictions = []
        risk_score = 0.0

        # 1. Check for absolute statements (often wrong)
        absolute_words = ['always', 'never', 'all', 'none', 'every', 'impossible', 'certainly', 'definitely']
        found_absolutes = [word for word in absolute_words if word in fact_text.lower()]

        if found_absolutes:
            risk_factors.append(f"Contains absolute language: {', '.join(found_absolutes)}")
            risk_score += 0.2

        # 2. Check for unverifiable claims
        unverifiable_patterns = [
            r'they say', r'people say', r'sources claim', r'reportedly',
            r'allegedly', r'rumors suggest', r'it is believed'
        ]

        for pattern in unverifiable_patterns:
            if re.search(pattern, fact_text, re.IGNORECASE):
                risk_factors.append(f"Contains unverifiable claim indicator: {pattern}")
                risk_score += 0.3
                break

        # 3. Check for numerical precision (too precise often suspicious)
        numbers = re.findall(r'\d+\.\d{3,}', fact_text)  # 3+ decimal places
        if numbers:
            risk_factors.append(f"Suspiciously precise numbers: {numbers[0]}")
            risk_score += 0.1

        # 4. Check fact length (very long facts are complex and risky)
        if len(fact_text) > 300:
            risk_factors.append(f"Fact is very long ({len(fact_text)} chars) - complex claims need corroboration")
            risk_score += 0.15

        # 5. Factor in domain trust
        if domain_trust is not None:
            if domain_trust < 0.3:
                risk_factors.append(f"Source has low trust score ({domain_trust:.2f})")
                risk_score += 0.3
            elif domain_trust < 0.5:
                risk_factors.append(f"Source has below-average trust ({domain_trust:.2f})")
                risk_score += 0.15
        else:
            risk_factors.append(f"Source trust unknown for: {urlparse(source_url).netloc}")
            risk_score += 0.1  # Small penalty for unknown sources

        # Calculate final risk score
        risk_score = min(1.0, risk_score)
        confidence = 0.7  # Moderate confidence in this analysis

        # Determine if corroboration needed
        corroboration_needed = risk_score > 0.3 or len(risk_factors) > 2

        # Make recommendation
        if risk_score >= 0.7:
            recommendation = 'REJECT'
        elif corroboration_needed:
            recommendation = 'DEFER'  # Need more sources
        else:
            recommendation = 'COMMIT'

        return FactRisk(
            fact_text=fact_text[:200],  # Truncate for storage
            risk_score=risk_score,
            confidence=confidence,
            risk_factors=risk_factors,
            contradictions=contradictions,
            corroboration_needed=corroboration_needed,
            recommendation=recommendation,
            timestamp=datetime.utcnow().isoformat()
        )

    def update_pattern_weight(self, pattern_id: str, adjustment: float, reason: str):
        """
        Update pattern weight based on self-correction feedback.

        Args:
            pattern_id: ID of pattern to adjust
            adjustment: Delta to apply (-1.0 to +1.0)
            reason: Why this adjustment is being made
        """
        if pattern_id not in self.pattern_weights:
            print(f"⚠️ Unknown pattern ID: {pattern_id}")
            return

        old_weight = self.pattern_weights[pattern_id]
        new_weight = max(0.1, min(2.0, old_weight + adjustment))  # Clamp to 0.1-2.0

        self.pattern_weights[pattern_id] = new_weight
        self._save_pattern_weights()

        print(f"🔧 Adjusted pattern '{pattern_id}': {old_weight:.2f} → {new_weight:.2f} ({reason})")

    def get_pattern_weights(self) -> Dict[str, float]:
        """Get current pattern weights (for audit/export)."""
        return self.pattern_weights.copy()


# Testing function
if __name__ == "__main__":
    print("🧪 Testing Refactored Immune System...")
    print("=" * 70)

    immune = ImmuneSystem()

    # Test 1: Clean content (should pass)
    print("\n1️⃣ Testing clean content...")
    clean_html = """
    <html>
    <head><title>Science Article</title></head>
    <body>
        <article>
            <h1>The Importance of Scientific Method</h1>
            <p>This is a well-written article about the scientific method and its applications.</p>
            <p>Research shows that systematic approaches lead to better understanding.</p>
        </article>
    </body>
    </html>
    """
    clean_text = "The Importance of Scientific Method. This is a well-written article about the scientific method and its applications. Research shows that systematic approaches lead to better understanding."

    assessment1 = immune.analyze_page("https://science.edu/article", clean_html, clean_text)
    print(f"   Threat score: {assessment1.overall_threat_score:.2f}")
    print(f"   Recommendation: {assessment1.recommendation}")
    print(f"   Signals: {len(assessment1.threat_signals)}")
    assert assessment1.recommendation == 'ALLOW', "Clean content should be allowed"
    print("   ✅ PASS")

    # Test 2: Suspicious HTML structure (should flag)
    print("\n2️⃣ Testing suspicious HTML structure...")
    suspicious_html = """
    <html><body>
    <div style="display:none">Hidden tracking pixel</div>
    <div style="visibility:hidden">More hidden content</div>
    <script>eval(atob('malicious'));</script>
    <script>document.write('<iframe src="evil.com" hidden></iframe>');</script>
    <meta http-equiv="refresh" content="0;url=http://redirect.com">
    <p>Some visible content here</p>
    </body></html>
    """

    assessment2 = immune.analyze_page("https://suspicious.xyz/page", suspicious_html, "Some visible content here")
    print(f"   Threat score: {assessment2.overall_threat_score:.2f}")
    print(f"   Signals found: {len(assessment2.threat_signals)}")
    for sig in assessment2.threat_signals:
        print(f"      - {sig.signal_type}: {sig.description}")
    print(f"   Recommendation: {assessment2.recommendation}")
    assert len(assessment2.threat_signals) >= 3, "Should detect multiple structure issues"
    assert assessment2.overall_threat_score > 0.4, "Should have elevated threat score"
    print("   ✅ PASS")

    # Test 3: Low quality content (should flag quality issues)
    print("\n3️⃣ Testing low quality content...")
    low_quality_html = """
    <html><body>
    <div class="ad-container">Advertisement</div>
    <div class="sponsored">Sponsored content</div>
    <div class="google_ads">More ads</div>
    <div id="adsense">Even more ads</div>
    <div class="ad-slot">Ad slot</div>
    <div class="promoted">Promoted</div>
    <div class="paywall">Subscribe to read more</div>
    <p>You won't believe what happens next! Click here for this one weird trick!</p>
    """ + ("x" * 10000)  # Lots of HTML
    low_quality_text = "You won't believe what happens next! Click here for this one weird trick!"  # Very little text

    assessment3 = immune.analyze_page("https://clickbait.com/article", low_quality_html, low_quality_text)
    print(f"   Threat score: {assessment3.overall_threat_score:.2f}")
    print(f"   Quality signals: {sum(1 for s in assessment3.threat_signals if s.signal_type == 'quality')}")
    for sig in assessment3.threat_signals:
        if sig.signal_type == 'quality':
            print(f"      - {sig.description}")
    print(f"   Recommendation: {assessment3.recommendation}")
    assert sum(1 for s in assessment3.threat_signals if s.signal_type == 'quality') >= 2, "Should detect quality issues"
    print("   ✅ PASS")

    # Test 4: Integration with existing security results
    print("\n4️⃣ Testing integration with AlphaWall results...")

    mock_alphawall_result = {
        'threat_score': 0.8,
        'threat_type': 'injection_attempt'
    }

    assessment4 = immune.analyze_page(
        "https://example.com/page",
        "<html><body><p>Test</p></body></html>",
        "Test",
        alphawall_result=mock_alphawall_result
    )

    print(f"   Combined threat score: {assessment4.overall_threat_score:.2f}")
    print(f"   Security signals: {sum(1 for s in assessment4.threat_signals if s.signal_type == 'security')}")
    print(f"   Recommendation: {assessment4.recommendation}")
    assert any('AlphaWall' in sig.description for sig in assessment4.threat_signals), "Should include AlphaWall result"
    print("   ✅ PASS")

    # Test 5: Fact risk assessment
    print("\n5️⃣ Testing fact risk assessment...")

    safe_fact = "Water boils at 100 degrees Celsius at standard atmospheric pressure."
    risky_fact = "They say that all experts always agree this is certainly impossible, with 99.9999% precision."

    fact_risk1 = immune.analyze_fact(safe_fact, np.random.rand(384), "https://science.edu", domain_trust=0.9)
    fact_risk2 = immune.analyze_fact(risky_fact, np.random.rand(384), "https://dubious.xyz", domain_trust=0.2)

    print(f"   Safe fact risk: {fact_risk1.risk_score:.2f} - {fact_risk1.recommendation}")
    print(f"   Risky fact risk: {fact_risk2.risk_score:.2f} - {fact_risk2.recommendation}")
    print(f"   Risk factors: {len(fact_risk2.risk_factors)}")

    assert fact_risk1.risk_score < fact_risk2.risk_score, "Risky fact should have higher risk"
    assert fact_risk2.corroboration_needed, "Risky fact should need corroboration"
    print("   ✅ PASS")

    print("\n" + "=" * 70)
    print("✅ All tests passed!")
    print("\nREFACTORING SUMMARY:")
    print("  ❌ REMOVED: Duplicate linguistic manipulation patterns")
    print("  ❌ REMOVED: Duplicate emotional manipulation detection")
    print("  ❌ REMOVED: Direct AlphaWall/warfare instantiation")
    print("  ✅ KEPT: HTML structure analysis (unique)")
    print("  ✅ KEPT: Content quality scoring (unique)")
    print("  ✅ KEPT: Source/domain analysis (unique)")
    print("  ✅ ADDED: Accept security results as input parameters")
    print("  ✅ ADDED: Domain trust integration")
    print("\n  Focus: Page-level analysis, not text-level (that's AlphaWall's job)")
