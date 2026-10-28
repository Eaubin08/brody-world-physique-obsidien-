import tempfile
import unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.p0_p5_integrated_evidence_v1 import run

class IntegratedEvidenceTests(unittest.TestCase):
    def test_all_six_gates(self):
        with tempfile.TemporaryDirectory() as d:
            report=run(Path(d)/"integrated")
            self.assertEqual(report["P1"]["source_parts"],2)
            self.assertEqual(report["P1"]["structural_parts"],2)
            self.assertLess(report["P1"]["coarse_parts"],2)
            self.assertGreater(report["P2"]["before_feedback_mae"],report["P2"]["after_feedback_mae"])
            self.assertTrue(report["P3"]["candidate_rejected"])
            self.assertEqual(len(report["P4"]["cases"]),4)
            self.assertGreater(report["P4"]["coverage"],0)
            self.assertLess(report["P4"]["coverage"],1)
            self.assertEqual(report["P5"]["pre_probe"]["decision"],"PROBE")
            self.assertEqual(report["P5"]["without_probe"]["decision"],"HOLD")
            self.assertFalse(report["P0"]["full_regression_executed"])
            self.assertFalse(report["P5"]["sens_mmonde_connected"])
            self.assertFalse(report["native_memory_write"])
            self.assertEqual(report["decision_authority"],"KX108_ONLY")
    def test_external_images_are_unlabeled(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"external";source.mkdir()
            Image.new("RGB",(64,64),"white").save(source/"sample.png")
            report=run(Path(d)/"integrated",external_images=source)
            self.assertEqual(report["P5"]["external_images_seen"],1)
            self.assertEqual(report["P5"]["external_exam_status"],"UNLABELED_ONLY")
            self.assertFalse(report["P5"]["real_world_transfer_proven"])
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"existing";out.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(out)

if __name__=="__main__":unittest.main()
