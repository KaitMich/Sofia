"""
GPU Configuration for Sophia AI
Central configuration for CPU/GPU device placement
"""

import torch

class GPUConfig:
    """
    Central GPU configuration and device management

    Provides intelligent device selection with fallback to CPU
    and utilities for model placement.
    """

    def __init__(self):
        self.cuda_available = torch.cuda.is_available()
        self.device = torch.device('cuda' if self.cuda_available else 'cpu')
        self.device_name = str(self.device)

        # Print configuration on initialization
        self._print_config()

    def _print_config(self):
        """Print GPU configuration info"""
        if self.cuda_available:
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"✅ GPU Configuration:")
            print(f"   Device: {gpu_name}")
            print(f"   VRAM: {gpu_memory:.1f} GB")
            print(f"   PyTorch device: {self.device}")
        else:
            print(f"⚠️  GPU not available - using CPU")
            print(f"   PyTorch device: {self.device}")
            print(f"   Hint: If you have an NVIDIA GPU, ensure CUDA drivers are installed")
            print(f"   and you're using a CUDA-enabled version of PyTorch.")

    def to_device(self, model):
        """
        Move a model to the configured device

        Args:
            model: PyTorch model or tensor

        Returns:
            Model/tensor on the appropriate device
        """
        return model.to(self.device)

    def get_device_str(self):
        """Get device as string for SentenceTransformer"""
        return self.device_name

    def move_inputs_to_device(self, inputs):
        """
        Move input dictionary to device (for transformer inputs)

        Args:
            inputs: Dict with tensors (from tokenizer)

        Returns:
            Dict with tensors moved to device
        """
        if isinstance(inputs, dict):
            return {k: v.to(self.device) for k, v in inputs.items()}
        return inputs.to(self.device)

    def get_memory_stats(self):
        """Get GPU memory statistics"""
        if not self.cuda_available:
            return {
                'device': 'cpu',
                'memory_allocated': 0,
                'memory_reserved': 0,
                'memory_total': 0
            }

        return {
            'device': 'cuda',
            'memory_allocated': torch.cuda.memory_allocated(0) / 1e9,
            'memory_reserved': torch.cuda.memory_reserved(0) / 1e9,
            'memory_total': torch.cuda.get_device_properties(0).total_memory / 1e9
        }

    def clear_cache(self):
        """Clear GPU cache if available"""
        if self.cuda_available:
            torch.cuda.empty_cache()


# Global singleton instance
_gpu_config = None

def get_gpu_config():
    """Get or create the global GPU configuration"""
    global _gpu_config
    if _gpu_config is None:
        _gpu_config = GPUConfig()
    return _gpu_config


if __name__ == "__main__":
    print("🔬 Testing GPU Configuration...")

    config = get_gpu_config()

    print(f"\nDevice: {config.device}")
    print(f"CUDA available: {config.cuda_available}")

    stats = config.get_memory_stats()
    print(f"\nMemory stats:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f} GB")
        else:
            print(f"  {key}: {value}")

    print("\n✅ GPU configuration test complete")
