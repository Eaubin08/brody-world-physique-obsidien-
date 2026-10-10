"""P2.10e: frozen train-derived geometric correction, evaluated on unseen images.

Learns only an offset (dx,dy) from paired TRAIN PNGs. On TEST it translates
the initial candidate image without access to the hidden target. An oracle
is only used AFTER predictions are sealed to report paired errors.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
from .p210a_visual_loop_contract_v0 import open_rgba,pixel_error,digest

SCHEMA="BRODY_P210E_TRANSFER_V0"

def _white_canvas(im):
    # Black ink on white opaque images, 8-bit grayscale; avoid unknown alpha.
    return im.convert("L")

def _ink_center(image):
    im=_white_canvas(image)
    points=[(x,y) for y in range(im.height) for x in range(im.width) if im.getpixel((x,y))<128]
    if not points:raise ValueError("empty foreground")
    return (sum(p[0] for p in points)/len(points),sum(p[1] for p in points)/len(points))

def learn_offset(train_pairs):
    if not train_pairs:raise ValueError("TRAIN empty")
    offsets=[]
    seen=set()
    for candidate,reference in train_pairs:
        paths=(str(Path(candidate).resolve()),str(Path(reference).resolve()))
        if paths[0]==paths[1] or any(p in seen for p in paths):
            raise ValueError("TRAIN duplicate or self-reference")
        seen.update(paths)
        a,b=open_rgba(candidate),open_rgba(reference)
        if a.size!=b.size:raise ValueError("TRAIN dimensions")
        c1,c2=_ink_center(a),_ink_center(b)
        offsets.append((round(c2[0]-c1[0]),round(c2[1]-c1[1])))
    offsets.sort()
    # Consensus only, no tuning using TEST truth.
    if len(set(offsets))!=1:raise ValueError("ambiguous TRAIN corrections")
    return offsets[0]

def _translate(im,dx,dy):
    src=_white_canvas(im)
    out=Image.new("L",src.size,255)
    out.paste(src,(dx,dy))
    return out

def run(manifest,out):
    manifest=Path(manifest)
    cfg=json.loads(manifest.read_text(encoding="utf-8"))
    if cfg.get("schema")!="BRODY_P210E_INPUT_V0":raise ValueError("schema")
    train=cfg.get("train",[]);test=cfg.get("test",[])
    if not test:raise ValueError("TEST empty")
    train_pairs=[(r["initial"],r["reference"]) for r in train]
    dx,dy=learn_offset(train_pairs)
    train_digests={digest(p) for pair in train_pairs for p in pair}
    test_records=[]
    for i,row in enumerate(test):
        initial,hidden=row["initial"],row["reference"]
        if digest(initial) in train_digests or digest(hidden) in train_digests:
            raise ValueError("TRAIN/TEST image content leakage")
        if Path(initial).resolve()==Path(hidden).resolve():raise ValueError("TEST self-reference")
        original=open_rgba(initial);target=open_rgba(hidden)
        if original.size!=target.size:raise ValueError("TEST dimensions")
        out_png=Path(out).with_suffix("").parent/(Path(out).stem+f"-test{i}.png")
        if out_png.exists():raise ValueError("existing candidate")
        # Commit candidate PNG BEFORE reading any target pixels for evaluation.
        out_png.parent.mkdir(parents=True,exist_ok=True)
        predicted=_translate(original,dx,dy)
        predicted.save(out_png)
        committed=digest(out_png)
        baseline=pixel_error(target,original)
        proposed=pixel_error(target,predicted.convert("RGBA"))
        test_records.append({"test_index":i,"initial_sha256":digest(initial),
            "reference_sha256":digest(hidden),"candidate_path":str(out_png.resolve()),
            "candidate_sha256":committed,"sealed_method":{"dx":dx,"dy":dy},
            "baseline_pixel_error":baseline,"memory_pixel_error":proposed,
            "delta_error":proposed-baseline,"candidate_committed_before_scoring":True})
    report={"schema":SCHEMA,"status":"SYNTHETIC_OR_LOCAL_CONTROLLED_TRANSFER_NOT_GENERAL_IMAGE_LEARNING",
        "method":"FROZEN_TRAIN_OFFSET","train_count":len(train),
        "test_count":len(test),"frozen_offset":{"dx":dx,"dy":dy},
        "rows":test_records,"improved":sum(r["delta_error"]<0 for r in test_records),
        "worsened":sum(r["delta_error"]>0 for r in test_records),
        "ties":sum(r["delta_error"]==0 for r in test_records),
        "test_feedback_used_for_learning":False,"native_memory_write":False,
        "decision_authority":"KX108_ONLY"}
    destination=Path(out)
    if destination.exists():raise ValueError("report exists")
    destination.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    r=run(args.manifest,args.out)
    print(json.dumps({k:r[k] for k in ("status","train_count","test_count","frozen_offset","improved","worsened","ties")}))
if __name__=="__main__":main()
