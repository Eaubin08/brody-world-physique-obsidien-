"""P2.9j: audit a frozen memory-first/spatial-fallback choice on P2.9h receipts.

No new predictions, no learning, and no use of scored errors for the choice.
Post-hoc policy analysis only; pre-registration on an independent suite required
before claiming a prospective advantage.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from math import hypot
from statistics import mean

SCHEMA="BRODY_P29J_FROZEN_HYBRID_REPLAY_V0"
MEM="A4_FROZEN_MEMORY"
SPATIAL="A1_SPATIAL_DELTA"

def audit(original):
    if original.get("schema")!="BRODY_P29H_PRECOMMITTED_POSITION_ABLATION_V0":
        raise ValueError("wrong schema")
    if original.get("test_feedback_used_for_learning") is not False or original.get("native_memory_write") is not False:
        raise ValueError("invalid source contract")
    if original.get("decision_authority")!="KX108_ONLY":
        raise ValueError("authority drift")
    forecasts={}
    for p in original["precommit"]:
        k=(p["clip"],p["future_frame"])
        if k in forecasts:raise ValueError("duplicate episode")
        if MEM not in p["predictions"] or SPATIAL not in p["predictions"]:
            raise ValueError("missing original precommit")
        m=p["predictions"][MEM]
        s=p["predictions"][SPATIAL]
        arm=MEM if m is not None else SPATIAL if s is not None else None
        forecasts[k]={"arm":arm,"xy":m if m is not None else s}
    scores={}
    for row in original["scores"]:
        key=(row["clip"],row["frame"]*6)
        if row["arm"] not in (MEM,SPATIAL):continue
        pair=key,row["arm"]
        if pair in scores:raise ValueError("duplicate evaluation")
        scores[pair]=row["error_px"]
    if len(forecasts)!=original["shared_test_cases"]:raise ValueError("incomplete episodes")
    results=[]
    for key,item in sorted(forecasts.items()):
        if (key,MEM) not in scores or (key,SPATIAL) not in scores:
            raise ValueError("missing scored arm")
        err=scores[(key,item["arm"])] if item["arm"] else None
        # A missing future observation produces a null score even when a
        # prediction was validly sealed. This is not a HOLD or a zero error.
        # Both arm scores must be null when the future observation is absent.
        observed = scores[(key,MEM)] is not None or scores[(key,SPATIAL)] is not None
        if observed and item["arm"] is not None and err is None:
            raise ValueError("selected arm has no score despite observed future")
        results.append({"clip":key[0],"frame":key[1],"chosen_arm":item["arm"],
                        "prediction_xy":item["xy"],"future_observed":observed,
                        "error_px":err})
    errors=[r["error_px"] for r in results if r["error_px"] is not None]
    observable=[r for r in results if r["future_observed"]]
    issued=sum(r["chosen_arm"] is not None for r in results)
    unscorable=sum(r["chosen_arm"] is not None and not r["future_observed"] for r in results)
    choices={MEM:sum(r["chosen_arm"]==MEM for r in results),
             SPATIAL:sum(r["chosen_arm"]==SPATIAL for r in results),
             "HOLD":sum(r["chosen_arm"] is None for r in results)}
    return {"schema":SCHEMA,"policy":"USE_FROZEN_MEMORY_IF_PROPOSED_ELSE_SPATIAL_ELSE_HOLD",
            "status":"POSTHOC_POLICY_REPLAY_NOT_PROSPECTIVE_VALIDATION",
            "total":len(results),"issued_predictions":issued,
            "issued_coverage":issued/len(results) if results else 0,
            "future_observed_cases":len(observable),"unscorable_predictions":unscorable,
            "accepted":len(errors),
            "coverage":len(errors)/len(observable) if observable else 0,
            "mean_error_px":mean(errors) if errors else None,
            "catastrophic_over_10px":sum(e>10 for e in errors),
            "choices":choices,"rows":results,"changed_original_proposals":False,
            "test_errors_used_to_choose":False,"independent_data_validation":False,
            "multirepresentation_fusion_proven":False,"world_physics_learned":False,
            "native_memory_write":False,"b8_promotion":False,"decision_authority":"KX108_ONLY"}

def produce(source,out,verify=False):
    raw=Path(source).read_bytes()
    result=audit(json.loads(raw))
    result["input_sha256"]=hashlib.sha256(raw).hexdigest()
    dest=Path(out)
    if verify:
        if result!=json.loads(dest.read_text(encoding="utf-8")):
            raise ValueError("replay mismatch")
        return {"verified":True,"total":result["total"]}
    if dest.exists():raise ValueError("output exists")
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return {k:result[k] for k in ("status","total","issued_predictions","issued_coverage","future_observed_cases","unscorable_predictions","accepted","coverage","mean_error_px","catastrophic_over_10px","choices")}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True);p.add_argument("--out",required=True)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    print(json.dumps(produce(a.source,a.out,a.verify)))
if __name__=="__main__":main()
