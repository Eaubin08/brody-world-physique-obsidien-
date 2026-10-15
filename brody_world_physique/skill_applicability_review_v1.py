"""F1D contradiction review: keep a learned skill, suspend unsafe automatic use.

A first blind examination is finished before contradiction feedback is allowed to
revise applicability. Revision is evaluated on a distinct fresh exam, and the
unobservable reversal is NOT pretended to be predictable from earlier frames.
"""
from __future__ import annotations
import argparse, json, hashlib, math
from pathlib import Path
from .experiential_skill_learning_v1 import run as teach, inspect_skill, sha, save, seal
from .f1b_physical_memory_bridge_v1 import episode
from .image_experience_guided_motion_v2 import forecast
from .image_multihypothesis_motion_memory_v1 import read
from .image_observed_motion_school_v1 import analyze, render
from .fusion_f9_intensive_education_v0 import digest

RETEST=(
    ("retention_new_height",(13,17,23,31,42)),
    ("retention_other_start",(6,10,16,24,35)),
    ("adversarial_hidden_reversal",(19,23,29,37,33)),
)
def check(policy):
    body={k:v for k,v in policy.items() if k!="digest"}
    if policy.get("digest")!=digest(body) or policy.get("schema")!="BRODY_SKILL_APPLICABILITY_REVIEW_V1":
        raise ValueError("INVALID_REVIEW")
    if policy.get("native_memory_write") is not False or policy.get("canonical_promotion") is not False or policy.get("decision_authority")!="KX108_ONLY":
        raise ValueError("INVALID_AUTHORITY")
    return policy

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    previous=teach(root/"prior_training")
    frozen_skill_file=root/"prior_training"/previous["skill_file"]
    skill=inspect_skill(frozen_skill_file)
    contradiction=next(r for r in previous["exam"] if r["case"]=="contradiction_reversal")
    if contradiction["utility_px"]>=0:raise ValueError("NO_CONTRADICTION_EVIDENCE")
    # Revision AFTER the historical blind exam, with explicit provenance.
    policy=seal({"schema":"BRODY_SKILL_APPLICABILITY_REVIEW_V1",
        "prior_skill_digest":previous["skill_digest"],
        "review_trigger":{"case":"contradiction_reversal",
                          "observed_utility_px":contradiction["utility_px"]},
        "context":skill["context"],
        "preconditions":skill["preconditions"],
        "dependencies":skill["dependencies"],
        "rule":"HOLD_IF_UNOBSERVABLE_TRANSITION_NOT_EXCLUDED",
        "reason":"The first four accelerating frames cannot rule out a later reversal.",
        "skill_preserved_not_destroyed":True,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"})
    check(policy)
    save(root/"candidate_applicability_review.json",policy)
    baseline_hashes=set()
    for case in previous["lessons"]:
        # Prior report retains only lesson metadata; use prior TRAIN manifests.
        manifest=root/"prior_training"/case["lesson"]/"manifest.json"
        baseline_hashes.update(sha(row["file"]) for row in read(manifest)["observations"])
        baseline_hashes.add(sha(root/"prior_training"/case["lesson"]/"frame_4.png"))
    result=[]
    for case,ys in RETEST:
        manifest,truth=episode(root,case,ys,x=46)
        if sha(truth) in baseline_hashes or any(sha(row["file"]) in baseline_hashes for row in read(manifest)["observations"]):
            raise ValueError("RETEST_TRAIN_LEAK")
        path=root/("blind_"+case)
        local=forecast(manifest,path)
        sealed=read(path/"sealed_forecast.json")
        accel=sealed["hypotheses"]["ACCELERATION"]
        applicable=local["context"]==skill["context"] and len(skill["residuals"])>=2
        dx=sum(r["dx"] for r in skill["residuals"])/len(skill["residuals"]) if applicable else 0.
        dy=sum(r["dy"] for r in skill["residuals"])/len(skill["residuals"]) if applicable else 0.
        shadow={**accel,"x":accel["x"]+dx,"y":accel["y"]+dy}
        render(shadow,path/"shadow_candidate.png")
        hold=applicable and policy["rule"]=="HOLD_IF_UNOBSERVABLE_TRANSITION_NOT_EXCLUDED"
        commit=seal({"case":case,"local_prediction":accel,"shadow_prediction":shadow,
            "review_digest":policy["digest"],"selected_for_external_use":None if hold else local["selected"],
            "status":"HOLD" if hold else local["mode"],
            "sha_forecast":sha(path/"sealed_forecast.json"),"sha_shadow":sha(path/"shadow_candidate.png"),
            "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"})
        save(path/"pre_feedback_commit.json",commit)
        real=analyze(truth)
        local_error=round(math.hypot(real["x"]-accel["x"],real["y"]-accel["y"]),5)
        shadow_error=round(math.hypot(real["x"]-shadow["x"],real["y"]-shadow["y"]),5)
        if commit["sha_forecast"]!=sha(path/"sealed_forecast.json") or commit["sha_shadow"]!=sha(path/"shadow_candidate.png"):
            raise ValueError("FORECAST_MUTATED")
        result.append({"case":case,"status":commit["status"],
            "base_error_px":local_error,"shadow_candidate_error_px":shadow_error,
            "shadow_utility_px":round(local_error-shadow_error,5),
            "candidate_preserved":True,"committed_before_truth":True})
    report={"schema":"BRODY_CONTRADICTION_SKILL_REVIEW_EXAM_V1",
        "history_verdict":previous["verdict"],
        "prior_positive_transfers":previous["positive_transfer_cases"],
        "prior_negative_transfers":previous["negative_transfer_cases"],
        "review_trigger":policy["review_trigger"],
        "retest":result,
        "retest_holds":sum(r["status"]=="HOLD" for r in result),
        "retest_coverage":sum(r["status"]!="HOLD" for r in result)/len(result),
        "original_skill_digest_unchanged":sha(frozen_skill_file)==sha(root/"prior_training"/"candidate_skill.json"),
        "applicability_bounded_by_non_identifiability":True,
        "adaptive_selective_risk_proven":False,
        "contradiction_prediction_proven":False,
        "real_world_transfer_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"F1D_FAIL_CLOSED_CONTRADICTION_REVIEW_CANDIDATE"}
    save(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args();r=run(args.out)
    print(json.dumps({"verdict":r["verdict"],"retest_holds":r["retest_holds"],
                      "retest_coverage":r["retest_coverage"]},indent=2))
if __name__=="__main__":main()
