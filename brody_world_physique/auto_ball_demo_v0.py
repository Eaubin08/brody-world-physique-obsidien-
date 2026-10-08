"""Bounded, fully automatic orange-ball detector for ONE known simulated MP4.

No segmentation model, camera tracker, physics discovery, or memory writes.
The source file SHA-256 is pinned to the controlled Brody test clip.  Pixel
locations in decoded frames are measured by reusable Pillow routines; OpenCV
only decodes the video.  The predictor is sealed BEFORE frame 4 is read.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Callable

from PIL import Image, ImageChops

from .preverbal_prediction_v0 import (
    PositionMeasurementV0, evaluate_with_heldout, predict_from_three,
)
from .video_observation_v0 import video_sha256, choose_frame_indices


# Exact sha256 for the user's Brody BALL SIMULATED fixture. No other video is
# implicitly classified as a stationary-camera orange-ball experiment.
KNOWN_TEST_VIDEO_SHA256 = "a089fdff99f20df5a54e227f46f3b869feb6764b793e2c8e5e024c065b17153f"


@dataclass(frozen=True)
class BallCandidateV0:
    center_x: float
    center_y: float
    bbox: tuple[int, int, int, int]
    orange_pixels: int
    method: str = "DEMO_ORANGE_HSV_THRESHOLD_NOT_GENERAL_SEGMENTATION"
    confidence_calibrated: bool = False


def detect_orange_ball(frame_rgb: Image.Image) -> BallCandidateV0:
    """Locate orange area in decoded RGB pixels; only valid for this demo scene.

    Thresholds chosen for the synthetic ball in the known video. The method
    must FAIL rather than invent coordinates when the orange region is absent
    or no longer ball-shaped.
    """
    if frame_rgb.width <= 0 or frame_rgb.height <= 0 or frame_rgb.width * frame_rgb.height > 20_000_000:
        raise ValueError("invalid or too large frame")
    hue, saturation, value = frame_rgb.convert("RGB").convert("HSV").split()
    hmask = hue.point(lambda v: 255 if 0 <= v <= 35 else 0)
    smask = saturation.point(lambda v: 255 if v >= 105 else 0)
    vmask = value.point(lambda v: 255 if v >= 130 else 0)
    mask = ImageChops.multiply(ImageChops.multiply(hmask, smask), vmask)
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("orange target absent; no position candidate")
    left, top, right, bottom = bbox
    width, height = right - left, bottom - top
    pixel_count = mask.histogram()[255]
    if (
        not 12 <= width <= 120
        or not 12 <= height <= 120
        or not .75 <= width / height <= 1.33
        or not .30 <= pixel_count / (width * height) <= .95
    ):
        raise ValueError("target not unique/ball-shaped; reject candidate")
    return BallCandidateV0(
        center_x=(left + right) / 2,
        center_y=(top + bottom) / 2,
        bbox=bbox,
        orange_pixels=pixel_count,
    )


def evaluate_known_demo_frames(
    fetch_rgb_frame: Callable[[int], Image.Image],
    *, source_sha256: str, fps: float, frame_indices: tuple[int, int, int, int],
    out_dir: str | Path,
) -> dict:
    """Decode/detect first 3, seal prediction, THEN fetch the fourth image.

    fetch_rgb_frame is a provider, not an authority: no physical reality is
    proven, even if the withheld location is near the predicted location.
    """
    if source_sha256 != KNOWN_TEST_VIDEO_SHA256:
        raise ValueError("video SHA256 mismatch: this detector is for the controlled demo only")
    if fps != 30.0 or frame_indices != (0, 3, 6, 9):
        raise ValueError("unexpected frame sampling for pinned simulation")
    out = Path(out_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("use a fresh output directory")
    locations = []
    for index in frame_indices[:3]:
        observed = detect_orange_ball(fetch_rgb_frame(index))
        locations.append(observed)

    def measurement(index: int, observed: BallCandidateV0) -> PositionMeasurementV0:
        return PositionMeasurementV0(
            entity_ref="synthetic:orange-ball-01",
            source_ref=f"sha256:{source_sha256}#frame:{index}#detector:orange-hsv-demo-v0",
            frame_ref=f"synthetic-fixed-camera:sha256:{source_sha256}",
            time_s=index / fps,
            x=observed.center_x,
            y=observed.center_y,
            unit="px",
            source_kind="SIMULATED",
            uncertainty_refs=("SIMULATED_SOURCE", "COLOR_THRESHOLD_CANDIDATE",
                              "DECODER_FPS_METADATA_UNVERIFIED"),
        )

    past = tuple(measurement(i, xy) for i, xy in zip(frame_indices[:3], locations))
    forecast = predict_from_three(past, frame_indices[3] / fps)
    out.mkdir(parents=True, exist_ok=True)
    predicted_path = out / "prediction_before_frame_4.json"
    predicted_path.write_text(json.dumps(asdict(forecast), indent=2) + "\n", encoding="utf-8")

    # Critical sequencing: the fourth frame is not requested until the
    # forecast receipt exists on disk.
    future_detection = detect_orange_ball(fetch_rgb_frame(frame_indices[3]))
    future = measurement(frame_indices[3], future_detection)
    verdict = evaluate_with_heldout(forecast, future)
    manifest = {
        "schema_version": "BRODY_PINNED_SIMULATED_BALL_VIDEO_V0",
        "source_video_sha256": source_sha256,
        "source_kind": "SIMULATED",
        "frame_indices": list(frame_indices),
        "position_detector": "ORANGE_HSV_PINNED_VIDEO_ONLY",
        "observations": [asdict(sample) for sample in (*past, future)],
        "detections": [asdict(d) for d in (*locations, future_detection)],
        "forecast_precommitted_before_heldout_detection": True,
        "evaluation": verdict,
        "physics_understood": False,
        "world_knowledge_validated": False,
        "independent_detection_validation": "NOT_RUN",
        "memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "decision_authority": "KX108_ONLY",
    }
    result_path = out / "evaluation.json"
    result_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "source_kind": "SIMULATED",
        "comparison": verdict["comparison"],
        "error": verdict["error"],
        "centers_xy": [(d.center_x, d.center_y) for d in (*locations, future_detection)],
        "forecast_sealed_before_heldout": True,
        "physics_understood": False,
        "evaluation": str(result_path),
    }


def run_known_ball_video(video: str | Path, out_dir: str | Path) -> dict:
    source = Path(video).resolve(strict=True)
    if not source.is_file() or source.stat().st_size <= 0:
        raise ValueError("video must be a nonempty local file")
    source_hash = video_sha256(source)
    if source_hash != KNOWN_TEST_VIDEO_SHA256:
        raise ValueError("source video differs from the approved simulated ball fixture")
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("opencv-python needed for video decoding; no new AI model is required") from exc
    capture = cv2.VideoCapture(str(source))
    try:
        if not capture.isOpened():
            raise RuntimeError("OpenCV could not decode video")
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = choose_frame_indices(
            fps=fps, frame_count=count, start_seconds=0, interval_seconds=.1,
        )

        def fetch_rgb_frame(index: int) -> Image.Image:
            capture.set(cv2.CAP_PROP_POS_FRAMES, index)
            ok, bgr = capture.read()
            if not ok or bgr is None:
                raise RuntimeError(f"unable to decode video frame {index}")
            if bgr.shape[1] != 960 or bgr.shape[0] != 540:
                raise ValueError("unexpected video frame dimensions")
            return Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))

        return evaluate_known_demo_frames(
            fetch_rgb_frame, source_sha256=source_hash,
            fps=fps, frame_indices=frames, out_dir=out_dir,
        )
    finally:
        capture.release()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Automatic BALL position detection for exact approved synthetic Brody fixture"
    )
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    result = run_known_ball_video(args.video, args.out)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
