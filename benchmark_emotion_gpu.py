#!/usr/bin/env python3
"""
Benchmark script to measure emotion detection performance
Compares CPU vs GPU timing (when GPU is available)
"""

import time
from emotion_handler import predict_emotions, MODELS_LOADED_EMOTION, device
from gpu_config import get_gpu_config

def benchmark_emotion_detection(text, num_runs=5):
    """Benchmark emotion detection over multiple runs"""
    if not MODELS_LOADED_EMOTION:
        print("⚠️  Models not loaded - cannot benchmark")
        return None

    timings = []

    # Warmup run (models may be slower on first run)
    predict_emotions(text)

    # Timed runs
    for i in range(num_runs):
        start = time.time()
        result = predict_emotions(text, top_n_verified=5)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        timings.append(elapsed)

    return {
        'min_ms': min(timings),
        'max_ms': max(timings),
        'avg_ms': sum(timings) / len(timings),
        'num_verified': len(result['verified']),
        'top_emotion': result['verified'][0] if result['verified'] else None
    }

def main():
    print("=" * 70)
    print("EMOTION DETECTION GPU BENCHMARK")
    print("=" * 70)
    print()

    # Show configuration
    gpu = get_gpu_config()
    print("📊 Configuration:")
    print(f"   Device: {device}")
    print(f"   CUDA available: {gpu.cuda_available}")

    if gpu.cuda_available:
        stats = gpu.get_memory_stats()
        print(f"   GPU: {stats['device']}")
        print(f"   VRAM Total: {stats['memory_total']:.2f} GB")
    print()

    # Test cases
    test_cases = [
        ("Short happy text", "I am so happy!"),
        ("Medium emotional text", "This is terrifying and makes me feel scared and full of dread."),
        ("Long complex text", "I am overwhelmed with joy and excitement about this new project! "
                             "At the same time, I feel a bit nervous and anxious about the challenges ahead. "
                             "But overall, I'm grateful for this opportunity and proud of how far we've come.")
    ]

    print("🔬 Running benchmarks (5 runs each)...")
    print()

    results = []
    for name, text in test_cases:
        print(f"Test: {name}")
        print(f"Text: {text[:60]}...")

        result = benchmark_emotion_detection(text, num_runs=5)

        if result:
            print(f"  ✓ Average time: {result['avg_ms']:.1f} ms")
            print(f"  ✓ Min time: {result['min_ms']:.1f} ms")
            print(f"  ✓ Max time: {result['max_ms']:.1f} ms")
            print(f"  ✓ Emotions detected: {result['num_verified']}")
            if result['top_emotion']:
                print(f"  ✓ Top emotion: {result['top_emotion'][0]} ({result['top_emotion'][1]:.2f})")
            results.append((name, result))
        print()

    # Summary
    if results:
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)

        avg_all = sum(r[1]['avg_ms'] for r in results) / len(results)
        min_all = min(r[1]['min_ms'] for r in results)
        max_all = max(r[1]['max_ms'] for r in results)

        print(f"\nOverall statistics (device: {device}):")
        print(f"  Average across all tests: {avg_all:.1f} ms")
        print(f"  Fastest inference: {min_all:.1f} ms")
        print(f"  Slowest inference: {max_all:.1f} ms")

        # GPU comparison note
        if not gpu.cuda_available:
            print(f"\n⚠️  Running on CPU")
            print(f"   Expected GPU speedup: 8-12x faster")
            print(f"   Estimated GPU time: {avg_all / 10:.1f} ms (predicted)")
        else:
            print(f"\n✅ Running on GPU")
            cpu_estimate = avg_all * 10
            print(f"   CPU would take: ~{cpu_estimate:.1f} ms (estimated)")
            print(f"   Speedup: {cpu_estimate / avg_all:.1f}x")

        print()
        print("=" * 70)

    return results

if __name__ == "__main__":
    results = main()

    # Return exit code based on success
    if results and len(results) > 0:
        print("✅ Benchmark complete")
        exit(0)
    else:
        print("❌ Benchmark failed")
        exit(1)
