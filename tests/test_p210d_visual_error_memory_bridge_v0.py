import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.p210c_targeted_image_correction_v0 import correct
from brody_world_physique.p210d_visual_error_memory_bridge_v0 import append,verify_ledger

class MemoryTests(unittest.TestCase):
    def prepare(self,folder,name,correct_mask=True):
        d=Path(folder);src=d/f"{name}-src.png";ini=d/f"{name}-ini.png"
        mask=d/f"{name}-mask.png";out=d/f"{name}-out.png"
        a=Image.new("RGB",(8,8),"white");b=a.copy()
        b.putpixel((2,2),(0,0,0))
        m=Image.new("L",(8,8),0)
        m.putpixel((2,2) if correct_mask else (7,7),255)
        a.save(src);b.save(ini);m.save(mask)
        correct(src,ini,mask,out)
        return src,ini,mask,out

    def test_append_two_different_outcomes_and_replay(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=Path(td)/"ledger.json"
            a=self.prepare(td,"help",True)
            b=self.prepare(td,"nohelp",False)
            self.assertEqual(append(ledger,*a)["verdict"],"ACCEPTED")
            self.assertEqual(append(ledger,*b)["verdict"],"HOLD_EQUAL")
            result=verify_ledger(ledger)
            self.assertEqual(len(result["entries"]),2)
            self.assertEqual(result["entries"][1]["previous_digest"],result["entries"][0]["entry_digest"])
            self.assertFalse(result["knowledge_promotion"])

    def test_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=Path(td)/"ledger.json";imgs=self.prepare(td,"first")
            append(ledger,*imgs)
            with self.assertRaises(ValueError):append(ledger,*imgs)

    def test_ledger_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=Path(td)/"ledger.json";imgs=self.prepare(td,"first")
            append(ledger,*imgs)
            data=json.loads(ledger.read_text(encoding="utf-8"))
            data["entries"][0]["after"]=1234
            ledger.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(ValueError):verify_ledger(ledger)

    def test_source_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            ledger=Path(td)/"ledger.json";imgs=self.prepare(td,"first")
            append(ledger,*imgs)
            Image.new("RGB",(8,8),"black").save(imgs[0])
            with self.assertRaises(ValueError):verify_ledger(ledger)

if __name__=="__main__":unittest.main()
