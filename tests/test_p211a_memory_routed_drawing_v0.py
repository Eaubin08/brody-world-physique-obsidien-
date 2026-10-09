import tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.p210c_targeted_image_correction_v0 import correct
from brody_world_physique.p210d_visual_error_memory_bridge_v0 import append
from brody_world_physique.p211a_memory_routed_drawing_v0 import run

class MemoryRoutedDrawingTests(unittest.TestCase):
    def setup_data(self,folder,useful):
        d=Path(folder)
        src=d/"train-source.png";ini=d/"train-initial.png"
        mask=d/"train-mask.png";cand=d/"train-candidate.png"
        a=Image.new("L",(SIDE,SIDE),255);b=a.copy()
        b.putpixel((3,3),0)
        m=Image.new("L",(SIDE,SIDE),0)
        m.putpixel((3,3) if useful else (12,12),255)
        a.save(src);b.save(ini);m.save(mask)
        correct(src,ini,mask,cand)
        ledger=d/"ledger.json"
        append(ledger,src,ini,mask,cand)
        new=d/"unseen.png"
        im=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(im).line((10,10,SIDE-12,SIDE-15),fill=0,width=3)
        im.save(new)
        return ledger,new

    def test_memory_changes_selected_generation_route(self):
        with tempfile.TemporaryDirectory() as td:
            left=Path(td)/"left";right=Path(td)/"right"
            left.mkdir();right.mkdir()
            help_ledger,new=self.setup_data(left,True)
            nohelp_ledger,new2=self.setup_data(right,False)
            r=run(help_ledger,new,Path(td)/"yes.png")
            r2=run(nohelp_ledger,new2,Path(td)/"no.png")
            self.assertEqual(r["selected_method"],"DRAW_GESTURES_V1")
            self.assertEqual(r2["selected_method"],"PASS_THROUGH")
            self.assertTrue(r["precommitted_before_reference_scoring"])
            self.assertFalse(r["general_visual_learning_proven"])

    def test_corrupted_ledger_fails_before_generation(self):
        with tempfile.TemporaryDirectory() as td:
            ledger,new=self.setup_data(td,True)
            ledger.write_text("{}",encoding="utf-8")
            with self.assertRaises(ValueError):
                run(ledger,new,Path(td)/"out.png")
            self.assertFalse((Path(td)/"out.png").exists())

    def test_teacher_reference_only_scored_after_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            ledger,new=self.setup_data(td,True)
            out=Path(td)/"out.png"
            r=run(ledger,new,out,reference=new)
            self.assertTrue(out.is_file())
            self.assertEqual(r["baseline_pixel_error"],0)
            self.assertTrue(r["precommitted_before_reference_scoring"])

if __name__=="__main__":unittest.main()
