import tempfile
import unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.f1i_f1l_batch_v1 import run

class F1ItoF1LTests(unittest.TestCase):
    def test_all_four_stages_without_external_data(self):
        with tempfile.TemporaryDirectory() as d:
            report=run(Path(d)/"batch")
            self.assertEqual(report["stage_count"],4)
            self.assertEqual(len(report["stages"]["F1I"]["cases"]),4)
            self.assertEqual(len(report["stages"]["F1J"]["roundtrips"]),3)
            self.assertEqual(len(report["stages"]["F1K"]["versions"]),3)
            self.assertEqual(report["stages"]["F1L"]["status"],"HOLD_NO_INDEPENDENT_IMAGES")
            self.assertFalse(report["full_integrated_education_proven"])
            self.assertFalse(report["canonical_promotion"])
            self.assertEqual(report["decision_authority"],"KX108_ONLY")
    def test_external_images_are_observed_without_semantic_claim(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"independent";source.mkdir()
            Image.new("RGB",(64,64),(14,86,152)).save(source/"sample.png")
            report=run(Path(d)/"batch",external_images=source)
            self.assertEqual(report["stages"]["F1L"]["images_evaluated"],1)
            self.assertFalse(report["stages"]["F1L"]["real_world_transfer_proven"])
    def test_never_overwrites_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/"existing";target.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(target)
if __name__=="__main__":unittest.main()
