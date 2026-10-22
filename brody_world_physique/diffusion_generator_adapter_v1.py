"""G02: Diffusion & Visual Generator Adapter with Strict Hardware Safety Barrier.

Guards against downloading heavy multi-gigabyte models (e.g., 6B, 12B, SDXL, Flux)
on machines lacking dedicated CUDA GPUs and high VRAM.

Machine Profile on this workstation:
- Integrated Intel UHD Graphics (shared system memory only, no dedicated CUDA VRAM).
- Free RAM ~1.5 GB.
- Heavy diffusion models (>2GB weights) WILL trigger Out-Of-Memory or severe thrashing.

Architecture:
- Explicit Hardware Safety Barrier: probes VRAM / CUDA before any model acquisition.
- If VRAM < 6GB or CUDA is absent, heavy diffusion weight downloads are STRICTLY FORBIDDEN.
- Bounded fallback mode: utilizes local procedural, geometric and instrument renderers
  producing valid GeneratedArtifactV0 objects complying with VisualEditIntentCandidateV1.

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- native_memory_write_allowed = False.
- auto_promotion_allowed = False.
- emits_act = False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import io
import os
import platform
import shutil
import sys
from typing import Any, Mapping
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, digest_bytes
from .instrument_school_v2 import render_instrument
from .visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RigorProfileV1,
    VisualComplianceReportV1,
    VisualEditIntentCandidateV1,
)

MIN_VRAM_GB_FOR_HEAVY_DIFFUSION = 6.0


class MachineFormFactorV1(str, Enum):
    LAPTOP_PORTABLE = "LAPTOP_PORTABLE"
    DESKTOP_FIXED = "DESKTOP_FIXED"
    SERVER_OR_CLOUD = "SERVER_OR_CLOUD"
    UNKNOWN = "UNKNOWN"


class GenerationModalityV1(str, Enum):
    """Strict taxonomic separation of visual generation modes."""
    PROCEDURAL_VISUAL_GENERATION = "PROCEDURAL_VISUAL_GENERATION"
    NEURAL_IMAGE_GENERATION = "NEURAL_IMAGE_GENERATION"
    PROGRAMMATIC_TOOL_ORCHESTRATION = "PROGRAMMATIC_TOOL_ORCHESTRATION"


class HeavyDiffusionDownloadBlockedError(RuntimeError):
    """Raised when attempting to download heavy diffusion weights while target hardware is on HOLD."""
    pass


@dataclass(frozen=True)
class HardwareProfileV1:
    """Probed hardware profile of the host system."""
    os_name: str
    architecture: str
    total_ram_gb: float
    free_ram_gb: float
    has_cuda: bool
    cuda_device_name: str | None
    dedicated_vram_gb: float
    is_heavy_diffusion_capable: bool
    reason: str
    form_factor: MachineFormFactorV1 = MachineFormFactorV1.UNKNOWN
    hold_on_heavy_weights: bool = True
    neural_generation_globally_prohibited: bool = False


def probe_hardware_profile() -> HardwareProfileV1:
    """Probes the current system's CPU, RAM, and GPU capabilities deterministically."""
    os_name = platform.system()
    arch = platform.machine()

    # Memory probe
    total_ram = 16.0
    free_ram = 2.0
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
            total_ram = round(stat.ullTotalPhys / (1024 ** 3), 2)
            free_ram = round(stat.ullAvailPhys / (1024 ** 3), 2)
    except Exception:
        pass

    # GPU probe
    has_cuda = False
    cuda_name = None
    dedicated_vram = 0.0

    try:
        import torch
        if torch.cuda.is_available():
            has_cuda = True
            cuda_name = torch.cuda.get_device_name(0)
            dedicated_vram = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2)
    except ImportError:
        has_cuda = False

    is_capable = has_cuda and (dedicated_vram >= MIN_VRAM_GB_FOR_HEAVY_DIFFUSION)
    if not has_cuda:
        reason = "NO_CUDA_GPU_DETECTED (Integrated graphics or CPU only; heavy diffusion models on HOLD)"
    elif dedicated_vram < MIN_VRAM_GB_FOR_HEAVY_DIFFUSION:
        reason = f"INSUFFICIENT_VRAM ({dedicated_vram} GB < {MIN_VRAM_GB_FOR_HEAVY_DIFFUSION} GB threshold; heavy diffusion models on HOLD)"
    else:
        reason = f"HARDWARE_CAPABLE ({cuda_name} with {dedicated_vram} GB VRAM; heavy diffusion permitted)"

    # Form factor probe (portable laptop vs fixed desktop)
    form_factor = MachineFormFactorV1.UNKNOWN
    try:
        import ctypes
        class SYSTEM_POWER_STATUS(ctypes.Structure):
            _fields_ = [
                ("ACLineStatus", ctypes.c_byte),
                ("BatteryFlag", ctypes.c_byte),
                ("BatteryLifePercent", ctypes.c_byte),
                ("SystemStatusFlag", ctypes.c_byte),
                ("BatteryLifeTime", ctypes.c_ulong),
                ("BatteryFullLifeTime", ctypes.c_ulong),
            ]
        sps = SYSTEM_POWER_STATUS()
        if hasattr(ctypes, "windll") and ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(sps)):
            if sps.BatteryFlag == 128:
                form_factor = MachineFormFactorV1.DESKTOP_FIXED
            elif sps.BatteryFlag != 255 and sps.BatteryLifePercent <= 100:
                form_factor = MachineFormFactorV1.LAPTOP_PORTABLE
    except Exception:
        pass

    return HardwareProfileV1(
        os_name=os_name,
        architecture=arch,
        total_ram_gb=total_ram,
        free_ram_gb=free_ram,
        has_cuda=has_cuda,
        cuda_device_name=cuda_name,
        dedicated_vram_gb=dedicated_vram,
        is_heavy_diffusion_capable=is_capable,
        reason=reason,
        form_factor=form_factor,
        hold_on_heavy_weights=not is_capable,
        neural_generation_globally_prohibited=False,
    )


@dataclass(frozen=True)
class GeneratedArtifactV0:
    """Artifact emitted by a visual generation adapter."""
    artifact_id: str
    image_sha256: str
    image_bytes: bytes
    generation_mode: str
    model_name: str
    hardware_profile: HardwareProfileV1
    compliance_report: VisualComplianceReportV1 | None
    is_generated: bool = True
    generation_modality: GenerationModalityV1 = GenerationModalityV1.PROCEDURAL_VISUAL_GENERATION
    is_procedural_fallback: bool = True
    native_memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False
    decision_authority: str = "KX108_ONLY"

    def as_pil_image(self) -> Image.Image:
        return Image.open(io.BytesIO(self.image_bytes))


class DiffusionGeneratorAdapterV1:
    """Adapter managing generation candidates while enforcing hardware barriers."""

    def __init__(self, hardware_profile: HardwareProfileV1 | None = None) -> None:
        self.hardware = hardware_profile or probe_hardware_profile()

    def request_heavy_model_download(self, model_identifier: str) -> None:
        """Enforces barrier against downloading heavy models without capable hardware."""
        if not self.hardware.is_heavy_diffusion_capable:
            raise HeavyDiffusionDownloadBlockedError(
                f"Blocked download of heavy diffusion model '{model_identifier}': {self.hardware.reason}"
            )

    def generate(
        self,
        intent: VisualEditIntentCandidateV1,
        *,
        base_canvas: Image.Image | None = None,
        tool: str = "PEN",
    ) -> GeneratedArtifactV0:
        """Executes safe bounded generation adhering to intent and hardware constraints."""
        canvas = base_canvas.convert("L").copy() if base_canvas else Image.new("L", (64, 64), 255)
        before_canvas = canvas.copy()

        # Execute bounded generation respecting LOCK regions
        draw = ImageDraw.Draw(canvas)

        # Parse requested goals procedurally
        goal = intent.goal_description.upper()
        if "CIRCLE" in goal or "ROUND" in goal:
            # Respect LOCK boundaries
            draw.ellipse([16, 16, 48, 48], outline=0, width=3)
        elif "SQUARE" in goal or "BOX" in goal:
            draw.rectangle([16, 16, 48, 48], outline=0, width=3)
        elif "CROSS" in goal:
            draw.line([(32, 16), (32, 48)], fill=0, width=3)
            draw.line([(16, 32), (48, 32)], fill=0, width=3)
        else:
            # Default stroke
            draw.line([(16, 32), (48, 32)], fill=0, width=3)

        # Restore any LOCK regions if they were inadvertently overwritten
        for rc in intent.region_constraints:
            if rc.constraint_kind == ConstraintKindV1.LOCK:
                x0, y0, x1, y1 = rc.bbox_xyxy
                crop = before_canvas.crop((x0, y0, x1, y1))
                canvas.paste(crop, (x0, y0))

        compliance = intent.check_compliance(before_canvas, canvas)

        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        raw_bytes = buf.getvalue()
        img_sha = digest_bytes(canvas.tobytes())

        return GeneratedArtifactV0(
            artifact_id=f"GEN-{intent.intent_id}",
            image_sha256=img_sha,
            image_bytes=raw_bytes,
            generation_mode="BOUNDED_PROCEDURAL_SAFE_FALLBACK",
            model_name="BRODY_SAFE_PROCEDURAL_GENERATOR_V1",
            hardware_profile=self.hardware,
            compliance_report=compliance,
        )
