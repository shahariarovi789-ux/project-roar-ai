# agents/hardware_scout.py
"""
Hardware Scout Agent.
Scans host device specifications (GPU VRAM, Apple Metal, System RAM, CPU cores)
and recommends the optimal open-source LLM model tier for local Ollama execution.
"""

import sys
import os
import platform
import subprocess
import psutil
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass
class HardwareProfile:
    os_name: str
    architecture: str
    cpu_cores: int
    total_ram_gb: float
    gpu_name: Optional[str]
    vram_gb: Optional[float]
    recommended_model: str
    recommended_quant: str
    recommendation_rationale: str
    supported_models: list

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HardwareScout:
    @classmethod
    def scan_device(cls) -> HardwareProfile:
        os_name = platform.system()
        arch = platform.machine()
        cpu_cores = psutil.cpu_count(logical=True) or 4
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)

        gpu_name = None
        vram_gb = None

        # 1. Try Apple Silicon detection (macOS Metal unified memory)
        if os_name == "Darwin" and ("arm" in arch or "aarch64" in arch):
            try:
                cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]
                brand = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
                gpu_name = f"Apple Silicon ({brand})" if brand else "Apple Silicon GPU (Metal)"
            except Exception:
                gpu_name = "Apple Silicon GPU (Metal Unified Memory)"
            # Apple unified memory: ~75% usable for VRAM
            vram_gb = round(ram_gb * 0.75, 1)

        # 2. Try NVIDIA GPU detection via nvidia-smi
        if not gpu_name:
            try:
                out = subprocess.check_output(
                    ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
                if out:
                    lines = out.split("\n")
                    parts = lines[0].split(",")
                    gpu_name = parts[0].strip()
                    vram_mb = float(parts[1].strip())
                    vram_gb = round(vram_mb / 1024, 1)
            except Exception:
                pass

        # 3. Model Recommendation Logic
        effective_vram = vram_gb if vram_gb is not None else 0.0

        if effective_vram >= 24.0:
            rec_model = "qwen2.5:32b"
            quant = "Q4_K_M"
            rationale = f"High-capacity VRAM ({effective_vram}GB) detected. High parameter model enabled with exceptional reasoning depth."
            supported = ["qwen2.5:32b", "qwen2.5:14b", "qwen2.5:7b", "llama3.1:8b", "phi3:mini"]
        elif effective_vram >= 12.0:
            rec_model = "qwen2.5:14b"
            quant = "Q4_K_M"
            rationale = f"Generous VRAM ({effective_vram}GB) detected. 14B parameter model provides top-tier pedagogical explanations and grading."
            supported = ["qwen2.5:14b", "qwen2.5:7b", "llama3.1:8b", "phi3:mini"]
        elif effective_vram >= 6.0:
            rec_model = "qwen2.5:7b"
            quant = "Q4_K_M"
            rationale = f"Standard GPU/Unified VRAM ({effective_vram}GB) detected. Optimal 7B model for speed and accuracy."
            supported = ["qwen2.5:7b", "llama3.2:3b", "phi3:mini"]
        else:
            rec_model = "phi3:mini"
            quant = "Q4_K_M"
            rationale = f"Lightweight CPU/VRAM environment ({ram_gb}GB RAM). High-efficiency compact 3.8B model selected."
            supported = ["phi3:mini", "llama3.2:3b", "qwen2.5:3b"]

        return HardwareProfile(
            os_name=os_name,
            architecture=arch,
            cpu_cores=cpu_cores,
            total_ram_gb=ram_gb,
            gpu_name=gpu_name or "Standard CPU / Integrated Graphics",
            vram_gb=vram_gb,
            recommended_model=rec_model,
            recommended_quant=quant,
            recommendation_rationale=rationale,
            supported_models=supported
        )


if __name__ == "__main__":
    profile = HardwareScout.scan_device()
    import json
    print("=== Hardware Scan Profile ===")
    print(json.dumps(profile.to_dict(), indent=2))
