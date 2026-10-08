"""Contract tests: experience captures REAL code provenance and replayable acts.

No imported memory may run Python code, create canonical knowledge or ACT.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
import json

from PIL import Image, ImageDraw

from brody_world_physique.drawing_school_v1 import run_school
from brody_world_physique.experience_memory_v1 import (
    SCHEMA, checked_gesture, code_fingerprint, digest_bytes, stable_bytes,
    verify_episode, verify_memory_bundle, verify_recipe,
)


class ExperienceContractTests(TestCase):
    def setUp(self):
        self.temp=TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/"new-school"
        self.result=run_school(self.root)
        self.index=json.loads((self.root/"experience_memory_index_v1.json").read_text())

    def _read_episode(self, name):
        loc=self.root/"experience_episodes_v1"/(name+".json")
        return loc,json.loads(loc.read_text(encoding="utf-8"))

    def _modify_record_and_rehash(self, name, edit):
        """Simulate a sophisticated local forger who changes episode & index."""
        loc,record=self._read_episode(name)
        edit(record)
        loc.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        entry=next(e for e in self.index["episodes"] if e["episode_id"]==name)
        entry["sha256"]=digest_bytes(loc.read_bytes())
        return entry

    def test_full_procedural_memory_trace_can_be_replayed_offline(self):
        report=verify_memory_bundle(self.root)
        self.assertEqual(report["status"],"PASS_LOCAL_REPLAY_ONLY")
        self.assertEqual(report["episodes"],10)
        self.assertTrue(report["memory_skill_selection_replayed"])
        self.assertTrue(report["code_identity_verified"])
        self.assertTrue(report["all_generated_artifacts_replayed"])
        self.assertFalse(report["world_knowledge_validated"])
        self.assertEqual(self.result["procedural_episodes"],10)
        self.assertGreater(report["candidate_ledger_records_verified"],25)
        p,data=self._read_episode("examen_triangle")
        self.assertEqual(data["schema_version"],SCHEMA)
        self.assertEqual(data["observation"]["source_kind"] if "source_kind" in data["observation"] else data["source_kind"],"SIMULATED")
        self.assertFalse(data["interpretation"]["semantic_shape_understood"])
        self.assertEqual(data["choice"]["selection_author"],"DETERMINISTIC_PIXEL_SCORE_ALGORITHM")
        self.assertIn("ADD",data["choice"]["available_actions"])
        self.assertFalse(data["procedure_ref"]["arbitrary_code_execution_allowed"])
        self.assertGreater(len(data["execution_trace"]["operations"]),0)
        self.assertEqual(data["retained_skill"]["status"],"CANDIDATE_ONLY")
        self.assertFalse(data["memory_boundary"]["memory_write_allowed"])
        self.assertEqual(data["memory_boundary"]["decision_authority"],"KX108_ONLY")
        self.assertEqual(data["procedure_ref"]["executed_capabilities"][1],
                         code_fingerprint("pixel-feedback-revision"))

    def test_harmful_memory_is_preserved_as_rejected_path(self):
        _,episode=self._read_episode("examen_croix")
        self.assertEqual(episode["choice"]["recall_gate"],"REJECTED_HARMFUL")
        self.assertTrue(any(x["kind"]=="NEGATIVE_SKILL_TRANSFER"
                            for x in episode["rejected_paths"]))
        self.assertGreater(episode["evaluation"]["raw_recall_error_px"],
                           episode["evaluation"]["blank_page_error_px"])
        self.assertLess(episode["evaluation"]["final_error_px"],
                        episode["evaluation"]["blank_page_error_px"])
        self.assertIsNotNone(episode["choice"]["memory_source_ref"])

    def test_changed_teacher_input_is_detected(self):
        file=self.root/"teacher_images"/"examen_cercle.png"
        original=file.read_bytes()
        with Image.open(file) as opened:
            altered=opened.copy()
        ImageDraw.Draw(altered).line(((0,0),(63,63)),fill=0,width=1)
        altered.save(file)
        with self.assertRaisesRegex(ValueError,"source image changed"):
            verify_memory_bundle(self.root)
        file.write_bytes(original)
        self.assertEqual(verify_memory_bundle(self.root)["episodes"],10)

    def test_changed_generated_artifact_is_detected(self):
        file=self.root/"attempts"/"examen_triangle_apres_correction.png"
        original=file.read_bytes()
        file.write_bytes(original+b"untrusted-extra-payload")
        with self.assertRaisesRegex(ValueError,"generated artifact was modified"):
            verify_memory_bundle(self.root)

    def test_modified_procedure_ref_fails_even_with_updated_receipt_sha(self):
        entry=self._modify_record_and_rehash(
            "examen_triangle",
            lambda e:e["procedure_ref"]["executed_capabilities"][1].update(
                {"code_sha256":"0"*64},
            ),
        )
        with self.assertRaisesRegex(ValueError,"procedure code identity changed"):
            verify_episode(self.root,entry)

    def test_altered_executed_edit_fails_even_with_updated_receipt_sha(self):
        def modification(obj):
            obj["execution_trace"]["operations"][0]["error_after"]=77777
        entry=self._modify_record_and_rehash("examen_triangle",modification)
        with self.assertRaisesRegex(ValueError,"recipe score does not replay"):
            verify_episode(self.root,entry)

    def test_unreviewed_promotion_or_action_is_not_accepted(self):
        entry=self._modify_record_and_rehash(
            "examen_croix",
            lambda e:e["memory_boundary"].update({"memory_write_allowed":True,
                                                    "emits_act":True}),
        )
        with self.assertRaisesRegex(ValueError,"authority escalation"):
            verify_episode(self.root,entry)
        with self.assertRaisesRegex(ValueError,"unsafe gesture kind"):
            checked_gesture({"kind":"__import__('os').system('whoami')",
                             "points":[[0,0],[1,1]]})

    def test_no_code_from_memory_and_replay_checks_bounds(self):
        with self.assertRaisesRegex(ValueError,"unknown capability"):
            code_fingerprint("malicious-module-from-memory")
        model=Image.new("L",(64,64),255)
        ImageDraw.Draw(model).line(((3,3),(40,3)),fill=0,width=3)
        trace=[{"revision":1,"action":"ERASE","target_index":999,
                "choice_rule":"MIN_PIXEL_XOR_STRICT_IMPROVEMENT_FIRST_TIE",
                "error_before":0}]
        with self.assertRaises(ValueError):
            verify_recipe(model,[],trace,rejected_memory=False,
                          expected_raw_error=len([p for p in model.tobytes() if p<128]),
                          expected_blank_error=len([p for p in model.tobytes() if p<128]),
                          expected_final_error=0)
