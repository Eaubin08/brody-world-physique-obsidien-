"""F1E honest selective-risk audit: confidence is empirical, not a future-event oracle.

Split prior examples into calibration and unseen tests. Predict before ground truth,
compare HOLD-all, ACT-all, and a bounded selective policy. No automatic promotion.
"""
from __future__ import annotations
import argparse, math, json
from pathlib import Path
from .experiential_skill_learning_v1 import run as teach, inspect_skill, save, sha, seal
from .f1b_physical_memory_bridge_v1 import episode
from .image_experience_guided_motion_v2 import forecast
from .image_multihypothesis_motion_memory_v1 import read
from .image_observed_motion_school_v1 import analyze

CALIBRATE=(("cal_regular_A",(12,16,22,30,41)),("cal_reversal_A",(12,16,22,30,26)),
           ("cal_regular_B",(15,19,25,33,44)),("cal_reversal_B",(15,19,25,33,29)))
TEST=(("eval_regular_A",(10,14,20,28,39)),("eval_reversal_A",(10,14,20,28,24)),
      ("eval_regular_B",(18,22,28,36,47)),("eval_reversal_B",(18,22,28,36,32)))
def commit_prediction(root,name,ys,skill,x):
    manifest,truth=episode(root,name,ys,x=x)
    folder=root/("prediction_"+name)
    result=forecast(manifest,folder)
    sealed=read(folder/"sealed_forecast.json")
    base=sealed["hypotheses"]["ACCELERATION"]
    apply=result["context"]==skill["context"] and len(skill["residuals"])>=2
    dy=sum(r["dy"] for r in skill["residuals"])/len(skill["residuals"]) if apply else 0
    dx=sum(r["dx"] for r in skill["residuals"])/len(skill["residuals"]) if apply else 0
    candidate={**base,"x":base["x"]+dx,"y":base["y"]+dy}
    # Directly keep the numerical candidate as a sealed commitment.
    doc=seal({"case":name,"context":result["context"],"candidate":candidate,
              "base":base,"skill_applied":apply,
              "forecast_sha256":sha(folder/"sealed_forecast.json"),
              "native_memory_write":False,"canonical_promotion":False,
              "decision_authority":"KX108_ONLY"})
    save(folder/"pre_feedback_commit.json",doc)
    return folder,truth,doc
def grade(folder,truth,doc):
    if doc["forecast_sha256"]!=sha(folder/"sealed_forecast.json"):
        raise ValueError("FORECAST_MUTATED")
    true=analyze(truth)
    p=doc["candidate"]
    return round(math.hypot(p["x"]-true["x"],p["y"]-true["y"]),5)
def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    old=teach(root/"historical_training")
    skill=inspect_skill(root/"historical_training"/old["skill_file"])
    calib=[]
    for i,(name,ys) in enumerate(CALIBRATE):
        folder,truth,doc=commit_prediction(root,name,ys,skill,x=38+i)
        error=grade(folder,truth,doc)
        calib.append({"case":name,"error_px":error,"context":doc["context"]})
    # Conservative reliability: within this indistinguishable observation family,
    # both continuations occur. Worst calibration error is an empirical risk bound,
    # not a probabilistic guarantee for future data.
    worst=max(x["error_px"] for x in calib)
    threshold=2.0  # Declared before fresh evaluation; units = pixels.
    can_select=worst<=threshold
    policy=seal({"schema":"BRODY_EMPIRICAL_SELECTIVE_POLICY_V1",
        "threshold_px":threshold,"calibration_max_error_px":worst,
        "calibration_cases":len(calib),"selection_allowed":can_select,
        "decision_rule":"ACT_CANDIDATE_ONLY_IF_CALIBRATION_WORST_LE_THRESHOLD",
        "no_statistical_coverage_guarantee":True,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"})
    save(root/"policy.json",policy)
    records=[]
    for i,(name,ys) in enumerate(TEST):
        folder,truth,doc=commit_prediction(root,name,ys,skill,x=48+i)
        status="CANDIDATE" if can_select and doc["skill_applied"] else "HOLD"
        selected=seal({"case":name,"status":status,"policy_digest":policy["digest"],
            "pre_feedback_digest":doc["digest"],"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"})
        save(folder/"selection_before_truth.json",selected)
        error=grade(folder,truth,doc)
        records.append({"case":name,"status":status,"candidate_error_px":error,
            "expected_risk_bound_px":worst,"committed_before_feedback":True})
    accepted=[r for r in records if r["status"]=="CANDIDATE"]
    report={"schema":"BRODY_F1E_SELECTIVE_RISK_AUDIT_V1",
        "calibration":calib,"policy":policy,"exam":records,
        "coverage":len(accepted)/len(records),
        "selective_mean_error_px":round(sum(r["candidate_error_px"] for r in accepted)/len(accepted),5) if accepted else None,
        "all_candidate_mean_error_px":round(sum(r["candidate_error_px"] for r in records)/len(records),5),
        "hold_all_coverage":0.0,"act_all_coverage":1.0,
        "positive_transfer_previously_observed":old["positive_transfer_cases"],
        "negative_transfer_previously_observed":old["negative_transfer_cases"],
        "hidden_reversal_not_detectable_from_observation":True,
        "calibration_guarantee":False,"physical_understanding_proven":False,
        "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY",
        "verdict":"F1E_EMPIRICAL_SELECTIVE_HOLD_IF_INSUFFICIENT_EVIDENCE"}
    save(root/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"coverage":r["coverage"],
        "calibration_max_error_px":r["policy"]["calibration_max_error_px"],
        "all_candidate_mean_error_px":r["all_candidate_mean_error_px"]},indent=2))
if __name__=="__main__":main()
