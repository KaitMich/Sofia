#!/usr/bin/env python3
"""
Benchmark script to measure vector embedding performance
Compares CPU vs GPU timing for vector operations
"""

import time
import numpy as np
from vector_engine import MODELS_LOADED, embed_text, fuse_vectors, device
from gpu_config import get_gpu_config

def benchmark_single_embedding(text, num_runs=10):
    """Benchmark single text embedding"""
    if not MODELS_LOADED:
        return None

    timings = []

    # Warmup
    embed_text(text, model_choice='minilm')

    # Timed runs
    for i in range(num_runs):
        start = time.time()
        vec = embed_text(text, model_choice='minilm')
        elapsed = (time.time() - start) * 1000  # Convert to ms
        timings.append(elapsed)

    return {
        'min_ms': min(timings),
        'max_ms': max(timings),
        'avg_ms': sum(timings) / len(timings),
        'vector_dim': len(vec) if vec else 0
    }

def benchmark_batch_embedding(texts, num_runs=5):
    """Benchmark batch embedding (multiple texts)"""
    if not MODELS_LOADED:
        return None

    timings = []

    # Warmup
    for text in texts:
        embed_text(text, model_choice='minilm')

    # Timed runs
    for i in range(num_runs):
        start = time.time()
        for text in texts:
            embed_text(text, model_choice='minilm')
        elapsed = (time.time() - start) * 1000  # Convert to ms
        timings.append(elapsed)

    return {
        'min_ms': min(timings),
        'max_ms': max(timings),
        'avg_ms': sum(timings) / len(timings),
        'batch_size': len(texts),
        'avg_per_item': sum(timings) / len(timings) / len(texts)
    }

def benchmark_vector_fusion(text, num_runs=10):
    """Benchmark vector fusion (both models)"""
    if not MODELS_LOADED:
        return None

    timings = []

    # Warmup
    fuse_vectors(text)

    # Timed runs
    for i in range(num_runs):
        start = time.time()
        vec, info = fuse_vectors(text)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        timings.append(elapsed)

    return {
        'min_ms': min(timings),
        'max_ms': max(timings),
        'avg_ms': sum(timings) / len(timings),
        'similarity': info['similarity'],
        'source': info['source']
    }

def main():
    print("=" * 70)
    print("VECTOR EMBEDDING GPU BENCHMARK")
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

    if not MODELS_LOADED:
        print("⚠️  Models not loaded - cannot benchmark")
        return 1

    # Test cases
    test_texts = {
        "Short": "AI consciousness",
        "Medium": "The relationship between algorithms and human creativity",
        "Long": "Artificial intelligence systems that can understand and process natural language "
               "are becoming increasingly sophisticated, enabling new forms of human-computer interaction "
               "and knowledge representation across multiple domains of inquiry."
    }

    batch_texts = [
        "What is consciousness?",
        "How do neural networks learn?",
        "The nature of symbolic reasoning",
        "Emotional intelligence in AI",
        "Ethics and artificial intelligence"
    ]

    print("🔬 Running benchmarks...")
    print()

    # Single embedding benchmarks
    print("=" * 70)
    print("SINGLE EMBEDDING (MiniLM model)")
    print("=" * 70)

    results = []
    for name, text in test_texts.items():
        print(f"\nTest: {name} text ({len(text)} chars)")
        print(f"Text: {text[:60]}...")

        result = benchmark_single_embedding(text, num_runs=10)

        if result:
            print(f"  ✓ Average time: {result['avg_ms']:.2f} ms")
            print(f"  ✓ Min time: {result['min_ms']:.2f} ms")
            print(f"  ✓ Max time: {result['max_ms']:.2f} ms")
            print(f"  ✓ Vector dimensions: {result['vector_dim']}")
            results.append((name, result))

    # Batch embedding benchmark
    print()
    print("=" * 70)
    print("BATCH EMBEDDING (5 texts)")
    print("=" * 70)
    print()

    batch_result = benchmark_batch_embedding(batch_texts, num_runs=5)

    if batch_result:
        print(f"Batch size: {batch_result['batch_size']} texts")
        print(f"  ✓ Total average time: {batch_result['avg_ms']:.2f} ms")
        print(f"  ✓ Average per item: {batch_result['avg_per_item']:.2f} ms")
        print(f"  ✓ Min time: {batch_result['min_ms']:.2f} ms")
        print(f"  ✓ Max time: {batch_result['max_ms']:.2f} ms")

    # Vector fusion benchmark
    print()
    print("=" * 70)
    print("VECTOR FUSION (MiniLM + E5)")
    print("=" * 70)
    print()

    fusion_text = "The golden ratio represents divine proportion"
    print(f"Test text: {fusion_text}")
    fusion_result = benchmark_vector_fusion(fusion_text, num_runs=10)

    if fusion_result:
        print(f"  ✓ Average time: {fusion_result['avg_ms']:.2f} ms")
        print(f"  ✓ Min time: {fusion_result['min_ms']:.2f} ms")
        print(f"  ✓ Max time: {fusion_result['max_ms']:.2f} ms")
        print(f"  ✓ Model similarity: {fusion_result['similarity']:.4f}")
        print(f"  ✓ Fusion source: {fusion_result['source']}")

    # Summary
    if results:
        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)

        avg_all = sum(r[1]['avg_ms'] for r in results) / len(results)
        min_all = min(r[1]['min_ms'] for r in results)
        max_all = max(r[1]['max_ms'] for r in results)

        print(f"\nOverall statistics (device: {device}):")
        print(f"  Single embedding average: {avg_all:.2f} ms")
        print(f"  Fastest embedding: {min_all:.2f} ms")
        print(f"  Slowest embedding: {max_all:.2f} ms")

        if batch_result:
            print(f"  Batch processing (5 items): {batch_result['avg_ms']:.2f} ms")
            print(f"  Batch per-item average: {batch_result['avg_per_item']:.2f} ms")

        if fusion_result:
            print(f"  Vector fusion average: {fusion_result['avg_ms']:.2f} ms")

        # GPU comparison note
        if not gpu.cuda_available:
            print(f"\n⚠️  Running on CPU")
            print(f"   Expected GPU speedup: 5-10x faster")
            print(f"   Estimated GPU time:")
            print(f"     Single embedding: {avg_all / 7:.2f} ms (predicted)")
            print(f"     Batch processing: {batch_result['avg_ms'] / 7:.2f} ms (predicted)" if batch_result else "")
            print(f"     Vector fusion: {fusion_result['avg_ms'] / 7:.2f} ms (predicted)" if fusion_result else "")
        else:
            print(f"\n✅ Running on GPU")
            cpu_estimate_single = avg_all * 7
            cpu_estimate_batch = batch_result['avg_ms'] * 7 if batch_result else 0
            print(f"   CPU would take:")
            print(f"     Single embedding: ~{cpu_estimate_single:.2f} ms (estimated)")
            if batch_result:
                print(f"     Batch processing: ~{cpu_estimate_batch:.2f} ms (estimated)")
            print(f"   Speedup: {cpu_estimate_single / avg_all:.1f}x")

        print()
        print("=" * 70)

    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        if exit_code == 0:
            print("✅ Benchmark complete")
        else:
            print("❌ Benchmark failed")
        exit(exit_code)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
