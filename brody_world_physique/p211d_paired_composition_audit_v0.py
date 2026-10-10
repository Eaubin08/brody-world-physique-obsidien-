"""P2.11d: paired generalization audit of frozen gestures on novel layouts.

Every candidate (and blank baseline) is emitted by P2.11c before the target
image is read. Ground-truth targets are externally supplied and must be
prepared before the run. This is not independent semantic image generation.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image
from .drawing_school_v0 import SIDE
from .p211c_gesture_recomposition_v0 import compose
from .p211b_frozen_gesture_transfer_v0 import read as read_memory
from .p210a_visual_loop_contract_v0 import digest,open_rgba,pixel_error

SCHEMA="BRODY_P211D_PAIRED_COMPOSITION_AUDIT_V0"

def run(manifest,out_dir):
    manifest=Path(manifest)
    cfg=json.loads(manifest.read_text(encoding="utf-8"))
    if cfg.get("schema")!="BRODY_P211D_MANIFEST_V0":raise ValueError("manifest schema")
    memory=Path(cfg["memory"])
    read_memory(memory)
    cases=cfg.get("cases")
    if not isinstance(cases,list) or not 1<=len(cases)<=40:raise ValueError("case count")
    out=Path(out_dir)
    if out.exists():raise ValueError("output exists: refuse overwrite")
    unique_refs=set()
    seen_layouts=set()
    for case in cases:
        layout=Path(case["layout"]);reference=Path(case["reference"])
        if layout.resolve() in seen_layouts:raise ValueError("reused layout")
        seen_layouts.add(layout.resolve())
        if not reference.is_file():raise ValueError("missing reference")
        ref_sha=digest(reference)
        if ref_sha in unique_refs:raise ValueError("duplicated test reference")
        unique_refs.add(ref_sha)
        # TRAIN reference must not equal any test target.
        if ref_sha==json.loads(memory.read_text(encoding="utf-8"))["train_sha256"]:
            raise ValueError("TRAIN/TEST content leakage")
    out.mkdir(parents=True)
    rows=[]
    for i,case in enumerate(cases):
        generated=compose(memory,case["layout"],out/f"case{i}.png")
        # compose() doesn't open reference, and seals both output images.
        target=open_rgba(case["reference"])
        if target.size!=(SIDE,SIDE):raise ValueError("reference dimensions")
        with Image.open(generated["candidate_path"]) as ci:
            candidate=ci.convert("RGBA")
        with Image.open(generated["blank_path"]) as bi:
            blank=bi.convert("RGBA")
        e1=pixel_error(target,candidate);e0=pixel_error(target,blank)
        rows.append({"case":i,"layout_sha256":digest(case["layout"]),
                     "reference_sha256":digest(case["reference"]),
                     "candidate_sha256":generated["candidate_sha256"],
                     "blank_sha256":generated["blank_sha256"],
                     "generated_path":generated["candidate_path"],
                     "blank_path":generated["blank_path"],
                     "memory_error":e1,"no_memory_blank_error":e0,
                     "memory_minus_blank":e1-e0,
                     "verdict":"IMPROVED" if e1<e0 else "WORSENED" if e1>e0 else "TIE",
                     "candidate_precommitted":True})
    summary={"schema":SCHEMA,"status":"CONTROLLED_GESTURE_TRANSFER_NOT_GENERAL_VISUAL_LEARNING",
        "memory_sha256":digest(memory),"manifest_sha256":digest(manifest),
        "cases":len(rows),"improved":sum(r["verdict"]=="IMPROVED" for r in rows),
        "worsened":sum(r["verdict"]=="WORSENED" for r in rows),
        "ties":sum(r["verdict"]=="TIE" for r in rows),
        "paired_mean_delta":sum(r["memory_minus_blank"] for r in rows)/len(rows),
        "rows":rows,"train_leakage_detected":False,
        "test_feedback_used_for_learning":False,
        "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (out/"report.json").write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.manifest,a.out)
    print(json.dumps({k:r[k] for k in ("status","cases","improved","worsened","ties","paired_mean_delta")}))
if __name__=="__main__":main()
