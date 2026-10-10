"""P2.12c: mixed TEST benchmark + inspectable 3-column image contact sheet.

A policy trained on TRAIN is frozen. TEST generation precedes target evaluation.
Test targets are external and never update the policy. Report all regressions.
"""
from __future__ import annotations
import argparse,json,csv
from pathlib import Path
from PIL import Image,ImageDraw
from .drawing_school_v0 import SIDE
from .p210a_visual_loop_contract_v0 import digest,open_rgba
from .p212b_frozen_shift_transfer_v0 import replay

SCHEMA="BRODY_P212C_MIXED_TEST_VISUAL_REPORT_V0"
def benchmark(memory,policy,manifest,out_dir):
    cfg=json.loads(Path(manifest).read_text(encoding="utf-8"))
    if cfg.get("schema")!="BRODY_P212C_CASES_V0":raise ValueError("manifest schema")
    cases=cfg.get("cases")
    if not isinstance(cases,list) or not 2<=len(cases)<=40:raise ValueError("case count")
    out=Path(out_dir)
    if out.exists():raise ValueError("output exists")
    layouts=set();targets=set()
    for row in cases:
        if not isinstance(row,dict) or set(row)!={"layout","reference","label"}:raise ValueError("case format")
        if not isinstance(row["label"],str) or not 1<=len(row["label"])<=50:raise ValueError("label")
        layout=Path(row["layout"]);ref=Path(row["reference"])
        if not layout.is_file() or not ref.is_file():raise ValueError("missing inputs")
        lh=digest(layout);rh=digest(ref)
        if lh in layouts or rh in targets:raise ValueError("duplicate case")
        layouts.add(lh);targets.add(rh)
        if open_rgba(ref).size!=(SIDE,SIDE):raise ValueError("image size")
    out.mkdir(parents=True)
    records=[]
    # First pass: all candidates sealed without accessing test references in replay.
    for i,case in enumerate(cases):
        result=replay(memory,policy,case["layout"],out/f"case{i}")
        records.append({"index":i,"label":case["label"],"layout":case["layout"],
                        "reference":case["reference"],"initial_sha256":result["baseline_sha256"],
                        "corrected_sha256":result["candidate_sha256"],
                        "candidate_committed_before_target":True})
    # Second pass: only now open targets to score and build image sheet.
    sheet=Image.new("RGB",(SIDE*3,len(cases)*(SIDE+24)),"white")
    painter=ImageDraw.Draw(sheet)
    for i,record in enumerate(records):
        case_dir=out/f"case{i}"
        scored=json.loads((case_dir/"report.json").read_text(encoding="utf-8"))
        if scored["baseline_sha256"]!=digest(case_dir/"baseline.png") or scored["candidate_sha256"]!=digest(case_dir/"frozen-policy.png"):
            raise ValueError("candidate integrity")
        target=open_rgba(record["reference"])
        with Image.open(case_dir/"baseline.png") as a:initial=a.convert("RGBA")
        with Image.open(case_dir/"frozen-policy.png") as b:corrected=b.convert("RGBA")
        # use same metric as previous phases
        from .p210a_visual_loop_contract_v0 import pixel_error
        err0=pixel_error(target,initial);err1=pixel_error(target,corrected)
        verdict="IMPROVED" if err1<err0 else "WORSENED" if err1>err0 else "TIE"
        record.update({"baseline_error":err0,"corrected_error":err1,"delta":err1-err0,"verdict":verdict,
                       "reference_sha256":digest(record["reference"])})
        y=i*(SIDE+24)
        painter.text((2,y+3),f"{i}: TARGET",fill="black")
        painter.text((SIDE+2,y+3),"INITIAL",fill="black")
        painter.text((SIDE*2+2,y+3),f"CORRECTED {verdict}",fill="black")
        for j,im in enumerate((target,initial,corrected)):
            sheet.paste(im.convert("RGB"),(SIDE*j,y+24))
    sheet.save(out/"comparison.png")
    with (out/"scores.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=["index","label","baseline_error","corrected_error","delta","verdict"])
        writer.writeheader()
        for row in records:writer.writerow({k:row[k] for k in writer.fieldnames})
    result={"schema":SCHEMA,"cases":len(records),"improved":sum(r["verdict"]=="IMPROVED" for r in records),
            "worsened":sum(r["verdict"]=="WORSENED" for r in records),
            "ties":sum(r["verdict"]=="TIE" for r in records),
            "mean_delta":sum(r["delta"] for r in records)/len(records),
            "mean_baseline_error":sum(r["baseline_error"] for r in records)/len(records),
            "mean_corrected_error":sum(r["corrected_error"] for r in records)/len(records),
            "comparison_png_sha256":digest(out/"comparison.png"),
            "policy_sha256":digest(policy),"manifest_sha256":digest(manifest),
            "frozen_policy":True,"no_test_feedback_used_for_learning":True,
            "samples":records,"native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (out/"summary.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def main():
    parser=argparse.ArgumentParser()
    for arg in ("memory","policy","manifest","out"):parser.add_argument("--"+arg,required=True)
    a=parser.parse_args();r=benchmark(a.memory,a.policy,a.manifest,a.out)
    print(json.dumps({k:r[k] for k in ("cases","improved","worsened","ties","mean_delta")}))
if __name__=="__main__":main()
