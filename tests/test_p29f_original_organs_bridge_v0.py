import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from brody_world_physique import p29f_original_organs_bridge_v0 as m

class OriginalOrgansBridgeTests(unittest.TestCase):
    def setup_sources(self,root):
        a=root/"p1";b=root/"v42";a.mkdir();b.mkdir()
        report_a={"source_kind":"SIMULATED","decision_authority":"KX108_ONLY",
          "native_memory_write_allowed":False,"video_sha256":"a"*64,
          "experiment_candidate":{"representation_views":{
            "RASTER":{},"SPATIAL":{"frame_ref":"camera"},"TEMPORAL":{"clock_kind":"SIMULATED_FRAME_TIME"},"MOTION":{}},
            "comparisons":{"full_frame_mae":13.2,"center_error_px":4.1}}}
        report_b={"source_kind":"SIMULATED","decision_authority":"KX108_ONLY",
          "native_memory_write_allowed":False,"rotation_frame":"SYNTHETIC_2D_CANVAS_NOT_3D_360",
          "reciprocal_relation_derived_by_reverse_vector":True,
          "lessons":[{},{}]}
        (a/"evaluation.json").write_text(json.dumps(report_a))
        (b/"evaluation.json").write_text(json.dumps(report_b))
        return dict(suite="suite",forecasts="forecasts",preview="preview",
                    p1_out=a,v42_out=b,v3="v3",v4="v4",v41="v41")

    def test_verified_reuse_without_fusing_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);args=self.setup_sources(root)
            with patch.object(m.p1,"verify",return_value={"status":"PASS_P1_MULTIREPRESENTATION_BOUNDED_REPLAY"}),patch.object(m.v42,"verify",return_value={"status":"PASS_V4_2_BOUNDED_ORIENTATION_AND_RECIPROCITY_REPLAY"}):
                r=m.assemble(**args)
                self.assertEqual(len(r["p1_representation_views"]),4)
                self.assertFalse(r["same_scene_cross_modal_inference"])
                self.assertFalse(r["native_memory_write"])
                self.assertEqual(r["decision_authority"],"KX108_ONLY")
                out=root/"joined.json"
                m.run(out,**args)
                self.assertTrue(m.verify(out,**args)["verified"])
                saved=json.loads(out.read_text());saved["p1_center_error_px"]=0
                out.write_text(json.dumps(saved))
                with self.assertRaises(ValueError):m.verify(out,**args)

    def test_original_verification_is_mandatory(self):
        with tempfile.TemporaryDirectory() as temp:
            args=self.setup_sources(Path(temp))
            with patch.object(m.p1,"verify",return_value={"status":"FAILED"}),patch.object(m.v42,"verify",return_value={"status":"PASS_V4_2_BOUNDED_ORIENTATION_AND_RECIPROCITY_REPLAY"}):
                with self.assertRaises(ValueError):m.assemble(**args)

    def test_absent_view_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            args=self.setup_sources(Path(temp))
            p=Path(args["p1_out"])/"evaluation.json"
            data=json.loads(p.read_text());del data["experiment_candidate"]["representation_views"]["MOTION"]
            p.write_text(json.dumps(data))
            with patch.object(m.p1,"verify",return_value={"status":"PASS_P1_MULTIREPRESENTATION_BOUNDED_REPLAY"}),patch.object(m.v42,"verify",return_value={"status":"PASS_V4_2_BOUNDED_ORIENTATION_AND_RECIPROCITY_REPLAY"}):
                with self.assertRaises(ValueError):m.assemble(**args)

if __name__=="__main__":unittest.main()
