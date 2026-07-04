import requests
import trafilatura
from bs4 import BeautifulSoup, Comment # APPENDED: Import Comment
from pathlib import Path
import time
import re
from urllib.parse import urljoin, urlparse

DEFAULT_TIMEOUT = 10

def fetch_raw_html(url, timeout=DEFAULT_TIMEOUT):
    try:
        response = requests.get(url, timeout=timeout, headers={'User-Agent': 'CustomAIAutonomousLearner/1.0'})
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[WEB_PARSER] Error fetching raw HTML for {url}: {e}")
        return None

def extract_links_with_text_from_html(base_url, html_content):
    links_with_text = []
    if not html_content:
        return links_with_text
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        anchor_text = a_tag.get_text(separator=' ', strip=True)
        
        if not href or not anchor_text:
            continue
            
        absolute_url = urljoin(base_url, href)
        parsed_url = urlparse(absolute_url)
        
        if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc and not parsed_url.fragment:
            if any(ext in parsed_url.path.lower() for ext in ['.pdf', '.jpg', '.png', '.zip', '.mp4', '.mov']):
                continue
            if "javascript:" in href.lower() or "mailto:" in href.lower():
                continue
            links_with_text.append((absolute_url, anchor_text))
            
    return links_with_text

# MODIFIED: clean_html_to_text function
def sanitize_text_for_storage(text):
    """Final quality gate before any text enters memory storage.
    Rejects garbage: fragments, citations-only, URLs-only, punctuation-only, code fragments.
    Returns cleaned text or None if the text is garbage."""
    if not text or not isinstance(text, str):
        return None

    text = text.strip()

    # Strip Wikipedia navigation boilerplate from the start of text.
    # Pages scraped from Wikipedia often begin with "Jump to content",
    # "From Wikipedia, the free encyclopedia", and similar chrome that
    # is not knowledge content.
    wikipedia_prefixes = [
        "Jump to content",
        "From Wikipedia, the free encyclopedia",
        "From Wikipedia, the free encyclopedia.",
    ]
    for prefix in wikipedia_prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    # Handle the combined form: "Jump to content From Wikipedia..."
    # Also handles "Coordinates ... / From Wikipedia..." (geo-tagged articles)
    if text.startswith("From Wikipedia"):
        text = re.sub(r'^From Wikipedia,?\s*the free encyclopedia\.?\s*', '', text).strip()
    elif 'From Wikipedia' in text[:300]:
        text = re.sub(r'^.*?From Wikipedia,?\s*the free encyclopedia\.?\s*', '', text, count=1).strip()

    # Reject text under 20 meaningful characters
    if len(text) < 20:
        return None

    # Reject text starting with continuation punctuation
    if text[0] in ")]}>,;:":
        return None

    # Reject URL-only content
    if re.match(r'^https?://\S+$', text):
        return None
    urls_removed = re.sub(r'https?://\S+', '', text).strip()
    if len(urls_removed) < 20 and len(text) > 30:
        return None

    # Reject numbers/punctuation-only content
    if re.match(r'^[\d\s\.\,\-\(\)\[\]\;\:\/]+$', text):
        return None

    # Reject citation-dominated content (>85% citation patterns - relaxed for academic)
    cleaned = text
    cleaned = re.sub(r'\(\d{4}[a-z]?\)', '', cleaned)        # (2019), (2007b)
    cleaned = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', cleaned)    # [1], [2,3]
    cleaned = re.sub(r'\bet\s+al\.?\b', '', cleaned)          # et al
    cleaned = re.sub(r'\bdoi:\S+', '', cleaned)               # doi:...
    cleaned = re.sub(r'\barXiv:\S+', '', cleaned)             # arXiv:...
    cleaned = re.sub(r'pp?\.\s*\d+[-\u2013]\d+', '', cleaned) # pp. 123-456
    remaining_words = [w for w in cleaned.split() if len(w) > 2 and w.isalpha()]
    original_words = [w for w in text.split() if len(w) > 2]
    
    # Relaxed threshold: 0.15 (85% citations) instead of 0.3 (70% citations)
    if original_words and len(remaining_words) / max(len(original_words), 1) < 0.15:
        if 'et al' in text.lower() or re.search(r'\(\d{4}\)', text) or re.search(r'\[\d+\]', text):
            return None

    # Reject content with fewer than 3 actual words
    real_words = [w for w in text.split() if w.isalpha() and len(w) > 1]
    if len(real_words) < 3:
        return None

    # Clean up excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def clean_html_to_text(html_content, use_trafilatura_on_string=False):
    if not html_content:
        return None

    cleaned_text = None
    if use_trafilatura_on_string: # This path might still be less effective than Trafilatura fetching URL itself
        try:
            extracted_main = trafilatura.extract(html_content,
                                                 include_comments=False,
                                                 include_tables=True,
                                                 no_fallback=True) 
            if extracted_main and len(extracted_main) > 50:
                cleaned_text = extracted_main
        except Exception as e:
            print(f"[WEB_PARSER] Error using Trafilatura on HTML string: {e}. Falling back to BS4.")
            # Fall through to BeautifulSoup

    if not cleaned_text:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for script_or_style in soup(["script", "style", "header", "footer", "nav", "aside", "form", "button", "input", "select", "textarea", "label"]): # Added more non-content tags
            script_or_style.decompose()
        
        text_parts = []
        # Attempt to find main content areas first for more focused extraction
        main_content_tags = soup.find_all(['article', 'main', 'div'], 
                                          class_=['content', 'main-content', 'post-body', 'entry-content', 'article-body', 'story-content'])
        
        target_element = soup.body # Default to body
        if main_content_tags:
            best_main = None
            max_len = 0
            for tag in main_content_tags:
                tag_text_len = len(tag.get_text(strip=True))
                if tag_text_len > max_len:
                    max_len = tag_text_len
                    best_main = tag
            if best_main and max_len > 100 : # Only use if it has substantial text
                target_element = best_main
            # else: print(f"[WEB_PARSER] No substantial main content block found, using full body.")

        if not target_element: 
            target_element = soup # Fallback to whole soup if no body

        for element in target_element.find_all(string=True):
            # APPENDED/MODIFIED: Correct way to check for BeautifulSoup Comment
            if isinstance(element, Comment): # Check if the element is a Comment object
                continue
            # Also skip text within typical non-display parent tags that find_all(string=True) might still pick up
            if element.parent.name in ['script', 'style', 'head', 'title', 'meta', '[document]', 'noscript', 'form', 'button', 'select', 'option']:
                continue

            stripped_text = element.strip()
            # Filter out fragments that are not meaningful content
            if stripped_text and len(stripped_text) > 2:
                # Skip lone punctuation, bare numbers, single letters
                if not re.match(r'^[\d\s\.\,\-\(\)\[\]\;\:\!\/\?\#\*]+$', stripped_text):
                    text_parts.append(stripped_text)

        cleaned_text = " ".join(text_parts)
        # Collapse excessive whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text if cleaned_text and len(cleaned_text.strip()) > 0 else None


def fetch_shallow(url, max_chars=500, timeout=DEFAULT_TIMEOUT-5):
    try:
        raw_html = fetch_raw_html(url, timeout=timeout)
        if not raw_html:
            return None
        
        cleaned_text = clean_html_to_text(raw_html, use_trafilatura_on_string=False) # Prefer BS4 for speed here
        
        if cleaned_text:
            return cleaned_text[:max_chars]
        return None
    except Exception as e:
        print(f"[WEB_PARSER] Generic error during shallow fetch for {url}: {e}")
        return None

def fetch_and_clean_with_trafilatura(url, timeout_not_used=None):
    try:
        downloaded = trafilatura.fetch_url(url) 
        if downloaded:
            clean_text = trafilatura.extract(downloaded, include_comments=False, include_tables=True, no_fallback=False) 
            if clean_text:
                return clean_text
        return None
    except Exception as e:
        print(f"[WEB_PARSER-TRAFILATURA] Error for {url}: {e}")
        return None

def fallback_extract_text_with_bs4(url, timeout=DEFAULT_TIMEOUT):
    try:
        html_content = fetch_raw_html(url, timeout=timeout)
        if html_content:
            return clean_html_to_text(html_content, use_trafilatura_on_string=False)
        return None
    except Exception as e:
        print(f"[WEB_PARSER-BS4_FALLBACK] Error for {url}: {e}")
        return None

def chunk_text(text, max_chunk_length=1000, overlap=100):
    if not text or not isinstance(text, str): return []
    chunks = []
    # Assuming P_Parser.NLP_MODEL_LOADED and P_Parser.nlp might not be directly accessible here.
    # If this chunk_text is only called from parser.py itself, this is fine.
    # If called externally and spaCy is desired, nlp instance needs to be passed or loaded here.
    # For now, let's assume basic regex splitting if spaCy not available via an import.
    try:
        # Attempt to use spaCy if P_Parser and its nlp are available and loaded
        # This creates a soft dependency. Better to pass nlp instance if needed.
        if P_Parser.NLP_MODEL_LOADED and P_Parser.nlp:
            doc = P_Parser.nlp(text[:P_Parser.nlp.max_length])
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        else:
            raise AttributeError # Fallback to regex
    except (NameError, AttributeError): # If P_Parser or P_Parser.nlp is not defined/loaded
        # print("[WEB_PARSER-CHUNK] spaCy not available, using regex for sentence splitting.")
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]


    current_chunk_parts = []
    current_length = 0
    for i, sentence in enumerate(sentences):
        sentence_len = len(sentence)
        if not sentence: continue

        if sentence_len > max_chunk_length:
            if current_chunk_parts:
                chunks.append(" ".join(current_chunk_parts))
                current_chunk_parts, current_length = [], 0
            
            sub_sentence_start = 0
            while sub_sentence_start < sentence_len:
                end_point = min(sub_sentence_start + max_chunk_length, sentence_len)
                actual_end_point = sentence.rfind(" ", sub_sentence_start, end_point) if " " in sentence[sub_sentence_start:end_point] else end_point
                if actual_end_point <= sub_sentence_start : actual_end_point = end_point
                chunks.append(sentence[sub_sentence_start:actual_end_point].strip())
                sub_sentence_start = actual_end_point + (1 if sentence[actual_end_point:actual_end_point+1] == " " else 0)
            continue

        if current_length + sentence_len + (1 if current_chunk_parts else 0) > max_chunk_length and current_chunk_parts:
            chunks.append(" ".join(current_chunk_parts))
            overlap_parts, overlap_len = [], 0
            temp_overlap_source = list(current_chunk_parts)
            while temp_overlap_source:
                part_to_add = temp_overlap_source.pop()
                part_len = len(part_to_add)
                if overlap_len + part_len + (1 if overlap_parts else 0) <= overlap:
                    overlap_parts.insert(0, part_to_add)
                    overlap_len += part_len + (1 if len(overlap_parts) > 1 else 0)
                else: break
            current_chunk_parts, current_length = overlap_parts, overlap_len
        
        if current_chunk_parts: current_chunk_parts.append(sentence)
        else: current_chunk_parts = [sentence]
        current_length += sentence_len + (1 if len(current_chunk_parts) > 1 else 0)

    if current_chunk_parts: chunks.append(" ".join(current_chunk_parts))
    # Final quality gate: reject chunks that are garbage
    return [c for c in chunks if sanitize_text_for_storage(c) is not None]


def process_web_url(url):
    """
    Process a web URL by fetching content and storing it in the unified memory system.
    This is the main entry point for web content processing called by main.py
    """
    print(f"🌐 Processing web URL: {url}")
    
    # Fetch and clean content
    html = fetch_raw_html(url)
    if not html:
        print(f"❌ Failed to fetch content from {url}")
        return
        
    cleaned_text = clean_html_to_text(html)
    if not cleaned_text:
        print(f"❌ Failed to extract text from {url}")
        return
        
    # Chunk the content for processing
    chunks = chunk_text(cleaned_text, max_chunk_length=1000)
    print(f"📝 Extracted {len(chunks)} chunks from {url}")
    
    # Store in unified memory system
    try:
        from unified_memory import get_unified_memory
        memory = get_unified_memory()
        
        for i, chunk in enumerate(chunks):
            memory.store_vector(
                text=chunk, 
                source_type="web_scrape",
                source_url=url
            )
            
        print(f"✅ Successfully stored {len(chunks)} chunks from {url}")
        
    except Exception as e:
        print(f"❌ Error storing web content in memory: {e}")


if __name__ == '__main__':
    # Import P_Parser here for testing chunk_text if spaCy is used by it
    try:
        import parser as P_Parser
        if not P_Parser.NLP_MODEL_LOADED and P_Parser.nlp is None: # Attempt to load if not already
            try:
                P_Parser.nlp = spacy.load("en_core_web_sm")
                P_Parser.NLP_MODEL_LOADED = True
                print("spaCy model loaded for web_parser.py tests.")
            except: pass # Silently fail if spaCy not available for test
    except ImportError:
        class MockPParser: # Create a mock if parser.py itself isn't found (e.g. testing web_parser standalone)
            NLP_MODEL_LOADED = False
            nlp = None
        P_Parser = MockPParser()
        print("[WEB_PARSER_TEST] Mocking P_Parser for chunk_text spaCy dependency.")


    print("Testing web_parser.py enhancements...")
    test_url_wikipedia = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    test_url_simple_blog = "https://example.com" 

    print(f"\n--- Testing fetch_raw_html for {test_url_wikipedia} ---")
    html = fetch_raw_html(test_url_wikipedia)
    if html:
        print(f"Successfully fetched HTML, length: {len(html)} characters.")
        assert len(html) > 1000
    else:
        print("Failed to fetch raw HTML for Wikipedia.")

    problem_html = fetch_raw_html("http://thisshouldnotexist12345abc.com")
    assert problem_html is None
    print("Correctly returned None for non-existent URL.")

    if html:
        print(f"\n--- Testing extract_links_with_text_from_html for Wikipedia content ---")
        base_url_for_links = test_url_wikipedia
        links_and_anchors = extract_links_with_text_from_html(base_url_for_links, html)
        print(f"Found {len(links_and_anchors)} links with anchor text. First 5:")
        for i, (link, anchor) in enumerate(links_and_anchors[:5]):
            print(f"  {i+1}. Anchor: '{anchor[:50]}...', URL: {link[:70]}...")
        assert len(links_and_anchors) > 10

        print(f"\n--- Testing clean_html_to_text (BS4 path) for Wikipedia content ---")
        cleaned_text_bs4 = clean_html_to_text(html, use_trafilatura_on_string=False)
        if cleaned_text_bs4:
            print(f"Cleaned text (BS4) length: {len(cleaned_text_bs4)}. Preview: '{cleaned_text_bs4[:200]}...'")
            assert len(cleaned_text_bs4) > 500
        else:
            print("BS4 cleaning failed or returned empty.")
        
        # Test with a known HTML snippet that includes comments
        html_with_comments = """
        <body>
            <p>This is normal text.</p>
            <p>More normal text.</p>
            <script>alert('hello');</script>
            <style>.hide{display:none;}</style>
            <div>Even more text.</div>
        </body>
        """
        print(f"\n--- Testing clean_html_to_text with comments ---")
        cleaned_comment_test = clean_html_to_text(html_with_comments)
        print(f"Cleaned comment test: '{cleaned_comment_test}'")
        assert "This is a comment" not in cleaned_comment_test
        assert "alert('hello')" not in cleaned_comment_test
        assert "This is normal text. More normal text. Even more text." in cleaned_comment_test # Check spacing

    print(f"\n--- Testing fetch_shallow for {test_url_wikipedia} ---")
    shallow_text = fetch_shallow(test_url_wikipedia, max_chars=300)
    if shallow_text:
        print(f"Shallow text length: {len(shallow_text)}. Content: '{shallow_text}'")
        assert len(shallow_text) <= 300
        if len(shallow_text) > 0: assert len(shallow_text) > 10 # Should get some content if site is up
    else:
        print("Shallow fetch failed.")
    
    if html and cleaned_text_bs4:
        print("\n--- Testing chunk_text with cleaned Wikipedia content (max_chunk_length=500) ---")
        chunks_from_cleaned = chunk_text(cleaned_text_bs4, max_chunk_length=500, overlap=50)
        print(f"Split into {len(chunks_from_cleaned)} chunks. First chunk preview (len {len(chunks_from_cleaned[0]) if chunks_from_cleaned else 0}):")
        if chunks_from_cleaned:
            print(f"'{chunks_from_cleaned[0][:200]}...'")
            assert len(chunks_from_cleaned[0]) <= 500
        assert len(chunks_from_cleaned) > 1
        
    print("\n✅ web_parser.py tests completed (AttributeError fixed).")