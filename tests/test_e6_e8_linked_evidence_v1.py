import tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.e6_e8_linked_evidence_v1 import run
class LinkedEvidenceTests(unittest.TestCase):
    def test_e6_hold_and_e7_local_boundary_e8_real_report_link(self):
        with tempfile.TemporaryDirectory() as d:
            r=run(Path(d)/"e6e8")
            self.assertEqual(r["E6"]["status"],"HOLD_NO_EXTERNAL_CORPUS")
            self.assertTrue(all(r["E7"]["verified_local_contracts"].values()))
            self.assertFalse(r["E7"]["upstream_mmonde_runtime_verified"])
            self.assertTrue(r["E8"]["e1_memory_retained"])
            self.assertGreaterEqual(r["E8"]["e23_worse_than_static"],1)
            self.assertEqual(r["E8"]["next_experiment_proposed"],"PROBE")
            self.assertFalse(r["E8"]["followup_probe_executed"])
            self.assertFalse(r["E8"]["shared_latent_world_model"])
            self.assertFalse(r["canonical_promotion"])
    def test_unverified_external_source(self):
        with tempfile.TemporaryDirectory() as d:
            pics=Path(d)/"pics";pics.mkdir()
            Image.new("RGB",(64,64),"white").save(pics/"photo.png")
            r=run(Path(d)/"run",external_images=pics)
            self.assertEqual(r["E6"]["examined"],1)
            self.assertFalse(r["E6"]["real_source_authenticated"])
    def test_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"prior";p.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(p)
if __name__=="__main__":unittest.main()
