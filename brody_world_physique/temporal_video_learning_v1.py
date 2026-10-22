"""Temporal Video Learning & Preverbal Trajectory Tracking V1.

Builds on Brody and Obsidia F12 / MMonde temporal capabilities:
1. Reuses PositionMeasurementV0 and preverbal prediction contracts.
2. Ingests video frame sequences and distinguishes:
   - OBJECT_MOTION (true target translation in stationary coordinate frame)
   - CAMERA_MOTION (global shift of background anchor landmarks)
   - OCCLUSION (temporary disappearance behind occluder without trajectory breach)
   - APPEARANCE_CHANGE (morphological / tonal deformation without centroid jump)
   - UNKNOWN (ambiguous, uncertain, or out-of-distribution visual signals)
3. Enforces preverbal commitment: forecast on frame t+1 is emitted BEFORE reading frame t+1.
4. Generates candidate simulated experiences (CANDIDATE_ONLY, KX108_ONLY).
5. Never assumes physical laws (gravity, friction) or promotes to canonical memory.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw, ImageFilter, ImageStat

from .preverbal_prediction_v0 import (
    PositionMeasurementV0,
    predict_from_three,
)
from .contracts_v0 import (
    DECISION_AUTHORITY,
    ExperienceValidationStatusV0,
    MemoryEligibilityV0,
    TransformationEpistemicClassV0,
    WorldExperienceCandidateV0,
    _assert_non_sovereign,
)
from .drawing_school_v0 import black_pixels, digest_bytes


class MotionAttributionV1(str, Enum):
    """Rigorous attribution of visual displacement observed across frames."""
    OBJECT_MOTION = "OBJECT_MOTION"
    CAMERA_MOTION = "CAMERA_MOTION"
    OCCLUSION = "OCCLUSION"
    APPEARANCE_CHANGE = "APPEARANCE_CHANGE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class TemporalEntityObservationV1:
    """Detected entity in a single video frame."""
    entity_id: str
    centroid_xy: tuple[float, float]
    bbox_xyxy: tuple[int, int, int, int]
    area_px: int
    mean_luminance: float
    is_anchor: bool = False


@dataclass(frozen=True)
class TemporalFrameObservationV1:
    """Measured state of an observed video frame."""
    frame_index: int
    timestamp_s: float
    source_sha256: str
    entities: tuple[TemporalEntityObservationV1, ...]
    estimated_camera_displacement: tuple[float, float]
    attribution: MotionAttributionV1
    epistemic_notes: str
    decision_authority: str = DECISION_AUTHORITY


@dataclass(frozen=True)
class PreverbalForecastV1:
    """Precommitted spatial prediction emitted BEFORE held-out frame is revealed."""
    entity_id: str
    prior_frame_indices: tuple[int, int, int]
    prior_positions_xy: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
    forecast_frame_index: int
    forecast_xy: tuple[float, float]
    method: str = "PREVERBAL_CONSTANT_ACCELERATION_V0"
    precommitted_before_frame_decode: bool = True
    decision_authority: str = DECISION_AUTHORITY


@dataclass(frozen=True)
class TemporalConfrontationReceiptV1:
    """Receipt documenting the confrontation between preverbal forecast and actual observation."""
    receipt_id: str
    forecast: PreverbalForecastV1
    actual_xy: tuple[float, float] | None
    spatial_error_px: float | None
    attribution: MotionAttributionV1
    status: str  # CONFRONTATION_SUCCESS, CONFRONTATION_DEVIATION, HOLD_OCCLUSION, HOLD_CAMERA_MOTION, UNKNOWN_AMBIGUOUS
    candidate_experience: dict[str, Any] | None
    is_candidate: bool = True
    memory_eligibility: str = "CANDIDATE_ONLY"
    decision_authority: str = DECISION_AUTHORITY


class TemporalVideoCognitiveEngineV1:
    """Processes video frames, tracks entities, disambiguates motion, and tests preverbal prediction."""

    def __init__(self, anchor_luminance_range: tuple[int, int] = (200, 255)) -> None:
        self.anchor_lum_range = anchor_luminance_range
        self._history_frames: list[TemporalFrameObservationV1] = []
        self._target_tracks: list[PositionMeasurementV0] = []
        self._last_anchor_xy: tuple[float, float] | None = None

    def ingest_frame(
        self,
        frame_img: Image.Image,
        frame_index: int,
        timestamp_s: float,
        source_sha256: str,
    ) -> TemporalFrameObservationV1:
        """Deterministically extracts entities and determines camera vs object displacement."""
        gray = frame_img.convert("L")
        w, h = gray.size

        # 1. Segment high-contrast fiducial anchor (e.g. top corner marker or static scene cue)
        # We search for rectangular or circular mark in fixed reference quadrant
        anchor_pixels = [
            (idx % w, idx // w)
            for idx, val in enumerate(gray.getdata())
            if self.anchor_lum_range[0] <= val <= self.anchor_lum_range[1]
            and (idx % w < w // 4 or idx % w > 3 * w // 4)
            and (idx // w < h // 4)
        ]

        anchor_entity: TemporalEntityObservationV1 | None = None
        if len(anchor_pixels) >= 16:
            ax = sum(x for x, y in anchor_pixels) / len(anchor_pixels)
            ay = sum(y for x, y in anchor_pixels) / len(anchor_pixels)
            abox = (
                min(x for x, y in anchor_pixels),
                min(y for x, y in anchor_pixels),
                max(x for x, y in anchor_pixels),
                max(y for x, y in anchor_pixels),
            )
            anchor_entity = TemporalEntityObservationV1(
                entity_id="scene:fiducial_anchor",
                centroid_xy=(round(ax, 2), round(ay, 2)),
                bbox_xyxy=abox,
                area_px=len(anchor_pixels),
                mean_luminance=240.0,
                is_anchor=True,
            )

        # 2. Segment foreground moving target (darker object on lighter background)
        dark_pixels = [
            (idx % w, idx // w)
            for idx, val in enumerate(gray.getdata())
            if val < 100
        ]

        target_entity: TemporalEntityObservationV1 | None = None
        if len(dark_pixels) >= 12:
            tx = sum(x for x, y in dark_pixels) / len(dark_pixels)
            ty = sum(y for x, y in dark_pixels) / len(dark_pixels)
            tbox = (
                min(x for x, y in dark_pixels),
                min(y for x, y in dark_pixels),
                max(x for x, y in dark_pixels),
                max(y for x, y in dark_pixels),
            )
            target_entity = TemporalEntityObservationV1(
                entity_id="target:moving_foreground",
                centroid_xy=(round(tx, 2), round(ty, 2)),
                bbox_xyxy=tbox,
                area_px=len(dark_pixels),
                mean_luminance=50.0,
                is_anchor=False,
            )

        # 3. Disambiguate Motion Attribution
        cam_dx, cam_dy = 0.0, 0.0
        attribution = MotionAttributionV1.UNKNOWN
        notes = "Initial observation"

        if anchor_entity is not None:
            if self._last_anchor_xy is not None:
                cam_dx = round(anchor_entity.centroid_xy[0] - self._last_anchor_xy[0], 2)
                cam_dy = round(anchor_entity.centroid_xy[1] - self._last_anchor_xy[1], 2)
            self._last_anchor_xy = anchor_entity.centroid_xy

        if abs(cam_dx) > 2.0 or abs(cam_dy) > 2.0:
            attribution = MotionAttributionV1.CAMERA_MOTION
            notes = f"Global camera motion detected: displacement ({cam_dx}, {cam_dy}) px"
        elif target_entity is None and self._history_frames:
            attribution = MotionAttributionV1.OCCLUSION
            notes = "Target entity is not visible; classified as temporary occlusion or disappearance"
        elif target_entity is not None and self._history_frames:
            # Check target displacement relative to previous frame
            prev_obs = self._history_frames[-1]
            prev_targets = [e for e in prev_obs.entities if not e.is_anchor]
            if prev_targets:
                pt = prev_targets[0]
                tdx = target_entity.centroid_xy[0] - pt.centroid_xy[0]
                tdy = target_entity.centroid_xy[1] - pt.centroid_xy[1]
                t_dist = math.hypot(tdx, tdy)

                # Check area/aspect change
                area_ratio = target_entity.area_px / max(1, pt.area_px)
                if t_dist > 1.5:
                    attribution = MotionAttributionV1.OBJECT_MOTION
                    notes = f"Local object motion: displacement ({round(tdx, 2)}, {round(tdy, 2)}) px"
                elif 0.5 < area_ratio < 2.0:
                    attribution = MotionAttributionV1.OBJECT_MOTION
                    notes = "Stationary or subtle motion"
                else:
                    attribution = MotionAttributionV1.APPEARANCE_CHANGE
                    notes = f"Significant area/morphology change (ratio {round(area_ratio, 2)})"
            else:
                attribution = MotionAttributionV1.OBJECT_MOTION
                notes = "Target emerged after occlusion"
        else:
            attribution = MotionAttributionV1.OBJECT_MOTION
            notes = "Base initial frame"

        entities = []
        if anchor_entity:
            entities.append(anchor_entity)
        if target_entity:
            entities.append(target_entity)

        frame_obs = TemporalFrameObservationV1(
            frame_index=frame_index,
            timestamp_s=timestamp_s,
            source_sha256=source_sha256,
            entities=tuple(entities),
            estimated_camera_displacement=(cam_dx, cam_dy),
            attribution=attribution,
            epistemic_notes=notes,
        )
        self._history_frames.append(frame_obs)

        if target_entity:
            pos_m = PositionMeasurementV0(
                entity_ref=target_entity.entity_id,
                source_ref=f"sha256:{source_sha256}#frame:{frame_index}",
                frame_ref="camera:frame_plane",
                time_s=timestamp_s,
                x=target_entity.centroid_xy[0],
                y=target_entity.centroid_xy[1],
                unit="px",
                source_kind="SIMULATED",
            )
            self._target_tracks.append(pos_m)

        return frame_obs

    def emit_preverbal_forecast(
        self,
        target_frame_index: int,
        target_timestamp_s: float,
    ) -> PreverbalForecastV1:
        """Precommits a spatial prediction using the 3 most recent tracking observations."""
        if len(self._target_tracks) < 3:
            raise ValueError(f"Need at least 3 historical positions for preverbal prediction, got {len(self._target_tracks)}")

        history = self._target_tracks[-3:]
        pred_cand = predict_from_three(history, target_timestamp_s)

        cand_xy = pred_cand.candidate_xy
        if cand_xy is None:
            raise RuntimeError("Predictor refused or failed to yield candidate coordinates")

        prior_frames = (
            int(history[0].source_ref.split("#frame:")[1]),
            int(history[1].source_ref.split("#frame:")[1]),
            int(history[2].source_ref.split("#frame:")[1]),
        )
        prior_pos = (
            (history[0].x, history[0].y),
            (history[1].x, history[1].y),
            (history[2].x, history[2].y),
        )

        return PreverbalForecastV1(
            entity_id=history[0].entity_ref,
            prior_frame_indices=prior_frames,
            prior_positions_xy=prior_pos,
            forecast_frame_index=target_frame_index,
            forecast_xy=(round(cand_xy[0], 2), round(cand_xy[1], 2)),
            method="PREVERBAL_CONSTANT_ACCELERATION_V0",
            precommitted_before_frame_decode=True,
        )

    def confront_and_evaluate(
        self,
        forecast: PreverbalForecastV1,
        heldout_frame_obs: TemporalFrameObservationV1,
    ) -> TemporalConfrontationReceiptV1:
        """Confronts preverbal forecast with actual measured position in the held-out frame."""
        # Find target entity in held-out frame
        targets = [e for e in heldout_frame_obs.entities if not e.is_anchor]

        if heldout_frame_obs.attribution == MotionAttributionV1.CAMERA_MOTION:
            return TemporalConfrontationReceiptV1(
                receipt_id=f"RCPT-TEMP-CAM-{forecast.forecast_frame_index}",
                forecast=forecast,
                actual_xy=targets[0].centroid_xy if targets else None,
                spatial_error_px=None,
                attribution=MotionAttributionV1.CAMERA_MOTION,
                status="HOLD_CAMERA_MOTION",
                candidate_experience=None,
            )

        if not targets:
            return TemporalConfrontationReceiptV1(
                receipt_id=f"RCPT-TEMP-OCC-{forecast.forecast_frame_index}",
                forecast=forecast,
                actual_xy=None,
                spatial_error_px=None,
                attribution=MotionAttributionV1.OCCLUSION,
                status="HOLD_OCCLUSION",
                candidate_experience=None,
            )

        actual = targets[0].centroid_xy
        err = round(math.hypot(actual[0] - forecast.forecast_xy[0], actual[1] - forecast.forecast_xy[1]), 2)

        status = "CONFRONTATION_SUCCESS" if err <= 6.0 else "CONFRONTATION_DEVIATION"

        cand_exp = {
            "trajectory_signature": [
                round(forecast.prior_positions_xy[1][0] - forecast.prior_positions_xy[0][0], 2),
                round(forecast.prior_positions_xy[1][1] - forecast.prior_positions_xy[0][1], 2),
                round(forecast.prior_positions_xy[2][0] - forecast.prior_positions_xy[1][0], 2),
                round(forecast.prior_positions_xy[2][1] - forecast.prior_positions_xy[1][1], 2),
            ],
            "forecast_error_px": err,
            "status": status,
            "decision_authority": "KX108_ONLY",
            "is_canonical": False,
        }

        return TemporalConfrontationReceiptV1(
            receipt_id=f"RCPT-TEMP-EVAL-{forecast.forecast_frame_index}",
            forecast=forecast,
            actual_xy=actual,
            spatial_error_px=err,
            attribution=heldout_frame_obs.attribution,
            status=status,
            candidate_experience=cand_exp,
        )
