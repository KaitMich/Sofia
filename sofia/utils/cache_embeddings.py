#!/usr/bin/env python3
"""
Batch Embedding Cache — Phase 1 of Adaptive Migration

Computes and caches embeddings for all existing memory items.
Run once to prepare existing data for the adaptive migration engine.

Usage:
    python3 cache_embeddings.py
"""

import json
import time
from pathlib import Path


def cache_embeddings_for_store(store_path: str, store_name: str):
    """Compute and cache embeddings for all items in a memory store."""
    from sofia.memory.adaptive_bridge_migration import get_or_compute_embedding

    path = Path(store_path)
    if not path.exists():
        print(f"  {store_name}: file not found, skipping")
        return 0, 0

    with open(path, 'r') as f:
        items = json.load(f)

    total = len(items)
    cached = sum(1 for i in items if i.get('embedding') is not None)
    needed = total - cached

    if needed == 0:
        print(f"  {store_name}: {total} items, all already have embeddings")
        return total, 0

    print(f"  {store_name}: {total} items, {cached} cached, {needed} need embedding...")

    newly_cached = 0
    for i, item in enumerate(items):
        if item.get('embedding') is not None:
            continue

        emb = get_or_compute_embedding(item)
        if emb is not None:
            newly_cached += 1

        if (i + 1) % 100 == 0:
            print(f"    Progress: {i+1}/{total} ({newly_cached} new embeddings)")

    # Save back with embeddings cached on items
    with open(path, 'w') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"  {store_name}: {newly_cached} new embeddings computed and cached")
    return total, newly_cached


def main():
    print("=" * 60)
    print("BATCH EMBEDDING CACHE")
    print("Computing embeddings for all existing memory items")
    print("=" * 60)
    print()

    start = time.time()
    total_items = 0
    total_new = 0

    for store_name, store_file in [
        ("Logic Memory", "data/logic_memory.json"),
        ("Bridge Memory", "data/bridge_memory.json"),
        ("Symbolic Memory", "data/symbolic_memory.json"),
    ]:
        items, new = cache_embeddings_for_store(store_file, store_name)
        total_items += items
        total_new += new

    elapsed = time.time() - start

    print()
    print("=" * 60)
    print(f"EMBEDDING CACHE COMPLETE")
    print(f"  Total items: {total_items}")
    print(f"  New embeddings: {total_new}")
    print(f"  Time: {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
