"""P1 independent contractual tests; full video/OpenCV chain is executed in CI."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
import json

from brody_world_physique.preverbal_prediction_v0 import PositionMeasurementV0
from brody_world_physique.multirepresentation_ball_bridge_v5 import (
    SCHEMA, candidate_episode, _selected_precommit, verify,
)


def sample(t,x,y,frame="fiducial:anchor"):
    return PositionMeasurementV0(
        entity_ref="simulated:foreground-object",
        source_ref=f"sha256:{'a'*64}#frame:{int(t*24)}#visual_candidate",
        frame_ref=frame,time_s=t,x=x,y=y,unit="px",source_kind="SIMULATED",
    )


def sample_input():
    h=[sample(0,30,30),sample(.25,40,35),sample(.5,50,40)]
    actual=sample(.75,61,45)
    prediction={"candidate_xy":[60,45],"status":"PREDICTION_CANDIDATE"}
    images={"artifact_sha256":{"last_observed.png":"b"*64,
                                "predicted_reverso_candidate.png":"c"*64,
                                "heldout_frame.png":"d"*64},
            "full_frame_pixel_mae":.75}
    return h,actual,prediction,images


class WorldRepresentationP1UnitTests(TestCase):
    def test_reuses_existing_candidate_contracts_and_four_views(self):
        out=candidate_episode(*sample_input(),"a"*64,"f"*64)
        self.assertEqual(len(out["representation_views"]),4)
        self.assertEqual(out["representation_views"]["SPATIAL"]["unit"],"px")
        self.assertEqual(out["representation_views"]["TEMPORAL"]["clock_kind"],
                         "SIMULATED_FRAME_TIME")
        self.assertEqual(out["independent_source_count"],1)
        self.assertEqual(out["comparisons"]["center_error_px"],1.0)
        self.assertEqual(out["comparisons"]["matched_linear_center_error_px"],1.0)
        self.assertFalse(out["comparisons"]["joint_representation_improvement_proven"])
        r=out["contract_refs"]
        self.assertEqual(len(r["schema_versions"]),4)
        self.assertEqual(r["memory_eligibility"],"CANDIDATE_ONLY")
        self.assertFalse(r["memory_write_allowed"])
        self.assertFalse(r["auto_promotion_allowed"])
        self.assertFalse(r["causal_proof"])
        self.assertFalse(r["canonical_world_state_instantiated"])
        self.assertEqual(r["decision_authority"],"KX108_ONLY")
        self.assertFalse(out["representation_views"]["RASTER"]["generated_is_observation"] if
                         "generated_is_observation" in out["representation_views"]["RASTER"] else False)

    def test_mixed_coordinate_frames_refused(self):
        h,t,p,v=sample_input()
        h[1]=sample(.25,40,35,frame="different-camera")
        with self.assertRaisesRegex(ValueError,"reference frames"):
            candidate_episode(h,t,p,v,"a"*64,"f"*64)

    def test_unavailable_physical_units_not_guessed(self):
        h,t,p,v=sample_input()
        from dataclasses import replace
        h[1]=replace(h[1],unit="m")
        with self.assertRaisesRegex(ValueError,"physical units"):
            candidate_episode(h,t,p,v,"a"*64,"f"*64)

    def test_future_must_follow_all_history(self):
        h,t,p,v=sample_input()
        h[2]=sample(1.,50,40)
        with self.assertRaisesRegex(ValueError,"nonmonotonic"):
            candidate_episode(h,t,p,v,"a"*64,"f"*64)

    def test_receipt_does_not_allow_future_frame_in_history(self):
        with TemporaryDirectory() as tmp:
            f=Path(tmp)/"precommits.jsonl"
            f.write_text(json.dumps({
                "clip":"test_01.mp4","camera_mode":"anchored",
                "next_frame_index":18,"proposal":{"status":"PREDICTION_CANDIDATE",
                  "candidate_xy":[42,40]},
                "history_refs":["f0","f6","sha256:abc#frame:18#bad"]
            })+"\n")
            with self.assertRaisesRegex(ValueError,"held-out"):
                _selected_precommit(f,"test_01.mp4")

    def test_missing_forecast_stays_hold_instead_of_fabricated_prediction(self):
        with TemporaryDirectory() as tmp:
            f=Path(tmp)/"receipts.jsonl"
            f.write_text(json.dumps({"clip":"test_01.mp4","camera_mode":"anchored",
                 "proposal":{"status":"HOLD_UNFAMILIAR_CHANGE","candidate_xy":None}})+"\n")
            with self.assertRaisesRegex(ValueError,"no eligible"):
                _selected_precommit(f,"test_01.mp4")

    def test_missing_evidence_prevents_fake_replay(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"evaluation.json").write_text(json.dumps({"schema":SCHEMA}))
            with self.assertRaises(Exception):
                verify(root/"missing.json",root/"missing.jsonl",root/"preview",root)
