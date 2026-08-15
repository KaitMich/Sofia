# sitecustomize.py - Global Python customization
"""
Explicitly imported by each entry-point script (not relied on to auto-load --
CPython does not reliably auto-import a bare sitecustomize.py sitting in a
script's own directory; that mechanism only fires for one placed in an actual
site-packages directory). Import this first, before anything else:
1. Reconfigures stdout and stderr to UTF-8 to prevent Windows console encoding errors.
2. Applies the torch.classes.__path__ fix before any modules import torch.
"""

import sys

# 1. UTF-8 Console / Stream Reconfiguration for Windows
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 2. PyTorch Streamlit Hot-Reload Compatibility
try:
    import torch
    import types

    if not hasattr(torch, "classes"):
        torch.classes = types.ModuleType("torch.classes")

    torch.classes.__path__ = []
except ImportError:
    pass
except Exception:
    pass
