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


@dataclass(frozen=True)
class TargetDiffusionModelProfileV1:
    """Hardware requirements profile tailored to a specific neural diffusion model."""
    model_identifier: str
    required_vram_gb: float
    minimum_cuda_compute: str = "7.5"
    supports_cpu_offload: bool = True
    quantization_supported: bool = True
    notes: str = ""


# Canonical model profiles registry
STANDARD_DIFFUSION_MODELS: Mapping[str, TargetDiffusionModelProfileV1] = {
    "TINY_SD_DISTILLED": TargetDiffusionModelProfileV1(
        model_identifier="TINY_SD_DISTILLED",
        required_vram_gb=3.5,
        minimum_cuda_compute="7.5",
        notes="Ultra-light distilled model, deployable on modest GPUs (4GB VRAM)",
    ),
    "STABLE_DIFFUSION_1_5": TargetDiffusionModelProfileV1(
        model_identifier="STABLE_DIFFUSION_1_5",
        required_vram_gb=4.0,
        minimum_cuda_compute="7.5",
        notes="Standard SD 1.5 baseline, requires ~4GB VRAM",
    ),
    "SDXL_BASE": TargetDiffusionModelProfileV1(
        model_identifier="SDXL_BASE",
        required_vram_gb=8.0,
        minimum_cuda_compute="8.0",
        notes="High-resolution SDXL model, requires 8GB VRAM",
    ),
    "FLUX_1_SCHNELL": TargetDiffusionModelProfileV1(
        model_identifier="FLUX_1_SCHNELL",
        required_vram_gb=12.0,
        minimum_cuda_compute="8.6",
        notes="Next-gen rectified flow model, requires 12GB+ VRAM",
    ),
}


@dataclass(frozen=True)
class WorkstationNeuralConfigV1:
    """Explicit configuration for high-end Workstation / PC Fixe neural generation."""
    workstation_node_id: str
    target_gpu_model: str
    dedicated_vram_gb: float
    selected_model: str = "STABLE_DIFFUSION_1_5"
    local_weights_dir: str | None = None
    cuda_compute_capability: str = "8.0"
    local_weights_present: bool = False
    decision_authority: str = "KX108_ONLY"

    def get_model_profile(self) -> TargetDiffusionModelProfileV1:
        return STANDARD_DIFFUSION_MODELS.get(
            self.selected_model,
            TargetDiffusionModelProfileV1(
                model_identifier=self.selected_model,
                required_vram_gb=4.0,
                minimum_cuda_compute="7.5",
            ),
        )

    def __post_init__(self) -> None:
        profile = self.get_model_profile()
        if self.dedicated_vram_gb < profile.required_vram_gb:
            raise ValueError(
                f"Workstation VRAM must be >= {profile.required_vram_gb} GB for model {profile.model_identifier}, "
                f"got {self.dedicated_vram_gb} GB"
            )


class DiffusionGeneratorAdapterV1:
    """Adapter managing generation candidates while enforcing hardware barriers."""

    def __init__(self, hardware_profile: HardwareProfileV1 | None = None) -> None:
        self.hardware = hardware_profile or probe_hardware_profile()
        self._workstation_config: WorkstationNeuralConfigV1 | None = None

    def configure_workstation_neural_environment(
        self,
        config: WorkstationNeuralConfigV1,
    ) -> dict[str, Any]:
        """Prepares the neural adapter for deployment on a verified fixed workstation.
        
        Strict distinction: procedural fallback success does NOT validate neural generation.
        """
        self._workstation_config = config
        return {
            "workstation_node_id": config.workstation_node_id,
            "gpu_model": config.target_gpu_model,
            "vram_gb": config.dedicated_vram_gb,
            "hold_active": not config.local_weights_present,
            "status": "WORKSTATION_NEURAL_STANDBY" if config.local_weights_present else "HOLD_AWAITING_LOCAL_WEIGHTS",
            "decision_authority": "KX108_ONLY",
        }

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


@dataclass(frozen=True)
class WorkstationRemoteDispatchPayloadV1:
    """Sanitized payload prepared for remote transmission to workstation."""
    intent_id: str
    goal_description: str
    region_constraints: list[dict[str, Any]]
    base_canvas_sha256: str | None
    base_canvas_bytes: bytes | None
    target_workstation_node: str
    hold_on_heavy_weights: bool = True
    neural_generation_requested: bool = True
    decision_authority: str = "KX108_ONLY"


class DesktopWorkstationDiffusionStubV1:
    """Client stub running on laptop/portable machine that prepares neural diffusion dispatches
    for a high-end fixed desktop workstation without downloading model weights locally.

    Constitutional guardrails:
    - Dedicated VRAM on laptop is low -> hold_on_heavy_weights remains True.
    - Never allocates CUDA memory locally.
    - Handshakes and validates remote workstation capabilities before packaging dispatch payloads.
    - Decision authority: KX108_ONLY.
    """

    def __init__(self, hardware_profile: HardwareProfileV1 | None = None) -> None:
        self.local_hardware = hardware_profile or probe_hardware_profile()
        self._verified_workstation: WorkstationNeuralConfigV1 | None = None

    @property
    def is_laptop_safe(self) -> bool:
        """Returns True if local machine is protected from heavy downloads."""
        return self.local_hardware.hold_on_heavy_weights is True

    def verify_workstation_handshake(
        self,
        config: WorkstationNeuralConfigV1,
    ) -> dict[str, Any]:
        """Validates that target workstation meets hardware requirements tailored to selected model."""
        profile = config.get_model_profile()
        if config.dedicated_vram_gb < profile.required_vram_gb:
            raise ValueError(
                f"Workstation {config.workstation_node_id} rejected: VRAM {config.dedicated_vram_gb} GB "
                f"< minimum {profile.required_vram_gb} GB for model {profile.model_identifier}"
            )
        self._verified_workstation = config
        return {
            "status": "HANDSHAKE_VERIFIED",
            "workstation_node_id": config.workstation_node_id,
            "target_gpu": config.target_gpu_model,
            "dedicated_vram_gb": config.dedicated_vram_gb,
            "selected_model": profile.model_identifier,
            "required_vram_gb": profile.required_vram_gb,
            "cuda_compute_capability": config.cuda_compute_capability,
            "local_laptop_hold_preserved": self.is_laptop_safe,
            "decision_authority": "KX108_ONLY",
        }

    def prepare_dispatch_payload(
        self,
        intent: VisualEditIntentCandidateV1,
        base_canvas: Image.Image | None = None,
    ) -> WorkstationRemoteDispatchPayloadV1:
        """Prepares a remote dispatch payload for the workstation without local diffusion execution."""
        if self._verified_workstation is None:
            raise RuntimeError("Cannot prepare dispatch payload before verifying workstation handshake.")

        base_sha = None
        base_bytes = None
        if base_canvas is not None:
            buf = io.BytesIO()
            base_canvas.save(buf, format="PNG")
            base_bytes = buf.getvalue()
            base_sha = digest_bytes(base_canvas.convert("L").tobytes())

        constraints_data = [
            {
                "region_id": getattr(rc, "region_id", ""),
                "bbox_xyxy": rc.bbox_xyxy,
                "kind": rc.constraint_kind.value,
                "tolerance_px": getattr(rc, "tolerance_px", 0.0),
                "rationale": getattr(rc, "rationale", ""),
            }
            for rc in intent.region_constraints
        ]

        return WorkstationRemoteDispatchPayloadV1(
            intent_id=intent.intent_id,
            goal_description=intent.goal_description,
            region_constraints=constraints_data,
            base_canvas_sha256=base_sha,
            base_canvas_bytes=base_bytes,
            target_workstation_node=self._verified_workstation.workstation_node_id,
            hold_on_heavy_weights=True,
            neural_generation_requested=True,
            decision_authority="KX108_ONLY",
        )
