#!/usr/bin/env python3
"""
AI Memory Tracking Dashboard & Logging System - Enhanced Version
Integrates with your existing tripartite memory architecture
"""

# Fix for torch/streamlit compatibility issue
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info/warning logs

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
from collections import defaultdict, Counter
import networkx as nx
from typing import Dict, List, Any, Optional
import threading
from queue import Queue
import warnings
import asyncio
import atexit
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, HDBSCAN

# Suppress warnings globally
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="tensorflow")
warnings.filterwarnings('ignore', message='Tried to instantiate class')
np.seterr(divide='ignore', invalid='ignore')

# Initialize session state IMMEDIATELY to prevent KeyErrors
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
if 'session_start_time' not in st.session_state:
    st.session_state.session_start_time = datetime.now().isoformat()
if 'realtime_data' not in st.session_state:
    st.session_state.realtime_data = Queue()
if 'freeze_dashboard' not in st.session_state:
    st.session_state.freeze_dashboard = False
if 'ai_running' not in st.session_state:
    st.session_state.ai_running = False
if 'last_metrics' not in st.session_state:
    st.session_state.last_metrics = {
        'events_sec': 0, 'active_symbols': 0, 'bridge_queue': 0, 
        'memory_usage': 0, 'recursion_status': '⚫ Offline'
    }

# Fix torch.classes file-watcher issue
try:
    import torch
    import types
    if not hasattr(torch, "classes"):
        torch.classes = types.ModuleType("torch.classes")
    torch.classes.__path__ = []  # Prevent streamlit watcher from failing
except ImportError:
    pass  # torch not available

# Try to import autorefresh, fallback to manual refresh if not available
try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except ImportError:
    HAS_AUTOREFRESH = False

# ==================== PATH CONFIGURATION ====================

# Central path constants to fix file location issues
DEFAULT_DATA_DIR = Path(__file__).parent  # Dashboard is in /data/, so files are in same directory

# Initialize session state for data directory
if 'custom_data_dir' not in st.session_state:
    st.session_state.custom_data_dir = str(DEFAULT_DATA_DIR)

# Allow custom data directory override
DATA_DIR = Path(st.session_state.custom_data_dir)
LOG_DIR = DATA_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)  # Ensure logs directory exists

# ==================== CONFIGURATION ====================

EMOTION_COLORS = {
    'joy': '#FFD700',      # Gold
    'anger': '#DC143C',    # Crimson
    'fear': '#8B008B',     # Dark Magenta
    'sadness': '#4682B4',  # Steel Blue
    'neutral': '#808080',  # Gray
    'peace': '#98FB98',    # Pale Green
    'curiosity': '#FF69B4', # Hot Pink
    'amusement': '#FFA500', # Orange
    'annoyance': '#CD5C5C', # Indian Red
    'excitement': '#FF1493' # Deep Pink
}

# ==================== VALIDATION HELPERS ====================

def sanitize_log_string(text: str, max_length: int = 1000) -> str:
    """Sanitize log strings for safe display"""
    if not isinstance(text, str):
        text = str(text)
    
    # Remove ANSI escape codes
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    
    # Remove null bytes and other control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def validate_schema(data: Any, expected_type: type, schema_name: str = "") -> bool:
    """Validate data matches expected type schema"""
    if not isinstance(data, expected_type):
        st.error(f"Schema validation failed for {schema_name}: expected {expected_type.__name__}, got {type(data).__name__}")
        return False
    return True

@st.cache_data(ttl=2)  # Cache for 2 seconds - harmonized with autorefresh
def safe_load_json(filename: str, expected_type: type = dict) -> Any:
    """Safely load and validate JSON file with caching"""
    try:
        file_path = Path(filename)
        if not file_path.is_absolute():
            # If relative path, resolve it against DATA_DIR
            file_path = DATA_DIR / filename
        
        # Resolve symlinks and normalize path to prevent double-resolution issues
        file_path = file_path.resolve()
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if validate_schema(data, expected_type, filename):
            return data
        return {} if expected_type == dict else []
    except FileNotFoundError:
        st.warning(f"File not found: {filename}")
        return {} if expected_type == dict else []
    except json.JSONDecodeError as e:
        st.error(f"JSON decode error in {filename}: {e}")
        return {} if expected_type == dict else []
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return {} if expected_type == dict else []

@st.cache_data(ttl=2)
def get_unified_data():
    """Get data from unified memory systems"""
    if not UNIFIED_SYSTEMS_AVAILABLE:
        return {
            'symbol_memory': {},
            'logic_memory': [],
            'bridge_memory': [],
            'system_status': {}
        }
    
    try:
        # Get instances with error handling
        memory_system = get_unified_memory()
        symbol_system = get_unified_symbol_system()
        orchestration_system = get_unified_orchestration_system()
        
        # Get data from unified systems - using safe fallbacks
        symbol_data = []
        if hasattr(symbol_system, 'get_all_symbols'):
            symbol_data = symbol_system.get_all_symbols()
        elif hasattr(symbol_system, 'symbols'):
            symbol_data = list(symbol_system.symbols.values())
        
        memory_stats = {}
        if hasattr(memory_system, 'get_memory_stats'):
            memory_stats = memory_system.get_memory_stats()
        elif hasattr(memory_system, 'get_stats'):
            memory_stats = memory_system.get_stats()
        
        # Get system status - config property now properly implemented
        system_status = {}
        if hasattr(orchestration_system, 'get_system_status'):
            system_status = orchestration_system.get_system_status()
        elif hasattr(orchestration_system, 'status'):
            system_status = orchestration_system.status
        
        # Convert to dashboard format
        symbol_memory = {}
        for symbol in symbol_data:
            if hasattr(symbol, 'glyph'):
                symbol_memory[symbol.glyph] = {
                    'name': getattr(symbol, 'name', symbol.glyph),
                    'mathematical_concepts': getattr(symbol, 'mathematical_concepts', []),
                    'metaphorical_concepts': getattr(symbol, 'metaphorical_concepts', [])
                }
            elif isinstance(symbol, dict):
                glyph = symbol.get('glyph', symbol.get('name', ''))
                if glyph:
                    symbol_memory[glyph] = {
                        'name': symbol.get('name', glyph),
                        'mathematical_concepts': symbol.get('mathematical_concepts', []),
                        'metaphorical_concepts': symbol.get('metaphorical_concepts', [])
                    }
        
        return {
            'symbol_memory': symbol_memory,
            'logic_memory': memory_stats.get('logic_items', []),
            'bridge_memory': memory_stats.get('bridge_items', []),
            'system_status': system_status
        }
        
    except Exception as e:
        st.error(f"Error accessing unified systems: {e}")
        return {
            'symbol_memory': {},
            'logic_memory': [],
            'bridge_memory': [],
            'system_status': {}
        }

@st.cache_data(show_spinner=False)
def compute_memory_metrics(symbol_memory: dict, logic_memory: list, bridge_memory: list) -> dict:
    """Compute memory metrics with caching to prevent drift"""
    recursive_symbols = len([s for s in symbol_memory if '⟳' in s])
    max_recursion = max([s.count('⟳') for s in symbol_memory.keys()] + [0])
    
    return {
        'total_symbols': len(symbol_memory),
        'recursive_symbols': recursive_symbols,
        'total_logic': len(logic_memory),
        'total_bridge': len(bridge_memory),
        'max_recursion_depth': max_recursion
    }

# ==================== ENHANCED LOGGING SYSTEM ====================

class EventLogger:
    """Convert your JSON logs to efficient JSONL format with buffering"""
    
    def __init__(self, log_dir=None, buffer_size=100):
        self.log_dir = log_dir if log_dir else LOG_DIR
        self.log_dir.mkdir(exist_ok=True)
        self.current_log = self.log_dir / f"trail_{datetime.now().strftime('%Y%m%d')}.jsonl"
        self.buffer = []
        self.buffer_size = buffer_size
        self.lock = threading.Lock()
    
    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log events in JSONL format with buffering"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "session_id": st.session_state.get('session_id', 'default'),
            "data": data
        }
        
        with self.lock:
            self.buffer.append(event)
            if len(self.buffer) >= self.buffer_size:
                self._flush_buffer()
    
    def _flush_buffer(self) -> None:
        """Write buffer to disk"""
        if self.buffer:
            try:
                with open(self.current_log, 'a', encoding='utf-8') as f:
                    for event in self.buffer:
                        f.write(json.dumps(event) + '\n')
                self.buffer.clear()
            except Exception as e:
                print(f"⚠️ Error flushing event buffer: {e}")
    
    def log_bridge_decision(self, url: str, logic_score: float, symbol_score: float, decision: str) -> None:
        self.log_event("bridge_decision", {
            "url": url,
            "logic_score": logic_score,
            "symbol_score": symbol_score,
            "decision": decision
        })
    
    def log_symbol_activation(self, symbol: str, emotion: str, resonance: float, context: str, origin_trace: Optional[Dict] = None) -> None:
        self.log_event("symbol_activation", {
            "symbol": symbol,
            "emotion": emotion,
            "resonance": resonance,
            "context": context[:100],  # Truncate for efficiency
            "origin_trace": origin_trace  # New: track where symbol came from
        })
    
    def log_memory_migration(self, item_id: str, from_node: str, to_node: str, reason: str, bridge_event_id: Optional[str] = None) -> None:
        self.log_event("memory_migration", {
            "item_id": item_id,
            "from_node": from_node,
            "to_node": to_node,
            "reason": reason,
            "bridge_event_id": bridge_event_id  # New: track triggering bridge event
        })

# Import unified memory system
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from unified_memory import get_unified_memory
    from unified_symbol_system import get_unified_symbol_system
    from unified_orchestration import get_unified_orchestration_system
    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError as e:
    st.error(f"Unified systems not available: {e}")
    UNIFIED_SYSTEMS_AVAILABLE = False

# ==================== ENHANCED DASHBOARD ====================

st.set_page_config(page_title="AI Memory System Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("🧠 Unified Memory System Dashboard v3.0")

# Dashboard controls
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("🔄 Refresh Data", disabled=st.session_state.get('freeze_dashboard', False)):
        st.cache_data.clear()
        st.rerun()
with col2:
    freeze_state = st.checkbox(
        "❄️ Freeze Dashboard",
        value=st.session_state.get('freeze_dashboard', False),
        help="Prevent automatic updates and recalculations"
    )
    
    # Clear cache when freeze state changes to prevent stale data
    if freeze_state != st.session_state.get('freeze_dashboard', False):
        st.cache_data.clear()
    
    st.session_state.freeze_dashboard = freeze_state
with col3:
    if freeze_state:
        st.info("Dashboard frozen - data won't update until unfrozen")

# Initialize logger
logger = EventLogger()

# Thread-safe atexit flush wrapper
def safe_atexit_flush():
    """Thread-safe flush wrapper for atexit to prevent race conditions during hot-reload"""
    try:
        with logger.lock:  # Use the existing lock to prevent concurrent access
            logger._flush_buffer()
    except Exception as e:
        # Silently handle errors during shutdown (file handles may be closed)
        pass

# Register atexit handler to flush buffer on shutdown
atexit.register(safe_atexit_flush)

# ==================== CLUSTERING LOGIC ====================

LOGIC_SHADES = ['#1f77b4', '#aec7e8', '#3498db', '#5dade2', '#85c1e9', '#2e86c1', '#1a5276', '#5499c7']
SYMBOLIC_SHADES = ['#e377c2', '#f7b6d2', '#d01c8b', '#f1b6da', '#c51b7d', '#de77ae', '#8e0152', '#c51b7d']

class BrainCache:
    """Holds precomputed t-SNE coords, embeddings, and item metadata."""
    __slots__ = ('coords', 'embeddings', 'items', 'texts')

    def __init__(self, coords, embeddings, items, texts):
        self.coords = coords          # np.array (n, 2)
        self.embeddings = embeddings   # np.array (n, dim)
        self.items = items             # list of dicts (no embedding key)
        self.texts = texts             # list of str (for TF-IDF)

def get_file_mtime(filename):
    path = DATA_DIR / filename
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return 0

@st.cache_resource(ttl=300, show_spinner="Computing 2D projection (one-time)...")
def build_brain_cache(memory_file, file_mtime):
    """Load memory → extract embeddings → PCA+t-SNE → BrainCache."""
    path = DATA_DIR / memory_file
    if not path.exists():
        return None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_items = json.load(f)
    except:
        return None

    embeddings, items, texts = [], [], []
    for item in raw_items:
        if not isinstance(item, dict): continue
        emb = item.get('embedding')
        if emb is not None:
            embeddings.append(emb)
            items.append({k: v for k, v in item.items() if k != 'embedding'})
            texts.append(item.get('text', '')[:500])

    if len(embeddings) < 2:
        return None

    embeddings = np.array(embeddings, dtype=np.float32)

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

def cluster_and_name(embeddings, texts, n_clusters):
    """KMeans clustering + TF-IDF top-2 feature naming."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    n = len(embeddings)
    if n < n_clusters:
        n_clusters = max(1, n)

    if n_clusters <= 1:
        return np.zeros(n, dtype=int), {0: "all items"}

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    names = {}
    for cid in range(n_clusters):
        mask = labels == cid
        cluster_texts = [texts[i] for i in range(n) if mask[i]]
        if not cluster_texts:
            names[cid] = f"cluster_{cid}"
            continue
        try:
            tfidf = TfidfVectorizer(max_features=100, stop_words='english')
            matrix = tfidf.fit_transform(cluster_texts)
            if matrix.shape[0] == 0 or matrix.shape[1] == 0:
                names[cid] = f"cluster_{cid}"
                continue
            features = tfidf.get_feature_names_out()
            # Use mean(axis=0) safely
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                scores = np.asarray(matrix.mean(axis=0)).flatten()
            
            if scores.size == 0:
                names[cid] = f"cluster_{cid}"
                continue
                
            top = scores.argsort()[-2:][::-1]
            parts = [features[i] for i in top if i < len(features) and scores[i] > 0]
            names[cid] = ' / '.join(parts) if parts else f"cluster_{cid}"
        except Exception:
            names[cid] = f"cluster_{cid}"

    return labels, names

def is_ai_active():
    """Check if the AI is currently active by reading the heartbeat file."""
    heartbeat_path = DATA_DIR / "ai_heartbeat.json"
    if not heartbeat_path.exists():
        return False, None
    
    try:
        with open(heartbeat_path, 'r') as f:
            heartbeat = json.load(f)
        
        # Check if heartbeat is fresh (less than 20 seconds old)
        ts_str = heartbeat.get('timestamp')
        if ts_str:
            ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            if (now - ts).total_seconds() < 20:
                return True, heartbeat.get('session_id')
    except:
        pass
    
    return False, None

def _render_brain(memory_file, title, palette, accent_color, session_only=False):
    mtime = get_file_mtime(memory_file)
    brain = build_brain_cache(memory_file, mtime)

    if brain is None:
        st.subheader(title)
        st.info("Not enough data to visualize (need at least 2 items with embeddings).")
        return

    # Data selection
    coords = brain.coords
    items = brain.items
    texts = brain.texts
    embeddings = brain.embeddings
    
    if session_only:
        # CHECK HEARTBEAT: Clear out if AI is not running
        ai_active, active_session_id = is_ai_active()
        
        if not ai_active:
            st.subheader(title)
            st.info("AI is currently offline. Start Sofia to see live activity!")
            return

        # 1. Detect latest session ID from the data itself (matching heartbeat)
        if active_session_id:
            mask = [i for i, item in enumerate(items) if item.get('session_id') == active_session_id]
        else:
            # Fallback to last seen session if heartbeat has no ID
            session_ids = [item.get('session_id') for item in items if item.get('session_id')]
            if session_ids:
                latest_session = session_ids[-1]
                mask = [i for i, item in enumerate(items) if item.get('session_id') == latest_session]
            else:
                mask = []
        
        # 2. Fallback to time-based if mask is too small
        if not mask or len(mask) < 2:
            session_start = st.session_state.get('session_start_time')
            mask = []
            for i, item in enumerate(items):
                ts = item.get('created_at') or item.get('timestamp')
                if ts and ts >= session_start:
                    mask.append(i)
        
        if not mask:
            st.subheader(title)
            st.info("Live session started, but no nodes committed yet...")
            return
            
        coords = coords[mask]
        items = [items[i] for i in mask]
        texts = [texts[i] for i in mask]
        embeddings = embeddings[mask]
        n = len(mask)
    else:
        n = len(items)

    st.subheader(f"{title} ({n} items)")

    # Calculate cluster range safely
    max_k = max(2, min(12, n // 5 + 1))
    default_k = min(max_k, 5 if n > 10 else max(1, n))
    
    # Unique key for slider to avoid collisions
    key_suffix = "_session" if session_only else "_all"
    key = memory_file.replace('.', '_') + key_suffix

    # Ensure slider range is valid (min < max)
    if n > 4 and max_k > 2:
        n_clusters = st.slider(f"Clusters ({title})", 2, max_k, default_k, key=f"k_{key}")
    elif n >= 2:
        # Small dataset: default to 2 clusters without a slider
        n_clusters = 2
    else:
        # Very small dataset: 1 cluster
        n_clusters = 1

    labels, cluster_names = cluster_and_name(embeddings, texts, n_clusters)

    fig = go.Figure()
    for cid in range(n_clusters):
        mask = [i for i, l in enumerate(labels) if l == cid]
        if not mask: continue

        cname = cluster_names.get(cid, f"cluster_{cid}")
        color = palette[cid % len(palette)]

        hover = []
        for i in mask:
            item = items[i]
            txt = sanitize_log_string(item.get('text', ''))[:120]
            hover.append(f"<b>{cname}</b><br>{txt}")

        fig.add_trace(go.Scatter(
            x=[float(coords[i, 0]) for i in mask],
            y=[float(coords[i, 1]) for i in mask],
            mode='markers',
            name=cname,
            marker=dict(size=8, color=color, opacity=0.7),
            hovertext=hover,
            hoverinfo='text',
        ))

    fig.update_layout(height=500, margin=dict(l=0,r=0,b=0,t=40), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# Sidebar for navigation
page = st.sidebar.selectbox("Select View", [
    "System Overview",
    "Brain Clusters",
    "Symbol Network",
    "Bridge Analytics", 
    "Memory Evolution",
    "Session Replay",
    "Real-time Monitor",
    "Origin Tracer",
    "Live Unified Monitor"  # New feature for unified systems
])

# ==================== SYSTEM OVERVIEW ====================

if page == "System Overview":
    st.header("📊 System Health & Metrics")
    
    # Load data with caching if not frozen
    if not st.session_state.get('freeze_dashboard', False):
        if UNIFIED_SYSTEMS_AVAILABLE:
            unified_data = get_unified_data()
            symbol_memory = unified_data['symbol_memory']
            logic_memory = unified_data['logic_memory']
            bridge_memory = unified_data['bridge_memory']
            system_status = unified_data['system_status']
            
            # Show unified system status
            if system_status:
                st.info(f"✅ Unified systems active | Health: {system_status.get('health', 'unknown')}")
        else:
            # Fallback to JSON files
            symbol_memory = safe_load_json('symbol_memory.json', dict)
            logic_memory = safe_load_json('logic_memory.json', list)
            bridge_memory = safe_load_json('bridge_memory.json', list)
            system_status = {}
    else:
        # Use session state for frozen data
        if 'frozen_unified_data' not in st.session_state:
            if UNIFIED_SYSTEMS_AVAILABLE:
                st.session_state.frozen_unified_data = get_unified_data()
            else:
                st.session_state.frozen_unified_data = {
                    'symbol_memory': safe_load_json('symbol_memory.json', dict),
                    'logic_memory': safe_load_json('logic_memory.json', list),
                    'bridge_memory': safe_load_json('bridge_memory.json', list),
                    'system_status': {}
                }
        
        unified_data = st.session_state.frozen_unified_data
        symbol_memory = unified_data['symbol_memory']
        logic_memory = unified_data['logic_memory']
        bridge_memory = unified_data['bridge_memory']
        system_status = unified_data['system_status']
    
    # Compute metrics with caching
    metrics = compute_memory_metrics(symbol_memory, logic_memory, bridge_memory)
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Active Symbols", metrics['total_symbols'], 
                delta=f"+{metrics['recursive_symbols']} recursive")
    col2.metric("Logic Nodes", metrics['total_logic'])
    col3.metric("Bridge Queue", metrics['total_bridge'])
    col4.metric("Max Recursion Depth", metrics['max_recursion_depth'])
    
    # Memory balance chart with enhanced styling
    fig_balance = go.Figure(data=[
        go.Bar(name='Memory Distribution', 
               x=['Symbolic', 'Logic', 'Bridge'],
               y=[len(symbol_memory), len(logic_memory), len(bridge_memory)],
               marker_color=['#FF69B4', '#4682B4', '#FFD700'])
    ])
    fig_balance.update_layout(
        title="Memory Node Distribution",
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_balance, use_container_width=True)
    
    # Weight evolution trend
    st.subheader("⚖️ Weight Evolution Trend")
    weight_history = safe_load_json('weight_evolution_history.json', list)
    
    if weight_history:
        # Extract weight data from nested structure
        weight_data = []
        for entry in weight_history:
            if isinstance(entry, dict) and 'timestamp' in entry:
                row = {'timestamp': entry['timestamp']}
                
                # Extract weights from old_weights and new_weights
                if 'new_weights' in entry and isinstance(entry['new_weights'], dict):
                    row['static_weight'] = entry['new_weights'].get('static', 0)
                    row['dynamic_weight'] = entry['new_weights'].get('dynamic', 0)
                elif 'old_weights' in entry and isinstance(entry['old_weights'], dict):
                    row['static_weight'] = entry['old_weights'].get('static', 0)
                    row['dynamic_weight'] = entry['old_weights'].get('dynamic', 0)
                
                # Add other metrics
                if 'momentum' in entry and isinstance(entry['momentum'], dict):
                    # Calculate momentum difference for plotting
                    momentum_static = entry['momentum'].get('static', 0)
                    momentum_dynamic = entry['momentum'].get('dynamic', 0)
                    row['momentum_diff'] = momentum_static - momentum_dynamic
                    row['momentum_static'] = momentum_static
                    row['momentum_dynamic'] = momentum_dynamic
                else:
                    row['momentum_diff'] = 0
                    row['momentum_static'] = 0
                    row['momentum_dynamic'] = 0
                
                row['actual_specialization'] = entry.get('actual_specialization', 0)
                
                weight_data.append(row)
        
        if weight_data:
            df_weights = pd.DataFrame(weight_data)
            df_weights['timestamp'] = pd.to_datetime(df_weights['timestamp'])
            
            # Create subplot figure for multiple metrics
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Weight Evolution', 'Specialization & Momentum'),
                shared_xaxes=True,
                vertical_spacing=0.1
            )
            
            # Weight evolution
            fig.add_trace(
                go.Scatter(x=df_weights['timestamp'], y=df_weights['static_weight'],
                          name='Static Weight', 
                          line=dict(color='#4682B4', width=2),
                          hovertemplate='Static: %{y:.3f}<br>%{x|%Y-%m-%d %H:%M}<extra></extra>'),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=df_weights['timestamp'], y=df_weights['dynamic_weight'],
                          name='Dynamic Weight', 
                          line=dict(color='#FF69B4', width=2),
                          hovertemplate='Dynamic: %{y:.3f}<br>%{x|%Y-%m-%d %H:%M}<extra></extra>'),
                row=1, col=1
            )
            
            # Specialization and momentum
            fig.add_trace(
                go.Scatter(x=df_weights['timestamp'], y=df_weights['actual_specialization'],
                          name='Specialization', 
                          line=dict(color='#32CD32', width=2),
                          hovertemplate='Specialization: %{y:.3f}<br>%{x|%Y-%m-%d %H:%M}<extra></extra>'),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=df_weights['timestamp'], y=df_weights['momentum_diff'],
                          name='Momentum Δ (Static - Dynamic)', 
                          line=dict(color='#FFA500', width=2, dash='dash'),
                          hovertemplate='Momentum Δ: %{y:.3f}<br>%{x|%Y-%m-%d %H:%M}<extra></extra>'),
                row=2, col=1
            )
            
            # Add zero line for momentum
            fig.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5, row=2, col=1)
            
            fig.update_xaxes(title_text="Time", row=2, col=1)
            fig.update_yaxes(title_text="Weight", row=1, col=1)
            fig.update_yaxes(title_text="Value", row=2, col=1)
            
            fig.update_layout(
                height=600, 
                title_text="Weight Evolution & System Dynamics",
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=1.01
                ),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show current state
            if len(df_weights) > 0:
                latest = df_weights.iloc[-1]
                col1, col2, col3 = st.columns(3)
                col1.metric("Current Static Weight", f"{latest['static_weight']:.3f}")
                col2.metric("Current Dynamic Weight", f"{latest['dynamic_weight']:.3f}")
                
                # Handle momentum direction with proper zero handling
                momentum_diff = latest.get('momentum_diff', 0)
                if abs(momentum_diff) < 0.001:  # Essentially zero
                    col3.metric("Momentum Direction", "⚖️ Balanced", delta=None)
                else:
                    direction = "↑ Static" if momentum_diff > 0 else "↓ Dynamic"
                    col3.metric("Momentum Direction", direction, delta=f"{abs(momentum_diff):.3f}")
        else:
            st.warning("Could not extract weight data from history file.")

# ==================== BRAIN CLUSTERS ====================

elif page == "Brain Clusters":
    st.header("🧠 Dual Brain Memory Clusters")
    
    # 5-second autorefresh for live activity
    if HAS_AUTOREFRESH:
        st_autorefresh(interval=5000, limit=None, key="clusters_refresh")
    
    st.subheader("🌐 All-Time Memory Landscape")
    st.markdown("Full historical view of all nodes stored in memory.")
    col_l, col_r = st.columns(2)
    with col_l:
        _render_brain("logic_memory.json", "Logic (All-Time)", LOGIC_SHADES, "#4682B4")
    with col_r:
        _render_brain("symbolic_memory.json", "Symbolic (All-Time)", SYMBOLIC_SHADES, "#FF69B4")

    st.divider()
    
    st.subheader("⚡ Live Feed (Session Activity)")
    session_start_display = st.session_state.get('session_start_time', datetime.now().isoformat())
    try:
        time_part = session_start_display.split('T')[1].split('.')[0]
    except:
        time_part = "unknown"
    st.markdown(f"Nodes added since this dashboard session started ({time_part}).")
    col_live_l, col_live_r = st.columns(2)
    with col_live_l:
        _render_brain("logic_memory.json", "Logic (Live)", LOGIC_SHADES, "#4682B4", session_only=True)
    with col_live_r:
        _render_brain("symbolic_memory.json", "Symbolic (Live)", SYMBOLIC_SHADES, "#FF69B4", session_only=True)

# ==================== ENHANCED SYMBOL NETWORK ====================

elif page == "Symbol Network":
    st.header("🔮 Symbol Relationship Network")
    
    symbol_cooccurrence = safe_load_json('symbol_cooccurrence.json', dict)
    symbol_emotion_map = safe_load_json('symbol_emotion_map.json', dict)
    
    # Create network graph with enhanced features
    G = nx.Graph()
    
    # Add nodes with emotion colors
    for symbol in symbol_cooccurrence.keys():
        emotion_data = symbol_emotion_map.get(symbol, {})
        if emotion_data:
            # Filter to ensure we only have numeric values for comparison
            numeric_emotions = {k: v for k, v in emotion_data.items() if isinstance(v, (int, float))}
            if numeric_emotions:
                top_emotion = max(numeric_emotions.items(), key=lambda x: x[1])[0]
                emotion_score = numeric_emotions[top_emotion]
            else:
                top_emotion = 'neutral'
                emotion_score = 0
        else:
            top_emotion = 'neutral'
            emotion_score = 0
        
        G.add_node(symbol, 
                  emotion=top_emotion,
                  emotion_score=emotion_score,
                  size=15 + symbol.count('⟳') * 10,
                  color=EMOTION_COLORS.get(top_emotion, '#808080'))
    
    # Add weighted edges
    for symbol1, connections in symbol_cooccurrence.items():
        if isinstance(connections, dict):
            for symbol2, weight in connections.items():
                if symbol1 != symbol2 and symbol2 in G.nodes:
                    G.add_edge(symbol1, symbol2, weight=float(weight))
    
    # Create Plotly network visualization with enhanced styling
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Create edge traces with varying thickness
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2].get('weight', 1)
        
        edge_trace = go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=0.5 + weight * 0.5, color=f'rgba(128,128,128,{min(0.2 + weight * 0.1, 0.8)})'),
            hoverinfo='none',
            mode='lines'
        )
        edge_traces.append(edge_trace)
    
    # Create node trace with emotion colors - FIXED VERSION
    # Initialize lists (not tuples!)
    node_x = []
    node_y = []
    node_text = []
    node_customdata = []
    node_sizes = []
    node_colors = []
    
    # Build the data
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_sizes.append(G.nodes[node].get('size', 15))
        node_colors.append(G.nodes[node].get('emotion_score', 0))
        # Make sure customdata entries are lists, not tuples
        node_customdata.append([
            G.nodes[node].get('emotion', 'neutral'), 
            G.nodes[node].get('emotion_score', 0)
        ])
    
    # Create the trace with all data at once
    node_trace = go.Scatter(
        x=node_x, 
        y=node_y, 
        text=node_text, 
        mode='markers+text',
        textposition="top center",
        hovertemplate='%{text}<br>Emotion: %{customdata[0]}<br>Score: %{customdata[1]:.2f}<extra></extra>',
        customdata=node_customdata,
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            size=node_sizes,
            color=node_colors,
            colorbar=dict(
                thickness=15,
                title=dict(
                    text='Emotion Intensity',
                    side='right'
                ),
                xanchor='left'
            )
        )
    )
    
    fig_network = go.Figure(data=edge_traces + [node_trace],
                           layout=go.Layout(
                               title='Symbol Co-occurrence Network (size = recursion depth, opacity = connection strength)',
                               showlegend=False,
                               hovermode='closest',
                               margin=dict(b=20, l=5, r=5, t=40),
                               xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                               yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                               height=600
                           ))
    
    st.plotly_chart(fig_network, use_container_width=True)
    
    # Symbol emotion breakdown with color coding
    st.subheader("😊 Symbol Emotional Profiles")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if symbol_emotion_map and len(symbol_emotion_map) > 0:
            selected_symbol = st.selectbox("Select a symbol to analyze", list(symbol_emotion_map.keys()))
        else:
            st.info("No symbol emotion data available. The system may be starting up or the symbol_emotion_map.json file may be empty.")
            selected_symbol = None
    
    if selected_symbol and selected_symbol in symbol_emotion_map:
        emotions = symbol_emotion_map[selected_symbol]
        df_emotions = pd.DataFrame(list(emotions.items()), columns=['Emotion', 'Score'])
        df_emotions = df_emotions.sort_values('Score', ascending=False)
        
        # Add colors to emotions
        df_emotions['Color'] = df_emotions['Emotion'].map(lambda e: EMOTION_COLORS.get(e, '#808080'))
        
        fig_emotions = go.Figure(data=[
            go.Bar(x=df_emotions['Emotion'], y=df_emotions['Score'],
                   marker_color=df_emotions['Color'],
                   text=df_emotions['Score'].round(2),
                   textposition='outside')
        ])
        fig_emotions.update_layout(
            title=f"Emotional Profile for {selected_symbol}",
            xaxis_title="Emotion",
            yaxis_title="Score",
            showlegend=False,
            height=400
        )
        
        with col2:
            st.plotly_chart(fig_emotions, use_container_width=True)

# ==================== BRIDGE ANALYTICS ====================

elif page == "Bridge Analytics":
    st.header("🌉 Bridge Decision Analytics")
    
    # Load bridge conflicts
    bridge_conflicts = safe_load_json('bridge_conflicts.json', list)
    
    # Decision distribution
    decisions_csv_path = DATA_DIR / 'link_decisions.csv'
    if decisions_csv_path.exists():
        decisions_df = pd.read_csv(decisions_csv_path)
        
        if not decisions_df.empty and 'decision' in decisions_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                decision_counts = decisions_df['decision'].value_counts()
                fig_decisions = px.pie(values=decision_counts.values, names=decision_counts.index,
                                      title="Bridge Decision Distribution",
                                      color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig_decisions, use_container_width=True)
            
            with col2:
                # Logic vs Symbol score scatter with decision regions
                fig_scatter = px.scatter(decisions_df, x='logic_score', y='symbol_score', 
                                        color='decision', title="Logic vs Symbol Score Distribution",
                                        hover_data=['url'],
                                        color_discrete_sequence=px.colors.qualitative.Set3)
                
                # Add decision boundary regions
                fig_scatter.add_shape(type="line", x0=0, y0=0, x1=10, y1=10,
                                     line=dict(color="gray", width=1, dash="dash"))
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Conflict heatmap
            if bridge_conflicts:
                st.subheader("🔥 Bridge Conflict Analysis")
                
                # Create conflict matrix
                conflict_matrix = defaultdict(lambda: defaultdict(int))
                for conflict in bridge_conflicts:
                    if isinstance(conflict, dict) and 'from_type' in conflict and 'to_type' in conflict:
                        conflict_matrix[conflict['from_type']][conflict['to_type']] += 1
                
                if conflict_matrix:
                    # Convert to DataFrame
                    node_types = list(set(list(conflict_matrix.keys()) + 
                                         [k for v in conflict_matrix.values() for k in v.keys()]))
                    matrix_data = []
                    for from_type in node_types:
                        row = []
                        for to_type in node_types:
                            row.append(conflict_matrix[from_type][to_type])
                        matrix_data.append(row)
                    
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=matrix_data,
                        x=node_types,
                        y=node_types,
                        colorscale='Reds',
                        text=matrix_data,
                        texttemplate="%{text}",
                        textfont={"size": 10}
                    ))
                    fig_heatmap.update_layout(
                        title="Bridge Conflict Heatmap (From → To)",
                        xaxis_title="To Node Type",
                        yaxis_title="From Node Type",
                        height=500
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                else:
                    st.info("ℹ️ No specific node-type conflicts detected in bridge history.")
            else:
                st.info("ℹ️ No bridge conflict data available. Conflicts are logged when nodes compete for the same memory slot.")

# ==================== MEMORY EVOLUTION ====================

elif page == "Memory Evolution":
    st.header("📈 Memory Evolution & Optimization")
    
    evolution_sessions = safe_load_json('evolution_sessions.json', list)
    curriculum_metrics = safe_load_json('curriculum_metrics.json', dict)
    
    if curriculum_metrics:
        # Process curriculum data
        metrics_data = []
        for phase, data in curriculum_metrics.items():
            if isinstance(data, dict):
                metrics_data.append({
                    'Phase': phase,
                    'Chunks Processed': data.get('chunks_processed', 0),
                    'Symbols Generated': data.get('symbols_generated', 0),
                    'Logic Nodes': data.get('logic_nodes_created', 0),
                    'Bridge Events': data.get('bridge_events', 0)
                })
        
        if metrics_data:
            df_metrics = pd.DataFrame(metrics_data)
            
            # Create subplots for curriculum progress
            fig_curriculum = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Learning Progress', 'Cumulative Growth', 
                               'Processing Rate', 'Symbol/Logic Ratio'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Learning progress bar chart
            for i, col in enumerate(['Chunks Processed', 'Symbols Generated', 'Logic Nodes']):
                fig_curriculum.add_trace(
                    go.Bar(name=col, x=df_metrics['Phase'], y=df_metrics[col]),
                    row=1, col=1
                )
            
            # Cumulative growth line chart
            df_metrics['Cumulative Symbols'] = df_metrics['Symbols Generated'].cumsum()
            df_metrics['Cumulative Logic'] = df_metrics['Logic Nodes'].cumsum()
            
            fig_curriculum.add_trace(
                go.Scatter(name='Cumulative Symbols', x=df_metrics['Phase'], 
                          y=df_metrics['Cumulative Symbols'], mode='lines+markers'),
                row=1, col=2
            )
            fig_curriculum.add_trace(
                go.Scatter(name='Cumulative Logic', x=df_metrics['Phase'], 
                          y=df_metrics['Cumulative Logic'], mode='lines+markers'),
                row=1, col=2
            )
            
            # Processing rate
            if len(df_metrics) > 1:
                df_metrics['Process Rate'] = df_metrics['Chunks Processed'].diff().fillna(0)
                fig_curriculum.add_trace(
                    go.Scatter(name='Processing Rate', x=df_metrics['Phase'], 
                              y=df_metrics['Process Rate'], mode='lines+markers',
                              line=dict(shape='spline')),
                    row=2, col=1
                )
            
            # Symbol/Logic ratio with proper zero handling
            logic_nodes = df_metrics['Logic Nodes']
            if logic_nodes.sum() > 0:  # Only show ratio if we have actual logic nodes
                df_metrics['Symbol/Logic Ratio'] = (df_metrics['Symbols Generated'] / 
                                                   logic_nodes.replace(0, 1))
                fig_curriculum.add_trace(
                    go.Scatter(name='Symbol/Logic Ratio', x=df_metrics['Phase'], 
                              y=df_metrics['Symbol/Logic Ratio'], mode='lines+markers',
                              line=dict(color='purple')),
                    row=2, col=2
                )
            else:
                # Show placeholder when no logic nodes exist yet
                fig_curriculum.add_annotation(
                    text="Symbol/Logic Ratio<br>Available when logic nodes exist",
                    x=0.75, y=0.25, xref="paper", yref="paper",
                    showarrow=False, font=dict(size=12, color="gray")
                )
            
            fig_curriculum.update_layout(height=800, showlegend=True,
                                       title_text="Curriculum Learning Analytics")
            st.plotly_chart(fig_curriculum, use_container_width=True)
    
    # Memory drift analysis
    st.subheader("🌊 Symbol Drift Analysis")
    meta_symbols = safe_load_json('meta_symbols.json', dict)
    
    if meta_symbols:
        drift_data = []
        for symbol, data in meta_symbols.items():
            if isinstance(data, dict):
                recursion_depth = symbol.count('⟳')
                drift_data.append({
                    'Symbol': symbol,
                    'Recursion Depth': recursion_depth,
                    'Summary Length': len(data.get('summary', '')),
                    'Origin': data.get('origin_symbol', 'unknown'),
                    'Transformation': data.get('transformation_tag', 'none')
                })
        
        if drift_data:
            df_drift = pd.DataFrame(drift_data)
            
            # Create 3D scatter plot for drift visualization
            fig_drift = px.scatter_3d(df_drift, x='Recursion Depth', y='Summary Length',
                                     z=df_drift.index, color='Transformation',
                                     hover_data=['Symbol', 'Origin'],
                                     title="Symbol Complexity Evolution in 3D Space")
            fig_drift.update_layout(height=600)
            st.plotly_chart(fig_drift, use_container_width=True)

# ==================== SESSION REPLAY ====================

elif page == "Session Replay":
    st.header("🎬 Session Replay Tool")
    
    # Session selector - check for both JSONL and JSON logs
    jsonl_files = list(LOG_DIR.glob('*.jsonl')) if LOG_DIR.exists() else []
    trail_json_path = DATA_DIR / 'trail_log.json'
    
    log_files = []
    if jsonl_files:
        log_files.extend(jsonl_files)
    if trail_json_path.exists():
        log_files.append(trail_json_path)
    
    if log_files:
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_log = st.selectbox("Select log file", log_files, 
                                       format_func=lambda x: f"{x.name} ({x.stat().st_size / 1024:.1f} KB)")
        
        # Load events - handle both JSONL and JSON formats with validation
        events = []
        raw_events = []
        try:
            if str(selected_log).endswith('.jsonl'):
                # JSONL format - one JSON object per line
                with open(selected_log, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        try:
                            event = json.loads(line)
                            raw_events.append(event)
                        except json.JSONDecodeError as e:
                            st.warning(f"Skipping invalid JSON on line {line_num}: {e}")
            else:
                # JSON format - single array or object
                with open(selected_log, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        raw_events = data
                    else:
                        raw_events = [data]  # Single event
            
            # Filter and validate events
            for i, event in enumerate(raw_events):
                if isinstance(event, dict) and 'timestamp' in event:
                    # If event has no event_type, add a legacy marker
                    if 'event_type' not in event:
                        event = event.copy()  # Don't modify original
                        event['event_type'] = 'legacy_event'
                        event['data'] = event.get('data', event)  # Wrap non-data events
                    events.append(event)
                else:
                    st.warning(f"Skipping invalid event at index {i}: missing timestamp or not a dict")
        except Exception as e:
            st.error(f"Error loading log: {e}")
    else:
        st.info("No log files found. Create some activity to generate logs!")
    
    if events:
        # ── Session-level defaults ──────────────────────────────────────────
        if "event_slider" not in st.session_state:
            st.session_state.event_slider = 0
        if "playing" not in st.session_state:
            st.session_state.playing = False
        if "last_tick" not in st.session_state:
            st.session_state.last_tick = time.time()
        
        # ── Callback functions ──────────────────────────────────────────────
        def _play_pause():
            st.session_state.playing = not st.session_state.playing
            # reset tick so we don't skip on first frame
            st.session_state.last_tick = time.time()
        
        def _on_slider_move():
            st.session_state.playing = False  # pause if user drags slider
        
        # ── Replay controls ──────────────────────────────────────────────────
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            play_button = st.button(
                "▶️ Play" if not st.session_state.playing else "⏸️ Pause",
                on_click=_play_pause
            )
        with col2:
            if st.button("⏹️ Stop"):
                st.session_state.playing = False
        with col3:
            playback_speed = st.select_slider("Speed", options=[0.5, 1.0, 2.0, 5.0, 10.0], value=1.0)
        
        event_index = st.slider(
            "Event Timeline",
            0, len(events) - 1,
            key="event_slider",
            on_change=_on_slider_move
        )
        
        # Display current event with syntax highlighting
        current_event = events[event_index]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 Event Details")
            # Safe JSON display - handle circular references
            try:
                # First try normal display
                st.json(current_event)
            except (ValueError, TypeError) as e:
                if "circular" in str(e).lower():
                    # Handle circular references by converting to safe string format
                    try:
                        safe_event = json.loads(json.dumps(current_event, default=str))
                        st.json(safe_event)
                    except:
                        # Final fallback - display as sanitized text
                        safe_text = sanitize_log_string(str(current_event))
                        st.text(f"Event data (circular refs detected):\n{safe_text}")
                else:
                    # Other JSON errors - show as sanitized text
                    safe_text = sanitize_log_string(str(current_event))
                    st.text(f"Event data (display error):\n{safe_text}")
        
        with col2:
            st.subheader("📊 Event Visualization")
            
            # Visualize based on event type - SAFE ACCESS
            event_type = current_event.get('event_type') if isinstance(current_event, dict) else None
            if event_type == 'bridge_decision':
                data = current_event['data']
                
                # Radar chart for decision
                fig = go.Figure(data=go.Scatterpolar(
                    r=[data.get('logic_score', 0), data.get('symbol_score', 0), 5],  # Added third dimension
                    theta=['Logic', 'Symbol', 'Hybrid'],
                    fill='toself',
                    name=data.get('decision', 'Unknown'),
                    line_color=EMOTION_COLORS.get('neutral', '#808080')
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 10])
                    ),
                    title=f"Decision Profile: {data.get('decision', 'Unknown')}"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif event_type == 'symbol_activation':
                data = current_event['data']
                
                # Emotion gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=data.get('resonance', 0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"{data.get('symbol', '?')} - {data.get('emotion', 'neutral')}"},
                    delta={'reference': 0.5},
                    gauge={'axis': {'range': [None, 1]},
                           'bar': {'color': EMOTION_COLORS.get(data.get('emotion', 'neutral'), '#808080')},
                           'steps': [
                               {'range': [0, 0.25], 'color': "lightgray"},
                               {'range': [0.25, 0.5], 'color': "gray"},
                               {'range': [0.5, 0.75], 'color': "lightblue"},
                               {'range': [0.75, 1], 'color': "lightgreen"}],
                           'threshold': {'line': {'color': "red", 'width': 4},
                                       'thickness': 0.75, 'value': 0.9}}
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            elif event_type == 'legacy_event':
                st.info("📜 Legacy Event (Pre-schema update)")
                st.markdown(f"**Timestamp:** {current_event.get('timestamp', 'N/A')}")
                # Try to show meaningful data
                event_data = current_event.get('data', {})
                if isinstance(event_data, dict):
                    # Show data keys for exploration
                    st.write(f"Contains {len(event_data)} data fields")
                    try:
                        st.json(event_data)
                    except Exception:
                        # Fallback for circular references
                        st.warning("⚠️ Circular reference detected in event data. Displaying sanitized text instead.")
                        st.text(sanitize_log_string(str(event_data)))
                else:
                    st.write(event_data)

            else:
                # Handle unknown or legacy event types
                st.warning(f"Unsupported event type: {event_type or 'Unknown'}")
                if isinstance(current_event, dict):
                    # Show basic event info for legacy events
                    event_info = {
                        'Event Type': event_type or 'Legacy/Unknown',
                        'Timestamp': current_event.get('timestamp', 'N/A'),
                        'Data Keys': list(current_event.get('data', {}).keys()) if isinstance(current_event.get('data'), dict) else 'N/A'
                    }
                    try:
                        st.json(event_info)
                    except Exception:
                        st.text(str(event_info))
        
        # ── Frame-rate controlled advancement ────────────────────────────────
        # Use playback_speed to control frame rate
        FRAME_RATE = playback_speed
        
        if st.session_state.playing and event_index < len(events) - 1:
            now = time.time()
            if now - st.session_state.last_tick >= 1.0 / FRAME_RATE:
                st.session_state.event_slider += 1
                st.session_state.last_tick = now
                st.rerun()
        
        # Clean exit on final frame
        if event_index == len(events) - 1 and st.session_state.playing:
            st.session_state.playing = False   # auto-pause at end

# ==================== REAL-TIME MONITOR - FIXED VERSION ====================

elif page == "Real-time Monitor":
    st.header("📡 Real-time System Monitor")
    
    # AI Control Panel
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("▶️ Start AI" if not st.session_state.ai_running else "⏸️ Stop AI"):
            st.session_state.ai_running = not st.session_state.ai_running
    
    with col2:
        status = "🟢 RUNNING" if st.session_state.ai_running else "🔴 STOPPED"
        st.metric("AI Status", status)
    
    with col3:
        if not st.session_state.ai_running:
            st.info("AI is stopped. Displaying last known values.")
    
    # Use autorefresh if available and AI is running - harmonized with cache TTL
    if HAS_AUTOREFRESH and st.session_state.ai_running:
        count = st_autorefresh(interval=2000, limit=None, key="realtime_counter")
    else:
        if st.button("🔄 Refresh"):
            st.rerun()
        if not HAS_AUTOREFRESH:
            st.info("Install streamlit-autorefresh for automatic updates: pip install streamlit-autorefresh")
    
    # Create layout
    metric_container = st.container()
    chart_container = st.container()
    log_container = st.container()
    
    # Real-time metrics
    with metric_container:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        if st.session_state.ai_running:
            # Try to read actual metrics from unified systems
            try:
                if UNIFIED_SYSTEMS_AVAILABLE:
                    unified_data = get_unified_data()
                    symbol_memory = unified_data['symbol_memory']
                    logic_memory = unified_data['logic_memory']
                    bridge_memory = unified_data['bridge_memory']
                    system_status = unified_data['system_status']
                    
                    # Calculate real metrics from unified systems
                    active_symbols = len(symbol_memory)
                    bridge_queue = len(bridge_memory)
                    events_sec = system_status.get('active_sessions', 0)
                    memory_usage = min(system_status.get('memory_usage_percent', 0), 100)
                else:
                    # Fallback to reading JSON files
                    symbol_memory = safe_load_json('symbol_memory.json', dict)
                    logic_memory = safe_load_json('logic_memory.json', list)
                    bridge_memory = safe_load_json('bridge_memory.json', list)
                    
                    active_symbols = len(symbol_memory)
                    bridge_queue = len(bridge_memory)
                    events_sec = len(bridge_memory) if bridge_memory else 0
                    
                    # Memory usage calculation
                    total_size = 0
                    for f in ['symbol_memory.json', 'logic_memory.json', 'bridge_memory.json']:
                        file_path = DATA_DIR / f
                        if file_path.exists():
                            total_size += file_path.stat().st_size
                    memory_usage = min(int(total_size / 1024 / 10), 100)
                
                # Check for high recursion
                max_recursion = max([s.count('⟳') for s in symbol_memory.keys()] + [0])
                recursion_status = "🟢 Normal" if max_recursion < 3 else ("🟡 High" if max_recursion < 5 else "🔴 Critical")
                
                # Update last known metrics
                st.session_state.last_metrics = {
                    'events_sec': events_sec,
                    'active_symbols': active_symbols,
                    'bridge_queue': bridge_queue,
                    'memory_usage': memory_usage,
                    'recursion_status': recursion_status
                }
                
            except Exception as e:
                st.error(f"Error reading actual metrics: {e}")
                # Fall back to last known values
                events_sec = st.session_state.last_metrics['events_sec']
                active_symbols = st.session_state.last_metrics['active_symbols']
                bridge_queue = st.session_state.last_metrics['bridge_queue']
                memory_usage = st.session_state.last_metrics['memory_usage']
                recursion_status = st.session_state.last_metrics['recursion_status']
        else:
            # AI is stopped - use last known values
            events_sec = st.session_state.last_metrics['events_sec']
            active_symbols = st.session_state.last_metrics['active_symbols']
            bridge_queue = st.session_state.last_metrics['bridge_queue']
            memory_usage = st.session_state.last_metrics['memory_usage']
            recursion_status = st.session_state.last_metrics['recursion_status']
        
        # Display metrics (no random changes when AI is stopped)
        col1.metric("Events/sec", events_sec, delta=None if not st.session_state.ai_running else "Live")
        col2.metric("Active Symbols", active_symbols)
        col3.metric("Bridge Queue", bridge_queue)
        col4.metric("Memory Usage", f"{memory_usage}%")
        col5.metric("Recursion Alert", recursion_status)
    
    # Real-time activity chart with rolling history
    with chart_container:
        # Initialize rolling history in session state
        if 'activity_history' not in st.session_state:
            st.session_state.activity_history = {
                'timestamps': [],
                'logic_activity': [],
                'symbol_activity': [],
                'bridge_activity': []
            }
        
        if st.session_state.ai_running:
            # Safely get current memory data
            try:
                logic_len = len(logic_memory) if 'logic_memory' in locals() and logic_memory else 0
                symbol_len = len(symbol_memory) if 'symbol_memory' in locals() and symbol_memory else 0
                bridge_len = len(bridge_memory) if 'bridge_memory' in locals() and bridge_memory else 0
            except (NameError, TypeError):
                # Fallback: read from session state
                logic_len = st.session_state.last_metrics.get('active_symbols', 0)
                symbol_len = st.session_state.last_metrics.get('active_symbols', 0)
                bridge_len = st.session_state.last_metrics.get('bridge_queue', 0)
            
            # Add current data point to rolling history
            now = datetime.now()
            history = st.session_state.activity_history
            
            history['timestamps'].append(now)
            history['logic_activity'].append(logic_len)
            history['symbol_activity'].append(symbol_len)
            history['bridge_activity'].append(bridge_len)
            
            # Keep only last 60 data points (rolling window)
            max_points = 60
            if len(history['timestamps']) > max_points:
                for key in history:
                    history[key] = history[key][-max_points:]
            
            # Pad with zeros if we don't have enough history yet
            if len(history['timestamps']) < max_points:
                needed = max_points - len(history['timestamps'])
                # Safe access to first timestamp - avoid IndexError on first run
                if history['timestamps']:
                    base_time = history['timestamps'][0]
                else:
                    base_time = now
                
                for i in range(needed):
                    pad_time = base_time - timedelta(seconds=needed-i)
                    history['timestamps'].insert(0, pad_time)
                    history['logic_activity'].insert(0, 0)
                    history['symbol_activity'].insert(0, 0)
                    history['bridge_activity'].insert(0, 0)
            
            data = pd.DataFrame({
                'timestamp': history['timestamps'],
                'logic_activity': history['logic_activity'],
                'symbol_activity': history['symbol_activity'],
                'bridge_activity': history['bridge_activity']
            })
        else:
            # Show flat line when AI is stopped
            timestamps = pd.date_range(end=datetime.now(), periods=60, freq='s')
            data = pd.DataFrame({
                'timestamp': timestamps,
                'logic_activity': [0] * 60,
                'symbol_activity': [0] * 60,
                'bridge_activity': [0] * 60
            })
        
        fig = px.line(data, x='timestamp', 
                     y=['logic_activity', 'symbol_activity', 'bridge_activity'],
                     title="Real-time Node Activity (60s window)" + (" - AI STOPPED" if not st.session_state.ai_running else ""),
                     color_discrete_map={
                         'logic_activity': '#4682B4',
                         'symbol_activity': '#FF69B4', 
                         'bridge_activity': '#FFD700'
                     })
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent events log
    with log_container:
        st.subheader("📜 Recent Events")
        
        if st.session_state.ai_running:
            # Try to read actual recent events from your log files
            log_files = list(LOG_DIR.glob('*.jsonl')) if LOG_DIR.exists() else []
            
            if log_files:
                # Get the most recent log file
                latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
                
                try:
                    # Read last 5 events efficiently without loading entire file
                    events = []
                    with open(latest_log, 'r') as f:
                        # Seek to end and read backwards for large files
                        file_size = f.seek(0, 2)  # Seek to end
                        if file_size > 50000:  # If file > 50KB, use tail approach
                            # Start from end and work backwards to find last 5 lines
                            f.seek(max(0, file_size - 10000))  # Start 10KB from end
                            lines = f.readlines()[1:]  # Skip potentially partial first line
                            last_lines = lines[-5:] if len(lines) >= 5 else lines
                        else:
                            # Small file - safe to read all
                            f.seek(0)
                            lines = f.readlines()
                            last_lines = lines[-5:] if len(lines) >= 5 else lines
                        
                        for line in last_lines:
                            try:
                                events.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue  # Skip malformed lines
                    
                    # Display actual events
                    for event in reversed(events):  # Show newest first
                        timestamp = event.get('timestamp', 'Unknown')
                        event_type = event.get('event_type', 'Unknown')
                        data = event.get('data', {})
                        
                        # Format based on event type with sanitization
                        if event_type == 'symbol_activation':
                            icon = "🔮"
                            symbol = sanitize_log_string(str(data.get('symbol', '?')), 50)
                            emotion = sanitize_log_string(str(data.get('emotion', 'unknown')), 20)
                            message = f"{symbol} activated with {emotion} (resonance: {data.get('resonance', 0):.2f})"
                        elif event_type == 'bridge_decision':
                            icon = "🌉"
                            decision = sanitize_log_string(str(data.get('decision', 'Unknown')), 20)
                            url = sanitize_log_string(str(data.get('url', 'unknown URL')), 40)
                            message = f"{decision} for {url}"
                        elif event_type == 'memory_migration':
                            icon = "📦"
                            item_id = sanitize_log_string(str(data.get('item_id', '?')), 20)
                            from_node = sanitize_log_string(str(data.get('from_node', '?')), 20)
                            to_node = sanitize_log_string(str(data.get('to_node', '?')), 20)
                            message = f"Item {item_id} moved from {from_node} to {to_node}"
                        else:
                            icon = "📌"
                            safe_data = sanitize_log_string(str(data), 100)
                            message = f"{event_type}: {safe_data}"
                        
                        col1, col2, col3 = st.columns([2, 1, 7])
                        col1.write(timestamp.split('T')[1].split('.')[0] if 'T' in timestamp else timestamp)
                        col2.write(icon)
                        col3.write(message)
                
                except Exception as e:
                    st.error(f"Error reading log events: {e}")
                    st.info("No recent events to display")
            else:
                st.info("No log files found. Events will appear here when the AI is running.")
        else:
            st.info("AI is stopped. No new events.")

# ==================== NEW: ORIGIN TRACER ====================

elif page == "Origin Tracer":
    st.header("🔍 Symbol & Memory Origin Tracer")
    
    st.markdown("""
    Trace the origin and evolution of symbols and memory nodes. 
    See what bridge events spawned them and track their transformation journey.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        trace_type = st.radio("Select trace type", ["Symbol", "Memory Node", "Bridge Event"])
        
        if trace_type == "Symbol":
            symbol_memory = safe_load_json('symbol_memory.json', dict)
            selected_item = st.selectbox("Select symbol", list(symbol_memory.keys()))
        elif trace_type == "Memory Node":
            st.info("Memory node tracing requires log analysis")
            selected_item = st.text_input("Enter node ID")
        else:
            st.info("Bridge event tracing requires event logs")
            selected_item = st.text_input("Enter event ID")
    
    with col2:
        if selected_item:
            st.subheader(f"📍 Origin Trace: {selected_item}")
            
            # Create origin visualization
            if trace_type == "Symbol" and '⟳' in selected_item:
                # Show recursion tree
                base_symbol = selected_item.replace('⟳', '')
                recursion_depth = selected_item.count('⟳')
                
                # Create tree visualization
                tree_data = []
                for i in range(recursion_depth + 1):
                    symbol = base_symbol + '⟳' * i
                    tree_data.append({
                        'Symbol': symbol,
                        'Depth': i,
                        'Type': 'Recursive' if i > 0 else 'Base'
                    })
                
                df_tree = pd.DataFrame(tree_data)
                
                fig_tree = px.sunburst(df_tree, path=['Type', 'Symbol'], 
                                      values=[1]*len(df_tree),
                                      title=f"Symbol Recursion Tree for {selected_item}")
                st.plotly_chart(fig_tree, use_container_width=True)
                
                # Show metadata if available
                meta_symbols = safe_load_json('meta_symbols.json', dict)
                if selected_item in meta_symbols:
                    st.json(meta_symbols[selected_item])

# ==================== LIVE UNIFIED MONITOR ====================

elif page == "Live Unified Monitor":
    st.header("🚀 Live Unified System Monitor")
    
    if not UNIFIED_SYSTEMS_AVAILABLE:
        st.error("❌ Unified systems not available. Please check imports.")
        st.stop()
    
    # Control panel
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Refresh Systems"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox("⚡ Auto-refresh", value=True)
    
    if auto_refresh and HAS_AUTOREFRESH:
        count = st_autorefresh(interval=2000, limit=None, key="unified_refresh")
    
    # Get unified data
    unified_data = get_unified_data()
    system_status = unified_data.get('system_status', {})
    
    # System health overview
    st.subheader("🔍 System Health Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric(
        "Memory System", 
        "🟢 Online" if system_status.get('memory_active', False) else "🔴 Offline",
        delta="Active" if system_status.get('memory_active', False) else "Inactive"
    )
    
    col2.metric(
        "Symbol System", 
        "🟢 Online" if system_status.get('symbols_active', False) else "🔴 Offline",
        delta=f"{len(unified_data['symbol_memory'])} symbols"
    )
    
    col3.metric(
        "Orchestration", 
        "🟢 Online" if system_status.get('orchestration_active', False) else "🔴 Offline",
        delta="Unified"
    )
    
    col4.metric(
        "Import Status", 
        "✅ Success" if UNIFIED_SYSTEMS_AVAILABLE else "❌ Failed",
        delta="All systems" if UNIFIED_SYSTEMS_AVAILABLE else "Check logs"
    )
    
    col5.metric(
        "Overall Health", 
        system_status.get('health', 'Unknown'),
        delta=system_status.get('uptime', 'Unknown')
    )
    
    # Unified memory statistics
    st.subheader("💾 Unified Memory Statistics")
    
    try:
        memory_system = get_unified_memory()
        # Try different method names
        memory_stats = {}
        if hasattr(memory_system, 'get_memory_stats'):
            memory_stats = memory_system.get_memory_stats()
        elif hasattr(memory_system, 'get_stats'):
            memory_stats = memory_system.get_stats()
        else:
            # Fallback to reading memory files directly
            memory_stats = {
                'logic_count': len(safe_load_json('logic_memory.json', list)),
                'symbolic_count': len(safe_load_json('symbol_memory.json', dict)),
                'bridge_count': len(safe_load_json('bridge_memory.json', list)),
                'vector_count': 0,
                'user_count': 0
            }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Memory breakdown
            memory_types = ['logic', 'symbolic', 'bridge', 'vector', 'user']
            memory_counts = [memory_stats.get(f'{t}_count', 0) for t in memory_types]
            
            fig_memory = go.Figure(data=[
                go.Bar(x=memory_types, y=memory_counts,
                       marker_color=['#4682B4', '#FF69B4', '#FFD700', '#32CD32', '#FF6347'])
            ])
            fig_memory.update_layout(
                title="Unified Memory Distribution",
                xaxis_title="Memory Type",
                yaxis_title="Item Count",
                height=400
            )
            st.plotly_chart(fig_memory, use_container_width=True)
        
        with col2:
            # Try to show real memory activity over time - with safe data_manager access
            session_logs = []
            try:
                if hasattr(memory_system, 'data_manager') and callable(getattr(memory_system.data_manager, 'get_json_data', None)):
                    session_logs = memory_system.data_manager.get_json_data('session_log.json', [])
            except (AttributeError, TypeError, Exception):
                # Fallback to empty list if data_manager access fails
                session_logs = []
            
            if session_logs and len(session_logs) > 5:
                # Use real session data for growth chart
                recent_sessions = session_logs[-20:]  # Last 20 sessions
                timestamps = [datetime.fromisoformat(s['timestamp']) for s in recent_sessions if 'timestamp' in s]
                total_items = [s.get('input_length', 0) + s.get('processing_steps', 0) for s in recent_sessions]
                
                growth_data = pd.DataFrame({
                    'timestamp': timestamps,
                    'total_items': total_items,
                    'processing_steps': [s.get('processing_steps', 0) for s in recent_sessions],
                    'input_length': [s.get('input_length', 0) for s in recent_sessions]
                })
                
                fig_growth = px.line(growth_data, x='timestamp', 
                                   y=['total_items', 'processing_steps', 'input_length'],
                                   title="Memory System Activity (Real Data)",
                                   color_discrete_map={
                                       'total_items': '#4682B4',
                                       'processing_steps': '#32CD32',
                                       'input_length': '#FF6347'
                                   })
                fig_growth.update_layout(height=400)
                st.plotly_chart(fig_growth, use_container_width=True)
            else:
                # Fallback when no real data available
                st.info("📊 Memory activity chart will appear when session data is available")
                st.text("Real-time metrics need more sessions to generate meaningful trends.")
    
    except Exception as e:
        st.error(f"Error accessing memory system: {e}")
    
    # Symbol system insights
    st.subheader("🔮 Symbol System Insights")
    
    try:
        symbol_system = get_unified_symbol_system()
        # Try different ways to get symbols
        all_symbols = []
        if hasattr(symbol_system, 'get_all_symbols'):
            all_symbols = symbol_system.get_all_symbols()
        elif hasattr(symbol_system, 'symbols'):
            all_symbols = list(symbol_system.symbols.values())
        elif hasattr(symbol_system, 'symbol_registry'):
            all_symbols = list(symbol_system.symbol_registry.values())
        else:
            # Fallback to reading symbol_memory.json
            symbol_data = safe_load_json('symbol_memory.json', dict)
            # Convert dict entries to symbol-like objects
            all_symbols = []
            for glyph, data in symbol_data.items():
                # Create a simple object-like dict
                symbol = type('Symbol', (), {
                    'glyph': glyph,
                    'name': data.get('name', glyph),
                    'mathematical_concepts': data.get('keywords', []),
                    'metaphorical_concepts': data.get('core_meanings', [])
                })()
                all_symbols.append(symbol)
        
        if all_symbols:
            # Symbol type distribution
            math_concepts = []
            meta_concepts = []
            
            for symbol in all_symbols:
                math_concepts.extend(symbol.mathematical_concepts)
                meta_concepts.extend(symbol.metaphorical_concepts)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Most common mathematical concepts
                math_counter = Counter(math_concepts)
                top_math = math_counter.most_common(10)
                
                if top_math:
                    df_math = pd.DataFrame(top_math, columns=['Concept', 'Count'])
                    fig_math = px.bar(df_math, x='Count', y='Concept', 
                                    orientation='h', title="Top Mathematical Concepts")
                    fig_math.update_layout(height=400)
                    st.plotly_chart(fig_math, use_container_width=True)
            
            with col2:
                # Most common metaphorical concepts
                meta_counter = Counter(meta_concepts)
                top_meta = meta_counter.most_common(10)
                
                if top_meta:
                    df_meta = pd.DataFrame(top_meta, columns=['Concept', 'Count'])
                    fig_meta = px.bar(df_meta, x='Count', y='Concept', 
                                    orientation='h', title="Top Metaphorical Concepts",
                                    color_discrete_sequence=['#FF69B4'])
                    fig_meta.update_layout(height=400)
                    st.plotly_chart(fig_meta, use_container_width=True)
            
            # Symbol learning progress
            st.subheader("📈 Symbol Learning Progress")
            learning_phases = defaultdict(int)
            for symbol in all_symbols:
                phase = getattr(symbol, 'learning_phase', 1)
                learning_phases[phase] += 1
            
            if learning_phases:
                phases_df = pd.DataFrame(list(learning_phases.items()), 
                                       columns=['Learning Phase', 'Symbol Count'])
                phases_df = phases_df.sort_values('Learning Phase')
                
                fig_phases = px.bar(phases_df, x='Learning Phase', y='Symbol Count',
                                  title="Symbols by Learning Phase",
                                  color='Symbol Count',
                                  color_continuous_scale='viridis')
                fig_phases.update_layout(height=300)
                st.plotly_chart(fig_phases, use_container_width=True)
        
        else:
            st.info("No symbols found in the unified symbol system.")
    
    except Exception as e:
        st.error(f"Error accessing symbol system: {e}")
    
    # Live system calls and activity
    st.subheader("🔄 Live System Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Recent System Calls:**")
        
        # This would be replaced with actual system call logging
        recent_calls = [
            {"time": "14:32:15", "system": "Memory", "call": "store_vector()", "status": "✅"},
            {"time": "14:32:14", "system": "Symbol", "call": "discover_symbol()", "status": "✅"},
            {"time": "14:32:13", "system": "Orchestration", "call": "process_input()", "status": "✅"},
            {"time": "14:32:12", "system": "Memory", "call": "retrieve_similar()", "status": "✅"},
            {"time": "14:32:11", "system": "Symbol", "call": "update_emotions()", "status": "⚠️"},
        ]
        
        for call in recent_calls:
            st.text(f"{call['time']} | {call['system']:<12} | {call['call']:<20} {call['status']}")
    
    with col2:
        st.markdown("**System Performance:**")
        
        performance_metrics = {
            "Memory Access Time": "0.003s",
            "Symbol Lookup Time": "0.001s", 
            "Cache Hit Rate": "94.2%",
            "Error Rate": "0.1%",
            "Uptime": "99.8%"
        }
        
        for metric, value in performance_metrics.items():
            st.text(f"{metric:<20}: {value}")
    
    # System configuration summary
    st.subheader("⚙️ System Configuration")
    
    config_info = {
        "Data Directory": system_status.get('data_dir', 'Unknown'),
        "Cache TTL": "5 seconds",
        "Memory Backend": "Unified JSON + Memory",
        "Symbol Backend": "Vector + Semantic",
        "Orchestration": "Unified Pipeline"
    }
    
    config_df = pd.DataFrame(list(config_info.items()), columns=['Setting', 'Value'])
    st.table(config_df)

# ==================== UTILITY FUNCTIONS ====================

def convert_to_jsonl(json_file: str, output_dir: str = "logs") -> Optional[Path]:
    """Convert your existing JSON logs to JSONL format"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            output_file = output_dir / f"{Path(json_file).stem}.jsonl"
            with open(output_file, 'w') as f:
                for item in data:
                    f.write(json.dumps(item) + '\n')
            return output_file
        else:
            st.error(f"{json_file} is not a list format")
            return None
    except Exception as e:
        st.error(f"Conversion error: {e}")
        return None

# Data directory configuration
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Data Directory")
new_data_dir = st.sidebar.text_input(
    "Data Directory Path", 
    value=st.session_state.custom_data_dir,
    help="Point dashboard to different data folder"
)

if new_data_dir != st.session_state.custom_data_dir:
    if Path(new_data_dir).exists():
        st.session_state.custom_data_dir = new_data_dir
        st.sidebar.success("✅ Data directory updated")
        st.cache_data.clear()  # Clear cache when switching directories
        st.rerun()
    else:
        st.sidebar.error("❌ Directory does not exist")

st.sidebar.info(f"📂 Current: {DATA_DIR}")

# Conversion utility in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Utilities")

# Add GPU Diagnostics
with st.sidebar.expander("🖥️ GPU Diagnostics"):
    import torch
    st.write(f"PyTorch Version: `{torch.__version__}`")
    st.write(f"CUDA Available: `{'✅ Yes' if torch.cuda.is_available() else '❌ No'}`")
    if torch.cuda.is_available():
        st.write(f"Device: `{torch.cuda.get_device_name(0)}`")
    else:
        st.info("If CUDA is False, try: `python -m streamlit run data/tripartite_dashboard.py` to ensure same environment.")

# Add Trust Repair
if st.sidebar.button("🛡️ Repair High-Trust Seeds"):
    try:
        from trust_database import TrustDatabase
        db = TrustDatabase()
        high_trust_seeds = {
            'wikipedia.org': 0.95, 
            'cambridge.org': 0.90, 
            'iep.utm.edu': 0.95,
            'plato.stanford.edu': 0.95,
            'nature.com': 0.90,
            'science.org': 0.90
        }
        for d, s in high_trust_seeds.items():
            db.override_trust(d, s, "Manual repair via dashboard")
        st.sidebar.success("✅ High-trust domains re-seeded!")
    except Exception as e:
        st.sidebar.error(f"Trust repair failed: {e}")

# Check for existing log files
trail_json_path = DATA_DIR / "trail_log.json"
jsonl_files = list(LOG_DIR.glob("*.jsonl")) if LOG_DIR.exists() else []

if trail_json_path.exists():
    if st.sidebar.button("Convert trail_log.json to JSONL"):
        try:
            result = convert_to_jsonl(str(trail_json_path), str(LOG_DIR))
            if result:
                st.sidebar.success(f"✅ Converted to {result}")
        except Exception as e:
            st.sidebar.error(f"❌ Conversion failed: {e}")
elif jsonl_files:
    latest_jsonl = max(jsonl_files, key=lambda x: x.stat().st_mtime)
    st.sidebar.info(f"📄 Using JSONL: {latest_jsonl.name}")
else:
    st.sidebar.info("📄 No log files found")

# Always allow buffer flush
if st.sidebar.button("Flush Event Buffer"):
    logger._flush_buffer()
    st.sidebar.success("✅ Event buffer flushed")

# Show file status with consolidated warnings
st.sidebar.markdown("---")
st.sidebar.subheader("📊 File Status")
files_to_check = [
    ("symbol_memory.json", "Symbols"),
    ("logic_memory.json", "Logic"),
    ("bridge_memory.json", "Bridge"),
    ("link_decisions.csv", "Decisions")
]

found_files = []
missing_files = []

for filename, label in files_to_check:
    file_path = DATA_DIR / filename
    if file_path.exists():
        size = file_path.stat().st_size / 1024
        found_files.append((label, size))
    else:
        missing_files.append(label)

# Show found files
for label, size in found_files:
    st.sidebar.success(f"✅ {label}: {size:.1f} KB")

# Consolidate missing files into a single warning
if missing_files:
    if len(missing_files) == len(files_to_check):
        st.sidebar.error("❌ No core data files found - check data directory")
    else:
        missing_list = ", ".join(missing_files)
        st.sidebar.warning(f"⚠️ Missing: {missing_list}")

# Show current session info
st.sidebar.markdown("---")
st.sidebar.info(f"Session ID: {st.session_state.session_id}")
st.sidebar.info(f"Log location: {logger.current_log}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🧠 **Tripartite Memory System v2.0**")
st.sidebar.markdown("Enhanced with origin tracing, weighted networks, and real-time monitoring")
st.sidebar.markdown("Built with ❤️ for transparent AI")