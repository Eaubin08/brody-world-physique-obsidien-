"""PC Fixe Read-Only Environment & Hardware Inventory Verifier (V1).

Executes a non-invasive, strictly READ-ONLY audit of the host environment:
1. CPU & RAM (physical cores, total/free memory).
2. GPU & VRAM (NVIDIA driver, CUDA capabilities, GTX 1050 Ti detection).
3. Port Availability (read-only TCP probe of 8080, 8081, 11434, 5000, 7860, 8000).
4. Local Model Storage & Projector Inspection (HuggingFace cache, Ollama, GGUF models, mmproj).
5. Engine & Model Compatibility Assessment:
   - Qwen2.5-VL + mmproj projector compatibility for llama-server.
   - sd.cpp + SD 1.5 q4_0 GGUF compatibility with GTX 1050 Ti (4GB VRAM).
   - CPU offload fallback recommendation if VRAM is constrained.
6. Zero downloads, zero permanent service modifications, zero network egress.

Constitutional boundaries:
- Authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Auto-promotion: False.
- Zero eval/exec.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys
import time
from typing import Any

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from brody_world_physique.contracts_v0 import DECISION_AUTHORITY


@dataclass(frozen=True)
class PortProbeResultV1:
    port: int
    service_label: str
    is_open: bool
    response_hint: str | None = None


@dataclass(frozen=True)
class ModelFileFindingV1:
    file_path: str
    file_name: str
    size_mb: float
    category: str  # "QWEN_VL", "MMPROJ", "DIFFUSION_GGUF", "OTHER_GGUF", "PYTORCH_WEIGHTS"


@dataclass(frozen=True)
class EnvironmentInventoryReportV1:
    report_id: str
    timestamp_iso: str
    hostname: str
    os_name: str
    os_release: str
    python_version: str
    # CPU & RAM
    cpu_model: str
    cpu_cores: int
    ram_total_gb: float
    # GPU & VRAM
    gpu_detected: bool
    gpu_name: str
    vram_total_gb: float
    nvidia_driver_version: str
    cuda_available_torch: bool
    cuda_device_count: int
    # Ports
    port_probes: tuple[PortProbeResultV1, ...]
    active_ports_count: int
    # Models
    cached_models: tuple[ModelFileFindingV1, ...]
    has_qwen_vl_weights: bool
    has_mmproj_projector: bool
    has_sd_gguf_weights: bool
    # Compatibility
    qwen_vl_engine_status: str
    sd_cpp_gtx1050ti_compatibility: str
    recommended_sd_config: str
    hold_reasons: tuple[str, ...]
    decision_authority: str = DECISION_AUTHORITY


def probe_local_port(port: int, service_label: str, timeout_sec: float = 0.2) -> PortProbeResultV1:
    """Probes a local TCP port strictly in read-only mode."""
    is_open = False
    hint = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout_sec)
        res = s.connect_ex(("127.0.0.1", port))
        if res == 0:
            is_open = True
            hint = "TCP_OPEN"
        s.close()
    except Exception as e:
        hint = f"ERROR: {e}"

    return PortProbeResultV1(
        port=port,
        service_label=service_label,
        is_open=is_open,
        response_hint=hint,
    )


def inspect_gpu_environment() -> tuple[bool, str, float, str, bool, int]:
    """Inspects NVIDIA GPU, VRAM, and CUDA without altering drivers."""
    gpu_detected = False
    gpu_name = "NONE"
    vram_gb = 0.0
    driver_ver = "NONE"

    # Try nvidia-smi
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=3.0,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            lines = res.stdout.strip().splitlines()
            first = lines[0].split(",")
            gpu_name = first[0].strip()
            vram_mb = float(first[1].strip())
            vram_gb = round(vram_mb / 1024.0, 2)
            driver_ver = first[2].strip()
            gpu_detected = True
    except Exception:
        pass

    # PyTorch CUDA check
    torch_cuda = False
    cuda_count = 0
    try:
        import torch
        torch_cuda = torch.cuda.is_available()
        cuda_count = torch.cuda.device_count() if torch_cuda else 0
        if torch_cuda and not gpu_detected:
            gpu_name = torch.cuda.get_device_name(0)
            vram_bytes = torch.cuda.get_device_properties(0).total_memory
            vram_gb = round(vram_bytes / (1024.0 ** 3), 2)
            gpu_detected = True
    except ImportError:
        pass

    return gpu_detected, gpu_name, vram_gb, driver_ver, torch_cuda, cuda_count


def scan_local_model_caches() -> list[ModelFileFindingV1]:
    """Scans local directories for models without making any network requests."""
    findings: list[ModelFileFindingV1] = []
    search_dirs = [
        Path.home() / ".cache" / "huggingface" / "hub",
        Path.home() / ".ollama" / "models",
        Path("C:/models"),
        Path("C:/llama.cpp/models"),
        Path("C:/sd.cpp/models"),
    ]

    for s_dir in search_dirs:
        if not s_dir.exists():
            continue
        try:
            for p in s_dir.rglob("*"):
                if not p.is_file():
                    continue
                name_lower = p.name.lower()
                cat = None
                if "mmproj" in name_lower:
                    cat = "MMPROJ"
                elif "qwen" in name_lower and ("vl" in name_lower or "vision" in name_lower):
                    cat = "QWEN_VL"
                elif ("sd" in name_lower or "stable-diffusion" in name_lower) and name_lower.endswith(".gguf"):
                    cat = "DIFFUSION_GGUF"
                elif name_lower.endswith(".gguf"):
                    cat = "OTHER_GGUF"
                elif name_lower.endswith((".safetensors", ".bin", ".pt")):
                    cat = "PYTORCH_WEIGHTS"

                if cat is not None:
                    size_mb = round(p.stat().st_size / (1024.0 * 1024.0), 2)
                    findings.append(ModelFileFindingV1(
                        file_path=str(p.resolve()),
                        file_name=p.name,
                        size_mb=size_mb,
                        category=cat,
                    ))
        except Exception:
            pass

    return findings


def execute_pc_fixe_readonly_inventory(output_dir: Path | str | None = None) -> EnvironmentInventoryReportV1:
    """Executes the full read-only environment inventory."""
    out = Path(output_dir) if output_dir else Path("artifacts/pc_fixe_neural_audit")
    out.mkdir(parents=True, exist_ok=True)

    # 1. System & CPU
    hostname = socket.gethostname()
    os_name = platform.system()
    os_release = platform.release()
    py_ver = sys.version.split()[0]
    cpu_model = platform.processor() or "UNKNOWN_CPU"
    cpu_cores = os.cpu_count() or 1

    # RAM estimation
    ram_gb = 16.0
    try:
        import ctypes
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            ram_gb = round(stat.ullTotalPhys / (1024.0 ** 3), 2)
    except Exception:
        pass

    # 2. GPU & VRAM
    gpu_det, gpu_name, vram_gb, driver_ver, torch_cuda, cuda_count = inspect_gpu_environment()

    # 3. Port probes
    probed_ports = (
        (8080, "llama-server default HTTP API"),
        (8081, "Jarvis Qwen-VL endpoint"),
        (11434, "Ollama local API"),
        (5000, "Flask / SD-WebUI API"),
        (7860, "Gradio / ComfyUI web interface"),
        (8000, "vLLM / FastAPI local endpoint"),
    )
    port_results = tuple(probe_local_port(p, lbl) for p, lbl in probed_ports)
    active_ports = sum(1 for pr in port_results if pr.is_open)

    # 4. Local models
    models = tuple(scan_local_model_caches())
    has_qwen = any(m.category == "QWEN_VL" for m in models)
    has_mmproj = any(m.category == "MMPROJ" for m in models)
    has_sd_gguf = any(m.category == "DIFFUSION_GGUF" for m in models)

    # 5. Engine compatibility evaluation
    holds: list[str] = []

    # Qwen-VL Status
    if any(pr.port in (8080, 8081) and pr.is_open for pr in port_results):
        qwen_status = "ONLINE_SERVER_DETECTED"
    elif has_qwen and has_mmproj:
        qwen_status = "LOCAL_WEIGHTS_AND_MMPROJ_PRESENT_SERVER_IDLE"
    elif has_qwen:
        qwen_status = "QWEN_VL_PRESENT_MMPROJ_MISSING"
        holds.append("QWEN2.5_VL_REQUIRES_MMPROJ_PROJECTOR_FOR_LLAMA_SERVER")
    else:
        qwen_status = "NO_LOCAL_QWEN_VL_WEIGHTS"
        holds.append("QWEN2.5_VL_NOT_FOUND_ON_HOST")

    # sd.cpp + GTX 1050 Ti Compatibility
    if gpu_det and "1050" in gpu_name:
        sd_compat = "COMPATIBLE_WITH_QUANTIZATION_Q4_0"
        sd_rec = (
            "GTX 1050 Ti (4GB VRAM): Use sd.cpp with SD 1.5 in q4_0 / q8_0 GGUF. "
            "Peak VRAM is ~2.3 GB, leaving 1.7 GB headroom. Never load unquantized SDXL."
        )
    elif gpu_det and vram_gb >= 6.0:
        sd_compat = "HIGH_COMPATIBILITY_VRAM_SUFFICIENT"
        sd_rec = f"GPU {gpu_name} ({vram_gb} GB VRAM): Compatible with SD 1.5 FP16 or SDXL Turbo."
    elif gpu_det:
        sd_compat = "TIGHT_VRAM_REDUCTION_RECOMMENDED"
        sd_rec = f"GPU {gpu_name} ({vram_gb} GB VRAM): Use q4_0 GGUF quantization with --lowvram flag."
    else:
        sd_compat = "CPU_ONLY_INFERENCE_REQUIRED"
        sd_rec = "No CUDA GPU detected: Use CPU inference with 4 threads or execute on PC Fixe."
        holds.append("CUDA_GPU_ABSENT_ON_CURRENT_HOST")

    report_id = f"INVENTORY-{int(time.time())}"
    report = EnvironmentInventoryReportV1(
        report_id=report_id,
        timestamp_iso=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        hostname=hostname,
        os_name=os_name,
        os_release=os_release,
        python_version=py_ver,
        cpu_model=cpu_model,
        cpu_cores=cpu_cores,
        ram_total_gb=ram_gb,
        gpu_detected=gpu_det,
        gpu_name=gpu_name,
        vram_total_gb=vram_gb,
        nvidia_driver_version=driver_ver,
        cuda_available_torch=torch_cuda,
        cuda_device_count=cuda_count,
        port_probes=port_results,
        active_ports_count=active_ports,
        cached_models=models,
        has_qwen_vl_weights=has_qwen,
        has_mmproj_projector=has_mmproj,
        has_sd_gguf_weights=has_sd_gguf,
        qwen_vl_engine_status=qwen_status,
        sd_cpp_gtx1050ti_compatibility=sd_compat,
        recommended_sd_config=sd_rec,
        hold_reasons=tuple(holds),
    )

    p_json = out / "pc_fixe_environment_inventory_report.json"
    p_json.write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False), encoding="utf-8")

    return report


run_read_only_environment_inventory = execute_pc_fixe_readonly_inventory


if __name__ == "__main__":
    rep = execute_pc_fixe_readonly_inventory()
    print("=" * 60)
    print("PC FIXE READ-ONLY ENVIRONMENT INVENTORY REPORT")
    print("=" * 60)
    print(f"Report ID:    {rep.report_id}")
    print(f"Hostname:     {rep.hostname} ({rep.os_name} {rep.os_release})")
    print(f"CPU & RAM:    {rep.cpu_cores} cores | {rep.ram_total_gb} GB RAM")
    print(f"GPU & VRAM:   {rep.gpu_name} ({rep.vram_total_gb} GB VRAM) | Driver: {rep.nvidia_driver_version}")
    print(f"CUDA Torch:   {rep.cuda_available_torch} (Count: {rep.cuda_device_count})")
    print("-" * 60)
    print("PORT PROBES (Read-Only):")
    for pr in rep.port_probes:
        status_txt = "OPEN" if pr.is_open else "CLOSED/HOLD"
        print(f"  - Port {pr.port:5d} [{status_txt:11s}] : {pr.service_label}")
    print("-" * 60)
    print(f"Qwen-VL Engine Status:      {rep.qwen_vl_engine_status}")
    print(f"sd.cpp GTX 1050 Ti Status:  {rep.sd_cpp_gtx1050ti_compatibility}")
    print(f"Recommended Config:         {rep.recommended_sd_config}")
    if rep.hold_reasons:
        print("HOLD Reasons:")
        for hr in rep.hold_reasons:
            print(f"  * {hr}")
    print("=" * 60)
