import sitecustomize
# v2_blank_start.py - Sofia v2 blank-start reset (July 4, 2026)
#
# Resets all LEARNED state so Sofia v2 begins from the designed blank start,
# with the stabilized pipeline (phases 1-5) in place from day one.
#
# What it does:
#   - Core memory stores emptied to their correct JSON shape (dashboards
#     require the files to exist and parse; they are never deleted)
#   - Accumulative logs/collections emptied to [] / {}
#   - Module-owned state files DELETED so owning modules bootstrap their
#     own defaults on first run (the original blank-start design)
#   - v1 crawl queue and quarantine DBs deleted (schemas recreate on init)
#   - v1 session logs deleted (preserved in ../sofia_v1_data_archive_*.tar.gz)
#
# What it deliberately KEEPS:
#   - trust.db / corroboration.db (freshly reset in Phase 5 - this IS v2 state)
#   - robots_cache.db / rate_limiter.db (operational caches of external facts)
#   - config files (adaptive_quarantine_config.json, seed manifests, ...)
#   - evolution anchor snapshots in data/backups/ (historical record of v1)
#
# v1 is fully preserved in ../sofia_v1_data_archive_20260704.tar.gz and in
# docs/baselines/baseline_20260704.json for v1-vs-v2 comparison studies.

import json
from pathlib import Path

DATA = Path("data")

BLANK_LIST = [
    # core stores
    "logic_memory.json", "symbolic_memory.json", "bridge_memory.json",
    "vector_memory.json", "trail_log.json",
    # accumulative logs and histories
    "learning_milestones.json", "memory_analytics_history.json",
    "brain_reflection_history.json", "bridge_decisions.json",
    "bridge_conflicts.json", "content_requests.json", "brain_metrics.json",
    "brain_contribution_metrics.json", "weight_evolution_history.json",
    "learning_goals.json",
]

BLANK_DICT = [
    # keyed collections of learned items — safe as {} (readers iterate)
    "symbol_memory.json", "user_memory.json", "cluster_names.json",
    "symbol_cooccurrence.json", "meta_symbols.json",
]

DELETE_STATE = [
    # module-owned state: owners recreate defaults on first run.
    # State dicts with EXPECTED KEYS must be deleted, not blanked to {} —
    # loaders bootstrap on a missing file but crash on an empty dict
    # (choice_architecture's KeyError: 'total_choices' taught us this).
    "curiosity_state.json", "learning_progression_detailed.json",
    "sovereignty_log.json", "consciousness_profile.json",
    "autonomy_profile.json", "adaptive_weights.json", "ai_heartbeat.json",
    "choice_history.json", "choice_guidance.json",
    "conversation_contexts.json", "context_patterns.json",
    "context_corrections.json", "bridge_reclassification_log.json",
]

DELETE_FILES = [
    # v1 operational data preserved in the archive
    "crawl/url_queue.db",
    "crawl_events.jsonl",
    "quarantine/quarantine.db",
]

DELETE_GLOBS = [
    "autonomous_sessions/*.json",
    "*.json.backup",            # stale store backups must not resurrect v1
    "vector_memory.json.backup",
]


def rearm_seed_coordinates():
    """Reset 'activated' flags in the seed manifest — v1 consumed the seeds;
    a blank-start v2 must be able to activate them again."""
    manifest_path = DATA / "seed_coordinates_manifest.json"
    if not manifest_path.exists():
        return 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rearmed = 0
    for section in manifest.values():
        if not isinstance(section, dict):
            continue
        for seed in section.get("seeds", []):
            if seed.get("activated"):
                seed["activated"] = False
                seed.pop("activated_in_session", None)
                seed.pop("activated_at", None)
                rearmed += 1
    if rearmed:
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                                 encoding="utf-8")
    return rearmed


def main():
    done = []
    for name in BLANK_LIST:
        p = DATA / name
        if p.exists():
            p.write_text("[]", encoding="utf-8")
            done.append(f"blanked list  {name}")
    for name in BLANK_DICT:
        p = DATA / name
        if p.exists():
            p.write_text("{}", encoding="utf-8")
            done.append(f"blanked dict  {name}")
    for name in DELETE_STATE + DELETE_FILES:
        p = DATA / name
        if p.exists():
            p.unlink()
            done.append(f"deleted       {name}")
    for pattern in DELETE_GLOBS:
        for p in DATA.glob(pattern):
            p.unlink()
            done.append(f"deleted       {p.relative_to(DATA)}")

    rearmed = rearm_seed_coordinates()
    if rearmed:
        done.append(f"re-armed      {rearmed} seed coordinates in manifest")

    for line in done:
        print(line)
    print(f"\n{len(done)} resets applied. Sofia v2 blank start ready.")
    print("Reminder: run reset_weights.py next (adaptive weights + migration age).")


if __name__ == "__main__":
    main()
