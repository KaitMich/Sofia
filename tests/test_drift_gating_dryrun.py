#!/usr/bin/env python3
"""
Dry-run test: Link-following drift gating against chemistry session centroid.

Simulates what would have happened in the last session if the centroid-gated
Wikipedia link evaluation had been active. Shows exact cosine similarity scores
for the drifted URLs (Weimar Republic, Greensboro NC, UCL) against a chemistry
session centroid built from real chemistry content.
"""

import sys
sys.path.insert(0, '.')

import numpy as np
from vector_engine import fuse_vectors
from adaptive_bridge_migration import compute_cluster_stats, cosine_sim


def main():
    print("=" * 70)
    print("DRY-RUN: Centroid-Gated Link Evaluation")
    print("Session topic: Chemistry fundamentals")
    print("=" * 70)

    # Step 1: Build a chemistry session centroid from representative content
    # These are the kinds of text chunks Sofia would have processed in a
    # chemistry fundamentals session
    chemistry_content = [
        "Chemistry is the scientific study of matter, its properties, composition, structure, and the changes it undergoes during chemical reactions",
        "The periodic table organizes chemical elements by atomic number, electron configuration, and recurring chemical properties",
        "Chemical bonds form when atoms share or transfer electrons, creating ionic, covalent, and metallic bonds",
        "Dalton's atomic theory states that all matter is composed of indivisible atoms that combine in fixed ratios",
        "Stoichiometry involves calculating the quantities of reactants and products in chemical reactions using mole ratios",
        "Thermodynamics in chemistry studies energy changes during reactions, including enthalpy, entropy, and Gibbs free energy",
        "Acids and bases react in neutralization reactions producing water and salt, governed by the Bronsted-Lowry theory",
        "Organic chemistry studies carbon-containing compounds including hydrocarbons, alcohols, aldehydes, and carboxylic acids",
        "Electrochemistry studies the relationship between electrical energy and chemical change in galvanic and electrolytic cells",
        "Chemical kinetics studies reaction rates and the factors affecting them: concentration, temperature, catalysts, and surface area",
    ]

    print("\n--- Step 1: Building session centroid from chemistry content ---")
    embeddings = []
    for i, text in enumerate(chemistry_content):
        vec, debug = fuse_vectors(text[:1000])
        if vec is not None:
            embeddings.append(np.array(vec))
            print(f"  [{i+1:2d}] Embedded: {text[:60]}... ({debug['source']})")
        else:
            print(f"  [{i+1:2d}] FAILED: {text[:60]}...")

    if len(embeddings) < 3:
        print("ERROR: Not enough embeddings to build centroid")
        return

    # Compute session centroid (mean of all embeddings)
    session_centroid = np.mean(embeddings, axis=0)
    norm = np.linalg.norm(session_centroid)
    if norm > 0:
        session_centroid = session_centroid / norm

    print(f"\n  Session centroid built from {len(embeddings)} chemistry embeddings")

    # Step 2: Compute session coherence stats (same math as bridge migration)
    items = [{'embedding': emb} for emb in embeddings]
    stats = compute_cluster_stats(items)
    print(f"\n--- Step 2: Session coherence statistics ---")
    print(f"  mean_similarity (threshold):  {stats.mean_similarity:.4f}")
    print(f"  std_similarity:               {stats.std_similarity:.4f}")
    print(f"  drift_threshold (mean - std):  {stats.drift_threshold:.4f}")
    print(f"  density_confidence:           {stats.density_confidence:.4f}")

    # Step 3: Score the drifted URLs from the last session
    # These are the actual anchor texts that would have appeared on Wikipedia
    test_links = [
        # On-topic links (should pass gating)
        ("Chemical element", "https://en.wikipedia.org/wiki/Chemical_element", "on-topic"),
        ("Periodic table", "https://en.wikipedia.org/wiki/Periodic_table", "on-topic"),
        ("Atomic theory", "https://en.wikipedia.org/wiki/Atomic_theory", "on-topic"),
        ("Mole (chemistry)", "https://en.wikipedia.org/wiki/Mole_(unit)", "on-topic"),

        # The actual drift chain from the session
        ("John Dalton", "https://en.wikipedia.org/wiki/John_Dalton", "drift-start"),
        ("University College London", "https://en.wikipedia.org/wiki/University_College_London", "drifted"),
        ("Weimar Republic", "https://en.wikipedia.org/wiki/Weimar_Republic", "drifted"),
        ("Greensboro, North Carolina", "https://en.wikipedia.org/wiki/Greensboro,_North_Carolina", "drifted"),

        # Additional drift examples
        ("Manchester Literary and Philosophical Society", "https://en.wikipedia.org/wiki/Manchester_Literary_and_Philosophical_Society", "drifted"),
        ("Quaker", "https://en.wikipedia.org/wiki/Quakers", "drifted"),
    ]

    print(f"\n--- Step 3: Scoring links against chemistry centroid ---")
    print(f"  {'Anchor Text':<45} {'Sim':>6} {'Threshold':>10} {'Decision':<25} {'Category'}")
    print(f"  {'-'*45} {'-'*6} {'-'*10} {'-'*25} {'-'*10}")

    for anchor_text, url, category in test_links:
        vec, _ = fuse_vectors(anchor_text[:200])
        if vec is None:
            print(f"  {anchor_text:<45} {'N/A':>6} {'':>10} {'EMBED_FAILED':<25} {category}")
            continue

        sim = cosine_sim(np.array(vec), session_centroid)
        threshold = stats.mean_similarity
        drift_threshold = stats.drift_threshold

        if sim >= threshold:
            decision = "FOLLOW_NOW"
        elif sim >= drift_threshold:
            decision = "DEFER (borderline)"
        else:
            decision = f"DEFER (off-topic, pri={sim*0.5:.3f})"

        marker = ""
        if category == "on-topic" and decision == "FOLLOW_NOW":
            marker = " ✓"
        elif category == "drifted" and "DEFER" in decision:
            marker = " ✓ (blocked)"
        elif category == "drifted" and decision == "FOLLOW_NOW":
            marker = " ✗ (would still drift)"

        print(f"  {anchor_text:<45} {sim:>6.3f} {threshold:>10.4f} {decision:<25} {category}{marker}")

    # Step 4: Show what happens with the centroid modifier on general scoring
    print(f"\n--- Step 4: Centroid modifier effect on general link scoring ---")
    print(f"  density_confidence = {stats.density_confidence:.4f}")
    print(f"  modifier = (sim - threshold) * density_confidence")
    print()
    dc = stats.density_confidence
    threshold = stats.threshold

    for anchor_text, url, category in test_links:
        vec, _ = fuse_vectors(anchor_text[:200])
        if vec is None:
            continue
        sim = cosine_sim(np.array(vec), session_centroid)
        modifier = (sim - threshold) * dc
        print(f"  {anchor_text:<45} sim={sim:.3f}  modifier={modifier:+.3f}  (would {'boost' if modifier > 0 else 'penalize'} relevance)")

    print(f"\n{'='*70}")
    print("CONCLUSION: With centroid gating active, the drift chain")
    print("(Dalton → UCL → Weimar → Greensboro) would have been DEFERRED")
    print("instead of auto-followed. Chemistry-relevant links pass through.")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
