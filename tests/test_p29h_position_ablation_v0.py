import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from brody_world_physique import p29h_position_ablation_v0 as m

class AblationTests(unittest.TestCase):
    def point(self,i):
        return SimpleNamespace(x=float(i),y=float(2*i),time_s=i*.25,source_ref=f"f{i}",frame_ref="f",entity_ref="ball",unit="px",source_kind="SIMULATED")

    def test_baselines_and_no_memory_hold(self):
        p=[self.point(i) for i in range(3)]
        r=m.predict(p,())
        self.assertEqual(r["A0_LAST_POSITION"],[2.,4.])
        self.assertEqual(r["A1_SPATIAL_DELTA"],[3.,6.])
        self.assertEqual(r["A2_TEMPORAL_VELOCITY"],[3.,6.])
        self.assertIsNone(r["A5_NO_MEMORY"])

    def test_future_not_passed_to_predict(self):
        points=[self.point(i) for i in range(12)]
        with TemporaryDirectory() as tmp:
            suite=Path(tmp)/"suite.json";suite.write_text("{}")
            def loader(_):return ([("train",Path("train.mp4"),"a"*64)],[("test",Path("test.mp4"),"b"*64)])
            def iterator(path,digest,**kwargs):return iter(points)
            called=[]
            def predictor(history,memory):
                called.append(tuple(x.source_ref for x in history))
                return {a:[history[-1].x,history[-1].y] for a in m.ARMS}
            with patch.object(m,"_load_probe_suite",side_effect=loader),patch.object(m,"iter_video_points",side_effect=iterator),patch.object(m,"video_sha256",return_value="b"*64),patch.object(m,"acquire_experiences",return_value=[]),patch.object(m,"predict",side_effect=predictor):
                result=m.evaluate(suite)
                self.assertEqual(result["shared_test_cases"],9)
                self.assertEqual(called[0],("f0","f1","f2"))
                self.assertEqual(result["precommit"][0]["future_frame"],18)
                self.assertTrue(result["test_feedback_used_for_learning"] is False)

if __name__=="__main__":unittest.main()
