"""Brody P2.4: adversarial representation hierarchy and contextual fluctuation probes.

No real image perception is claimed. These are deliberately small, controlled
feature-track fixtures used to falsify the *interpretation* contract before
connecting F16 pixels / MMonde / F12 dynamics. They are not a learned model.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from statistics import median

SCHEMA="BRODY_P24_CONTEXTUAL_FLUCTUATION_V0"


def interpret(observation:dict)->dict:
    """Avoid conflating camera pixels, object world motion, and unknown noise."""
    if observation.get("source_kind")!="SIMULATED" or observation.get("schema")!=SCHEMA:
        raise ValueError("invalid input provenance")
    apparent=observation["object_image_displacement"]
    background=observation.get("background_displacements",[])
    # A raw image observation lives in the camera plane; never call it world truth.
    if not isinstance(apparent,(int,float)) or isinstance(apparent,bool):
        raise ValueError("invalid apparent displacement")
    if any(not isinstance(x,(int,float)) or isinstance(x,bool) for x in background):
        raise ValueError("invalid background measurements")
    if observation.get("time_delta_s",0)<=0 or observation.get("view_frame")!="CAMERA_X":
        raise ValueError("unknown time frame or units")
    if observation.get("alignment_known") is not True:
        return {"status":"HOLD_FRAME_ALIGNMENT_UNKNOWN","world_displacement":None,
                "apparent_displacement":apparent,"used_background":False}
    if len(background)<3:
        return {"status":"HOLD_INSUFFICIENT_CONTEXT","world_displacement":None,
                "apparent_displacement":apparent,"used_background":False}
    estimated=median(background)
    residuals=[abs(x-estimated) for x in background]
    # An adversarial inconsistent signal should remain available, not silently
    # crushed into a pooled point estimate.
    if sum(d<=1.0 for d in residuals)<(len(background)*0.75):
        return {"status":"HOLD_CONFLICTING_CONTEXT","world_displacement":None,
                "apparent_displacement":apparent,"used_background":False}
    return {"status":"CANDIDATE_CONTEXTUAL_CORRECTION",
            "world_displacement":apparent-estimated,
            "apparent_displacement":apparent,"camera_shift_estimate":estimated,
            "used_background":True,"source_independent":False,
            "physical_causality_proven":False}


def fixtures():
    """Paired apparent movements; differing context, plus hostile variations."""
    base={"schema":SCHEMA,"source_kind":"SIMULATED","view_frame":"CAMERA_X",
          "time_delta_s":0.25,"alignment_known":True,
          "object_image_displacement":10.0}
    cases=[
      ("moving_object_fixed_camera",{**base,"background_displacements":[0,0,0,0,0]},10.0),
      ("fixed_object_moving_camera",{**base,"background_displacements":[10,10,10,10,10]},0.0),
      ("both_moving",{**base,"background_displacements":[4,4,4,4,4]},6.0),
      ("outlier_recoverable",{**base,"background_displacements":[4,4,4,4,85]},6.0),
      ("ambiguous_conflict",{**base,"background_displacements":[4,-8,17,0,22]},None),
      ("missing_context",{**base,"background_displacements":[]},None),
      ("unknown_alignment",{**base,"alignment_known":False,
                              "background_displacements":[10,10,10]},None),
    ]
    return cases


def evaluate():
    results=[]
    for name,observation,truth in fixtures():
        prediction=interpret(observation)
        eligible=truth is not None
        success=(prediction["world_displacement"] is None if not eligible
                 else prediction["world_displacement"]==truth)
        results.append({"case":name,"expected_world_displacement":truth,
                        "status":prediction["status"],
                        "estimated_world_displacement":prediction["world_displacement"],
                        "passed":success})
    return {"schema":SCHEMA,"source_kind":"SIMULATED",
            "evaluations":results,
            "passed":sum(x["passed"] for x in results),
            "total":len(results),
            "all_pass":all(x["passed"] for x in results),
            "knowledge_learned":False,"raw_pixels_tested":False,
            "physical_world_understood":False,
            "native_memory_write_allowed":False,
            "decision_authority":"KX108_ONLY"}


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args(argv)
    report=evaluate()
    data=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if a.verify:
        if a.out.read_text(encoding="utf-8")!=data:
            raise ValueError("mismatched P2.4 replay")
    else:
        if a.out.exists():
            raise ValueError("refuse overwrite")
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(data,encoding="utf-8")
    print(json.dumps({"passed":report["passed"],"total":report["total"],
                      "verified":a.verify,"all_pass":report["all_pass"]}))
    return 0 if report["all_pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
