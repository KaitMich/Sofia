# cluster_namer.py - Enhanced Clustering System
# Consolidated with clustering.py for comprehensive clustering capabilities

import json
from pathlib import Path
from collections import Counter
import random
import numpy as np
from sklearn.cluster import KMeans

SYMBOL_PATH = Path("data/symbol_memory.json")
NAMED_CLUSTERS_PATH = Path("data/cluster_names.json")

EMOJI_POOL = ["🌀", "💔", "🛡️", "🌱", "🔥", "🌙", "🌊", "🧭", "⚡", "🪞"]

def cluster_memory(memory_data, n_clusters=2):
    """
    Simple K-means clustering for memory data.
    Consolidated from clustering.py functionality.
    
    Args:
        memory_data: List of dict items with 'vector' and 'text' keys
        n_clusters: Number of clusters to create
        
    Returns:
        Dictionary mapping cluster labels to lists of texts
    """
    if not memory_data or len(memory_data) < n_clusters:
        return {}
    
    vectors = [item["vector"] for item in memory_data if "vector" in item]
    texts = [item["text"] for item in memory_data if "text" in item]
    
    if len(vectors) != len(texts) or not vectors:
        return {}

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(vectors)

    clusters = {}
    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(texts[i])

    return clusters

def generate_cluster_id(texts):
    # Ensure this line uses regular spaces for indentation
    return hash(" ".join(texts)) % 1000000

def pick_cluster_name(texts, keywords, emotions, cluster_id=None):
    # Ensure this line uses regular spaces for indentation
    if cluster_id is None:
        # Ensure this line uses regular spaces for indentation
        cluster_id = generate_cluster_id(texts)
    # Ensure this line uses regular spaces for indentation
    return generate_cluster_name(cluster_id, keywords, emotions)

def generate_cluster_name(cluster_id, keywords, emotions):
    # Ensure this line uses regular spaces for indentation
    if keywords:
        # Ensure this line uses regular spaces for indentation
        top = Counter(keywords).most_common(1)[0][0].title()
    # Ensure this line uses regular spaces for indentation
    elif emotions:
        # Ensure this line uses regular spaces for indentation
        top = max(emotions, key=lambda x: x[1])[0].title()
    # Ensure this line uses regular spaces for indentation
    else:
        # Ensure this line uses regular spaces for indentation
        top = "Theme"

    # Ensure this line uses regular spaces for indentation
    emoji = random.choice(EMOJI_POOL)
    # Ensure this line uses regular spaces for indentation
    return f"{emoji} {top}"

def load_symbols():
    # Ensure this line uses regular spaces for indentation
    if SYMBOL_PATH.exists():
        # Ensure this line uses regular spaces for indentation
        with open(SYMBOL_PATH, "r", encoding="utf-8") as f:
            # Ensure this line uses regular spaces for indentation
            return json.load(f)
    # Ensure this line uses regular spaces for indentation
    return {}

def extract_texts(symbols):
    """Extract text representations from symbols for clustering."""
    texts = []
    for v in symbols.values():
        name = v.get('name', '')
        keywords = ' '.join(v.get('keywords', []))
        
        # Handle different emotion data structures
        emotions_data = v.get('emotions', {})
        if isinstance(emotions_data, dict):
            emotions = ' '.join(emotions_data.keys())
        elif isinstance(emotions_data, list):
            emotions = ' '.join(str(e) for e in emotions_data)
        else:
            emotions = ''
        
        text = f"{name} {keywords} {emotions}".strip()
        texts.append(text)
    
    return texts

def cluster_symbols(symbols_dict, threshold=0.5): # Changed input name for clarity
    # Ensure this line uses regular spaces for indentation
    from sklearn.metrics.pairwise import cosine_similarity
    # Ensure this line uses regular spaces for indentation
    from sklearn.feature_extraction.text import TfidfVectorizer

    # symbols_dict is expected to be the raw dict loaded from symbol_memory.json
    # Need to convert it to a list of symbol details first, and keep track of original keys if needed.
    # For simplicity, assuming the caller of cluster_symbols might pass list(raw.values()) as in assign_cluster_names

    # If symbols_dict is actually a list of symbol objects (as passed by assign_cluster_names)
    if isinstance(symbols_dict, list):
        symbol_list_for_texts = symbols_dict
    elif isinstance(symbols_dict, dict): # If it's a dict, get values
        symbol_list_for_texts = list(symbols_dict.values())
    else:
        print("❌ Invalid symbols format for clustering.")
        return []


    # Ensure this line uses regular spaces for indentation
    texts = extract_texts(dict(zip(range(len(symbol_list_for_texts)), symbol_list_for_texts))) # Reconstruct a temporary dict for extract_texts
    # Ensure this line uses regular spaces for indentation
    if not texts:
        print("❌ No texts extracted from symbols for clustering.")
        return []
    # Ensure this line uses regular spaces for indentation
    vectorizer = TfidfVectorizer().fit_transform(texts)
    # Ensure this line uses regular spaces for indentation
    sim_matrix = cosine_similarity(vectorizer)

    # Ensure this line uses regular spaces for indentation
    clusters = []
    # Ensure this line uses regular spaces for indentation
    visited = set()

    # Ensure this line uses regular spaces for indentation
    for i in range(len(symbol_list_for_texts)): # Iterate based on the length of the list used for texts
        # Ensure this line uses regular spaces for indentation
        if i in visited:
            # Ensure this line uses regular spaces for indentation
            continue
        # Ensure this line uses regular spaces for indentation
        cluster = [i]
        # Ensure this line uses regular spaces for indentation
        visited.add(i)
        # Ensure this line uses regular spaces for indentation
        for j in range(len(symbol_list_for_texts)):
            # Ensure this line uses regular spaces for indentation
            if j not in visited and sim_matrix[i][j] > threshold:
                # Ensure this line uses regular spaces for indentation
                cluster.append(j)
                # Ensure this line uses regular spaces for indentation
                visited.add(j)
        # Ensure this line uses regular spaces for indentation
        clusters.append(cluster)

    # Ensure this line uses regular spaces for indentation
    return clusters

def summarize_cluster(symbol_list_param, indices): # Changed param name to avoid conflict
    # Ensure this line uses regular spaces for indentation
    # texts_in_cluster = [symbol_list_param[i] for i in indices] # This uses symbol_list from outer scope
    cluster_symbol_objects = [symbol_list_param[i] for i in indices]


    # Ensure this line uses regular spaces for indentation
    names = [s.get('name', 'Unnamed Symbol') for s in cluster_symbol_objects]
    # Ensure this line uses regular spaces for indentation
    all_keywords_in_cluster = []
    # Ensure this line uses regular spaces for indentation
    for s_obj in cluster_symbol_objects:
        # Ensure this line uses regular spaces for indentation
        all_keywords_in_cluster.extend(s_obj.get('keywords', []))
    # Ensure this line uses regular spaces for indentation
    all_emotions_in_cluster = []
    # Ensure this line uses regular spaces for indentation
    for s_obj in cluster_symbol_objects:
        # Ensure this line uses regular spaces for indentation
        # Assuming 'emotions' can be a list of strings or a dict like {'emotion': score}
        # For Counter, we need individual emotion strings.
        emotions_data = s_obj.get('emotions', [])
        if isinstance(emotions_data, dict):
            all_emotions_in_cluster.extend(emotions_data.keys())
        elif isinstance(emotions_data, list): # If it's a list of strings already or list of dicts/tuples
            for item in emotions_data:
                if isinstance(item, str):
                    all_emotions_in_cluster.append(item)
                elif isinstance(item, dict) and 'emotion' in item: # From symbol_memory format
                    all_emotions_in_cluster.append(item['emotion'])
                elif isinstance(item, tuple) and len(item) > 0: # From parser output
                    all_emotions_in_cluster.append(item[0])


    # Ensure this line uses regular spaces for indentation
    all_words = all_keywords_in_cluster + all_emotions_in_cluster
    # Ensure this line uses regular spaces for indentation
    most_common = Counter(all_words).most_common(3)

    # Ensure this line uses regular spaces for indentation
    summary = names[0] if names else "Theme" # Default to first symbol name in cluster
    # Ensure this line uses regular spaces for indentation
    if most_common:
        # Ensure this line uses regular spaces for indentation
        summary = most_common[0][0].title() # Use most common keyword/emotion as name

    # Ensure this line uses regular spaces for indentation
    emoji = random.choice(EMOJI_POOL)
    # Ensure this line uses regular spaces for indentation
    return emoji, summary

def assign_cluster_names():
    # Ensure this line uses regular spaces for indentation
    raw_symbols_data = load_symbols() # This is a dict {token: details}
    # Ensure this line uses regular spaces for indentation
    if not raw_symbols_data:
        # Ensure this line uses regular spaces for indentation
        print("❌ No symbols to cluster in cluster_namer.")
        # Ensure this line uses regular spaces for indentation
        return

    # cluster_symbols expects a list of symbol detail dicts
    # Ensure this line uses regular spaces for indentation
    symbol_list_for_clustering = list(raw_symbols_data.values())
    # Ensure this line uses regular spaces for indentation
    if not symbol_list_for_clustering:
        print("❌ Symbol data is empty, cannot cluster.")
        return

    # Ensure this line uses regular spaces for indentation
    clusters_indices = cluster_symbols(symbol_list_for_clustering) # Pass the list

    # Ensure this line uses regular spaces for indentation
    named_clusters = {}
    # Ensure this line uses regular spaces for indentation
    for i, group_indices in enumerate(clusters_indices):
        # Ensure this line uses regular spaces for indentation
        emoji, name = summarize_cluster(symbol_list_for_clustering, group_indices) # Pass list and indices
        # Ensure this line uses regular spaces for indentation
        named_clusters[f"cluster_{i}"] = {
            # Ensure this line uses regular spaces for indentation
            "name": name,
            # Ensure this line uses regular spaces for indentation
            "emoji": emoji,
            # Ensure this line uses regular spaces for indentation
            "members": [symbol_list_for_clustering[idx].get('symbol', 'UnknownSymbol') for idx in group_indices] # Get symbol token
        # Ensure this line uses regular spaces for indentation
        }

    # Ensure this line uses regular spaces for indentation
    try:
        NAMED_CLUSTERS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(NAMED_CLUSTERS_PATH, "w", encoding="utf-8") as f:
            # Ensure this line uses regular spaces for indentation
            json.dump(named_clusters, f, indent=2)
        # Ensure this line uses regular spaces for indentation
        print(f"✅ Named {len(named_clusters)} clusters and saved to {NAMED_CLUSTERS_PATH}.")
    except Exception as e:
        print(f"Error saving named clusters: {e}")

if __name__ == "__main__":
    # Create a dummy symbol_memory.json for testing if it doesn't exist
    if not SYMBOL_PATH.exists() or SYMBOL_PATH.stat().st_size == 0:
        print(f"Creating dummy symbol memory for cluster_namer test: {SYMBOL_PATH}")
        dummy_symbol_memory = {
            "💡": {"symbol": "💡", "name": "Bright Idea", "keywords": ["idea", "innovation", "light"], "emotions": {"curiosity": 0.8, "excitement": 0.7}},
            "⚙️": {"symbol": "⚙️", "name": "Workings", "keywords": ["process", "mechanism", "gear"], "emotions": {"focus": 0.9}},
            "💭": {"symbol": "💭", "name": "Deep Thought", "keywords": ["thought", "contemplation", "idea"], "emotions": {"wonder": 0.6, "curiosity": 0.5}},
            "📚": {"symbol": "📚", "name": "Knowledge Store", "keywords": ["book", "information", "learning"], "emotions": {}}
        }
        SYMBOL_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(SYMBOL_PATH, "w", encoding="utf-8") as f:
            json.dump(dummy_symbol_memory, f, indent=2)
    
    assign_cluster_names()

    # Test generate_cluster_id directly if needed
    # test_texts_for_id = ["hello world", "another test"]
    # print(f"Generated ID for {test_texts_for_id}: {generate_cluster_id(test_texts_for_id)}")

    # Test pick_cluster_name directly if needed
    # test_keywords_for_name = ["apple", "banana", "apple"]
    # test_emotions_for_name = [("joy", 0.8), ("sadness", 0.3)]
    # print(f"Generated name for kws & emos: {pick_cluster_name(test_texts_for_id, test_keywords_for_name, test_emotions_for_name)}")
    # print(f"Generated name for only emos: {pick_cluster_name(test_texts_for_id, [], test_emotions_for_name)}")
    # print(f"Generated name for no kws/emos: {pick_cluster_name(test_texts_for_id, [], [])}")