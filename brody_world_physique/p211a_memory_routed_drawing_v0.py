"""P2.11a: frozen experience-gated DRAWING on a new image.

Reads validated P2.10d memory. Only its verdicts select whether the existing
drawing_school_v1 gesture renderer is called. No TEST reference until after
candidate PNG has been committed. This is a routing integration probe, not
visual understanding or a learnt drawing policy.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image
from .drawing_school_v0 import SIDE
from .drawing_school_v1 import render,suggest_gestures_from_reference
from .p210a_visual_loop_contract_v0 import open_rgba,pixel_error,digest
from .p210d_visual_error_memory_bridge_v0 import verify_ledger

SCHEMA="BRODY_P211A_MEMORY_ROUTED_DRAWING_V0"

def run(ledger,initial,out,reference=None):
    history=verify_ledger(ledger)["entries"]
    # Reuse experience verdicts, not pixels from any past source.
    accepted=sum(e["verdict"]=="ACCEPTED" for e in history)
    method="DRAW_GESTURES_V1" if accepted else "PASS_THROUGH"
    start=open_rgba(initial)
    if start.size!=(SIDE,SIDE):raise ValueError("drawing school expects SIDE x SIDE")
    outfile=Path(out)
    if outfile.exists() or outfile.with_suffix(".json").exists():
        raise ValueError("refuse overwrite")
    if method=="DRAW_GESTURES_V1":
        candidate=render(suggest_gestures_from_reference(start))
    else:
        candidate=start.convert("L")
    outfile.parent.mkdir(parents=True,exist_ok=True)
    candidate.save(outfile)
    # The PNG must already exist before any target reference is opened.
    sealed_sha=digest(outfile)
    result={"schema":SCHEMA,"status":"LIMITED_MEMORY_ROUTING_PROBE",
            "ledger_sha256":digest(ledger),"initial_sha256":digest(initial),
            "sealed_candidate_sha256":sealed_sha,
            "selected_method":method,"prior_accepted_experiences":accepted,
            "precommitted_before_reference_scoring":True,
            "memory_influences_generation":True,
            "reverso_connected":False,"general_visual_learning_proven":False,
            "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    if reference:
        target=open_rgba(reference)
        if target.size!=start.size:raise ValueError("target dimensions")
        result["target_sha256"]=digest(reference)
        result["baseline_pixel_error"]=pixel_error(target,start)
        result["candidate_pixel_error"]=pixel_error(target,candidate.convert("RGBA"))
        result["delta_error"]=result["candidate_pixel_error"]-result["baseline_pixel_error"]
    outfile.with_suffix(".json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ledger",required=True);p.add_argument("--initial",required=True)
    p.add_argument("--out",required=True);p.add_argument("--reference")
    a=p.parse_args()
    r=run(a.ledger,a.initial,a.out,a.reference)
    print(json.dumps({k:r[k] for k in ("status","selected_method","prior_accepted_experiences")}))
if __name__=="__main__":main()
