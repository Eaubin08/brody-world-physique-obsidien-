"""Contract tests for conservative P2 baseline diagnostic."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from brody_world_physique import p2_ablation_diagnostic_v0 as p2
from brody_world_physique.preverbal_prediction_v0 import PositionMeasurementV0


class P2DiagnosticTest(unittest.TestCase):
    def test_precommit_baselines_and_future_leak_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            suite=root/"suite.json"
            suite.write_text('{"source":"SIMULATED"}',encoding="utf-8")
            video=root/"test_01.mp4"
            video.write_bytes(b"synthetic")
            digest=p2._hash(video)
            def point(idx, x):
                return PositionMeasurementV0(
                    entity_ref="simulated:foreground-object",
                    source_ref=f"sha256:{digest}#frame:{idx}#visual_candidate",
                    frame_ref=f"scene-fiducial:{digest}:anchored",
                    time_s=idx/24,x=x,y=20.0,unit="px",
                    source_kind="SIMULATED",uncertainty_refs=("SIMULATED",))
            samples=[point(0,0),point(6,6),point(12,12),point(18,18)]
            receipts=root/"receipts.jsonl"
            row={"clip":"test_01.mp4","camera_mode":"anchored",
                 "history_refs":[p.source_ref for p in samples[:3]],
                 "next_frame_index":18,
                 "proposal":{"status":"PREDICTION_CANDIDATE",
                             "candidate_xy":[18.0,20.0]}}
            receipts.write_text(json.dumps(row)+"\n",encoding="utf-8")
            with patch.object(p2,"_load_probe_suite",return_value=([],[("test_01.mp4",video,digest)])), patch.object(p2,"iter_video_points",return_value=iter(samples)):
                report=p2.evaluate(suite,receipts)
                self.assertEqual(report["p2_verdict"],"P2_INCONCLUSIVE")
                self.assertEqual(report["summary"]["A1_linear_kinematics"]["mean_error_px"],0)
                self.assertFalse(report["ablation_gain_proven"])
                row["history_refs"][-1]=samples[-1].source_ref
                receipts.write_text(json.dumps(row)+"\n",encoding="utf-8")
                with self.assertRaises(ValueError):
                    p2.evaluate(suite,receipts)

    def test_reject_nonfinite_forecast(self):
        self.assertFalse(p2._finite_xy([float("nan"),4]))
        self.assertFalse(p2._finite_xy([True,4]))
        self.assertTrue(p2._finite_xy([1.0,4.0]))


if __name__=="__main__":
    unittest.main()
