"""P2.11e: post-generation analysis of layout/target coherence and local gesture failures.

Reads P2.11d sealed outputs. Never edits them or learns from TEST. Reports
contradictions as INVALID_GOAL and keeps both failures and best-version links.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from PIL import Image
from .drawing_school_v0 import SIDE
from .p210a_visual_loop_contract_v0 import digest
from .p211b_frozen_gesture_transfer_v0 import read as read_memory

SCHEMA="BRODY_P211E_REGRESSION_DIAGNOSTIC_V0"

def ink(path):
    with Image.open(path) as raw:
        if raw.size!=(SIDE,SIDE):raise ValueError("image dimensions")
        im=raw.convert("L")
        return {(x,y) for y in range(SIDE) for x in range(SIDE) if im.getpixel((x,y))<128}

def _boxes(path):
    spec=json.loads(Path(path).read_text(encoding="utf-8"))
    boxes=spec.get("boxes")
    if spec.get("schema")!="BRODY_P211C_LAYOUT_V0" or not isinstance(boxes,list) or not 1<=len(boxes)<=12:
        raise ValueError("layout")
    for b in boxes:
        if not isinstance(b,list) or len(b)!=4 or any(type(v)!=int for v in b):
            raise ValueError("layout box")
        if not (0<=b[0]<b[2]<SIDE and 0<=b[1]<b[3]<SIDE):
            raise ValueError("layout bounds")
    return boxes

def audit(manifest,generated_folder,output):
    cfg=json.loads(Path(manifest).read_text(encoding="utf-8"))
    report=json.loads((Path(generated_folder)/"report.json").read_text(encoding="utf-8"))
    if cfg.get("schema")!="BRODY_P211D_MANIFEST_V0" or report.get("schema")!="BRODY_P211D_PAIRED_COMPOSITION_AUDIT_V0":
        raise ValueError("source schemas")
    memory=Path(cfg["memory"])
    read_memory(memory)
    if report["memory_sha256"]!=digest(memory) or report["manifest_sha256"]!=digest(manifest):
        raise ValueError("source provenance")
    cases=cfg["cases"];rows=report["rows"]
    if len(cases)!=len(rows) or len(rows)!=report["cases"]:raise ValueError("counts")
    diagnosed=[]
    for i,(case,row) in enumerate(zip(cases,rows)):
        boxes=_boxes(case["layout"])
        if row["case"]!=i or row["layout_sha256"]!=digest(case["layout"]) or row["reference_sha256"]!=digest(case["reference"]):
            raise ValueError("case evidence changed")
        if row["candidate_sha256"]!=digest(row["generated_path"]) or row["blank_sha256"]!=digest(row["blank_path"]):
            raise ValueError("sealed output changed")
        target=ink(case["reference"]);candidate=ink(row["generated_path"]);blank=ink(row["blank_path"])
        if blank:raise ValueError("baseline is not blank")
        inside=lambda pt:any(x1<=pt[0]<=x2 and y1<=pt[1]<=y2 for x1,y1,x2,y2 in boxes)
        target_in={p for p in target if inside(p)}
        target_out=target-target_in
        generated_in={p for p in candidate if inside(p)}
        generated_out=candidate-generated_in
        # Declared drawing task with zero target ink is not a valid proof of failure.
        goal="INVALID_GOAL_EMPTY_TARGET" if not target else (
            "INVALID_GOAL_NO_INK_IN_REQUESTED_BOXES" if not target_in else "PARTIAL_REFERENCE" if target_out or any(not any(x1<=p[0]<=x2 and y1<=p[1]<=y2 for p in target) for x1,y1,x2,y2 in boxes) else "CONSISTENT_LAYOUT_REFERENCE")
        misses=len(target-candidate)
        extra=len(candidate-target)
        if misses+extra!=row["memory_error"] or len(target)!=row["no_memory_blank_error"]:
            raise ValueError("reported metric mismatch")
        valid=goal=="CONSISTENT_LAYOUT_REFERENCE"
        # Retain the candidate; mark blank as posthoc best only if comparable.
        best="UNDETERMINED_GOAL_MISMATCH" if not valid else (
            "MEMORY_CANDIDATE" if row["memory_error"]<row["no_memory_blank_error"] else
            "BLANK_BASELINE" if row["memory_error"]>row["no_memory_blank_error"] else "TIE")
        diagnosed.append({"case":i,"goal_status":goal,"valid_goal":valid,
            "missing_foreground_pixels":misses,"extra_foreground_pixels":extra,
            "target_pixels_in_boxes":len(target_in),"target_pixels_outside_boxes":len(target_out),
            "generated_pixels_in_boxes":len(generated_in),"generated_pixels_outside_boxes":len(generated_out),
            "posthoc_best":best,"correction_applied":False,
            "attempt_preserved":True,"blind_learning_from_test":False})
    result={"schema":SCHEMA,"status":"POSTHOC_DIAGNOSTIC_NO_LEARNING",
            "manifest_sha256":digest(manifest),"p211d_report_sha256":digest(Path(generated_folder)/"report.json"),
            "cases":len(diagnosed),"valid_goals":sum(r["valid_goal"] for r in diagnosed),
            "goal_mismatches":sum(not r["valid_goal"] for r in diagnosed),
            "rows":diagnosed,"test_feedback_used_for_learning":False,
            "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    out=Path(output)
    if out.exists():raise ValueError("output exists")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--generated",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();r=audit(a.manifest,a.generated,a.out)
    print(json.dumps({k:r[k] for k in ("status","cases","valid_goals","goal_mismatches")}))
if __name__=="__main__":main()
