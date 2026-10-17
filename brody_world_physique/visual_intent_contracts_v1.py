"""G01: Visual Edit Intent Candidate Contracts (LOCK, FLEX, IGNORE).

Formalizes visual edition and generation intent under explicit spatial and
property constraints:
- LOCK: Immutable region or property; any modification is an inviolable defect.
- FLEX: Permissible elasticity; deformation or adaptation within bounded numerical tolerance.
- IGNORE: Unconstrained aspect; changes are freely disregarded.

Constitutional boundaries:
- Candidate only: is_candidate = True.
- Decision authority: KX108_ONLY.
- Readonly: readonly = True.
- No automatic memory promotion or direct execution authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping, Sequence
from types import MappingProxyType
from PIL import Image

from .drawing_school_v0 import black_pixels, digest_bytes


class ConstraintKindV1(str, Enum):
    LOCK = "LOCK"
    FLEX = "FLEX"
    IGNORE = "IGNORE"


class RigorProfileV1(str, Enum):
    STRICT_GEOMETRIC = "STRICT_GEOMETRIC"
    SEMANTIC_SKETCH = "SEMANTIC_SKETCH"
    PERMISSIVE_STYLE = "PERMISSIVE_STYLE"


@dataclass(frozen=True)
class RegionConstraintV1:
    """Spatial bounding box constraint on a canvas [x0, y0, x1, y1]."""
    region_id: str
    bbox_xyxy: tuple[int, int, int, int]
    constraint_kind: ConstraintKindV1
    tolerance_px: float = 0.0
    rationale: str = ""

    def __post_init__(self) -> None:
        x0, y0, x1, y1 = self.bbox_xyxy
        if not (0 <= x0 <= x1 <= 512 and 0 <= y0 <= y1 <= 512):
            raise ValueError(f"Invalid bounding box coordinates: {self.bbox_xyxy}")
        if self.constraint_kind == ConstraintKindV1.LOCK and self.tolerance_px != 0.0:
            raise ValueError("LOCK constraint must have tolerance_px == 0.0")
        if self.tolerance_px < 0.0:
            raise ValueError("tolerance_px cannot be negative")


@dataclass(frozen=True)
class PropertyConstraintV1:
    """High-level property constraint (e.g. topology, stroke_count, orientation)."""
    property_name: str
    constraint_kind: ConstraintKindV1
    target_value: Any
    tolerance_numeric: float = 0.0
    rationale: str = ""

    def __post_init__(self) -> None:
        if self.constraint_kind == ConstraintKindV1.LOCK and self.tolerance_numeric != 0.0:
            raise ValueError("LOCK property constraint must have tolerance_numeric == 0.0")
        if self.tolerance_numeric < 0.0:
            raise ValueError("tolerance_numeric cannot be negative")


@dataclass(frozen=True)
class VisualComplianceReportV1:
    """Deterministic audit report evaluating compliance against visual intent."""
    intent_id: str
    compliant: bool
    lock_violations: tuple[str, ...] = ()
    flex_violations: tuple[str, ...] = ()
    ignored_inspections: tuple[str, ...] = ()
    max_observed_deviation: float = 0.0
    decision_authority: str = "KX108_ONLY"


@dataclass(frozen=True)
class VisualEditIntentCandidateV1:
    """G01 Candidate Visual Edit Intent.
    
    Contains LOCK / FLEX / IGNORE constraints across regions and properties.
    """
    intent_id: str
    goal_description: str
    rigor_profile: RigorProfileV1
    region_constraints: tuple[RegionConstraintV1, ...] = ()
    property_constraints: tuple[PropertyConstraintV1, ...] = ()
    source_reference_hash: str = ""
    decision_authority: str = "KX108_ONLY"
    readonly: bool = True
    is_candidate: bool = True

    def __post_init__(self) -> None:
        if self.decision_authority != "KX108_ONLY":
            raise ValueError("Decision authority must be KX108_ONLY")
        if not self.readonly:
            raise ValueError("VisualEditIntentCandidateV1 must be readonly")
        if not self.is_candidate:
            raise ValueError("VisualEditIntentCandidateV1 must be a candidate")

    def check_compliance(
        self,
        before_image: Image.Image,
        after_image: Image.Image,
        metadata_after: Mapping[str, Any] | None = None,
    ) -> VisualComplianceReportV1:
        """Inspects changes between before_image and after_image against constraints."""
        b_gray = before_image.convert("L")
        a_gray = after_image.convert("L")
        if b_gray.size != a_gray.size:
            return VisualComplianceReportV1(
                intent_id=self.intent_id,
                compliant=False,
                lock_violations=("CANVAS_DIMENSION_CHANGED",),
            )

        w, h = b_gray.size
        b_pixels = b_gray.load()
        a_pixels = a_gray.load()

        lock_violations: list[str] = []
        flex_violations: list[str] = []
        ignored_count: list[str] = []
        max_deviation = 0.0

        # 1. Evaluate Region Constraints
        for rc in self.region_constraints:
            if rc.constraint_kind == ConstraintKindV1.IGNORE:
                ignored_count.append(rc.region_id)
                continue

            x0, y0, x1, y1 = rc.bbox_xyxy
            diff_px = 0
            total_px = max(1, (x1 - x0) * (y1 - y0))

            for y in range(y0, y1):
                for x in range(x0, x1):
                    if b_pixels[x, y] != a_pixels[x, y]:
                        diff_px += 1

            if rc.constraint_kind == ConstraintKindV1.LOCK:
                if diff_px > 0:
                    lock_violations.append(
                        f"Region {rc.region_id} altered ({diff_px} pixels modified in locked area)"
                    )
            elif rc.constraint_kind == ConstraintKindV1.FLEX:
                deviation = diff_px / total_px
                max_deviation = max(max_deviation, deviation)
                allowed_ratio = rc.tolerance_px / 100.0 if rc.tolerance_px > 1.0 else rc.tolerance_px
                if deviation > allowed_ratio:
                    flex_violations.append(
                        f"Region {rc.region_id} exceeded tolerance: {deviation:.3f} > {allowed_ratio:.3f}"
                    )

        # 2. Evaluate Property Constraints
        if metadata_after:
            for pc in self.property_constraints:
                if pc.constraint_kind == ConstraintKindV1.IGNORE:
                    ignored_count.append(pc.property_name)
                    continue

                actual_val = metadata_after.get(pc.property_name)
                if actual_val is None:
                    continue

                if pc.constraint_kind == ConstraintKindV1.LOCK:
                    if actual_val != pc.target_value:
                        lock_violations.append(
                            f"Property {pc.property_name} changed: expected {pc.target_value}, got {actual_val}"
                        )
                elif pc.constraint_kind == ConstraintKindV1.FLEX:
                    try:
                        num_diff = abs(float(actual_val) - float(pc.target_value))
                        if num_diff > pc.tolerance_numeric:
                            flex_violations.append(
                                f"Property {pc.property_name} exceeded tolerance: diff {num_diff} > {pc.tolerance_numeric}"
                            )
                    except (ValueError, TypeError):
                        if actual_val != pc.target_value:
                            flex_violations.append(
                                f"Property {pc.property_name} non-numeric mismatch"
                            )

        compliant = (len(lock_violations) == 0 and len(flex_violations) == 0)
        return VisualComplianceReportV1(
            intent_id=self.intent_id,
            compliant=compliant,
            lock_violations=tuple(lock_violations),
            flex_violations=tuple(flex_violations),
            ignored_inspections=tuple(ignored_count),
            max_observed_deviation=max_deviation,
        )
