import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from brody_world_physique import p29g_one_video_bridge_v0 as m

def fixture(root):
    folder=root/"p1";folder.mkdir()
    report={
       "video_sha256":"a"*64,
       "experiment_candidate":{
          "shared_source_sha256":"a"*64,"independent_source_count":1,
          "frames":{"history_refs":["f0","f1","f2"],"heldout_ref":"f3"},
          "contract_refs":{"projection":"pr","memory_write_allowed":False,
                           "decision_authority":"KX108_ONLY"},
          "representation_views":{
            "RASTER":{"predicted_generated_sha256":"b"*64,"heldout_source_frame_sha256":"c"*64},
            "SPATIAL":{"unit":"px","frame_ref":"frame","history_xy":[[0,0],[1,2],[2,4]]},
            "TEMPORAL":{"history_t_s":[0,1,2],"clock_kind":"SIMULATED_FRAME_TIME"},
            "MOTION":{"estimated_velocity_px_per_s":[1,2]}},
          "comparisons":{"center_error_px":3,"full_frame_mae":8}}}
    (folder/"evaluation.json").write_text(json.dumps(report))
    return {"suite":"s","forecasts":"f","preview":"p","p1_out":folder}

class SameSourceTests(unittest.TestCase):
    @patch.object(m.p1,"verify",return_value={"status":"PASS_P1_MULTIREPRESENTATION_BOUNDED_REPLAY"})
    def test_same_video_views_and_replay(self,_):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);kw=fixture(root)
            result=m.evidence(**kw)
            self.assertEqual(result["same_source_view_count"],4)
            self.assertEqual(result["independent_source_count"],1)
            self.assertEqual(result["reciprocal_residual"],0)
            self.assertFalse(result["joint_improvement_proven"])
            self.assertFalse(result["native_memory_write"])
            out=root/"joined.json"
            m.run(out,**kw)
            self.assertTrue(m.verify(out,**kw)["verified"])
            saved=json.loads(out.read_text());saved["raster_mae"]=0
            out.write_text(json.dumps(saved))
            with self.assertRaises(ValueError):m.verify(out,**kw)

    @patch.object(m.p1,"verify",return_value={"status":"PASS_P1_MULTIREPRESENTATION_BOUNDED_REPLAY"})
    def test_mismatched_motion_rejected(self,_):
        with tempfile.TemporaryDirectory() as td:
            kw=fixture(Path(td));p=kw["p1_out"]/"evaluation.json"
            x=json.loads(p.read_text());x["experiment_candidate"]["representation_views"]["MOTION"]["estimated_velocity_px_per_s"]=[9,9]
            p.write_text(json.dumps(x))
            with self.assertRaises(ValueError):m.evidence(**kw)

    @patch.object(m.p1,"verify",return_value={"status":"FAILED"})
    def test_original_p1_verify_mandatory(self,_):
        with tempfile.TemporaryDirectory() as td:
            kw=fixture(Path(td))
            with self.assertRaises(ValueError):m.evidence(**kw)

if __name__=="__main__":unittest.main()
