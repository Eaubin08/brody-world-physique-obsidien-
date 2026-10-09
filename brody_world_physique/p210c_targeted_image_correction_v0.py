"""P2.10c: local mask-guided image correction and preserved rollback evidence.

A simple existing-image compositor, NOT an autonomous image generator.
Teacher/source pixels are visible to the supervised correction step.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageChops
from .p210a_visual_loop_contract_v0 import open_rgba,pixel_error,digest
from .p210b_visual_error_atlas_v0 import diagnose

def correct(source,initial,mask,output,*,mode="replace_region"):
    if mode!="replace_region":raise ValueError("unsupported method")
    out=Path(output)
    if out.exists():raise ValueError("refuse overwrite")
    a,b=open_rgba(source),open_rgba(initial)
    with Image.open(mask) as raw:
        m=raw.convert("L")
    if a.size!=b.size or m.size!=a.size:raise ValueError("dimension mismatch")
    m=m.point(lambda v:255 if v>=128 else 0)
    if not m.getbbox():raise ValueError("empty correction mask")
    # Region-scoped, teacher-guided compositing. This is NOT learned synthesis.
    new=Image.composite(a,b,m)
    old_score=pixel_error(a,b);new_score=pixel_error(a,new)
    decision="ACCEPTED" if new_score<old_score else "HOLD_EQUAL" if new_score==old_score else "ROLLED_BACK"
    dest=out
    dest.parent.mkdir(parents=True,exist_ok=True)
    new.save(dest)
    selected=dest if decision=="ACCEPTED" else Path(initial)
    result={"schema":"BRODY_P210C_LOCAL_CORRECTION_V0",
        "source_sha256":digest(source),"initial_sha256":digest(initial),
        "mask_sha256":digest(mask),"candidate_sha256":digest(dest),
        "best_sha256":digest(selected),"candidate_path":str(dest.resolve()),
        "best_path":str(selected.resolve()),"error_before":old_score,
        "error_after":new_score,"verdict":decision,
        "teacher_pixels_visible_to_correction":True,
        "learned_visual_generator":False,"outside_mask_preserved":True,
        "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    report=out.with_suffix(".json")
    if report.exists():raise ValueError("report exists")
    report.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def verify(output,source,initial,mask):
    result=json.loads(Path(output).with_suffix(".json").read_text(encoding="utf-8"))
    if result["schema"]!="BRODY_P210C_LOCAL_CORRECTION_V0":raise ValueError("schema")
    if (result["source_sha256"]!=digest(source) or result["initial_sha256"]!=digest(initial)
        or result["mask_sha256"]!=digest(mask) or result["candidate_sha256"]!=digest(output)):
        raise ValueError("input/candidate changed")
    a,b,c=open_rgba(source),open_rgba(initial),open_rgba(output)
    with Image.open(mask) as raw:
        m=raw.convert("L")
    m=m.point(lambda v:255 if v>=128 else 0)
    if a.size!=b.size or c.size!=a.size or m.size!=a.size:raise ValueError("dimension mismatch")
    expected=Image.composite(a,b,m)
    if ImageChops.difference(expected,c).getbbox():raise ValueError("candidate replay mismatch")
    before=pixel_error(a,b);after=pixel_error(a,c)
    verdict="ACCEPTED" if after<before else "HOLD_EQUAL" if after==before else "ROLLED_BACK"
    best=output if verdict=="ACCEPTED" else initial
    if (result["error_before"]!=before or result["error_after"]!=after
        or result["verdict"]!=verdict or result["best_sha256"]!=digest(best)
        or result["decision_authority"]!="KX108_ONLY"
        or result["native_memory_write"] is not False):
        raise ValueError("receipt mismatch")
    return {"verified":True,"verdict":verdict}

def main():
    p=argparse.ArgumentParser()
    for field in ("source","initial","mask","out"):p.add_argument("--"+field,required=True)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    print(json.dumps(verify(a.out,a.source,a.initial,a.mask) if a.verify
                     else correct(a.source,a.initial,a.mask,a.out)))
if __name__=="__main__":main()
