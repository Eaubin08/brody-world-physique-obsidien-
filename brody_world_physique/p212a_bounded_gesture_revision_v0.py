"""P2.12a — supervised local gesture revision on an aligned drawing target.

First generation is sealed without reference. Then bounded candidate transforms
are proposed from the already sealed gestures (without using target pixels).
A teacher reference scores those proposals only after all PNGs exist.
Posthoc choice is NOT autonomous generation/learning and cannot validate TEST.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image
from .drawing_school_v0 import SIDE
from .drawing_school_v1 import GestureV1,render
from .p211b_frozen_gesture_transfer_v0 import read as read_memory
from .p211c_gesture_recomposition_v0 import _remap
from .p210a_visual_loop_contract_v0 import digest,pixel_error,open_rgba

SCHEMA="BRODY_P212A_BOUNDED_GESTURE_REVISION_V0"
SHIFTS=((0,0),(-2,0),(2,0),(0,-2),(0,2))
def shifted(gestures,dx,dy):
    return tuple(
        GestureV1(points=tuple((min(SIDE-1,max(0,x+dx)),min(SIDE-1,max(0,y+dy))) for x,y in g.points),kind=g.kind)
        for g in gestures)

def run(memory,layout,reference,out_dir):
    out=Path(out_dir)
    if out.exists():raise ValueError("output exists")
    _,motor=read_memory(memory)
    spec=json.loads(Path(layout).read_text(encoding="utf-8"))
    boxes=spec.get("boxes")
    if spec.get("schema")!="BRODY_P211C_LAYOUT_V0" or not isinstance(boxes,list) or not 1<=len(boxes)<=12:
        raise ValueError("layout")
    # Validate ALL boxes before any output or target evaluation.
    groups=[_remap(motor,b) for b in boxes]
    out.mkdir(parents=True)
    proposals=[]
    for idx,(dx,dy) in enumerate(SHIFTS):
        gestures=tuple(g for group in groups for g in shifted(group,dx,dy))
        candidate=render(gestures)
        path=out/f"version{idx}.png"
        candidate.save(path)
        proposals.append({"index":idx,"shift":[dx,dy],"path":str(path.resolve()),"sha256":digest(path)})
    # All proposals sealed before reference pixels are opened.
    target=open_rgba(reference)
    if target.size!=(SIDE,SIDE):raise ValueError("target dimensions")
    scored=[]
    for row in proposals:
        err=pixel_error(target,open_rgba(row["path"]))
        scored.append({**row,"error_px":err})
    baseline=scored[0]["error_px"]
    best=min(scored,key=lambda x:(x["error_px"],x["index"]))
    chosen=best if best["error_px"]<baseline else scored[0]
    state="ACCEPTED_REVISION" if chosen["index"]!=0 else ("HOLD_EQUAL" if all(x["error_px"]==baseline for x in scored) else "ROLLBACK_OR_NO_GAIN")
    receipt={"schema":SCHEMA,"status":"POSTHOC_SUPERVISED_REVISION_ONLY",
        "memory_sha256":digest(memory),"layout_sha256":digest(layout),"reference_sha256":digest(reference),
        "proposals_committed_before_reference_scoring":True,
        "source_pixel_access_during_candidate_generation":False,
        "attempts":scored,"baseline_error_px":baseline,
        "selected_index":chosen["index"],"best_error_px":chosen["error_px"],
        "verdict":state,"all_failed_attempts_preserved":True,
        "test_feedback_used_for_learning":False,"native_memory_write":False,
        "decision_authority":"KX108_ONLY"}
    (out/"report.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return receipt

def main():
    p=argparse.ArgumentParser()
    for name in ("memory","layout","reference","out"):p.add_argument("--"+name,required=True)
    a=p.parse_args()
    r=run(a.memory,a.layout,a.reference,a.out)
    print(json.dumps({k:r[k] for k in ("status","verdict","baseline_error_px","best_error_px","selected_index")}))
if __name__=="__main__":main()
