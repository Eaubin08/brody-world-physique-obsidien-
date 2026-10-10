"""P2.11c: composition of verified learned gestures into user-specified boxes.

The new layout is an explicit instruction (IN), not inferred from a hidden target.
No target pixels are accessed until candidate and blank-baseline PNGs are sealed.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image
from .drawing_school_v0 import SIDE
from .drawing_school_v1 import GestureV1,render
from .p211b_frozen_gesture_transfer_v0 import read as read_gesture_memory
from .p210a_visual_loop_contract_v0 import digest,open_rgba,pixel_error

SCHEMA="BRODY_P211C_COMPOSED_GESTURES_V0"

def _remap(gestures,box):
    if not isinstance(box,list) or len(box)!=4 or any(type(n)!=int for n in box):
        raise ValueError("box must contain four integers")
    x1,y1,x2,y2=box
    if not (0<=x1<x2<SIDE and 0<=y1<y2<SIDE):
        raise ValueError("invalid box")
    pts=[p for g in gestures for p in g.points]
    xmin=min(p[0] for p in pts);xmax=max(p[0] for p in pts)
    ymin=min(p[1] for p in pts);ymax=max(p[1] for p in pts)
    def remap(p):
        x=round(x1+(p[0]-xmin)*(x2-x1)/max(1,xmax-xmin))
        y=round(y1+(p[1]-ymin)*(y2-y1)/max(1,ymax-ymin))
        return (min(x2,max(x1,x)),min(y2,max(y1,y)))
    return tuple(GestureV1(points=tuple(remap(p) for p in g.points),kind=g.kind) for g in gestures)

def compose(memory,layout,out,reference=None):
    memories=read_gesture_memory(memory)
    _,gestures=memories
    spec=json.loads(Path(layout).read_text(encoding="utf-8"))
    boxes=spec.get("boxes")
    if spec.get("schema")!="BRODY_P211C_LAYOUT_V0" or not isinstance(boxes,list) or not 1<=len(boxes)<=12:
        raise ValueError("layout schema/budget")
    transformed=tuple(g for box in boxes for g in _remap(gestures,box))
    target=Path(out)
    baseline=target.with_name(target.stem+"-blank.png")
    report=target.with_suffix(".json")
    if any(p.exists() for p in (target,baseline,report)):
        raise ValueError("refuse overwriting results")
    target.parent.mkdir(parents=True,exist_ok=True)
    candidate=render(transformed)
    blank=Image.new("L",(SIDE,SIDE),255)
    candidate.save(target)
    blank.save(baseline)
    sha=digest(target)
    baseline_sha=digest(baseline)
    data={"schema":SCHEMA,"memory_sha256":digest(memory),
          "layout_sha256":digest(layout),"method":"FROZEN_GESTURE_BOX_RECOMPOSITION",
          "boxes":len(boxes),"gestures":len(transformed),
          "candidate_sha256":sha,"blank_sha256":baseline_sha,
          "candidate_path":str(target.resolve()),
          "blank_path":str(baseline.resolve()),
          "reference_unseen_during_generation":True,
          "learned_gestures_reused":True,"layout_given_by_user":True,
          "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    if reference is not None:
        gold=open_rgba(reference)
        if gold.size!=(SIDE,SIDE):raise ValueError("reference dimensions")
        data["reference_sha256"]=digest(reference)
        data["candidate_error"]=pixel_error(gold,candidate.convert("RGBA"))
        data["blank_error"]=pixel_error(gold,blank.convert("RGBA"))
        data["delta_error"]=data["candidate_error"]-data["blank_error"]
        data["verdict"]="IMPROVED" if data["delta_error"]<0 else "WORSENED" if data["delta_error"]>0 else "TIE"
    report.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return data

def main():
    p=argparse.ArgumentParser()
    for k in ("memory","layout","out"):p.add_argument("--"+k,required=True)
    p.add_argument("--reference")
    a=p.parse_args()
    d=compose(a.memory,a.layout,a.out,a.reference)
    print(json.dumps({k:d[k] for k in ("schema","boxes","gestures","candidate_sha256")}))
if __name__=="__main__":main()
