"""P2.12d: conservative TRAIN-only gate for deciding whether to apply a shift.

No context signal predicts the required shift yet: on mixed TRAIN evidence,
the safe decision is HOLD. A uniform positive TRAIN gain permits ACT; test
reference is opened after generated candidates and decision have been sealed.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from .p210a_visual_loop_contract_v0 import digest,open_rgba,pixel_error
from .p210d_visual_error_memory_bridge_v0 import hexdigest
from .p212b_frozen_shift_transfer_v0 import replay
from .drawing_school_v0 import SIDE

SCHEMA="BRODY_P212D_TRAIN_GATE_V0"
def fit(policy_path,train_receipts,out_path):
    out=Path(out_path)
    if out.exists():raise ValueError("gate exists")
    policy=json.loads(Path(policy_path).read_text(encoding="utf-8"))
    if policy.get("schema")!="BRODY_P212B_FROZEN_SHIFT_POLICY_V0" or policy.get("receipt_digest")!=hexdigest({k:v for k,v in policy.items() if k!="receipt_digest"}):
        raise ValueError("policy invalid")
    idx=policy["shift_index"]
    if type(idx) is not int or not 0<=idx<5:raise ValueError("invalid shift")
    known={r["path_sha256"] for r in policy["train_receipts"]}
    receipts=list(train_receipts)
    if len(receipts)!=len(known):raise ValueError("TRAIN count mismatch")
    seen=set();gains=[]
    for p in receipts:
        p=Path(p)
        hash_=digest(p)
        if hash_ not in known or hash_ in seen:raise ValueError("unknown or duplicate TRAIN")
        seen.add(hash_)
        rec=json.loads(p.read_text(encoding="utf-8"))
        if rec.get("schema")!="BRODY_P212A_BOUNDED_GESTURE_REVISION_V0" or rec.get("memory_sha256")!=policy["memory_sha256"]:
            raise ValueError("TRAIN invalid")
        entries=rec["attempts"]
        if len(entries)!=5 or any(r.get("index")!=i or r.get("sha256")!=digest(r["path"]) for i,r in enumerate(entries)):
            raise ValueError("TRAIN proposal altered")
        gains.append(entries[0]["error_px"]-entries[idx]["error_px"])
    decision="ACT" if idx!=0 and all(g>0 for g in gains) else "HOLD"
    result={"schema":SCHEMA,"policy_sha256":digest(policy_path),
            "source_train_sha256":sorted(seen),"train_gains":gains,
            "authority":"KX108_ONLY","decision":decision,
            "rule":"ACT_ONLY_IF_ALL_TRAIN_GAINS_POSITIVE_AND_NONZERO_SHIFT",
            "no_contextual_visual_classification":True,"native_memory_write":False}
    result["receipt_digest"]=hexdigest(result)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def evaluate(memory,policy,gate,manifest,out_dir):
    out=Path(out_dir)
    if out.exists():raise ValueError("output exists")
    g=json.loads(Path(gate).read_text(encoding="utf-8"))
    if g.get("schema")!=SCHEMA or g.get("receipt_digest")!=hexdigest({k:v for k,v in g.items() if k!="receipt_digest"}) or g["policy_sha256"]!=digest(policy):
        raise ValueError("invalid gate")
    if g["decision"] not in ("ACT","HOLD"):raise ValueError("invalid decision")
    cfg=json.loads(Path(manifest).read_text(encoding="utf-8"))
    cases=cfg.get("cases")
    if cfg.get("schema")!="BRODY_P212C_CASES_V0" or not isinstance(cases,list) or not 2<=len(cases)<=40:
        raise ValueError("TEST manifest")
    out.mkdir(parents=True)
    pending=[]
    for i,c in enumerate(cases):
        sub=out/f"case{i}"
        result=replay(memory,policy,c["layout"],sub)
        # Selection occurs here, before target is opened.
        chosen=sub/("frozen-policy.png" if g["decision"]=="ACT" else "baseline.png")
        pending.append({"index":i,"label":c["label"],"reference":c["reference"],
                        "decision":g["decision"],"choice_sha256":digest(chosen),
                        "baseline_sha256":result["baseline_sha256"],
                        "shift_sha256":result["candidate_sha256"],
                        "selected_path":str(chosen),"baseline_path":str(sub/"baseline.png"),
                        "target_hidden_during_decision":True})
    sheet=Image.new("RGB",(SIDE*3,len(pending)*(SIDE+24)),"white")
    pen=ImageDraw.Draw(sheet)
    for row in pending:
        i=row["index"]
        target=open_rgba(row["reference"])
        base=open_rgba(row["baseline_path"])
        selected=open_rgba(row["selected_path"])
        row["baseline_error"]=pixel_error(target,base)
        row["selected_error"]=pixel_error(target,selected)
        row["delta"]=row["selected_error"]-row["baseline_error"]
        row["verdict"]="IMPROVED" if row["delta"]<0 else "WORSENED" if row["delta"]>0 else "TIE"
        y=i*(SIDE+24)
        for j,(label,im) in enumerate((("TARGET",target),("INITIAL",base),("GATE "+g["decision"],selected))):
            pen.text((j*SIDE+2,y+2),label,fill="black")
            sheet.paste(im.convert("RGB"),(j*SIDE,y+24))
    sheet.save(out/"comparison.png")
    result={"schema":"BRODY_P212D_GATE_TEST_REPORT_V0",
        "cases":len(pending),"decision":g["decision"],
        "improved":sum(r["verdict"]=="IMPROVED" for r in pending),
        "worsened":sum(r["verdict"]=="WORSENED" for r in pending),
        "ties":sum(r["verdict"]=="TIE" for r in pending),
        "mean_delta":sum(r["delta"] for r in pending)/len(pending),
        "samples":pending,"comparison_sha256":digest(out/"comparison.png"),
        "test_feedback_used_for_learning":False,"native_memory_write":False,
        "decision_authority":"KX108_ONLY"}
    (out/"summary.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--policy",required=True)
    p.add_argument("--train-receipts",nargs="+");p.add_argument("--gate")
    p.add_argument("--memory");p.add_argument("--manifest");p.add_argument("--out",required=True)
    a=p.parse_args()
    if a.train_receipts and a.gate is None and a.memory is None and a.manifest is None:
        r=fit(a.policy,a.train_receipts,a.out)
    elif not a.train_receipts and a.gate and a.memory and a.manifest:
        r=evaluate(a.memory,a.policy,a.gate,a.manifest,a.out)
    else:p.error("TRAIN: --train-receipts --out; TEST: --gate --memory --manifest --out")
    print(json.dumps({"schema":r["schema"],"decision":r["decision"]}))
if __name__=="__main__":main()
