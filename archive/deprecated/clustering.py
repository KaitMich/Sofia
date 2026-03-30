#!/usr/bin/env python3
"""
DEPRECATED: clustering.py - Basic K-means clustering

This functionality has been CONSOLIDATED into cluster_namer.py for better integration.
Use cluster_namer.cluster_memory() instead.

INTEGRATION STATUS: COMPLETED - Functionality moved to cluster_namer.py
"""

# Legacy imports for backward compatibility
from sklearn.cluster import KMeans
import numpy as np

def cluster_memory(memory_data, n_clusters=2):
    """
    DEPRECATED: Use cluster_namer.cluster_memory() instead.
    
    This function remains for backward compatibility but functionality
    has been moved to cluster_namer.py for better integration.
    """
    print("⚠️ WARNING: clustering.py is deprecated. Use cluster_namer.cluster_memory() instead.")
    
    # Import from new location
    try:
        from cluster_namer import cluster_memory as new_cluster_memory
        return new_cluster_memory(memory_data, n_clusters)
    except ImportError:
        # Fallback to original implementation
        vectors = [item["vector"] for item in memory_data]
        texts = [item["text"] for item in memory_data]

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(vectors)

        clusters = {}
        for i, label in enumerate(labels):
            clusters.setdefault(label, []).append(texts[i])

        return clusters
