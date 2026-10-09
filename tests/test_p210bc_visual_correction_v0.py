import tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.p210b_visual_error_atlas_v0 import diagnose
from brody_world_physique.p210c_targeted_image_correction_v0 import correct,verify

class ImageCorrectionTests(unittest.TestCase):
    def fixtures(self,folder):
        d=Path(folder)
        source=Image.new("RGB",(12,12),"white")
        initial=source.copy()
        for x in (2,3,4):initial.putpixel((x,2),(0,0,0))
        mask=Image.new("L",(12,12),0)
        for x in (2,3,4):mask.putpixel((x,2),255)
        paths=[]
        for name,image in (("source.png",source),("initial.png",initial),("mask.png",mask)):
            path=d/name;image.save(path);paths.append(path)
        return source,initial,mask,paths

    def test_region_diagnostic_and_correction(self):
        with tempfile.TemporaryDirectory() as folder:
            s,i,m,(src,initial,mask)=self.fixtures(folder)
            result=diagnose(s,i,m)
            self.assertEqual(result["object_changed_pixels"],3)
            self.assertEqual(result["background_changed_pixels"],0)
            self.assertEqual(result["error_type"],"UNKNOWN")
            out=Path(folder)/"candidate.png"
            receipt=correct(src,initial,mask,out)
            self.assertEqual(receipt["verdict"],"ACCEPTED")
            self.assertEqual(receipt["error_after"],0)
            self.assertTrue(verify(out,src,initial,mask)["verified"])

    def test_protected_region_detects_error(self):
        with tempfile.TemporaryDirectory() as folder:
            s,i,m,_=self.fixtures(folder)
            protected=Image.new("L",(12,12),0)
            protected.putpixel((2,2),255)
            with self.assertRaises(ValueError):diagnose(s,i,m,protected)
            blank=Image.new("L",(12,12),0)
            protected=Image.new("L",(12,12),0)
            protected.putpixel((2,2),255)
            metrics=diagnose(s,i,blank,protected)
            self.assertEqual(metrics["protected_changed_pixels"],1)

    def test_equal_attempt_and_replay_tamper(self):
        with tempfile.TemporaryDirectory() as folder:
            _,_,_,(src,initial,mask)=self.fixtures(folder)
            # mask only covers a blank pixel => no change in error
            m=Image.new("L",(12,12),0);m.putpixel((9,9),255);m.save(mask)
            out=Path(folder)/"candidate.png"
            receipt=correct(src,initial,mask,out)
            self.assertEqual(receipt["verdict"],"HOLD_EQUAL")
            self.assertEqual(receipt["best_sha256"],receipt["initial_sha256"])
            self.assertTrue(verify(out,src,initial,mask)["verified"])
            Image.new("RGB",(12,12),"black").save(out)
            with self.assertRaises(ValueError):verify(out,src,initial,mask)

    def test_dimension_or_empty_mask_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            _,_,_,(src,initial,mask)=self.fixtures(folder)
            Image.new("L",(12,12),0).save(mask)
            with self.assertRaises(ValueError):
                correct(src,initial,mask,Path(folder)/"failed.png")
            Image.new("L",(4,4),255).save(mask)
            with self.assertRaises(ValueError):
                correct(src,initial,mask,Path(folder)/"failed.png")
if __name__=="__main__":unittest.main()
