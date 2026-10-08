"""Image instrument selection: before-result choice and safe episodic memory."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
import json

from PIL import Image

from brody_world_physique.drawing_school_v1 import GestureV1, run_school as make_prior
from brody_world_physique.instrument_school_v2 import (
    TOOLS, _gray_pixel_loss, render_instrument, run_school,
    select_tool, verify_school,
)


class PureInstrumentContracts(TestCase):
    def test_tool_renders_are_visibly_different_and_directional(self):
        g=(GestureV1(points=((9,10),(54,43)),kind="STRAIGHT_STROKE"),)
        images=[render_instrument(g,tool) for tool in TOOLS]
        self.assertEqual(len({img.tobytes() for img in images}),3)
        self.assertTrue(all(img.size==(64,64) for img in images))
        self.assertGreater(_gray_pixel_loss(images[0],images[1]),0)

    def test_untrusted_tool_and_oversized_motor_action_fail_closed(self):
        stroke=GestureV1(((2,2),(30,30)),"STRAIGHT_STROKE")
        with self.assertRaisesRegex(ValueError,"unknown/untrusted"):
            render_instrument((stroke,),"../../unsafe.py")
        with self.assertRaisesRegex(ValueError,"beyond canvas"):
            render_instrument((GestureV1(((1,1),(67,66)),"STRAIGHT_STROKE"),),"PEN")

    def test_selector_learns_from_empirical_loss_not_coded_style_mapping(self):
        # For the same arbitrary LIGHT intent, demonstrate a contradictory
        # world where PEN wins. The selector must follow feedback, not teacher
        # fixture's actual mapping LIGHT -> PENCIL.
        training=({"id":"a","goal":"LIGHT",
                   "trial_losses":{"PENCIL":12.,"PEN":1.,"NIB":3.}},)
        proposal=select_tool(training,"LIGHT")
        self.assertEqual(proposal["chosen_tool"],"PEN")
        self.assertEqual(proposal["based_on_training_ids"],["a"])
        self.assertFalse(proposal["confidence_calibrated"])

    def test_unfamiliar_goal_refuses_to_guess(self):
        training=({"id":"a","goal":"LIGHT",
                   "trial_losses":{"PENCIL":1.,"PEN":10.,"NIB":3.}},)
        self.assertIsNone(select_tool(training,"UNSEEN_INTENT")["chosen_tool"])
        self.assertIsNone(select_tool((),"LIGHT")["chosen_tool"])
        with self.assertRaisesRegex(ValueError,"incomplete teacher"):
            select_tool(({"id":"a","goal":"LIGHT","trial_losses":{"PENCIL":0}},),"LIGHT")


class EndToEndCourse(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=TemporaryDirectory()
        cls.base=Path(cls.tmp.name)
        cls.prior=cls.base/"prior_v1"
        make_prior(cls.prior)
        cls.results={}
        for n in (0,1,9):
            cls.results[n]=run_school(
                cls.base/("tools_%02d"%n),
                prior_school=cls.prior,training_lessons=n,
            )

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_zero_one_many_experiences_and_heldout_abstention(self):
        zero,one,many=(self.results[x] for x in (0,1,9))
        self.assertEqual((zero["chosen"],zero["hold"]),(0,4))
        self.assertEqual((one["chosen"],one["hold"]),(1,3))
        self.assertEqual((many["chosen"],many["hold"]),(3,1))
        self.assertEqual([x["choice"] for x in many["choices"]],
                         ["PENCIL","PEN","NIB",None])
        self.assertTrue(all(x["choice"]==x["winner_after_holdout"]
                            for x in many["choices"] if x["choice"]))
        self.assertEqual(verify_school(self.base/"tools_09")["status"],
                         "PASS_BOUNDED_EPISODIC_TOOL_REPLAY")

    def test_precommit_has_no_future_target_and_is_frozen(self):
        root=self.base/"tools_09"
        index=json.loads((root/"instrument_experience_index.json").read_text())
        ledger=json.loads((root/"evaluation.json").read_text())
        receipts=[json.loads(r) for r in
                  (root/"choices_before_heldout.jsonl").read_text().splitlines()]
        self.assertEqual(index["training_lessons"],9)
        self.assertTrue(index["prior_school_replay_verified"])
        self.assertTrue(all(not r["target_accessed_before_decision"] for r in receipts))
        self.assertTrue(all("heldout_target_sha256" not in r for r in receipts))
        self.assertTrue(all(x["memory_mutations_from_test"]==0 for x in ledger["exams"]))
        self.assertFalse(ledger["semantic_tool_comprehension_proven"])
        self.assertFalse(ledger["real_world_generalization_proven"])

    def test_memory_and_generated_image_tamper_rejected(self):
        root=self.base/"tools_09"
        image=root/"instrument_art"/"exam_01_prediction.png"
        original=image.read_bytes()
        try:
            image.write_bytes(original+b"changed")
            with self.assertRaisesRegex(ValueError,"prediction does not match"):
                verify_school(root)
        finally:
            image.write_bytes(original)
        self.assertEqual(verify_school(root)["decisions_verified"],4)

    def test_invalid_memory_is_detected_even_if_report_stays_same(self):
        root=self.base/"tools_09"
        loc=root/"instrument_skill_memory.json"
        previous=loc.read_bytes()
        try:
            data=json.loads(previous)
            data["native_memory_write_allowed"]=True
            loc.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,"sealed instrument evidence modified"):
                verify_school(root)
        finally:
            loc.write_bytes(previous)

    def test_no_overwriting_old_experiences(self):
        with self.assertRaisesRegex(ValueError,"fresh output"):
            run_school(self.base/"tools_09",prior_school=self.prior)

    def test_test_targets_after_precommit_retain_sha(self):
        root=self.base/"tools_09"
        report=json.loads((root/"evaluation.json").read_text())
        targets=[root/"instrument_art"/(x["id"]+"_heldout_target.png")
                 for x in report["exams"]]
        self.assertTrue(all(x.is_file() for x in targets))
        self.assertTrue(all(x["decision_sealed_before_target_rendered"]
                            for x in report["exams"]))
        self.assertTrue(all(x["chosen_error_px_mean"] is None
                            for x in report["exams"] if x["goal"]=="UNSEEN_INTENT"))
