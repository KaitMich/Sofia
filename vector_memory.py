from unified_memory import get_unified_memory


def retrieve_similar_vectors(
    query_text: str,
    top_n: int = 5,
    max_phase_allowed=None,   # accepted for call-site compatibility, not used
    min_confidence: float = 0.0,
    include_quarantined: bool = False,
) -> list:
    """
    Thin shim over UnifiedMemory.retrieve_similar_vectors.

    max_phase_allowed is accepted but not forwarded — the unified memory
    system does not partition by phase at the vector level.
    min_confidence maps to similarity_threshold.
    """
    return get_unified_memory().retrieve_similar_vectors(
        query_text,
        top_n=top_n,
        include_quarantined=include_quarantined,
        similarity_threshold=min_confidence,
    )
