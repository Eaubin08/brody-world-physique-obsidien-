"""No semantic VLM or new physical law: measurement-only prediction tests."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase

from brody_world_physique.preverbal_prediction_v0 import (
    PositionMeasurementV0, evaluate_four_measurements,
    evaluate_with_heldout, measurement_from_mmonde_world_observation,
    predict_from_three, main,
)


class PreverbalPredictionTests(TestCase):
    def make(self, t, x, y, *, frame="camera-fixed-px", unit="px",
             source_kind="SIMULATED", entity="toy-object", ref=None):
        return PositionMeasurementV0(
            entity_ref=entity, source_ref=ref or f"frame:{t}",
            frame_ref=frame, time_s=t, x=x, y=y,
            unit=unit, source_kind=source_kind,
        )

    def test_separate_predict_and_measure_with_heldout(self):
        # Analytic synthetic sequence: x(t)=2t, y(t)=t².
        samples = [self.make(t, 2*t, t*t) for t in range(4)]
        prediction = predict_from_three(samples[:3], 3)
        self.assertEqual(prediction.candidate_xy, (6., 9.))
        self.assertEqual(prediction.linear_baseline_xy, (6., 7.))
        self.assertFalse(prediction.physical_law_proven)
        self.assertFalse(prediction.source_kind_verified_real)
        result = evaluate_with_heldout(prediction, samples[3])
        self.assertEqual(result["error"]["proposed"], 0)
        self.assertEqual(result["comparison"], "BETTER_THAN_LINEAR_BASELINE")
        self.assertEqual(result["physics_causality"], "UNKNOWN")
        self.assertFalse(result["world_knowledge_validated"])
        self.assertFalse(result["memory_write_allowed"])
        self.assertFalse(result["model_weight_update"])

    def test_heldout_does_not_leak_into_prediction(self):
        history = [self.make(t, 2*t, t*t) for t in range(3)]
        predicted = predict_from_three(history, 3)
        miss = evaluate_with_heldout(predicted, self.make(3, 200, 200))
        hit = evaluate_with_heldout(predicted, self.make(3, 6, 9))
        self.assertEqual(predicted.candidate_xy, (6., 9.))
        self.assertGreater(miss["error"]["proposed"], hit["error"]["proposed"])

    def test_constant_speed_ties_linear_not_claiming_breakthrough(self):
        seq = [self.make(t, 5*t, 10*t) for t in range(4)]
        result = evaluate_four_measurements(seq)
        self.assertEqual(result["comparison"], "TIED_WITH_LINEAR_BASELINE")
        self.assertEqual(result["error"]["proposed"], 0.0)
        self.assertEqual(result["epistemic_status"], "ONE_EPISODE_CANDIDATE_ONLY")

    def test_observed_claim_does_not_automatically_make_reality_proven(self):
        seq = [self.make(t, 2*t, t*t, source_kind="OBSERVED_CLAIM") for t in range(4)]
        result = evaluate_four_measurements(seq)
        self.assertFalse(result["real_world_proven"])
        self.assertFalse(result["prediction"]["source_kind_verified_real"])

    def test_generated_stays_generated(self):
        seq = [self.make(t, 2*t, t*t, source_kind="GENERATED") for t in range(4)]
        result = evaluate_four_measurements(seq)
        self.assertEqual(result["prediction"]["source_kind"], "GENERATED")
        self.assertFalse(result["real_world_proven"])

    def test_no_mixing_frames_units_entities_or_origins(self):
        seq = [self.make(t, t, t) for t in range(4)]
        for changed in [
            self.make(3, 3, 3, frame="camera-moving"),
            self.make(3, 3, 3, unit="m"),
            self.make(3, 3, 3, entity="another"),
            self.make(3, 3, 3, source_kind="OBSERVED_CLAIM"),
        ]:
            with self.assertRaisesRegex(ValueError, "spatial frame"):
                evaluate_four_measurements(seq[:3] + [changed])

    def test_invalid_timing_or_reused_source_rejected(self):
        seq = [self.make(t, t, t) for t in range(4)]
        with self.assertRaisesRegex(ValueError, "timestamps"):
            evaluate_four_measurements(seq[:3]+[self.make(2, 3, 3)])
        with self.assertRaisesRegex(ValueError, "prediction target"):
            predict_from_three(seq[:3], 2)
        pred = predict_from_three(seq[:3], 3)
        with self.assertRaisesRegex(ValueError, "distinct source"):
            evaluate_with_heldout(pred, self.make(3, 3, 3, ref="frame:0"))
        with self.assertRaisesRegex(ValueError, "timestamp"):
            evaluate_with_heldout(pred, self.make(4, 4, 4))

    def test_refuse_nonfinite_or_unknown_frame(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            self.make(0, float("nan"), 0)
        with self.assertRaisesRegex(ValueError, "finite"):
            self.make(0, float("inf"), 0)
        with self.assertRaisesRegex(ValueError, "spatial"):
            self.make(0, 0, 0, frame="UNKNOWN")
        with self.assertRaisesRegex(ValueError, "source_kind"):
            self.make(0, 0, 0, source_kind="REAL_PROVEN")

    def test_irregular_times_supported_and_not_assumed_equal(self):
        # p(t)=t², use irregular samples and forecast.
        seq=[self.make(t, t*t, 2*t*t) for t in (0,1,3,6)]
        result=evaluate_four_measurements(seq)
        self.assertAlmostEqual(result["error"]["proposed"], 0)
        self.assertGreater(result["error"]["linear_baseline"], 0)

    def test_mmonde_structural_bridge_requires_real_source_and_frame(self):
        row = SimpleNamespace(
            observation_id="obs:1", observed_at="2026-10-08T10:00:00+00:00",
            entity_ref="obj:1",
            source_refs=("camera-raw:frame:1",),
            space={"frame_ref": "camera-0"},
            state={"position":{"x":10,"y":20,"unit":"px"}},
            uncertainty=("DEPTH_UNKNOWN",),readonly=True,
            decision_authority="KX108_ONLY",
        )
        point = measurement_from_mmonde_world_observation(row)
        self.assertEqual(point.source_kind, "OBSERVED_CLAIM")
        self.assertEqual(point.uncertainty_refs, ("DEPTH_UNKNOWN",))
        self.assertEqual(point.x, 10)
        row.source_refs=()
        with self.assertRaisesRegex(ValueError, "source references"):
            measurement_from_mmonde_world_observation(row)
        row.source_refs=("recovered",)
        row.observed_at="2026-10-08T10:00:00"
        with self.assertRaisesRegex(ValueError, "timezone"):
            measurement_from_mmonde_world_observation(row)
        row.observed_at="2026-10-08T10:00:00Z"
        row.decision_authority="FAKE_KX"
        with self.assertRaisesRegex(ValueError, "authority"):
            measurement_from_mmonde_world_observation(row)

    def test_cli_produces_bounded_receipt_no_memory(self):
        with TemporaryDirectory() as temp:
            root=Path(temp); inp=root/"four.json"; out=root/"episode.json"
            seq=[self.make(t, 2*t, t*t) for t in range(4)]
            from dataclasses import asdict
            inp.write_text(json.dumps({"measurements":[asdict(m) for m in seq]}))
            status=main(["--input",str(inp),"--out",str(out)])
            self.assertEqual(status,0)
            saved=json.loads(out.read_text())
            self.assertEqual(saved["comparison"],"BETTER_THAN_LINEAR_BASELINE")
            self.assertEqual(len(saved["experiment_input_sha256"]),64)
            self.assertFalse(saved["memory_write_allowed"])
            with self.assertRaises(SystemExit):
                main(["--input",str(inp),"--out",str(inp)])
