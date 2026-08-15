> **CORRECTED March 27, 2026** -- See SOPHIA_TRUTH_FRAMEWORK.md for project-wide corrections.

# GPU Setup Guide for Sophia AI

**Quick Reference:** How to set up Sophia for optimal performance

---

## Which Setup Do I Need?

| Environment | Setup Type | Performance | Use Case |
|-------------|------------|-------------|----------|
| **Windows Production** | GPU-Accelerated | 10x faster | Running Sophia, user interaction |
| **WSL Development** | CPU-Only | Slower but functional | Testing, development, CI/CD |
| **Linux Server** | GPU-Accelerated (if CUDA) | 10x faster | Production deployment |
| **Mac** | CPU-Only | Slower but functional | Development only |

---

## Setup 1: Windows GPU Production (Recommended)

### Prerequisites
- Windows 10/11
- NVIDIA GPU with CUDA support (RTX 4070 Super or similar)
- 12GB+ VRAM recommended

### Installation

**Step 1: Install CUDA PyTorch**
```bash
cd "C:\path\to\sofia"
pip install -r requirements.txt
```

This automatically installs PyTorch with CUDA support.

**Step 2: Verify GPU**
```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

**Expected output:**
```
CUDA available: True
GPU: NVIDIA GeForce RTX 4070 SUPER
```

**Step 3: Test GPU Acceleration**
```bash
python benchmark_emotion_gpu.py
```

**Expected output:**
```
✅ GPU Configuration:
   Device: NVIDIA GeForce RTX 4070 SUPER
   VRAM: 12.0 GB

Overall statistics (device: cuda:0):
  Average across all tests: 2.7 ms
  Speedup: 10.0x
```

### Done!
Sophia is now running with GPU acceleration.

---

## Setup 2: WSL CPU Development

### Prerequisites
- Windows Subsystem for Linux (WSL2)
- No GPU required

### Installation

**Step 1: Install CPU-only PyTorch**
```bash
cd "/path/to/sofia"

# Remove CUDA version if present
pip uninstall torch torchvision torchaudio -y

# Install CPU-only version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Step 2: Install Core Dependencies**
```bash
pip install numpy scipy scikit-learn sentence-transformers transformers
pip install beautifulsoup4 requests pydantic joblib threadpoolctl
```

**Step 3: Verify CPU Mode**
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

**Expected output:**
```
PyTorch: 2.9.1+cpu
CUDA available: False
```

**Step 4: Test Functionality**
```bash
python benchmark_emotion_gpu.py
```

**Expected output:**
```
⚠️  GPU not available - using CPU
   PyTorch device: cpu

Overall statistics (device: cpu):
  Average across all tests: 27.0 ms
```

### Done!
WSL is set up for development and testing.

---

## Troubleshooting

### "CUDA available: False" on Windows

**Problem:** PyTorch installed without CUDA support

**Solution:**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### "libcudnn.so.9: cannot open shared object file"

**Problem:** CUDA libraries not installed or not in path

**Solution (Windows):**
- Reinstall NVIDIA drivers
- Install CUDA Toolkit from NVIDIA website
- Restart computer

**Solution (WSL):**
- Use CPU-only setup (WSL doesn't need GPU)
- Follow "Setup 2: WSL CPU Development"

### Slow Performance on GPU

**Check 1: Verify GPU is being used**
```python
from emotion_handler import device
print(f"Device: {device}")  # Should be "cuda:0"
```

**Check 2: Verify VRAM usage**
```python
from gpu_config import get_gpu_config
gpu = get_gpu_config()
stats = gpu.get_memory_stats()
print(stats)
```

**Check 3: Clear GPU cache**
```python
from gpu_config import get_gpu_config
gpu = get_gpu_config()
gpu.clear_cache()
```

### Models Loading Slowly

**Expected:** First run loads models from disk (~2-3 seconds)
**Subsequent runs:** Models cached in memory (instant)

If loading remains slow:
1. Check disk speed (SSD vs HDD)
2. Check antivirus (may scan model files)
3. Move models to faster drive

---

## Performance Comparison

### Emotion Detection (3 Models)

| Setup | Average Time | Speedup | Use Case |
|-------|--------------|---------|----------|
| GPU (RTX 4070 Super) | 2.7 ms | 10x | Production |
| CPU (Modern i7/i9) | 27 ms | 1x baseline | Development |

### User Impact

**100 Messages:**
- GPU: 0.27 seconds total emotion detection
- CPU: 2.7 seconds total emotion detection

**1000 Memory Items:**
- GPU: 2.7 seconds total emotion detection
- CPU: 27 seconds total emotion detection

---

## Next: What Gets GPU Acceleration?

### Phase 1 (Complete) ✅
- **emotion_handler.py** - 3 transformer models
- **Impact:** 10x faster emotion detection
- **Status:** Production-ready

### Phase 2 (Future)
- **vector_engine.py** - Embedding models (MiniLM, E5)
- **Impact:** 5-10x faster vector operations
- **Status:** Planned

### Phase 3 (Future)
- **Symbol encoding** - Batch optimization
- **Impact:** 8-15x faster symbol matching
- **Status:** Planned

### Phase 4 (Future)
- **Smart routing** - Intelligent CPU/GPU task allocation
- **Impact:** Optimal resource utilization
- **Status:** Planned

---

## FAQ

**Q: Do I need a GPU?**
A: No, but it's 10x faster. CPU works fine for development.

**Q: What GPU do I need?**
A: Any NVIDIA GPU with 8GB+ VRAM. RTX 4070 Super (12GB) is ideal.

**Q: Can I use AMD GPU?**
A: Not yet. PyTorch CUDA requires NVIDIA. AMD ROCm support is possible future work.

**Q: Will this work on Mac?**
A: Mac uses CPU-only (no CUDA support). Functional but slower.

**Q: How much faster is GPU?**
A: 8-12x faster for emotion detection, 5-10x for embeddings (Phase 2).

**Q: Does GPU use more power?**
A: Yes, but only when processing. Idle power is minimal.

**Q: Can I switch between CPU and GPU?**
A: Yes! The code automatically detects and uses what's available.

**Q: What if my GPU has only 4GB VRAM?**
A: Emotion models need ~3GB. Should work but may be tight. 8GB+ recommended.

---

## Quick Commands

### Check Current Setup
```bash
python -c "from gpu_config import get_gpu_config; get_gpu_config()"
```

### Benchmark Performance
```bash
python benchmark_emotion_gpu.py
```

### Test Emotion Detection
```bash
python -c "from emotion_handler import predict_emotions; print(predict_emotions('I am so happy!'))"
```

### Check GPU Memory
```bash
python -c "from gpu_config import get_gpu_config; print(get_gpu_config().get_memory_stats())"
```

### Clear GPU Cache
```bash
python -c "from gpu_config import get_gpu_config; get_gpu_config().clear_cache()"
```

---

## Support

**Documentation:**
- Full details: `docs/GPU_OPTIMIZATION_PHASE1.md`
- System updates: `docs/NOVEMBER_2025_UPDATES.md`
- Main README: `README.md`

**Files to check:**
- `gpu_config.py` - GPU configuration
- `emotion_handler.py` - GPU-accelerated models
- `benchmark_emotion_gpu.py` - Performance testing

---

*Last updated: November 25, 2025*
*GPU Optimization Phase 1 Complete*
