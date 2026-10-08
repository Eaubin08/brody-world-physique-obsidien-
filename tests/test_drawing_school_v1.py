"""Drawing V1: erase/replace, curves, source-gated memory, and chain receipts."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image, ImageDraw

from brody_world_physique.drawing_school_v0 import black_pixels
from brody_world_physique.drawing_school_v1 import (
    GestureV1, SkillV1, _error, _skeletonize, _trace_paths, correct_drawing,
    recall, render, suggest_gestures_from_reference, teacher_exams,
    teacher_lessons, run_school,
)


def reference(strokes):
    image=Image.new("L",(64,64),255)
    pen=ImageDraw.Draw(image)
    for pts in strokes:pen.line(pts,fill=0,width=3,joint="curve")
    return image


class DrawingV1Tests(TestCase):
    def test_skeleton_and_trace_nonempty_lines_and_circles(self):
        lessons=dict(teacher_lessons())
        for kind in ("cours_trait","cours_triangle","cours_cercle"):
            source=lessons[kind]
            thin=_skeletonize(black_pixels(source))
            self.assertTrue(thin,kind)
            paths=_trace_paths(thin)
            self.assertTrue(paths,kind)
            self.assertTrue(suggest_gestures_from_reference(source),kind)

    def test_really_erase_worse_wrong_stroke(self):
        model=reference([((12,15),(48,15))])
        candidate=GestureV1(((12,41),(48,41)),"STRAIGHT_STROKE")
        outcome=correct_drawing(model,(candidate,),max_revisions=0)
        self.assertTrue(outcome["memory_rejected"])
        self.assertGreater(outcome["raw_recall_error"],outcome["blank_error"])
        self.assertEqual(outcome["error_after_recall_gate"],outcome["blank_error"])
        # Erasure isn't just a statistic: rendered copy omits the bad stroke.
        self.assertEqual(black_pixels(outcome["image"]),set())

    def test_replacement_or_erasure_repairs_a_partly_right_attempt(self):
        model=reference([((10,16),(51,16)),((10,35),(51,35))])
        existing=(GestureV1(((10,16),(51,16)),"STRAIGHT_STROKE"),
                  GestureV1(((12,46),(24,46)),"STRAIGHT_STROKE"))
        before=_error(black_pixels(model),existing)
        outcome=correct_drawing(model,existing,max_revisions=12)
        self.assertLess(outcome["final_error"],before)
        self.assertFalse(outcome["memory_rejected"])
        self.assertTrue(any(x["action"] in ("ERASE","REPLACE")
                            for x in outcome["changes"]))

    def test_triangle_vectorization_improves_baseline(self):
        model=dict(teacher_lessons())["cours_triangle"]
        outcome=correct_drawing(model)
        self.assertLess(outcome["final_error"],outcome["blank_error"])
        self.assertTrue(outcome["changes"])

    def test_circle_and_curve_representable_without_ellipse_tool_for_student(self):
        model=dict(teacher_lessons())["cours_cercle"]
        gestures=suggest_gestures_from_reference(model)
        self.assertTrue(any(g.kind=="CURVED_STROKE" for g in gestures))
        outcome=correct_drawing(model)
        self.assertLess(outcome["final_error"],outcome["blank_error"])
        # Circle reference is a raster; student strokes are generic curves
        # extracted from skeleton, not a hardcoded circle/ellipse command.
        self.assertTrue(all(g.kind in ("CURVED_STROKE","STRAIGHT_STROKE")
                            for g in outcome["gestures"]))

    def test_run_cold_memory_and_holdout_sources(self):
        with TemporaryDirectory() as folder:
            result=run_school(Path(folder)/"drawing")
            self.assertEqual(result["train"],4)
            self.assertEqual(result["exams"],6)
            self.assertGreater(result["ledger_events"],0)
            self.assertFalse(result["native_memory_write_allowed"])
            import json
            report=json.loads((Path(folder)/"drawing"/"evaluation.json").read_text())
            self.assertFalse(report["memory_promotion_allowed"])
            self.assertFalse(report["autonomous_image_generation"])
            self.assertTrue(all(e["seen_by_learner_at_exam"] for e in report["unseen_exams"]))
            self.assertTrue(all(e["after_correction_error_pixels"]
                                <=e["initial_after_memory_gate"] for e in report["unseen_exams"]))
            self.assertTrue((Path(folder)/"drawing"/"candidate_experience_ledger.jsonl").exists())
            with self.assertRaisesRegex(ValueError,"new output"):
                run_school(Path(folder)/"drawing")
