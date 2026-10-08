"""Cold start, episode-only learning, no future leakage or physics truths."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from brody_world_physique.preverbal_prediction_v0 import PositionMeasurementV0
from brody_world_physique.experiential_video_v0 import (
    ExperienceV0, signature_from_three, acquire_experiences,
    propose_from_experiences, run_suite, _load_suite,
)


class ExperientialLearningTests(TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def samples(self, hashcode, count=6, *, speed=2, y0=10, phase=0):
        return [
            PositionMeasurementV0(
                entity_ref="synthetic:moving-marker",
                source_ref=f"sha256:{hashcode}#frame:{i*6}",
                frame_ref="fixed-camera:sha256:"+hashcode,
                time_s=i*0.25,
                x=float(15+i*speed), y=float(y0+phase*i+i*i),
                source_kind="SIMULATED", unit="px",
            ) for i in range(count)
        ]

    def test_empty_memory_cannot_claim_a_prediction(self):
        samples=self.samples("a"*64)
        result=propose_from_experiences([],samples[:3])
        self.assertEqual(result["status"],"HOLD_NO_EXPERIENCE")
        self.assertIsNone(result["candidate_xy"])

    def test_train_on_own_observed_transitions_then_propose_for_new_source(self):
        train=self.samples("a"*64,count=8)
        memory=acquire_experiences(train,"a"*64)
        self.assertEqual(len(memory),5)
        self.assertTrue(all(x.source_sha256=="a"*64 for x in memory))
        test=self.samples("b"*64,count=8,y0=150)
        proposed=propose_from_experiences(memory,test[:3])
        self.assertEqual(proposed["status"],"PREDICTION_CANDIDATE")
        self.assertTrue(all("sha256:"+"a"*64 in r for r in proposed["reused_source_refs"]))
        self.assertEqual(proposed["physical_law_known"],False)
        self.assertFalse(proposed["knowledge_validated"])

    def test_new_out_of_distribution_route_must_hold(self):
        train=self.samples("a"*64,count=8)
        memory=acquire_experiences(train,"a"*64)
        stranger=self.samples("b"*64,count=8,speed=85)
        result=propose_from_experiences(memory,stranger[:3])
        self.assertEqual(result["status"],"HOLD_UNFAMILIAR_CHANGE")

    def test_invalid_samples_do_not_become_learning(self):
        samples=self.samples("a"*64,count=3)
        with self.assertRaisesRegex(ValueError,"too short"):
            acquire_experiences(samples,"a"*64)
        other=list(self.samples("a"*64))
        other[2]=PositionMeasurementV0(
            entity_ref="different-object",source_ref="invalid",frame_ref="f",
            time_s=.5,x=10,y=20,unit="px",source_kind="SIMULATED",
        )
        with self.assertRaisesRegex(ValueError,"incompatible"):
            signature_from_three(other[:3])

    def test_source_disjointness_and_simulated_manifest_mandatory(self):
        folder=self.root/"suite";folder.mkdir()
        (folder/"one.mp4").write_bytes(b"not a video but only manifest validation")
        digest="1"*64
        manifest={"schema_version":"BRODY_SELF_SUPERVISED_VIDEO_SUITE_V1",
                  "source_kind":"SIMULATED",
                  "train":[{"file":"one.mp4","sha256":digest,"split":"TRAIN","source_kind":"SIMULATED"}],
                  "test":[{"file":"one.mp4","sha256":digest,"split":"TEST","source_kind":"SIMULATED"}]}
        source=folder/"suite.json";source.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,"overlap"):
            _load_suite(source)
        manifest["test"][0]["file"]="../other.mp4"
        source.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            _load_suite(source)
        manifest["test"][0]["file"]="two.mp4"
        (folder/"two.mp4").write_bytes(b"still not actually a video")
        manifest["test"][0]["sha256"]="2"*64
        manifest["test"][0]["source_kind"]="OBSERVED_CLAIM"
        source.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,"contradiction"):
            _load_suite(source)

    def test_holdout_prediction_precommitted_and_test_never_enters_memory(self):
        folder=self.root/"suite";folder.mkdir()
        for filename in ("train_01.mp4","test_01.mp4"):
            (folder/filename).write_bytes(b"mock; no model/data provider")
        a,b="a"*64,"b"*64
        manifest={"schema_version":"BRODY_SELF_SUPERVISED_VIDEO_SUITE_V1",
                  "source_kind":"SIMULATED",
                  "train":[{"file":"train_01.mp4","sha256":a,"split":"TRAIN","source_kind":"SIMULATED"}],
                  "test":[{"file":"test_01.mp4","sha256":b,"split":"TEST","source_kind":"SIMULATED"}]}
        (folder/"suite.json").write_text(json.dumps(manifest))
        output=self.root/"out"
        observed=[]
        def fake_frames(path,digest):
            if digest==a:
                yield from self.samples(a,count=12)
            else:
                for i,sample in enumerate(self.samples(b,count=12,y0=150)):
                    if i==3:
                        predictions=(output/"predictions_before_heldout.jsonl").read_text().splitlines()
                        self.assertGreaterEqual(len(predictions),1)
                        first=json.loads(predictions[0])
                        self.assertEqual(first["history_refs"][-1],
                                         "sha256:"+b+"#frame:12")
                    observed.append(i)
                    yield sample
        with patch("brody_world_physique.experiential_video_v0._video_points",
                   side_effect=lambda video,digest: fake_frames(video,digest)):
            result=run_suite(folder/"suite.json",output)
        self.assertEqual(result["cold_start"],"HOLD_NO_EXPERIENCE")
        self.assertEqual(result["training_candidate_transitions"],9)
        self.assertEqual(result["test_predictions"],9)
        self.assertEqual(result["test_holds_unknown"],0)
        self.assertEqual(observed,list(range(12)))
        report=json.loads((output/"evaluation.json").read_text())
        self.assertFalse(report["physics_understood"])
        self.assertFalse(report["world_knowledge_validated"])
        self.assertEqual(report["test_memory_mutations"],0)
        acquired=json.loads((output/"learning_candidates.json").read_text())
        self.assertEqual(len(acquired["experiences"]),9)
        self.assertTrue(all(x["source_sha256"]==a for x in acquired["experiences"]))

    def test_cannot_reuse_output_over_previous_experiment(self):
        self.assertEqual(propose_from_experiences([],self.samples("a"*64)[:3])["status"],
                         "HOLD_NO_EXPERIENCE")
