"""Synthetic-only reproducible bench for preverbal temporal prediction.

Not an observation of the physical world. Real tests require independent,
source-tagged position measurements from an actual video/camera or sensor.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from brody_world_physique.preverbal_prediction_v0 import (
    PositionMeasurementV0, evaluate_four_measurements
)


def demo(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    # A moving colored marker in a SYNTHETIC XY coordinate space.
    # The model does not learn why it moves (e.g. gravity), just a curve.
    samples = [
        PositionMeasurementV0(
            entity_ref="toy:marker-01",
            source_ref=f"synthetic:frame:{t}",
            frame_ref="synthetic-camera-unchanged",
            time_s=float(t),
            x=float(6 + 4 * t),
            y=float(3 + t*t),
            unit="px",
            source_kind="SIMULATED",
        )
        for t in (0, 1, 2, 3)
    ]
    (out / "source_measurements.json").write_text(
        json.dumps({"measurements": [asdict(x) for x in samples],
                    "fixture": "SYNTHETIC_NOT_REAL_WORLD"}, indent=2) + "\n",
        encoding="utf-8",
    )
    result = evaluate_four_measurements(samples)
    (out / "heldout_evaluation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if result["comparison"] != "BETTER_THAN_LINEAR_BASELINE":
        raise AssertionError("synthetic kinematic benchmark unexpectedly failed")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("build/preverbal-world-demo"))
    args = parser.parse_args()
    result = demo(args.out)
    print("source_kind=SIMULATED")
    print("comparison=" + result["comparison"])
    print("error_proposed=" + str(result["error"]["proposed"]))
    print("physics_understood=False")
    print("output=" + str(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
