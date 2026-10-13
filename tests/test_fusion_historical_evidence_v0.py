import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.fusion_historical_evidence_v0 import compile_evidence,SCHEMA
class HistoricalFusionTests(unittest.TestCase):
    def setup(self,root):
        root=Path(root)
        white=root/"teacher.png";same=root/"memory.png";different=root/"first.png"
        Image.new("RGB",(64,64),"white").save(white)
        Image.new("RGB",(64,64),"white").save(same)
        Image.new("RGB",(64,64),"black").save(different)
        manifest=root/"manifest.json"
        manifest.write_text(json.dumps({"schema":SCHEMA,"episodes":[
            {"id":"historical-01","stage":"E0","mode":"GUIDED",
             "files":{"teacher":str(white),"first":str(different),"from_memory":str(same)}},
            {"id":"historical-02","stage":"E1","mode":"HIDDEN_TARGET",
             "files":{"after_feedback":str(different)}}]}),encoding="utf-8")
        return manifest,white,same,different
    def test_explicit_teacher_scores_and_missing_teacher_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,teacher,same,other=self.setup(td)
            original=teacher.read_bytes()
            report=compile_evidence(manifest,Path(td)/"output")
            self.assertEqual(report["count"],2)
            scores=report["episodes"][0]["scores"]
            self.assertEqual(scores["from_memory"]["mismatch_pixels"],0)
            self.assertEqual(scores["first"]["mismatch_pixels"],64*64)
            self.assertIsNone(report["episodes"][1]["scores"]["after_feedback"]["mismatch_pixels"])
            self.assertTrue((Path(td)/"output"/"historical_comparison.png").is_file())
            self.assertEqual(original,teacher.read_bytes())
    def test_existing_output_and_missing_file_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,*_=self.setup(td)
            path=Path(td)/"output";path.mkdir()
            with self.assertRaises(ValueError):compile_evidence(manifest,path)
            config=json.loads(manifest.read_text())
            config["episodes"][0]["files"]["teacher"]=str(Path(td)/"absent.png")
            manifest.write_text(json.dumps(config))
            with self.assertRaises(ValueError):compile_evidence(manifest,Path(td)/"fresh")
    def test_duplicate_episode_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            manifest,*_=self.setup(td)
            config=json.loads(manifest.read_text())
            config["episodes"][1]["id"]=config["episodes"][0]["id"]
            manifest.write_text(json.dumps(config))
            with self.assertRaises(ValueError):compile_evidence(manifest,Path(td)/"out")
if __name__=="__main__":unittest.main()
