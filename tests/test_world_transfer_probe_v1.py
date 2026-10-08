"""Pure contract checks for generalized synthetic visual-transfer experiments.

The real OpenCV video decode/generation integration runs separately in CI.
"""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from brody_world_physique.experiential_video_v0 import ExperienceV0
from brody_world_physique.preverbal_prediction_v0 import PositionMeasurementV0
from brody_world_physique.world_transfer_probe_v1 import (
    _load_probe_suite, propose_with_conflict_gate,
)


def measurement(t, x, y):
    return PositionMeasurementV0(
        entity_ref="simulated:foreground-object",source_ref=f"fixture:frame:{t}",
        frame_ref="scene-fiducial:fixture:anchored",time_s=float(t),
        x=float(x),y=float(y),unit="px",source_kind="SIMULATED",
    )


def experience(source, dx, dy):
    return ExperienceV0(
        signature=(9.,3.,9.,3.),
        outcome_displacement=(dx,dy),
        source_sha256=source,
        prior_refs=("a","b","c"), future_ref="next:"+source,
    )


class TransferProbesContractsTests(TestCase):
    def test_conflicting_futures_same_history_lead_to_hold(self):
        hist=[measurement(t,20+9*t,40+3*t) for t in range(3)]
        learned=(experience("a"*64,9.,34.),experience("b"*64,9.,-34.))
        result=propose_with_conflict_gate(learned,hist)
        self.assertEqual(result["status"],"HOLD_CONFLICTING_EXPERIENCES")
        self.assertIsNone(result["candidate_xy"])
        self.assertEqual(result["evidence_source_count"],2)
        self.assertFalse(result["physical_law_proven"])

    def test_reusable_single_experience_remains_unproven_candidate(self):
        hist=[measurement(t,20+9*t,40+3*t) for t in range(3)]
        learned=(experience("a"*64,9.,3.),)
        result=propose_with_conflict_gate(learned,hist)
        self.assertEqual(result["status"],"PREDICTION_CANDIDATE")
        self.assertFalse(result["physical_law_proven"])
        self.assertFalse(result["knowledge_validated"])

    def test_novel_history_abstains(self):
        hist=[measurement(t,20+60*t,40+10*t) for t in range(3)]
        result=propose_with_conflict_gate((experience("a"*64,9.,3.),),hist)
        self.assertEqual(result["status"],"HOLD_UNFAMILIAR_CHANGE")
        self.assertIsNone(result["candidate_xy"])

    def test_train_test_hash_overlap_rejected(self):
        with TemporaryDirectory() as temp:
            base=Path(temp)
            for name in ("tr.mp4","te.mp4"):
                (base/name).write_bytes(b"not a video")
            shared="a"*64
            manifest={
                "schema_version":"BRODY_TRANSFER_PROBE_V1",
                "source_kind":"SIMULATED",
                "train":[{"file":"tr.mp4","sha256":shared,
                          "split":"TRAIN","source_kind":"SIMULATED"}],
                "test":[{"file":"te.mp4","sha256":shared,
                         "split":"TEST","source_kind":"SIMULATED"}],
            }
            p=base/"suite.json"
            p.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,"duplicate"):
                _load_probe_suite(p)
            manifest["test"][0]["sha256"]="b"*64
            manifest["test"][0]["file"]="../escape.mp4"
            p.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                _load_probe_suite(p)

    def test_denies_unproven_real_source_in_simulated_benchmark(self):
        with TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"a.mp4").write_bytes(b"fake")
            (root/"b.mp4").write_bytes(b"fake")
            manifest={
                "schema_version":"BRODY_TRANSFER_PROBE_V1",
                "source_kind":"OBSERVED_CLAIM",
                "train":[{"file":"a.mp4","sha256":"a"*64,
                          "split":"TRAIN","source_kind":"SIMULATED"}],
                "test":[{"file":"b.mp4","sha256":"b"*64,
                         "split":"TEST","source_kind":"SIMULATED"}],
            }
            f=root/"suite.json"
            f.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,"manifest"):
                _load_probe_suite(f)
