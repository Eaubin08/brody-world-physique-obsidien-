"""P2.12b: learn a fixed global gesture shift from TRAIN receipts and replay on TEST.

Shift selection is TRAIN-only. TEST reference, if present, is opened only after
both PNGs have been saved; no TEST feedback modifies the frozen policy.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .drawing_school_v1 import render
from .p211b_frozen_gesture_transfer_v0 import read as read_memory
from .p211c_gesture_recomposition_v0 import _remap
from .p212a_bounded_gesture_revision_v0 import SHIFTS,shifted
from .p210a_visual_loop_contract_v0 import digest,open_rgba,pixel_error
from .p210d_visual_error_memory_bridge_v0 import hexdigest

POLICY_SCHEMA="BRODY_P212B_FROZEN_SHIFT_POLICY_V0"
REPORT_SCHEMA="BRODY_P212B_BLIND_TRANSFER_V0"

def train(memory,train_receipts,policy_path):
    out=Path(policy_path)
    if out.exists():raise ValueError("policy exists")
    read_memory(memory)
    if not isinstance(train_receipts,list) or not 2<=len(train_receipts)<=40:
        raise ValueError("TRAIN receipt count")
    used=set();cost=[0]*len(SHIFTS);all_receipts=[]
    for receipt_path in train_receipts:
        path=Path(receipt_path).resolve(strict=True)
        if path in used:raise ValueError("duplicate TRAIN receipt")
        used.add(path)
        rec=json.loads(path.read_text(encoding="utf-8"))
        if rec.get("schema")!="BRODY_P212A_BOUNDED_GESTURE_REVISION_V0" or rec.get("memory_sha256")!=digest(memory) or not rec.get("proposals_committed_before_reference_scoring"):
            raise ValueError("invalid TRAIN receipt")
        attempts=rec.get("attempts")
        if not isinstance(attempts,list) or len(attempts)!=len(SHIFTS):
            raise ValueError("candidate mismatch")
        for i,row in enumerate(attempts):
            if row.get("index")!=i or row.get("shift")!=list(SHIFTS[i]) or row.get("sha256")!=digest(row["path"]):
                raise ValueError("TRAIN evidence altered")
            if type(row.get("error_px")) is not int or row["error_px"]<0:
                raise ValueError("invalid error")
            cost[i]+=row["error_px"]
        all_receipts.append({"path_sha256":digest(path),"layout_sha256":rec["layout_sha256"],
                             "teacher_reference_sha256":rec["reference_sha256"]})
    if len({r["layout_sha256"] for r in all_receipts})!=len(all_receipts):
        raise ValueError("duplicate TRAIN layout")
    best=min(range(len(cost)),key=lambda i:(cost[i],i))
    policy={"schema":POLICY_SCHEMA,"memory_sha256":digest(memory),
            "train_receipts":all_receipts,"train_count":len(all_receipts),
            "cost_by_shift":cost,"shift_index":best,"shift":list(SHIFTS[best]),
            "frozen_before_test":True,"native_memory_write":False,
            "decision_authority":"KX108_ONLY"}
    policy["receipt_digest"]=hexdigest(policy)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(policy,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return policy

def replay(memory,policy_path,layout,out_dir,reference=None):
    out=Path(out_dir)
    if out.exists():raise ValueError("output exists")
    _,motor=read_memory(memory)
    policy=json.loads(Path(policy_path).read_text(encoding="utf-8"))
    if policy.get("schema")!=POLICY_SCHEMA or policy.get("receipt_digest")!=hexdigest({k:v for k,v in policy.items() if k!="receipt_digest"}):
        raise ValueError("policy altered")
    i=policy["shift_index"]
    if type(i) is not int or not 0<=i<len(SHIFTS) or policy.get("shift")!=list(SHIFTS[i]) or policy.get("memory_sha256")!=digest(memory):
        raise ValueError("policy mismatch")
    layout_sha=digest(layout)
    if any(row["layout_sha256"]==layout_sha for row in policy["train_receipts"]):
        raise ValueError("TEST layout already in TRAIN")
    spec=json.loads(Path(layout).read_text(encoding="utf-8"))
    boxes=spec.get("boxes")
    if spec.get("schema")!="BRODY_P211C_LAYOUT_V0" or not isinstance(boxes,list) or not 1<=len(boxes)<=12:raise ValueError("layout")
    gestures=tuple(g for b in boxes for g in _remap(motor,b))
    out.mkdir(parents=True)
    base=out/"baseline.png";candidate=out/"frozen-policy.png"
    render(gestures).save(base)
    render(shifted(gestures,*SHIFTS[i])).save(candidate)
    summary={"schema":REPORT_SCHEMA,"policy_sha256":digest(policy_path),
             "memory_sha256":digest(memory),"layout_sha256":layout_sha,
             "shift":list(SHIFTS[i]),"baseline_sha256":digest(base),
             "candidate_sha256":digest(candidate),"target_unseen_for_policy_selection":True,
             "test_feedback_used_for_learning":False,"native_memory_write":False,
             "decision_authority":"KX108_ONLY"}
    if reference is not None:
        sha=digest(reference)
        if any(row["teacher_reference_sha256"]==sha for row in policy["train_receipts"]):
            raise ValueError("TEST target duplicates TRAIN teacher")
        target=open_rgba(reference)
        if target.size!=render(gestures).size:raise ValueError("target dimensions")
        b=pixel_error(target,open_rgba(base));c=pixel_error(target,open_rgba(candidate))
        summary.update({"test_target_sha256":sha,"baseline_error":b,"policy_error":c,
                        "delta":c-b,"verdict":"IMPROVED" if c<b else "WORSENED" if c>b else "TIE"})
    (out/"report.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return summary

def main():
    p=argparse.ArgumentParser();p.add_argument("--memory",required=True)
    p.add_argument("--train-receipts",nargs="+");p.add_argument("--policy",required=True)
    p.add_argument("--layout");p.add_argument("--out");p.add_argument("--reference")
    a=p.parse_args()
    if a.train_receipts and not a.layout and not a.out:
        result=train(a.memory,a.train_receipts,a.policy)
    elif not a.train_receipts and a.layout and a.out:
        result=replay(a.memory,a.policy,a.layout,a.out,a.reference)
    else:p.error("TRAIN: --train-receipts; TEST: --layout and --out")
    print(json.dumps({"schema":result["schema"],"shift":result["shift"]}))
if __name__=="__main__":main()
