"""Annotate four REAL VIDEO frames for the existing preverbal prediction test.

This is NOT automatic object tracking, Jarvis camera integration, semantic
vision, or evidence of learned physics. Human clicks provide candidate
positions. Three annotations are sent to the predictor and a prediction
receipt is written BEFORE the fourth frame is displayed to the annotator.

OpenCV is imported only inside the UI entrypoint: no new model installed.
Video hashes stay local, no upload, no canonical memory writes.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
from typing import Any, Iterable

from .preverbal_prediction_v0 import (
    SOURCE_KINDS, PositionMeasurementV0, evaluate_with_heldout, predict_from_three,
)


def video_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def choose_frame_indices(
    *, fps: float, frame_count: int, start_seconds: float, interval_seconds: float
) -> tuple[int, int, int, int]:
    """Select four ascending positions on one video timeline, not four cameras."""
    if (
        not all(isinstance(n, (int, float)) and not isinstance(n, bool) and isfinite(n)
                for n in (fps, start_seconds, interval_seconds))
        or not isinstance(frame_count, int)
        or isinstance(frame_count, bool)
        or fps <= 0 or fps > 1000 or frame_count < 4
        or start_seconds < 0 or interval_seconds <= 0
    ):
        raise ValueError("invalid FPS, frame count, start or interval")
    start = round(fps * start_seconds)
    step = round(fps * interval_seconds)
    if step < 1:
        raise ValueError("sampling interval too short for video FPS")
    chosen = tuple(int(start + i * step) for i in range(4))
    if chosen[-1] >= frame_count:
        raise ValueError("not enough video frames: reduce start or interval")
    return chosen  # type: ignore[return-value]


def make_measurements(
    indices: tuple[int, int, int, int] | tuple[int, int, int],
    points: Iterable[tuple[float, float]],
    *, fps: float, video_hash: str, entity_ref: str, source_kind: str
) -> tuple[PositionMeasurementV0, ...]:
    """Create candidate observations from a user's manual clicks.

    These are image-plane pixel coordinates, not meters or GPS coordinates.
    Camera motion, annotation accuracy and physical causality remain unknown.
    """
    coords = tuple(points)
    if len(coords) != len(indices) or len(indices) not in (3, 4):
        raise ValueError("need exactly one point per selected frame")
    if not isinstance(fps, (float, int)) or not isfinite(fps) or fps <= 0:
        raise ValueError("FPS must be valid")
    if len(video_hash) != 64 or any(c not in "0123456789abcdef" for c in video_hash):
        raise ValueError("valid SHA256 of source video required")
    if not entity_ref or not entity_ref.strip():
        raise ValueError("entity_ref is required")
    if source_kind not in SOURCE_KINDS:
        raise ValueError("source_kind must be explicitly classified")
    if tuple(indices) != tuple(sorted(set(indices))):
        raise ValueError("frame indices must be distinct and increasing")
    samples = []
    for idx, point in zip(indices, coords):
        if not isinstance(idx, int) or idx < 0 or len(point) != 2:
            raise ValueError("invalid frame index or selected point")
        x, y = point
        if not all(isinstance(v, (float, int)) and not isinstance(v, bool) and isfinite(v) and v >= 0
                   for v in (x, y)):
            raise ValueError("coordinates must be finite image pixel positions")
        samples.append(PositionMeasurementV0(
            entity_ref=entity_ref,
            source_ref=f"sha256:{video_hash}#frame:{idx}#annotation:human",
            frame_ref=f"camera-image-plane:sha256:{video_hash}",
            time_s=idx / fps,
            x=float(x), y=float(y), unit="px",
            source_kind=source_kind,
            uncertainty_refs=("MANUAL_POINT_APPROXIMATE", "VIDEO_FPS_METADATA_UNVERIFIED",
                              "CAMERA_MOTION_UNVERIFIED", "OBJECT_IDENTITY_USER_ASSERTED"),
        ))
    return tuple(samples)


def _annotate_frame(cv2: Any, capture: Any, frame_index: int,
                    window_name: str, prompt: str) -> tuple[float, float]:
    """Manual image-coordinate annotation, preview and explicit confirmation.

    WINDOW_AUTOSIZE preserves the image's native pixel grid; a freely
    resized window can lead to ambiguous mouse-image coordinate transforms.
    A click is not final until the user presses Enter/Space.
    """
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = capture.read()
    if not ok or frame is None:
        raise RuntimeError(f"cannot decode frame {frame_index}")
    height, width = frame.shape[:2]
    selected: dict[str, tuple[float, float]] = {}

    def mouse(event: int, x: int, y: int, flags: int, param: Any) -> None:
        if event == cv2.EVENT_LBUTTONDOWN and 0 <= x < width and 0 <= y < height:
            selected["xy"] = (float(x), float(y))

    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(window_name, mouse)
    try:
        while True:
            canvas = frame.copy()
            cv2.putText(
                canvas, prompt[:92], (15, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 2, cv2.LINE_AA,
            )
            if "xy" in selected:
                x, y = (int(q) for q in selected["xy"])
                cv2.drawMarker(canvas, (x, y), (0, 255, 255),
                               markerType=cv2.MARKER_CROSS, markerSize=24,
                               thickness=2)
                cv2.putText(canvas, f"Click: x={x} y={y} | Enter=OK R=redo",
                            (15, height - 18), cv2.FONT_HERSHEY_SIMPLEX,
                            0.55, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow(window_name, canvas)
            key = cv2.waitKey(25) & 0xFF
            if key == 27:
                raise RuntimeError("user cancelled annotation with Escape")
            if key in (ord("r"), ord("R")):
                selected.clear()
            if key in (13, 10, 32) and "xy" in selected:
                point = selected["xy"]
                print(f"FRAME {frame_index}: confirmed pixel position x={point[0]:.0f}, y={point[1]:.0f}")
                return point
    finally:
        cv2.destroyWindow(window_name)


def annotate_video(
    video: str | Path, out_dir: str | Path, *,
    start_seconds: float = 0,
    interval_seconds: float = 0.2,
    entity_ref: str = "user-selected-object-01",
    source_kind: str,
) -> dict[str, Any]:
    """Manual experiment; no model weights, automatic segmentation, or cloud."""
    try:
        import cv2  # Reuse Jarvis' OpenCV when available
    except ImportError as exc:
        raise RuntimeError(
            "cv2 not available in this Python environment; check your existing "
            "Jarvis OpenCV interpreter first, no new vision model needed"
        ) from exc

    source = Path(video).resolve(strict=True)
    destination = Path(out_dir).resolve()
    if not source.is_file() or source.stat().st_size == 0:
        raise ValueError("video must be a nonempty local file")
    if destination == source or destination == source.parent:
        raise ValueError("output directory must not overwrite source video")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("use an empty/new output directory")
    source_hash = video_sha256(source)
    capture = cv2.VideoCapture(str(source))
    try:
        if not capture.isOpened():
            raise RuntimeError("cannot decode video via existing OpenCV runtime")
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        selected = choose_frame_indices(
            fps=fps, frame_count=frame_count,
            start_seconds=start_seconds, interval_seconds=interval_seconds,
        )
        # PRECOMMIT: the fourth video frame is not even loaded for annotation
        # until after the forecast has been calculated AND saved.
        points = [
            _annotate_frame(cv2, capture, index, "Brody video observation",
                            f"Frame {j+1}/4: click SAME object's center; Esc cancels")
            for j, index in enumerate(selected[:3])
        ]
        history = make_measurements(
            selected[:3], points, fps=fps, video_hash=source_hash,
            entity_ref=entity_ref, source_kind=source_kind
        )
        forecast = predict_from_three(history, selected[3] / fps)
        destination.mkdir(parents=True, exist_ok=True)
        prediction_path = destination / "prediction_before_frame_4.json"
        prediction_path.write_text(
            json.dumps(asdict(forecast), indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
        )
        print("Prediction sealed before fourth annotation:", prediction_path)
        heldout_xy = _annotate_frame(
            cv2, capture, selected[3], "Brody video observation",
            "Frame 4/4: click SAME object's center; Esc cancels"
        )
        all_samples = make_measurements(
            selected, points + [heldout_xy], fps=fps,
            video_hash=source_hash, entity_ref=entity_ref, source_kind=source_kind
        )
        evaluation = evaluate_with_heldout(forecast, all_samples[-1])
        metadata = {
            "schema_version": "BRODY_MANUAL_VIDEO_ANNOTATION_V0",
            "source_video_sha256": source_hash,
            "source_kind_declared_by_user": source_kind,
            "source_kind_independently_verified": False,
            "source_video_bytes": source.stat().st_size,
            "fps_from_decoder_unverified": fps,
            "frame_indices": selected,
            "observation_method": "FOUR_MANUAL_IMAGE_PLANE_CLICKS",
            "prediction_precommitted_before_fourth_annotation": True,
            "camera_motion_external_check": "NOT_RUN",
            "object_identity_independent_check": "NOT_RUN",
            "real_world_proven": False,
            "physical_law_proven": False,
            "model_weight_update": False,
            "memory_write_allowed": False,
            "decision_authority": "KX108_ONLY",
        }
        observations_path = destination / "source_measurements.json"
        observations_path.write_text(
            json.dumps({"measurements": [asdict(x) for x in all_samples],
                        "metadata": metadata}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        evaluation_path = destination / "heldout_evaluation.json"
        evaluation_path.write_text(
            json.dumps({"metadata": metadata, "evaluation": evaluation}, indent=2,
                       ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return {"comparison": evaluation["comparison"], "error": evaluation["error"],
                "prediction": str(prediction_path), "measurements": str(observations_path),
                "evaluation": str(evaluation_path),
                "physics_understood": False, "world_knowledge_validated": False}
    finally:
        capture.release()
        cv2.destroyAllWindows()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Brody real-video candidate: mark 3 object positions, precommit forecast, mark 4th"
    )
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--start-seconds", type=float, default=0)
    parser.add_argument("--interval-seconds", type=float, default=0.2)
    parser.add_argument("--entity-ref", default="user-selected-object-01")
    parser.add_argument("--source-kind", choices=sorted(SOURCE_KINDS), required=True,
                        help="Required provenance declaration; SIMULATED for our test video")
    args = parser.parse_args(argv)
    result = annotate_video(
        args.video, args.out, start_seconds=args.start_seconds,
        interval_seconds=args.interval_seconds, entity_ref=args.entity_ref,
        source_kind=args.source_kind,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
