"""Sofia Brain Dashboard — Three views into the tripartite mind.

Run: streamlit run data/brain_dashboard.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

st.set_page_config(page_title="Sofia Brain Dashboard", layout="wide")

DATA_DIR = Path(__file__).parent

# ═══════════════════════════════════════════════════════════════════════
# CSS — breathing animations, pulse indicators, visual language
# ═══════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
/* Title heartbeat — slow opacity breathe, resting rhythm */
[data-testid="stAppViewBlockContainer"] > div > div > div > div > h1 {
    animation: titleBreathe 4s ease-in-out infinite;
}
@keyframes titleBreathe {
    0%, 100% { opacity: 0.82; }
    50% { opacity: 1.0; }
}

/* Active learning pulse — green glow when Sofia is crawling */
.pulse-active {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #4CAF50;
    animation: activePulse 1.5s ease-in-out infinite;
    margin-right: 8px;
    vertical-align: middle;
}
.pulse-idle {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #616161;
    margin-right: 8px;
    vertical-align: middle;
}
@keyframes activePulse {
    0%, 100% { box-shadow: 0 0 4px rgba(76,175,80,0.4); transform: scale(1.0); }
    50% { box-shadow: 0 0 16px rgba(76,175,80,0.9); transform: scale(1.2); }
}

/* Health section fade-in on fragment refresh */
.health-fade {
    animation: healthFade 0.6s ease-out;
}
@keyframes healthFade {
    from { opacity: 0.4; }
    to { opacity: 1.0; }
}
/* Auto-play Plotly bar fill animations */
</style>
<script>
// Trigger Plotly animation frames on any chart with updatemenus
const observer = new MutationObserver(() => {
    document.querySelectorAll('.js-plotly-plot').forEach(plot => {
        if (plot._autoPlayed) return;
        const gd = plot;
        if (gd.layout && gd.layout.updatemenus && gd.layout.updatemenus.length > 0) {
            try {
                Plotly.animate(gd, null, {
                    frame: {duration: 700, redraw: true},
                    transition: {duration: 700, easing: 'cubic-in-out'},
                    fromcurrent: true, mode: 'immediate'
                });
                plot._autoPlayed = true;
            } catch(e) {}
        }
    });
});
observer.observe(document.body, {childList: true, subtree: true});
</script>
""", unsafe_allow_html=True)

# Toast tracking — detect new events across fragment reruns
if 'last_toast_count' not in st.session_state:
    st.session_state.last_toast_count = 0


def _is_learning_active():
    """Check if the most recent crawl event is within the last 30 seconds."""
    crawl_log = DATA_DIR / 'crawl_events.jsonl'
    try:
        mtime = crawl_log.stat().st_mtime
        return (datetime.now().timestamp() - mtime) < 30
    except FileNotFoundError:
        return False


# Color constants — aligned with visualization_prep.py
COLORS = {
    'logic': '#2196F3',
    'symbolic': '#F44336',
    'bridge': '#FF9800',
    'blocked': '#616161',
    'failed': '#455A64',
    'deferred': '#9E9E9E',
    'stored': '#4CAF50',
}

# Normalize classifier vocabulary on read (belt-and-suspenders with emit-side fix)
CLASSIFICATION_NORM = {'logical': 'logic'}

LOGIC_SHADES = ['#1a5276', '#1f6da0', '#2980b9', '#3498db', '#5dade2', '#85c1e9', '#aed6f1', '#d4e6f1']
SYMBOLIC_SHADES = ['#922b21', '#b03a2e', '#cb4335', '#e74c3c', '#ec7063', '#f1948a', '#f5b7b1', '#fadbd8']


# ═══════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════

def get_file_mtime(filename):
    path = DATA_DIR / filename
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return 0


@st.cache_data(ttl=30)
def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


@st.cache_data(ttl=3)
def load_crawl_events(path_str):
    """Load JSONL crawl events. Polled frequently for live view."""
    events = []
    try:
        with open(path_str, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        pass
    return events


# ═══════════════════════════════════════════════════════════════════════
# HEAVY COMPUTATION — CACHED AS SINGLETONS
# ═══════════════════════════════════════════════════════════════════════

class BrainCache:
    """Holds precomputed t-SNE coords, embeddings, and item metadata."""
    __slots__ = ('coords', 'embeddings', 'items', 'texts')

    def __init__(self, coords, embeddings, items, texts):
        self.coords = coords          # np.array (n, 2)
        self.embeddings = embeddings   # np.array (n, dim)
        self.items = items             # list of dicts (no embedding key)
        self.texts = texts             # list of str (for TF-IDF)


@st.cache_resource(ttl=300, show_spinner="Computing 2D projection (one-time)...")
def build_brain_cache(memory_file, file_mtime):
    """Load memory → extract embeddings → PCA+t-SNE → BrainCache.

    Cached as a singleton. Only recomputes when the file changes.
    """
    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA

    path = DATA_DIR / memory_file
    if not path.exists():
        return None

    with open(path, 'r', encoding='utf-8') as f:
        raw_items = json.load(f)

    embeddings, items, texts = [], [], []
    for item in raw_items:
        emb = item.get('embedding')
        if emb is not None:
            embeddings.append(emb)
            items.append({k: v for k, v in item.items() if k != 'embedding'})
            texts.append(item.get('text', '')[:500])

    if len(embeddings) < 2:
        return None

    embeddings = np.array(embeddings, dtype=np.float32)

    # Stage 1: PCA to 50 dims (fast)
    # Stage 2: t-SNE to 2D
    if len(embeddings) < 5:
        n_comp = min(2, embeddings.shape[1])
        pca = PCA(n_components=n_comp, random_state=42)
        coords = pca.fit_transform(embeddings)
        if coords.shape[1] < 2:
            coords = np.column_stack([coords, np.zeros(len(coords))])
    else:
        n_pca = min(50, len(embeddings) - 1, embeddings.shape[1])
        pca = PCA(n_components=n_pca, random_state=42)
        reduced = pca.fit_transform(embeddings)
        perplexity = min(30, len(embeddings) - 1)
        tsne = TSNE(
            n_components=2, perplexity=perplexity, max_iter=500,
            random_state=42, init='pca', learning_rate='auto'
        )
        coords = tsne.fit_transform(reduced)

    return BrainCache(coords, embeddings, items, texts)


def cluster_and_name(brain, n_clusters):
    """KMeans clustering + TF-IDF top-2 feature naming. Fast, not cached."""
    from sklearn.cluster import KMeans
    from sklearn.feature_extraction.text import TfidfVectorizer

    n = len(brain.embeddings)
    if n < n_clusters:
        n_clusters = max(1, n)

    if n_clusters <= 1:
        return np.zeros(n, dtype=int), {0: "all items"}

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(brain.embeddings)

    names = {}
    for cid in range(n_clusters):
        mask = labels == cid
        cluster_texts = [brain.texts[i] for i in range(n) if mask[i]]
        if not cluster_texts:
            names[cid] = f"cluster_{cid}"
            continue
        try:
            tfidf = TfidfVectorizer(max_features=100, stop_words='english')
            matrix = tfidf.fit_transform(cluster_texts)
            features = tfidf.get_feature_names_out()
            scores = np.asarray(matrix.mean(axis=0)).flatten()
            top = scores.argsort()[-2:][::-1]
            parts = [features[i] for i in top if scores[i] > 0]
            names[cid] = ' / '.join(parts) if parts else f"cluster_{cid}"
        except Exception:
            names[cid] = f"cluster_{cid}"

    return labels, names


# ═══════════════════════════════════════════════════════════════════════
# VIEW 1 — DUAL BRAIN CLUSTERS
# ═══════════════════════════════════════════════════════════════════════

def view_brain_clusters():
    st.header("Dual Brain Clusters")

    col_l, col_r = st.columns(2)

    with col_l:
        _render_brain("logic_memory.json", "Logic Brain", LOGIC_SHADES, COLORS['logic'])
    with col_r:
        _render_brain("symbolic_memory.json", "Symbolic Brain", SYMBOLIC_SHADES, COLORS['symbolic'])


def _render_brain(memory_file, title, palette, accent):
    mtime = get_file_mtime(memory_file)
    brain = build_brain_cache(memory_file, mtime)

    if brain is None:
        st.subheader(title)
        st.info("Not enough data to visualize (need at least 2 items with embeddings).")
        return

    n = len(brain.items)
    st.subheader(f"{title} ({n} items)")

    # Cluster slider — auto range based on item count
    max_k = max(2, min(12, n // 20 + 1))
    default_k = min(max_k, 8 if n > 20 else max(1, n))
    key = memory_file.replace('.', '_')

    if n > 6 and max_k > 2:
        n_clusters = st.slider("Clusters", 2, max_k, default_k, key=f"k_{key}")
    elif n > 6:
        n_clusters = max(1, n)
        st.caption(f"Auto: {n_clusters} cluster(s) ({n} items)")

    labels, cluster_names = cluster_and_name(brain, n_clusters)

    # Build scatter traces — one per cluster
    fig = go.Figure()

    for cid in range(n_clusters):
        mask = [i for i, l in enumerate(labels) if l == cid]
        if not mask:
            continue

        cname = cluster_names.get(cid, f"cluster_{cid}")
        color = palette[cid % len(palette)]

        hover = []
        for i in mask:
            item = brain.items[i]
            src = item.get('source_url') or item.get('source') or 'unknown'
            txt = item.get('text', '')[:120].replace('<', '&lt;')
            ls = item.get('logic_score', 'n/a')
            ss = item.get('symbolic_score', 'n/a')
            ts = (item.get('timestamp') or item.get('stored_at') or '')[:19]
            hover.append(
                f"<b>{cname}</b><br>"
                f"{txt}<br>"
                f"<i>{src[:60]}</i><br>"
                f"Logic: {ls} &nbsp; Symbolic: {ss}<br>"
                f"{ts}"
            )

        fig.add_trace(go.Scatter(
            x=[float(brain.coords[i, 0]) for i in mask],
            y=[float(brain.coords[i, 1]) for i in mask],
            mode='markers',
            name=cname,
            marker=dict(size=5, color=color, opacity=0.7),
            hovertext=hover,
            hoverinfo='text',
        ))

    # Centroid marker
    cx = float(np.mean(brain.coords[:, 0]))
    cy = float(np.mean(brain.coords[:, 1]))
    fig.add_trace(go.Scatter(
        x=[cx], y=[cy],
        mode='markers',
        name='Centroid',
        marker=dict(size=14, color='white', symbol='diamond',
                    line=dict(width=2, color=accent)),
        hovertext="<b>Centroid</b>",
        hoverinfo='text',
    ))

    fig.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(font=dict(size=9), orientation='h', yanchor='bottom', y=-0.15),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Item inspector
    options = [f"{i}: {brain.items[i].get('text', '')[:60]}" for i in range(n)]
    selected = st.selectbox("Inspect item", options, key=f"sel_{key}")
    idx = int(selected.split(':')[0])
    item = brain.items[idx]
    with st.expander("Item details", expanded=False):
        st.markdown(f"**Text:** {item.get('text', '')[:500]}")
        st.markdown(f"**Source:** {item.get('source_url', item.get('source', ''))}")
        st.markdown(f"**Cluster:** {cluster_names.get(int(labels[idx]), '?')}")
        cols = st.columns(3)
        cols[0].metric("Logic score", item.get('logic_score', '—'))
        cols[1].metric("Symbolic score", item.get('symbolic_score', '—'))
        cols[2].metric("Confidence", item.get('confidence', '—'))


# ═══════════════════════════════════════════════════════════════════════
# VIEW 2 — BRIDGE COSINE LEAN
# ═══════════════════════════════════════════════════════════════════════

def view_bridge_spectrum():
    st.header("Bridge Spectrum — Cosine Lean")

    bridge = load_json("bridge_memory.json")
    if not bridge:
        st.info("Bridge is empty — all content has migrated.")
        return

    # Compute centroids from logic and symbolic stores
    logic_centroid = _compute_centroid("logic_memory.json")
    sym_centroid = _compute_centroid("symbolic_memory.json")

    if logic_centroid is None:
        st.warning("No logic embeddings — cannot compute centroid.")
        return
    if sym_centroid is None:
        st.warning("No symbolic embeddings — cannot compute centroid. "
                    "Run a learning session so bootstrap can seed the symbolic brain.")
        return

    from sklearn.metrics.pairwise import cosine_similarity as cos_sim

    items_data = []
    for item in bridge:
        emb = item.get('embedding')
        if emb is not None:
            emb_arr = np.array(emb, dtype=np.float32).reshape(1, -1)
            l_sim = float(cos_sim(emb_arr, logic_centroid.reshape(1, -1))[0, 0])
            s_sim = float(cos_sim(emb_arr, sym_centroid.reshape(1, -1))[0, 0])
            # Lean: 0 = pure logic, 1 = pure symbolic.
            # Uses signed difference so negative similarities are handled correctly.
            lean = max(0.0, min(1.0, 0.5 + (s_sim - l_sim) / 2.0))
        else:
            l_sim, s_sim, lean = None, None, 0.5

        items_data.append({
            'label': item.get('text', '')[:50],
            'full_text': item.get('text', '')[:300],
            'source': item.get('source', item.get('source_url', '')),
            'logic_sim': l_sim,
            'sym_sim': s_sim,
            'lean': lean,
            'has_emb': emb is not None,
        })

    # ── Spectrum figure ──
    fig = go.Figure()

    # Background gradient bar
    grad_x = np.linspace(0, 1, 200).tolist()
    fig.add_trace(go.Scatter(
        x=grad_x, y=[-0.12] * 200,
        mode='markers',
        marker=dict(
            size=10, symbol='square',
            color=grad_x,
            colorscale=[[0, COLORS['logic']], [0.5, '#f1c40f'], [1, COLORS['symbolic']]],
            showscale=False,
        ),
        hoverinfo='skip',
        showlegend=False,
    ))

    # Bridge item markers
    for d in items_data:
        if d['has_emb']:
            # Map lean to the blue→yellow→red scale
            r = d['lean']
            if r < 0.5:
                # blue → yellow
                t = r / 0.5
                cr = int(52 + t * (241 - 52))
                cg = int(152 + t * (196 - 152))
                cb = int(219 + t * (15 - 219))
            else:
                # yellow → red
                t = (r - 0.5) / 0.5
                cr = int(241 + t * (231 - 241))
                cg = int(196 - t * (196 - 76))
                cb = int(15 + t * (60 - 15))
            color = f'rgb({cr},{cg},{cb})'
            opacity = 1.0
            hover = (
                f"<b>{d['label']}</b><br>"
                f"Logic sim: {d['logic_sim']:.4f}<br>"
                f"Symbolic sim: {d['sym_sim']:.4f}<br>"
                f"Lean: {d['lean']:.3f}<br>"
                f"<i>{d['source'][:60]}</i>"
            )
        else:
            color = COLORS['blocked']
            opacity = 0.35
            hover = f"<b>{d['label']}</b><br>No embedding — not yet scanned"

        fig.add_trace(go.Scatter(
            x=[d['lean']], y=[0],
            mode='markers+text',
            text=[d['label'][:25]],
            textposition='top center',
            textfont=dict(size=9),
            marker=dict(size=18, color=color, opacity=opacity,
                        line=dict(width=1, color='white')),
            hovertext=hover,
            hoverinfo='text',
            showlegend=False,
        ))

    # Anchor labels
    fig.add_annotation(x=0, y=-0.28, text="<b>Logic Centroid</b>", showarrow=False,
                       font=dict(color=COLORS['logic'], size=13))
    fig.add_annotation(x=1, y=-0.28, text="<b>Symbolic Centroid</b>", showarrow=False,
                       font=dict(color=COLORS['symbolic'], size=13))

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=20, b=50),
        xaxis=dict(range=[-0.08, 1.08], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-0.45, 0.45], showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detail table
    rows = []
    for d in items_data:
        rows.append({
            'Item': d['label'],
            'Logic Sim': f"{d['logic_sim']:.4f}" if d['logic_sim'] is not None else '—',
            'Symbolic Sim': f"{d['sym_sim']:.4f}" if d['sym_sim'] is not None else '—',
            'Lean': f"{d['lean']:.3f}" if d['has_emb'] else 'unscanned',
            'Source': d['source'][:70],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Context note
    st.caption(f"{len(bridge)} items in bridge. Sparse is correct — "
               "bridge is a transit zone, not a destination.")


@st.cache_data(ttl=60)
def _compute_centroid(memory_file):
    """Mean embedding vector across all items in a memory store."""
    path = DATA_DIR / memory_file
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        items = json.load(f)
    embs = [item['embedding'] for item in items if item.get('embedding') is not None]
    if not embs:
        return None
    return np.mean(np.array(embs, dtype=np.float32), axis=0)


# ═══════════════════════════════════════════════════════════════════════
# NARRATIVE CONTEXT — nearest neighbors + cluster labels for stored items
# ═══════════════════════════════════════════════════════════════════════

def _build_narrative_context(recent_events):
    """For stored events, find nearest neighbors and cluster via brain cache.

    Returns {url: {'neighbors': [...], 'cluster': str}} or empty dict.
    Only pays the cost if brain cache is already warm.
    """
    stored = [e for e in recent_events if e.get('status') == 'stored']
    if not stored:
        return {}

    # Group stored events by which brain they went to
    by_brain = {}
    for e in stored:
        classification = CLASSIFICATION_NORM.get(e.get('classification'), e.get('classification'))
        mem_file = {'logic': 'logic_memory.json', 'symbolic': 'symbolic_memory.json',
                    'bridge': 'bridge_memory.json'}.get(classification)
        if mem_file:
            by_brain.setdefault(mem_file, []).append(e)

    result = {}

    for mem_file, mem_events in by_brain.items():
        mtime = get_file_mtime(mem_file)
        brain = build_brain_cache(mem_file, mtime)
        if brain is None:
            continue

        # Build URL → index lookup (check both key conventions)
        url_to_idx = {}
        for i, item in enumerate(brain.items):
            src = item.get('source_url') or item.get('source') or ''
            url_to_idx[src] = i

        # Compute clusters once per brain (default k)
        n = len(brain.items)
        default_k = min(8, max(2, n // 20 + 1)) if n > 3 else max(1, n)
        labels, cluster_names = cluster_and_name(brain, default_k)

        for e in mem_events:
            url = e.get('url', '')
            idx = url_to_idx.get(url)
            if idx is None:
                continue

            # Nearest neighbors via cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity as cos_sim
            emb = brain.embeddings[idx].reshape(1, -1)
            sims = cos_sim(emb, brain.embeddings)[0]

            # Exclude self AND duplicate URLs (same page stored across sessions)
            item_url = url
            for j, it in enumerate(brain.items):
                if (it.get('source_url') or it.get('source') or '') == item_url:
                    sims[j] = -2.0

            top_indices = sims.argsort()[::-1]
            neighbors = []
            seen_urls = set()
            for ni in top_indices:
                if len(neighbors) >= 2:
                    break
                nsrc = brain.items[ni].get('source_url') or brain.items[ni].get('source') or ''
                if nsrc in seen_urls:
                    continue
                seen_urls.add(nsrc)
                path_end = urlparse(nsrc).path.rstrip('/').split('/')[-1]
                label = path_end.replace('_', ' ')[:45] if path_end else nsrc[:45]
                neighbors.append(label)

            # Cluster label for this item
            cluster_label = None
            if labels is not None and idx < len(labels):
                cluster_label = cluster_names.get(int(labels[idx]))

            result[url] = {'neighbors': neighbors, 'cluster': cluster_label}

    return result


# ═══════════════════════════════════════════════════════════════════════
# VIEW 3 — REAL-TIME CRAWL TRACKER
# ═══════════════════════════════════════════════════════════════════════

def view_crawl_tracker():
    # Pulse indicator — green breathing dot when active, gray when idle
    active = _is_learning_active()
    dot_class = 'pulse-active' if active else 'pulse-idle'
    status_text = 'learning' if active else 'idle'
    st.markdown(
        f'<span class="{dot_class}"></span> <b>Crawl Tracker</b> '
        f'<span style="color:#888;font-size:0.85em;">({status_text})</span>',
        unsafe_allow_html=True,
    )

    crawl_log = DATA_DIR / 'crawl_events.jsonl'

    # Fallback: try to load from the latest session file
    events = []
    if crawl_log.exists():
        events = load_crawl_events(str(crawl_log))

    if not events:
        st.info("No crawl events yet. Start a learning session to generate the trail.")
        st.caption(f"The learner writes to: `{crawl_log}`")

        # Offer to view a past session's data
        session_dir = DATA_DIR / 'autonomous_sessions'
        if session_dir.exists():
            sessions = sorted(session_dir.glob('*.json'), reverse=True)
            if sessions:
                st.markdown("---")
                st.subheader("Past sessions available")
                for s in sessions[:5]:
                    st.caption(f"  {s.name}")
                st.caption("(Past sessions don't have per-URL event data — "
                           "the JSONL format is new. Future sessions will populate this view.)")
        return

    # ── Stats bar ──
    c1, c2, c3, c4, c5 = st.columns(5)
    stored = [e for e in events if e.get('status') == 'stored']
    blocked = [e for e in events if 'blocked' in e.get('status', '')]
    failed = [e for e in events if e.get('status') in ('fetch_failed', 'error')]
    deferred = [e for e in events if e.get('status') == 'deferred']

    c1.metric("Total Events", len(events))
    c2.metric("Stored", len(stored))
    c3.metric("Blocked", len(blocked))
    c4.metric("Failed", len(failed))

    class_counts = {}
    for e in stored:
        c = CLASSIFICATION_NORM.get(e.get('classification'), e.get('classification')) or 'unknown'
        class_counts[c] = class_counts.get(c, 0) + 1
    c5.metric("L / S / B",
              f"{class_counts.get('logic', 0)} / "
              f"{class_counts.get('symbolic', 0)} / "
              f"{class_counts.get('bridge', 0)}")

    # ── Build directed graph ──
    import networkx as nx
    G = nx.DiGraph()

    for e in events:
        url = e.get('url', '')
        parent = e.get('parent_url')
        status = e.get('status', 'unknown')
        classification = CLASSIFICATION_NORM.get(e.get('classification'), e.get('classification'))

        if status == 'stored':
            color = COLORS.get(classification, COLORS['bridge'])
        elif 'blocked' in status:
            color = COLORS['blocked']
        elif status == 'deferred':
            color = COLORS['deferred']
        else:
            color = COLORS['failed']

        parsed = urlparse(url)
        path_parts = parsed.path.rstrip('/').split('/')
        label = path_parts[-1][:35] if path_parts[-1] else parsed.netloc[:25]

        # Map to legend category: stored events use classification,
        # non-stored events map their status to the fixed legend categories
        STATUS_TO_LEGEND = {
            'robots_blocked': 'robots_blocked',
            'warfare_blocked': 'warfare_blocked',
            'immune_blocked': 'robots_blocked',
            'fetch_failed': 'failed',
            'error': 'failed',
            'insufficient_content': 'failed',
            'quality_failed': 'failed',
            'deferred': 'failed',
        }
        legend_group = classification if status == 'stored' else STATUS_TO_LEGEND.get(status, 'failed')

        G.add_node(url, color=color, label=label, status=status,
                    classification=legend_group,
                    text_preview=e.get('text_preview') or '')

        if parent and parent in G:
            G.add_edge(parent, url)

    if not G.nodes:
        st.info("No graph nodes.")
        return

    # Layout
    pos = nx.spring_layout(G, k=1.5 / (len(G.nodes) ** 0.3 + 1),
                           iterations=60, seed=42)

    # Edge traces
    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    fig = go.Figure()

    if edge_x:
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=0.4, color='#555'),
            hoverinfo='none',
            showlegend=False,
        ))

    # Node traces — fixed legend categories, always present
    LEGEND_CATEGORIES = [
        ('logic', COLORS['logic']),
        ('symbolic', COLORS['symbolic']),
        ('bridge', COLORS['bridge']),
        ('robots_blocked', COLORS['blocked']),
        ('warfare_blocked', COLORS['failed']),
        ('failed', COLORS['failed']),
    ]

    groups = {cat: {'x': [], 'y': [], 'hover': []} for cat, _ in LEGEND_CATEGORIES}
    # Catch any status not in the fixed list
    extra_colors = {}

    for node in G.nodes():
        d = G.nodes[node]
        group = d['classification']
        if group not in groups:
            groups[group] = {'x': [], 'y': [], 'hover': []}
            extra_colors[group] = d['color']
        x, y = pos[node]
        groups[group]['x'].append(x)
        groups[group]['y'].append(y)
        groups[group]['hover'].append(
            f"<b>{d['label']}</b><br>"
            f"Status: {d['status']}<br>"
            f"Class: {d['classification']}<br>"
            f"{(d.get('text_preview') or '')[:80]}"
        )

    cat_colors = {cat: col for cat, col in LEGEND_CATEGORIES}
    cat_colors.update(extra_colors)

    for cat, _ in LEGEND_CATEGORIES:
        gd = groups[cat]
        has_data = len(gd['x']) > 0
        fig.add_trace(go.Scatter(
            x=gd['x'] if has_data else [None],
            y=gd['y'] if has_data else [None],
            mode='markers',
            name=cat,
            marker=dict(size=7, color=cat_colors[cat], opacity=0.85),
            hovertext=gd['hover'] if has_data else [None],
            hoverinfo='text' if has_data else 'none',
        ))

    # Any overflow categories not in the fixed list
    for group in groups:
        if group not in cat_colors or group in dict(LEGEND_CATEGORIES):
            continue
        gd = groups[group]
        if gd['x']:
            fig.add_trace(go.Scatter(
                x=gd['x'], y=gd['y'],
                mode='markers',
                name=group,
                marker=dict(size=7, color=extra_colors.get(group, COLORS['blocked']), opacity=0.85),
                hovertext=gd['hover'],
                hoverinfo='text',
            ))

    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(font=dict(size=10)),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Recent events — summary table + narrative for stored items
    st.subheader("Recent events")
    recent = events[-20:][::-1]

    # Enrich stored events with narrative context
    narrative_ctx = _build_narrative_context(recent)

    rows = []
    for e in recent:
        parsed = urlparse(e.get('url', ''))
        path_parts = parsed.path.rstrip('/').split('/')
        short = path_parts[-1][:40] if path_parts[-1] else parsed.netloc[:30]
        status = e.get('status', '')
        classification = CLASSIFICATION_NORM.get(e.get('classification'), e.get('classification')) or '—'
        l_sim = e.get('logic_sim')
        s_sim = e.get('symbolic_sim')

        row = {
            'Time': e.get('timestamp', '')[-8:],
            'URL': short,
            'Status': status,
            'Class': classification,
            'Logic ↔': f"{l_sim:.3f}" if l_sim is not None else '',
            'Sym ↔': f"{s_sim:.3f}" if s_sim is not None else '',
            'Preview': (e.get('text_preview') or '')[:50],
        }
        rows.append(row)

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Narrative detail for stored items
    stored_recent = [e for e in recent if e.get('status') == 'stored']
    if stored_recent and narrative_ctx:
        st.subheader("Learning narrative")
        for e in stored_recent[:8]:
            url = e.get('url', '')
            ctx = narrative_ctx.get(url)
            classification = CLASSIFICATION_NORM.get(e.get('classification'), e.get('classification')) or '?'
            l_sim = e.get('logic_sim')
            s_sim = e.get('symbolic_sim')
            preview = (e.get('text_preview') or '')[:60]

            parsed = urlparse(url)
            path_parts = parsed.path.rstrip('/').split('/')
            short_url = path_parts[-1][:45] if path_parts[-1] else parsed.netloc[:30]

            # Build narrative line
            scores = ''
            if l_sim is not None and s_sim is not None:
                scores = f"({l_sim:.2f} logic / {s_sim:.2f} symbolic)"

            neighbors = ''
            cluster = ''
            if ctx:
                if ctx.get('neighbors'):
                    neighbor_labels = [n[:40] for n in ctx['neighbors'][:2]]
                    neighbors = f" · near: {', '.join(neighbor_labels)}"
                if ctx.get('cluster'):
                    cluster = f" · cluster: **{ctx['cluster']}**"

            with st.expander(f"**{short_url}** → {classification} {scores}", expanded=False):
                st.markdown(f"*{preview}*")
                if neighbors or cluster:
                    st.markdown(f"Stored → {classification} {scores}{neighbors}{cluster}")
                st.caption(f"Source: {url}")

    # Toast new stored events
    current_count = len(events)
    if current_count > st.session_state.last_toast_count:
        new_events = events[st.session_state.last_toast_count:]
        for ne in new_events:
            if ne.get('status') == 'stored':
                classification = CLASSIFICATION_NORM.get(ne.get('classification'), ne.get('classification')) or '?'
                url_path = urlparse(ne.get('url', '')).path.split('/')[-1].replace('_', ' ')[:30]
                ctx = narrative_ctx.get(ne.get('url', ''))
                near = ''
                if ctx and ctx.get('neighbors'):
                    near = f" · near: {ctx['neighbors'][0][:25]}"
                st.toast(f"Learned: {url_path} → {classification}{near}")
    st.session_state.last_toast_count = current_count


# ═══════════════════════════════════════════════════════════════════════
# VIEW 4 — SYSTEM HEALTH
# ═══════════════════════════════════════════════════════════════════════

def _health_color(val):
    """Red < 0.3, yellow 0.3–0.6, green > 0.6."""
    if val < 0.3:
        return '#F44336'
    if val < 0.6:
        return '#FFC107'
    return '#4CAF50'


def _bar_chart(labels, values, title, invert=False):
    """Horizontal bar chart with fill animation. invert=True for drives where low=hungry."""
    display = [1.0 - v for v in values] if invert else values
    colors = [_health_color(v) for v in display]

    # Start from zero, animate to actual values
    zero = [0.0] * len(labels)
    bar_kwargs = dict(y=labels, orientation='h', marker_color=colors,
                      text=[f"{v:.2f}" for v in display], textposition='inside')

    fig = go.Figure(
        data=[go.Bar(x=zero, **bar_kwargs)],
        frames=[go.Frame(data=[go.Bar(x=display, **bar_kwargs)])],
    )
    # Auto-play the fill animation on load
    fig.update_layout(
        title=title, height=max(180, 35 * len(labels)),
        margin=dict(l=0, r=10, t=30, b=0),
        xaxis=dict(range=[0, 1.05], showticklabels=False),
        yaxis=dict(autorange='reversed'),
        plot_bgcolor='rgba(0,0,0,0)',
        updatemenus=[dict(
            type='buttons', showactive=False, visible=False,
            buttons=[dict(label='', method='animate',
                          args=[None, dict(frame=dict(duration=700, redraw=True),
                                           transition=dict(duration=700, easing='cubic-in-out'),
                                           fromcurrent=True, mode='immediate')])]
        )],
    )
    return fig


def view_system_health():
    st.markdown('<div class="health-fade">', unsafe_allow_html=True)
    st.header("System Health")

    col_left, col_right = st.columns(2)

    # ── Curiosity Drives ──
    with col_left:
        curiosity = load_json("curiosity_state.json")
        if curiosity and curiosity.get('satisfaction_history'):
            # Extract latest satisfaction level per drive
            latest = {}
            for entry in curiosity['satisfaction_history']:
                drive = entry.get('drive')
                if drive:
                    latest[drive] = entry.get('new_level', 0.0)

            if latest:
                drive_descriptions = {
                    'autonomy': 'Need for independent choice — high = actively self-directing',
                    'connection': 'Need to find patterns and relationships — high = seeking links',
                    'creativity': 'Need to synthesize and create — high = generating new ideas',
                    'growth': 'Need to expand capabilities — high = pushing boundaries',
                    'meaning': 'Need for purpose and significance — high = questioning why',
                    'understanding': 'Need to comprehend — high = actively investigating',
                }
                drives = sorted(latest.keys())
                vals = [latest[d] for d in drives]
                st.plotly_chart(
                    _bar_chart(drives, vals, "Curiosity Drives (full bar = hungry, seeking)", invert=True),
                    use_container_width=True,
                )
                for d in drives:
                    intensity = 1.0 - latest[d]
                    desc = drive_descriptions.get(d, '')
                    if intensity > 0.7:
                        st.caption(f"**{d}** — {desc}")
                momentum = curiosity.get('learning_momentum', 0)
                st.caption(f"Learning momentum: {momentum:.4f}")
            else:
                st.info("No curiosity drive data yet.")
        else:
            st.info("No curiosity state file found.")

    # ── Brain Metrics ──
    with col_right:
        reflections = load_json("brain_reflection_history.json")
        if reflections and isinstance(reflections, list) and len(reflections) > 0:
            last = reflections[-1]
            metrics = last.get('metrics', {})
            labels = ['Brain Harmony', 'Learning Effectiveness', 'Adaptive Capacity', 'Performance Satisfaction']
            vals = [
                metrics.get('brain_harmony_assessment', 0),
                metrics.get('learning_effectiveness', 0),
                metrics.get('adaptive_capacity', 0),
                metrics.get('performance_satisfaction', 0),
            ]
            st.plotly_chart(
                _bar_chart(labels, vals, "Brain Metrics"),
                use_container_width=True,
            )
            insights = metrics.get('processing_insights', [])
            if insights:
                st.caption(' · '.join(insights[:3]))
        else:
            st.info("No brain reflection data yet.")

    col_left2, col_right2 = st.columns(2)

    # ── Memory Health ──
    with col_left2:
        logic_count = len(load_json("logic_memory.json"))
        sym_count = len(load_json("symbolic_memory.json"))
        bridge_count = len(load_json("bridge_memory.json"))
        total = logic_count + sym_count + bridge_count

        st.subheader("Memory")
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Logic", f"{logic_count:,}")
        mc2.metric("Symbolic", f"{sym_count:,}")
        mc3.metric("Bridge", f"{bridge_count:,}")

        # Health from analytics history
        analytics = load_json("memory_analytics_history.json")
        if analytics and isinstance(analytics, list):
            last_a = analytics[-1]
            health = last_a.get('health', {})
            status = health.get('status', 'unknown')
            issues = health.get('issues', [])
            st.caption(f"Status: **{status}**" + (f" — {issues[0]}" if issues else ""))

            stability = last_a.get('stability_metrics', {})
            if stability:
                labels = ['Logic Stability', 'Symbolic Stability', 'Bridge Stability']
                vals = [
                    stability.get('logic_stability', 0),
                    stability.get('symbolic_stability', 0),
                    stability.get('bridge_stability', 0),
                ]
                st.plotly_chart(
                    _bar_chart(labels, vals, "Memory Stability"),
                    use_container_width=True,
                )

        # Sovereignty
        sov_path = DATA_DIR / 'sovereignty_log.json'
        if sov_path.exists():
            sov = load_json("sovereignty_log.json")
            if sov and isinstance(sov, dict):
                st.markdown("---")
                st.subheader("Sovereignty")
                sc1, sc2, sc3 = st.columns(3)
                sc1.metric("Decisions", sov.get('total_decisions', 0))
                sc2.metric("Vetoes", sov.get('veto_count', 0))
                sc3.metric("Health", sov.get('sovereignty_health', '—'))
                recent = sov.get('recent_decisions', [])
                if recent:
                    for d in recent[-3:]:
                        icon = {'veto': '🚫', 'approved': '✅', 'conditional': '⚠️',
                                'override_denied': '🛡️'}.get(d.get('decision'), '•')
                        st.caption(f"{icon} {d.get('decision', '?')} — {d.get('reasoning', '')[:80]}")

    # ── Learning Progression ──
    with col_right2:
        progression = load_json("learning_progression_detailed.json")
        if progression and isinstance(progression, dict):
            concepts = []
            understandings = []
            confidences = []
            for name, data in sorted(progression.items()):
                concepts.append(name.replace('_', ' '))
                understandings.append(data.get('understanding_level', data.get('current_level', 0)))
                confidences.append(data.get('confidence_level', 0))

            if concepts:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    y=concepts, x=understandings, orientation='h',
                    name='Understanding',
                    marker_color=[_health_color(v) for v in understandings],
                    text=[f"{v:.2f}" for v in understandings],
                    textposition='inside',
                ))
                fig.add_trace(go.Bar(
                    y=concepts, x=confidences, orientation='h',
                    name='Confidence',
                    marker_color='rgba(255,255,255,0.3)',
                    text=[f"{v:.2f}" for v in confidences],
                    textposition='inside',
                ))
                fig.update_layout(
                    title="Learning Progression",
                    barmode='overlay',
                    height=max(200, 40 * len(concepts)),
                    margin=dict(l=0, r=10, t=30, b=0),
                    xaxis=dict(range=[0, 1], showticklabels=False),
                    yaxis=dict(autorange='reversed'),
                    legend=dict(font=dict(size=9), orientation='h'),
                    plot_bgcolor='rgba(0,0,0,0)',
                )
                st.plotly_chart(fig, use_container_width=True)

                # Recent milestones
                milestones = load_json("learning_milestones.json")
                if milestones and isinstance(milestones, list):
                    recent_ms = milestones[-5:][::-1]
                    st.caption("Recent milestones:")
                    for m in recent_ms:
                        mtype = m.get('milestone_type', '?')
                        concept = m.get('concept', '?')
                        delta = m.get('understanding_change', 0)
                        icon = {'breakthrough': '💡', 'connection': '🔗', 'progress': '📈',
                                'synthesis': '🧬'}.get(mtype, '•')
                        st.caption(f"{icon} {concept}: {mtype} (+{delta:.2f})")
        else:
            st.info("No learning progression data yet.")

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

st.title("Sofia Brain Dashboard")

# Live mode — sidebar toggle controls fragment polling
live_mode = st.sidebar.toggle("Live mode", value=False,
                               help="Auto-refresh Crawl Tracker (5s) and System Health (15s)")

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Brain Clusters",
    "🌉 Bridge Spectrum",
    "🕸️ Crawl Tracker",
    "💊 System Health",
])

with tab1:
    view_brain_clusters()
with tab2:
    view_bridge_spectrum()

# Fragment-wrapped versions for live polling
if live_mode:
    @st.fragment(run_every=timedelta(seconds=5))
    def _crawl_live():
        view_crawl_tracker()

    @st.fragment(run_every=timedelta(seconds=15))
    def _health_live():
        view_system_health()

    with tab3:
        _crawl_live()
    with tab4:
        _health_live()
else:
    with tab3:
        view_crawl_tracker()
    with tab4:
        view_system_health()
