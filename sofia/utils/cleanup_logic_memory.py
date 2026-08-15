"""
Logic Memory Garbage Cleanup
Removes entries matching 4 criteria:
1. Text under 20 characters
2. Primarily citation references (et al, doi, arXiv with no substantive knowledge)
3. URL-only entries
4. Text starting with continuation punctuation
"""

import json
import re
import shutil
from datetime import datetime

LOGIC_MEMORY_PATH = "data/logic_memory.json"
BACKUP_PATH = f"data/logic_memory_pre_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json.backup"

def is_garbage(entry):
    """Returns (True, reason) if entry is garbage, (False, None) if valid."""
    text = entry.get("text", "")

    if text is None:
        return True, "null_text"

    text = text.strip()

    # Criterion 1: Under 20 characters
    if len(text) < 20:
        return True, f"too_short ({len(text)} chars): {repr(text[:50])}"

    # Criterion 4: Starts with continuation punctuation
    if text and text[0] in ")]}>,;:":
        return True, f"continuation_punct: {repr(text[:80])}"

    # Criterion 3: URL-only (text is primarily a URL with minimal other content)
    url_pattern = re.compile(r'^https?://\S+$')
    if url_pattern.match(text):
        return True, f"url_only: {repr(text[:80])}"

    # Also catch entries that are >80% URL content
    urls_removed = re.sub(r'https?://\S+', '', text).strip()
    if len(urls_removed) < 20 and len(text) > 30:
        return True, f"mostly_url: {repr(text[:80])}"

    # Criterion 2: Primarily citation references
    # Pattern: "et al" is the core content, not embedded in a real sentence
    # Check if removing citations leaves almost nothing
    cleaned_of_citations = text
    # Remove patterns like (2019), [1], [2,3], et al., doi:..., arXiv:...
    cleaned_of_citations = re.sub(r'\(\d{4}[a-z]?\)', '', cleaned_of_citations)  # (2019), (2007b)
    cleaned_of_citations = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', cleaned_of_citations)  # [1], [2,3]
    cleaned_of_citations = re.sub(r'\bet\s+al\.?\b', '', cleaned_of_citations)  # et al
    cleaned_of_citations = re.sub(r'\bdoi:\S+', '', cleaned_of_citations)  # doi:...
    cleaned_of_citations = re.sub(r'\barXiv:\S+', '', cleaned_of_citations)  # arXiv:...
    cleaned_of_citations = re.sub(r'pp?\.\s*\d+[-–]\d+', '', cleaned_of_citations)  # pp. 123-456
    cleaned_of_citations = re.sub(r'vol\.\s*\d+', '', cleaned_of_citations, flags=re.IGNORECASE)  # vol. 3
    cleaned_of_citations = re.sub(r'[A-Z]\.\s*[A-Z]\.', '', cleaned_of_citations)  # A. B. (initials)
    cleaned_of_citations = cleaned_of_citations.strip()

    # If removing citation patterns leaves <30% of original meaningful content
    remaining_words = [w for w in cleaned_of_citations.split() if len(w) > 2 and w.isalpha()]
    original_words = [w for w in text.split() if len(w) > 2]

    if original_words and len(remaining_words) / max(len(original_words), 1) < 0.3:
        # Mostly citations
        if 'et al' in text.lower() or re.search(r'\(\d{4}\)', text) or re.search(r'\[\d+\]', text):
            return True, f"citation_dump: {repr(text[:80])}"

    # Also catch pure year/number entries that slipped past length check
    if re.match(r'^[\d\s\.\,\-\(\)]+$', text):
        return True, f"numbers_only: {repr(text[:80])}"

    # Catch code fragments with no explanatory text
    if re.match(r'^[\*\/\{\}\[\]\(\)\=\+\-\<\>\;\:\.\,\s\w]{0,50}$', text):
        # Check if it has actual words
        words = [w for w in text.split() if w.isalpha() and len(w) > 2]
        if len(words) < 2:
            return True, f"code_fragment: {repr(text[:80])}"

    return False, None


def main():
    # Load
    print(f"Loading {LOGIC_MEMORY_PATH}...")
    with open(LOGIC_MEMORY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    print(f"Total entries: {total}")

    # Classify
    garbage = []
    valid = []

    for i, entry in enumerate(data):
        is_bad, reason = is_garbage(entry)
        if is_bad:
            garbage.append((i, entry, reason))
        else:
            valid.append(entry)

    # Report
    print(f"\n{'='*60}")
    print(f"GARBAGE FOUND: {len(garbage)} entries ({len(garbage)/total*100:.1f}%)")
    print(f"VALID ENTRIES: {len(valid)} entries ({len(valid)/total*100:.1f}%)")
    print(f"{'='*60}\n")

    # Categorize garbage by reason
    categories = {}
    for idx, entry, reason in garbage:
        cat = reason.split(':')[0].split('(')[0].strip()
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((idx, entry, reason))

    for cat, items in sorted(categories.items()):
        print(f"\n--- {cat.upper()} ({len(items)} entries) ---")
        for idx, entry, reason in items[:5]:  # Show first 5 per category
            text = entry.get('text', '')
            print(f"  [{idx}] {reason}")
        if len(items) > 5:
            print(f"  ... and {len(items)-5} more")

    # Backup
    print(f"\nBacking up to {BACKUP_PATH}...")
    shutil.copy2(LOGIC_MEMORY_PATH, BACKUP_PATH)
    print(f"Backup created: {BACKUP_PATH}")

    # Write cleaned data
    print(f"\nWriting {len(valid)} valid entries to {LOGIC_MEMORY_PATH}...")
    with open(LOGIC_MEMORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(valid, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"CLEANUP COMPLETE")
    print(f"  Before: {total} entries")
    print(f"  Removed: {len(garbage)} entries")
    print(f"  After: {len(valid)} entries")
    print(f"  Backup: {BACKUP_PATH}")
    print(f"{'='*60}")

    # Check for any remaining null/empty entries that could cause NoneType
    null_count = 0
    empty_count = 0
    for entry in valid:
        text = entry.get('text')
        if text is None:
            null_count += 1
        elif not text.strip():
            empty_count += 1

    print(f"\nNoneType safety check on remaining entries:")
    print(f"  Null text fields: {null_count}")
    print(f"  Empty text fields: {empty_count}")
    if null_count == 0 and empty_count == 0:
        print(f"  ✅ No NoneType crash risk")
    else:
        print(f"  ⚠️ WARNING: Found entries that could cause NoneType errors")


if __name__ == "__main__":
    main()
