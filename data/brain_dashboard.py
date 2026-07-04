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
import subprocess
import psutil

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
    import networkx as nx

    # Pulse indicator
    active = _is_learning_active()
    dot_class = 'pulse-active' if active else 'pulse-idle'
    status_text = 'learning' if active else 'idle'
    st.markdown(
        f'<span class="{dot_class}"></span> <b>Crawl Tracker</b> '
        f'<span style="color:#888;font-size:0.85em;">({status_text})</span>',
        unsafe_allow_html=True,
    )

    crawl_log = DATA_DIR / 'crawl_events.jsonl'
    all_events = load_crawl_events(str(crawl_log)) if crawl_log.exists() else []

    if not all_events:
        st.info("No crawl events yet. Start a learning session to generate the trail.")
        return

    # ── Session toggle ──
    session_ids = list(dict.fromkeys(
        e.get('session_id', '') for e in all_events if e.get('session_id')))
    scope = st.radio("Scope", ["Current Session", "All Sessions"],
                     horizontal=True, label_visibility='collapsed',
                     key='crawl_scope')
    latest_sid = session_ids[-1] if session_ids else None

    if scope == "Current Session" and latest_sid:
        events = [e for e in all_events if e.get('session_id') == latest_sid]
        st.caption(f"Session: {latest_sid} ({len(events)} events)")
    else:
        events = all_events

    if not events:
        st.info("No events for this session yet.")
        return

    # ── Stats bar ──
    c1, c2, c3, c4, c5 = st.columns(5)
    stored = [e for e in events if e.get('status') == 'stored']
    blocked = [e for e in events if 'blocked' in e.get('status', '')]
    failed = [e for e in events if e.get('status') in ('fetch_failed', 'error')]

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
    G = nx.DiGraph()

    STATUS_TO_LEGEND = {
        'robots_blocked': 'robots_blocked',
        'warfare_blocked': 'warfare_blocked',
        'immune_blocked': 'robots_blocked',
        'fetch_failed': 'failed', 'error': 'failed',
        'insufficient_content': 'failed', 'quality_failed': 'failed',
        'deferred': 'failed',
    }

    for e in events:
        url = e.get('url', '')
        parent = e.get('parent_url')
        status = e.get('status', 'unknown')
        classification = CLASSIFICATION_NORM.get(
            e.get('classification'), e.get('classification'))

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
        legend_group = (classification if status == 'stored'
                        else STATUS_TO_LEGEND.get(status, 'failed'))

        G.add_node(url, color=color, label=label, status=status,
                    classification=legend_group,
                    text_preview=e.get('text_preview') or '')

        if parent and parent in G:
            G.add_edge(parent, url)

    if not G.nodes:
        st.info("No graph nodes.")
        return

    # ── Stable layout: cache positions, only compute new nodes ──
    cache_key = 'crawl_pos_cache'
    if cache_key not in st.session_state:
        st.session_state[cache_key] = {}
    pos_cache = st.session_state[cache_key]

    new_nodes = [n for n in G.nodes if n not in pos_cache]
    if new_nodes:
        sub = G.subgraph(new_nodes)
        new_pos = nx.spring_layout(
            sub, k=1.5 / (len(G.nodes) ** 0.3 + 1),
            iterations=60, seed=42)
        pos_cache.update(new_pos)

    pos = {n: pos_cache[n] for n in G.nodes if n in pos_cache}

    # ── Edge traces — colored by destination node ──
    edge_groups = {}  # color -> (xs, ys)
    for u, v in G.edges():
        if u not in pos or v not in pos:
            continue
        dest_color = G.nodes[v].get('color', '#555')
        if dest_color not in edge_groups:
            edge_groups[dest_color] = {'x': [], 'y': []}
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_groups[dest_color]['x'].extend([x0, x1, None])
        edge_groups[dest_color]['y'].extend([y0, y1, None])

    fig = go.Figure()

    for edge_color, coords in edge_groups.items():
        fig.add_trace(go.Scatter(
            x=coords['x'], y=coords['y'],
            mode='lines',
            line=dict(width=0.6, color=edge_color),
            opacity=0.4,
            hoverinfo='none', showlegend=False,
        ))

    # ── Node traces ──
    LEGEND_CATEGORIES = [
        ('logic', COLORS['logic']),
        ('symbolic', COLORS['symbolic']),
        ('bridge', COLORS['bridge']),
        ('robots_blocked', COLORS['blocked']),
        ('warfare_blocked', COLORS['failed']),
        ('failed', COLORS['failed']),
    ]

    groups = {cat: {'x': [], 'y': [], 'hover': []} for cat, _ in LEGEND_CATEGORIES}
    extra_colors = {}

    for node in G.nodes():
        if node not in pos:
            continue
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

    cat_colors = dict(LEGEND_CATEGORIES)
    cat_colors.update(extra_colors)

    for cat, _ in LEGEND_CATEGORIES:
        gd = groups[cat]
        has_data = len(gd['x']) > 0
        fig.add_trace(go.Scatter(
            x=gd['x'] if has_data else [None],
            y=gd['y'] if has_data else [None],
            mode='markers', name=cat,
            marker=dict(size=7, color=cat_colors[cat], opacity=0.85),
            hovertext=gd['hover'] if has_data else [None],
            hoverinfo='text' if has_data else 'none',
        ))

    for group in groups:
        if group in dict(LEGEND_CATEGORIES):
            continue
        gd = groups[group]
        if gd['x']:
            fig.add_trace(go.Scatter(
                x=gd['x'], y=gd['y'], mode='markers', name=group,
                marker=dict(size=7,
                            color=extra_colors.get(group, COLORS['blocked']),
                            opacity=0.85),
                hovertext=gd['hover'], hoverinfo='text',
            ))

    # uirevision preserves zoom/pan state across refreshes
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=10, b=40),
        uirevision='crawl_tracker',
        legend=dict(font=dict(size=11), orientation='h',
                    yanchor='top', y=-0.02, xanchor='center', x=0.5),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        dragmode='pan',
    )
    st.plotly_chart(fig, use_container_width=True, config={
        'scrollZoom': True,
        'displayModeBar': True,
        'modeBarButtonsToAdd': ['zoom2d', 'pan2d', 'resetScale2d'],
    })

    # ── Recent events table ──
    st.subheader("Recent events")
    recent = events[-20:][::-1]
    narrative_ctx = _build_narrative_context(recent)

    rows = []
    for e in recent:
        parsed = urlparse(e.get('url', ''))
        path_parts = parsed.path.rstrip('/').split('/')
        short = path_parts[-1][:40] if path_parts[-1] else parsed.netloc[:30]
        status = e.get('status', '')
        classification = CLASSIFICATION_NORM.get(
            e.get('classification'), e.get('classification')) or '—'
        l_sim = e.get('logic_sim')
        s_sim = e.get('symbolic_sim')
        rows.append({
            'Time': e.get('timestamp', '')[-8:],
            'URL': short,
            'Status': status,
            'Class': classification,
            'Logic': f"{l_sim:.3f}" if l_sim is not None else '',
            'Sym': f"{s_sim:.3f}" if s_sim is not None else '',
            'Preview': (e.get('text_preview') or '')[:50],
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Narrative detail
    stored_recent = [e for e in recent if e.get('status') == 'stored']
    if stored_recent and narrative_ctx:
        st.subheader("Learning narrative")
        for e in stored_recent[:8]:
            url = e.get('url', '')
            ctx = narrative_ctx.get(url)
            classification = CLASSIFICATION_NORM.get(
                e.get('classification'), e.get('classification')) or '?'
            l_sim = e.get('logic_sim')
            s_sim = e.get('symbolic_sim')
            preview = (e.get('text_preview') or '')[:60]

            parsed = urlparse(url)
            path_parts = parsed.path.rstrip('/').split('/')
            short_url = path_parts[-1][:45] if path_parts[-1] else parsed.netloc[:30]

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

            with st.expander(f"**{short_url}** → {classification} {scores}",
                             expanded=False):
                st.markdown(f"*{preview}*")
                if neighbors or cluster:
                    st.markdown(
                        f"Stored → {classification} {scores}{neighbors}{cluster}")
                st.caption(f"Source: {url}")

    # Toast new stored events
    current_count = len(all_events)
    if current_count > st.session_state.last_toast_count:
        new_events = all_events[st.session_state.last_toast_count:]
        for ne in new_events:
            if ne.get('status') == 'stored':
                classification = CLASSIFICATION_NORM.get(
                    ne.get('classification'), ne.get('classification')) or '?'
                url_path = (urlparse(ne.get('url', '')).path
                            .split('/')[-1].replace('_', ' ')[:30])
                ctx = narrative_ctx.get(ne.get('url', ''))
                near = ''
                if ctx and ctx.get('neighbors'):
                    near = f" · near: {ctx['neighbors'][0][:25]}"
                st.toast(f"Learned: {url_path} → {classification}{near}")
    st.session_state.last_toast_count = current_count


# ═══════════════════════════════════════════════════════════════════════
# ── System Metrics (psutil + nvidia-smi) ──────────────────────────────

def _find_sofia_pid() -> int | None:
    """Find Sofia's main Python process by command-line pattern."""
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = ' '.join(p.info['cmdline'] or [])
            if 'python' in (p.info['name'] or '').lower() and 'enhanced_autonomous' in cmd:
                return p.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None


def _get_system_metrics() -> dict:
    """Cross-platform system + Sofia process metrics via psutil + nvidia-smi."""
    # ── CPU (system-wide) ──
    cpu_pct = psutil.cpu_percent(interval=None)

    # ── RAM ──
    vm = psutil.virtual_memory()
    sys_ram_used_gb = round(vm.used / (1024 ** 3), 1)
    sys_ram_total_gb = round(vm.total / (1024 ** 3), 1)
    sys_ram_pct = vm.percent

    sofia_ram_gb = 0.0
    sofia_pid = _find_sofia_pid()
    if sofia_pid:
        try:
            proc = psutil.Process(sofia_pid)
            sofia_ram_gb = round(proc.memory_info().rss / (1024 ** 3), 2)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # ── GPU / VRAM ──
    gpu_pct = 0.0
    sys_vram_used_gb = 0.0
    sys_vram_total_gb = 0.0
    sys_vram_pct = 0.0
    sofia_vram_gb = 0.0
    gpu_temp = 0.0
    try:
        out = subprocess.check_output(
            ['nvidia-smi',
             '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu',
             '--format=csv,noheader,nounits'],
            timeout=3, text=True).strip()
        parts = [x.strip() for x in out.split(',')]
        gpu_pct = float(parts[0])
        sys_vram_used_gb = round(float(parts[1]) / 1024, 1)
        sys_vram_total_gb = round(float(parts[2]) / 1024, 1)
        sys_vram_pct = round(100 * float(parts[1]) / float(parts[2]), 1) if float(parts[2]) else 0
        gpu_temp = float(parts[3])
    except Exception:
        pass

    # Per-process VRAM for Sofia
    if sofia_pid:
        try:
            apps = subprocess.check_output(
                ['nvidia-smi', '--query-compute-apps=pid,used_memory',
                 '--format=csv,noheader,nounits'],
                timeout=3, text=True).strip()
            for row in apps.splitlines():
                cols = [c.strip() for c in row.split(',')]
                if len(cols) >= 2 and cols[0] == str(sofia_pid):
                    sofia_vram_gb = round(float(cols[1]) / 1024, 2)
                    break
        except Exception:
            pass

    return {
        'cpu_pct': cpu_pct,
        'sys_ram_used_gb': sys_ram_used_gb, 'sys_ram_total_gb': sys_ram_total_gb,
        'sys_ram_pct': sys_ram_pct, 'sofia_ram_gb': sofia_ram_gb,
        'gpu_pct': gpu_pct,
        'sys_vram_used_gb': sys_vram_used_gb, 'sys_vram_total_gb': sys_vram_total_gb,
        'sys_vram_pct': sys_vram_pct, 'sofia_vram_gb': sofia_vram_gb,
        'gpu_temp': gpu_temp, 'sofia_pid': sofia_pid,
    }


def _record_metrics_history(m: dict):
    """Accumulate metrics in session_state for historical graphs."""
    if 'metrics_history' not in st.session_state:
        st.session_state['metrics_history'] = {
            'timestamps': [], 'cpu': [], 'sys_ram': [],
            'gpu': [], 'sys_vram': [], 'temp': [],
            'sofia_ram': [], 'sofia_vram': [],
        }
    h = st.session_state['metrics_history']
    h['timestamps'].append(datetime.now())
    h['cpu'].append(m['cpu_pct'])
    h['sys_ram'].append(m['sys_ram_pct'])
    h['gpu'].append(m['gpu_pct'])
    h['sys_vram'].append(m['sys_vram_pct'])
    h['temp'].append(m['gpu_temp'])
    h['sofia_ram'].append(m['sofia_ram_gb'])
    h['sofia_vram'].append(m['sofia_vram_gb'])
    cap = 720
    for k in h:
        if len(h[k]) > cap:
            h[k] = h[k][-cap:]


def _gauge(value, title, suffix='%', max_val=100, color=None):
    """Compact Plotly gauge indicator."""
    if color is None:
        if value < 50:
            color = '#4CAF50'
        elif value < 80:
            color = '#FFC107'
        else:
            color = '#F44336'
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=value,
        number={'suffix': suffix, 'font': {'size': 24}},
        title={'text': title, 'font': {'size': 11}},
        gauge={
            'axis': {'range': [0, max_val], 'tickwidth': 0,
                     'tickcolor': 'rgba(0,0,0,0)'},
            'bar': {'color': color},
            'bgcolor': 'rgba(255,255,255,0.05)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, max_val * 0.5], 'color': 'rgba(76,175,80,0.08)'},
                {'range': [max_val * 0.5, max_val * 0.8], 'color': 'rgba(255,193,7,0.08)'},
                {'range': [max_val * 0.8, max_val], 'color': 'rgba(244,67,54,0.08)'},
            ],
        },
    ))
    fig.update_layout(height=160, margin=dict(l=15, r=15, t=35, b=5))
    return fig


# Shared layout defaults for all charts
_CHART_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12),
    margin=dict(l=50, r=20, t=50, b=40),
    legend=dict(orientation='h', yanchor='top', y=-0.15,
                xanchor='center', x=0.5, font=dict(size=11)),
)


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
    st.header("System Health")

    # ── Hardware Gauges ──
    m = _get_system_metrics()
    _record_metrics_history(m)

    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.plotly_chart(_gauge(m['cpu_pct'], 'CPU'), use_container_width=True)
    with g2:
        label = f"RAM (sys {m['sys_ram_used_gb']}/{m['sys_ram_total_gb']} GB)"
        st.plotly_chart(_gauge(m['sys_ram_pct'], label), use_container_width=True)
    with g3:
        st.plotly_chart(_gauge(m['gpu_pct'], 'GPU'), use_container_width=True)
    with g4:
        label = f"VRAM (sys {m['sys_vram_used_gb']}/{m['sys_vram_total_gb']} GB)"
        st.plotly_chart(_gauge(m['sys_vram_pct'], label), use_container_width=True)

    # Sofia process + GPU temp row
    s1, s2, s3, s4 = st.columns(4)
    sofia_status = "running" if m['sofia_pid'] else "not detected"
    s1.metric("Sofia", sofia_status)
    s2.metric("Sofia RAM", f"{m['sofia_ram_gb']:.2f} GB")
    s3.metric("Sofia VRAM", f"{m['sofia_vram_gb']:.2f} GB")
    s4.metric("GPU Temp", f"{m['gpu_temp']:.0f} C")

    # Resource History
    h = st.session_state.get('metrics_history', {})
    if len(h.get('timestamps', [])) > 1:
        with st.expander("Resource History", expanded=False):
            hfig = make_subplots(rows=2, cols=2, shared_xaxes=True,
                                 subplot_titles=('CPU %', 'System RAM %',
                                                 'GPU %', 'System VRAM %'),
                                 vertical_spacing=0.15, horizontal_spacing=0.10)
            ts = h['timestamps']
            for i, (key, row, col) in enumerate([
                ('cpu', 1, 1), ('sys_ram', 1, 2),
                ('gpu', 2, 1), ('sys_vram', 2, 2)
            ]):
                hfig.add_trace(go.Scatter(
                    x=ts, y=h[key], mode='lines',
                    line=dict(width=1.5,
                              color=['#2196F3', '#4CAF50', '#FF9800', '#9C27B0'][i]),
                    showlegend=False,
                ), row=row, col=col)
                hfig.update_yaxes(range=[0, 100], row=row, col=col)
            hfig.update_layout(height=320, font=dict(size=11),
                               margin=dict(l=40, r=15, t=35, b=15),
                               plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(hfig, use_container_width=True)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    # ── Sofia's Inner State (Curiosity Drives) ──
    with col_left:
        st.subheader("Sofia's Inner State")
        curiosity = load_json("curiosity_state.json")
        if curiosity and curiosity.get('satisfaction_history'):
            latest = {}
            for entry in curiosity['satisfaction_history']:
                drive = entry.get('drive')
                if drive:
                    latest[drive] = entry.get('new_level', 0.0)

            if latest:
                drive_labels = {
                    'autonomy': ('Self-directing', '#E91E63'),
                    'connection': ('Seeking patterns', '#2196F3'),
                    'creativity': ('Creating & synthesizing', '#FF9800'),
                    'growth': ('Pushing boundaries', '#4CAF50'),
                    'meaning': ('Questioning purpose', '#9C27B0'),
                    'understanding': ('Investigating', '#00BCD4'),
                }
                for d in sorted(latest.keys()):
                    sat = latest[d]
                    hunger = 1.0 - sat
                    label, color = drive_labels.get(d, (d, '#888'))
                    # Intensity label
                    if hunger > 0.7:
                        intensity = "hungry"
                    elif hunger > 0.4:
                        intensity = "seeking"
                    else:
                        intensity = "satisfied"
                    st.markdown(
                        f"**{d.title()}** — {label} "
                        f"<span style='color:{color};font-weight:bold'>"
                        f"({intensity})</span>",
                        unsafe_allow_html=True)
                    st.progress(hunger, text=f"{hunger:.0%} drive intensity")

                momentum = curiosity.get('learning_momentum', 0)
                st.caption(f"Learning momentum: {momentum:.4f}")
            else:
                st.info("No curiosity drive data yet.")
        else:
            st.info("Waiting for first learning session to generate curiosity data.")

    # ── Brain Metrics ──
    with col_right:
        st.subheader("Brain Metrics")
        reflections = load_json("brain_reflection_history.json")
        if reflections and isinstance(reflections, list) and len(reflections) > 0:
            last = reflections[-1]
            metrics = last.get('metrics', {})
            labels = ['Brain Harmony', 'Learning Effectiveness',
                      'Adaptive Capacity', 'Performance Satisfaction']
            vals = [
                metrics.get('brain_harmony_assessment', 0),
                metrics.get('learning_effectiveness', 0),
                metrics.get('adaptive_capacity', 0),
                metrics.get('performance_satisfaction', 0),
            ]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=labels, x=vals, orientation='h',
                marker_color=[_health_color(v) for v in vals],
                text=[f"{v:.2f}" for v in vals], textposition='inside'))
            fig.update_layout(
                height=220, xaxis=dict(range=[0, 1], showticklabels=False),
                yaxis=dict(autorange='reversed'),
                **_CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
            insights = metrics.get('processing_insights', [])
            if insights:
                st.caption(' / '.join(insights[:3]))
        else:
            st.info(
                "Brain reflection data populates after Sofia runs her "
                "self-assessment cycle (triggered every ~100 URLs processed). "
                "File: `brain_reflection_history.json`")

    st.markdown("---")

    col_left2, col_right2 = st.columns(2)

    # ── Memory Health ──
    with col_left2:
        st.subheader("Memory")
        logic_count = len(load_json("logic_memory.json"))
        sym_count = len(load_json("symbolic_memory.json"))
        bridge_count = len(load_json("bridge_memory.json"))

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Logic", f"{logic_count:,}")
        mc2.metric("Symbolic", f"{sym_count:,}")
        mc3.metric("Bridge", f"{bridge_count:,}")

        analytics = load_json("memory_analytics_history.json")
        if analytics and isinstance(analytics, list):
            last_a = analytics[-1]
            health = last_a.get('health', {})
            status = health.get('status', 'unknown')
            issues = health.get('issues', [])
            st.caption(f"Health: **{status}**" + (f" — {issues[0]}" if issues else ""))

            stability = last_a.get('stability_metrics', {})
            if stability:
                for store, key in [('Logic', 'logic_stability'),
                                   ('Symbolic', 'symbolic_stability'),
                                   ('Bridge', 'bridge_stability')]:
                    val = stability.get(key, 0)
                    st.progress(min(1.0, val), text=f"{store} stability: {val:.2f}")

        # ── Sovereignty ──
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
                        st.caption(f"{icon} **{d.get('decision', '?')}** — "
                                   f"{d.get('reasoning', '')[:80]}")

    # ── Learning Progression ──
    with col_right2:
        st.subheader("Learning Progression")
        progression = load_json("learning_progression_detailed.json")
        if progression and isinstance(progression, dict) and len(progression) > 0:
            concepts = []
            understandings = []
            confidences = []
            for name, data in sorted(progression.items()):
                concepts.append(name.replace('_', ' '))
                understandings.append(
                    data.get('understanding_level', data.get('current_level', 0)))
                confidences.append(data.get('confidence_level', 0))

            if concepts:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    y=concepts, x=understandings, orientation='h',
                    name='Understanding',
                    marker_color=[_health_color(v) for v in understandings],
                    text=[f"{v:.2f}" for v in understandings],
                    textposition='inside'))
                fig.add_trace(go.Bar(
                    y=concepts, x=confidences, orientation='h',
                    name='Confidence',
                    marker_color='rgba(255,255,255,0.3)',
                    text=[f"{v:.2f}" for v in confidences],
                    textposition='inside'))
                fig.update_layout(
                    barmode='overlay',
                    height=max(220, 40 * len(concepts)),
                    xaxis=dict(range=[0, 1], showticklabels=False),
                    yaxis=dict(autorange='reversed'),
                    **_CHART_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)

                milestones = load_json("learning_milestones.json")
                if milestones and isinstance(milestones, list):
                    recent_ms = milestones[-5:][::-1]
                    st.caption("Recent milestones:")
                    for ml in recent_ms:
                        mtype = ml.get('milestone_type', '?')
                        concept = ml.get('concept', '?')
                        delta = ml.get('understanding_change', 0)
                        icon = {'breakthrough': '💡', 'connection': '🔗',
                                'progress': '📈', 'synthesis': '🧬'}.get(mtype, '•')
                        st.caption(f"{icon} {concept}: {mtype} (+{delta:.2f})")
        else:
            st.info(
                "Learning progression data populates as Sofia builds concept "
                "models across multiple sessions. Needs sustained learning on "
                "related topics. File: `learning_progression_detailed.json`")


# ═══════════════════════════════════════════════════════════════════════
# VIEW 5 — LIVE RUN
# ═══════════════════════════════════════════════════════════════════════

def _load_live_memory_counts():
    """Read current L/S/B counts from the JSON files on disk."""
    logic = load_json("logic_memory.json")
    symbolic = load_json("symbolic_memory.json")
    bridge = load_json("bridge_memory.json")
    return {
        'logic': len(logic) if isinstance(logic, list) else 0,
        'symbolic': len(symbolic) if isinstance(symbolic, list) else 0,
        'bridge': len(bridge) if isinstance(bridge, list) else 0,
    }


def _load_crawl_events_parsed(session_filter: str | None = None):
    """Load crawl events, optionally filtered by session_id.
    Returns (timestamps, total_count, session_count, latest_session_id)."""
    crawl_log = DATA_DIR / 'crawl_events.jsonl'
    if not crawl_log.exists():
        return [], 0, 0, None
    timestamps = []
    total = 0
    session_count = 0
    latest_sid = None
    try:
        with open(crawl_log, 'r', encoding='utf-8') as f:
            for line in f:
                total += 1
                try:
                    ev = json.loads(line)
                    sid = ev.get('session_id', '')
                    ts = ev.get('timestamp', '')
                    if not latest_sid and sid:
                        latest_sid = sid
                    if sid:
                        latest_sid = sid
                    if session_filter and sid != session_filter:
                        continue
                    session_count += 1
                    if ts:
                        timestamps.append(ts)
                except (json.JSONDecodeError, KeyError):
                    pass
    except Exception:
        pass
    return timestamps, total, session_count, latest_sid


def view_live_run():
    """Real-time view of the current (or most recent) learning session."""
    st.header("Live Run")

    scope = st.radio("Scope", ["Current Session", "All Events"],
                     horizontal=True, label_visibility='collapsed')

    # Detect the latest session_id from crawl events
    _, total_all, _, latest_sid = _load_crawl_events_parsed()
    session_filter = latest_sid if scope == "Current Session" else None

    timestamps, _, session_count, _ = _load_crawl_events_parsed(session_filter)

    # ── Memory counts ──
    counts = _load_live_memory_counts()
    total_mem = counts['logic'] + counts['symbolic'] + counts['bridge']

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Logic", f"{counts['logic']:,}")
    m2.metric("Symbolic", f"{counts['symbolic']:,}")
    m3.metric("Bridge", f"{counts['bridge']:,}")
    m4.metric("Total", f"{total_mem:,}")

    # ── Crawl rate ──
    rate = 0.0
    if len(timestamps) >= 2:
        recent = timestamps[-100:]
        try:
            t_first = datetime.fromisoformat(recent[0])
            t_last = datetime.fromisoformat(recent[-1])
            span_min = (t_last - t_first).total_seconds() / 60
            if span_min > 0:
                rate = round(len(recent) / span_min, 1)
        except Exception:
            pass

    r1, r2, r3 = st.columns(3)
    r1.metric("URLs / min", f"{rate}")
    r2.metric("Session events", f"{session_count:,}")
    r3.metric("Session", latest_sid or "none")

    # ── Accumulate history ──
    if 'live_run_history' not in st.session_state:
        st.session_state['live_run_history'] = {
            'timestamps': [], 'logic': [], 'symbolic': [], 'bridge': [],
            'rate': [], 'session_events': [],
        }
    h = st.session_state['live_run_history']
    h['timestamps'].append(datetime.now())
    h['logic'].append(counts['logic'])
    h['symbolic'].append(counts['symbolic'])
    h['bridge'].append(counts['bridge'])
    h['rate'].append(rate)
    h['session_events'].append(session_count)
    cap = 720
    for k in h:
        if len(h[k]) > cap:
            h[k] = h[k][-cap:]

    # ── Charts ──
    if len(h['timestamps']) > 1:
        fig_mem = go.Figure()
        fig_mem.add_trace(go.Scatter(
            x=h['timestamps'], y=h['logic'], name='Logic',
            mode='lines', line=dict(width=2, color='#2196F3')))
        fig_mem.add_trace(go.Scatter(
            x=h['timestamps'], y=h['symbolic'], name='Symbolic',
            mode='lines', line=dict(width=2, color='#9C27B0')))
        fig_mem.add_trace(go.Scatter(
            x=h['timestamps'], y=h['bridge'], name='Bridge',
            mode='lines', line=dict(width=2, color='#FF9800')))
        fig_mem.update_layout(title='Memory Counts Over Time',
                              height=320, **_CHART_LAYOUT)
        st.plotly_chart(fig_mem, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            fig_rate = go.Figure()
            fig_rate.add_trace(go.Scatter(
                x=h['timestamps'], y=h['rate'], name='URLs/min',
                mode='lines+markers', line=dict(width=2, color='#4CAF50'),
                marker=dict(size=3)))
            fig_rate.update_layout(title='Crawl Rate', height=280, **_CHART_LAYOUT)
            st.plotly_chart(fig_rate, use_container_width=True)
        with col_b:
            fig_ev = go.Figure()
            fig_ev.add_trace(go.Scatter(
                x=h['timestamps'], y=h['session_events'], name='Events',
                mode='lines', fill='tozeroy',
                line=dict(width=1.5, color='#00BCD4'),
                fillcolor='rgba(0,188,212,0.1)'))
            fig_ev.update_layout(title='Session Events', height=280, **_CHART_LAYOUT)
            st.plotly_chart(fig_ev, use_container_width=True)
    else:
        st.caption("Charts will appear after a few refresh cycles.")


# ═══════════════════════════════════════════════════════════════════════
# VIEW 6 — RUN HISTORY
# ═══════════════════════════════════════════════════════════════════════

def _load_all_sessions():
    """Parse all session JSONs from autonomous_sessions/. Cached per Streamlit run."""
    if 'parsed_sessions' in st.session_state:
        return st.session_state['parsed_sessions']
    session_dir = DATA_DIR / 'autonomous_sessions'
    if not session_dir.exists():
        return []
    sessions = []
    for fp in sorted(session_dir.glob('*.json')):
        if '_emergency' in fp.name:
            continue
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                d = json.load(f)
            # Extract a completed_at timestamp for sorting
            ts_str = d.get('completed_at', '')
            try:
                ts = datetime.fromisoformat(ts_str)
            except Exception:
                ts = datetime.min
            stats = d.get('stats', {})
            dist = d.get('final_memory_stats', {}).get('distribution', {})
            sessions.append({
                'session_id': d.get('session_id', fp.stem),
                'timestamp': ts,
                'elapsed_minutes': d.get('elapsed_time_minutes', 0),
                'urls_processed': stats.get('urls_processed', 0),
                'chunks_learned': stats.get('chunks_learned', 0),
                'links_followed': stats.get('links_followed', 0),
                'links_deferred': stats.get('links_deferred', 0),
                'robots_blocks': stats.get('robots_blocks', 0),
                'immune_blocks': stats.get('immune_blocks', 0),
                'security_blocks': stats.get('security_blocks', 0),
                'logic_count': dist.get('logic', {}).get('count', 0),
                'symbolic_count': dist.get('symbolic', {}).get('count', 0),
                'bridge_count': dist.get('bridge', {}).get('count', 0),
                'total_items': d.get('final_memory_stats', {}).get('total_items', 0),
            })
        except Exception:
            continue
    sessions.sort(key=lambda s: s['timestamp'])
    st.session_state['parsed_sessions'] = sessions
    return sessions


def view_run_history():
    """Historical view across all learning sessions."""
    st.header("Run History")
    sessions = _load_all_sessions()
    if not sessions:
        st.info("No session files found in data/autonomous_sessions/")
        return

    df = pd.DataFrame(sessions)
    st.caption(f"{len(df)} sessions loaded")

    # ── L/S/B growth across sessions ──
    fig_lsb = go.Figure()
    fig_lsb.add_trace(go.Scatter(
        x=df['timestamp'], y=df['logic_count'], name='Logic',
        mode='lines+markers', line=dict(width=2, color='#2196F3'),
        marker=dict(size=4)))
    fig_lsb.add_trace(go.Scatter(
        x=df['timestamp'], y=df['symbolic_count'], name='Symbolic',
        mode='lines+markers', line=dict(width=2, color='#9C27B0'),
        marker=dict(size=4)))
    fig_lsb.add_trace(go.Scatter(
        x=df['timestamp'], y=df['bridge_count'], name='Bridge',
        mode='lines+markers', line=dict(width=2, color='#FF9800'),
        marker=dict(size=4)))
    fig_lsb.update_layout(title='Memory Growth Across Sessions',
                          height=380, **_CHART_LAYOUT)
    st.plotly_chart(fig_lsb, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_urls = go.Figure()
        fig_urls.add_trace(go.Bar(
            x=df['timestamp'], y=df['urls_processed'],
            marker_color='#4CAF50', name='URLs processed'))
        fig_urls.update_layout(title='URLs Processed Per Session',
                               height=300, showlegend=False, **_CHART_LAYOUT)
        st.plotly_chart(fig_urls, use_container_width=True)

    with col2:
        fig_dur = go.Figure()
        fig_dur.add_trace(go.Scatter(
            x=df['timestamp'], y=df['elapsed_minutes'],
            mode='lines+markers', name='Duration (min)',
            line=dict(width=2, color='#FF5722'), marker=dict(size=4)))
        fig_dur.update_layout(title='Session Duration Trend',
                              height=300, showlegend=False, **_CHART_LAYOUT)
        st.plotly_chart(fig_dur, use_container_width=True)

    # ── Security blocks ──
    fig_sec = go.Figure()
    fig_sec.add_trace(go.Bar(
        x=df['timestamp'], y=df['robots_blocks'],
        name='Robots.txt', marker_color='#FFC107'))
    fig_sec.add_trace(go.Bar(
        x=df['timestamp'], y=df['immune_blocks'],
        name='Immune', marker_color='#F44336'))
    fig_sec.add_trace(go.Bar(
        x=df['timestamp'], y=df['security_blocks'],
        name='Warfare', marker_color='#9E9E9E'))
    fig_sec.update_layout(title='Security Blocks Per Session',
                          barmode='stack', height=300, **_CHART_LAYOUT)
    st.plotly_chart(fig_sec, use_container_width=True)

    # ── Links followed vs deferred ──
    if 'links_deferred' in df.columns and df['links_deferred'].sum() > 0:
        fig_links = go.Figure()
        fig_links.add_trace(go.Bar(
            x=df['timestamp'], y=df['links_followed'],
            name='Followed', marker_color='#4CAF50'))
        fig_links.add_trace(go.Bar(
            x=df['timestamp'], y=df['links_deferred'],
            name='Deferred', marker_color='#FF9800'))
        fig_links.update_layout(title='Links Followed vs Deferred',
                                barmode='group', height=300, **_CHART_LAYOUT)
        st.plotly_chart(fig_links, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

st.title("Sofia Brain Dashboard")

# Live mode — sidebar toggle controls fragment polling
live_mode = st.sidebar.toggle("Live mode", value=False,
                               help="Auto-refresh live tabs every 10 seconds")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧠 Brain Clusters",
    "🌉 Bridge Spectrum",
    "🕸️ Crawl Tracker",
    "💊 System Health",
    "🔴 Live Run",
    "📊 Run History",
])

with tab1:
    view_brain_clusters()
with tab2:
    view_bridge_spectrum()

# Run History is always static
with tab6:
    view_run_history()

# Fragment-wrapped versions for live polling (uniform 10s)
if live_mode:
    @st.fragment(run_every=timedelta(seconds=10))
    def _crawl_live():
        view_crawl_tracker()

    @st.fragment(run_every=timedelta(seconds=10))
    def _health_live():
        view_system_health()

    @st.fragment(run_every=timedelta(seconds=10))
    def _live_run_live():
        view_live_run()

    with tab3:
        _crawl_live()
    with tab4:
        _health_live()
    with tab5:
        _live_run_live()
else:
    with tab3:
        view_crawl_tracker()
    with tab4:
        view_system_health()
    with tab5:
        view_live_run()
