"""F1G intervention laboratory: independent marker and physical-contact factors.

A pre-outcome intervention on the decorative marker is not a physical
intervention. A second factor models an observable contact event in a controlled
simulator. The experiment distinguishes both using factorial matched pairs.
Causal statements remain local to the synthetic simulator.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from .experiential_skill_learning_v1 import save, seal, sha
from .observed_cue_education_v1 import build, observe_marker
from .image_experience_guided_motion_v2 import forecast
from .image_multihypothesis_motion_memory_v1 import read
from .image_observed_motion_school_v1 import analyze

# Each 2x2 block keeps observed ball history fixed. Two controlled variables
# are independently assigned before rendering the future state. In this toy
# simulator marker has no physical effect; contact changes the continuation.
TRAIN=((10,14,20,28),(12,16,22,30))
TEST=((16,20,26,34),(18,22,28,36))
def continuation(history,contact):
    y=history[-1]
    velocity=history[-1]-history[-2]
    accel=(history[-1]-history[-2])-(history[-2]-history[-3])
    next_y=y+velocity+accel+1
    return next_y-15 if contact else next_y

def prepare(root,name,history,marker,contact,x):
    values=tuple(history)+(continuation(history,contact),)
    manifest,truth=build(root,name,values,marker,x)
    last=Path(read(manifest)["observations"][-1]["file"])
    observed=observe_marker(last)
    if observed!=marker:raise ValueError("MARKER_READ_FAILED")
    forecast_dir=root/("forecast_"+name)
    forecast(manifest,forecast_dir)
    predicted=read(forecast_dir/"sealed_forecast.json")["hypotheses"]["ACCELERATION"]
    return forecast_dir,truth,observed,predicted

def group(root,prefix,histories):
    records=[]
    for hi,history in enumerate(histories):
        for contact in (False,True):
            for marker in (False,True):
                name=f"{prefix}_{hi}_contact{int(contact)}_marker{int(marker)}"
                folder,truth,observed,predicted=prepare(root,name,history,marker,contact,20+hi*12)
                commit=seal({"case":name,"history_id":hi,"marker_observed":observed,
                    "predicted":predicted,"forecast_sha256":sha(folder/"sealed_forecast.json"),
                    "native_memory_write":False,"canonical_promotion":False,
                    "decision_authority":"KX108_ONLY"})
                save(folder/"pre_feedback_commit.json",commit)
                actual=analyze(truth)
                if commit["forecast_sha256"]!=sha(folder/"sealed_forecast.json"):
                    raise ValueError("FORECAST_MUTATED")
                records.append({"case":name,"history_id":hi,"marker":marker,
                    "contact":contact,"residual_y":actual["y"]-predicted["y"],
                    "source_sha256":sha(truth),"committed_before_feedback":True})
    return records

def effects(rows):
    # Factorial average difference, not a universal causal estimate.
    def mean(flag,value):
        vals=[r["residual_y"] for r in rows if r[flag]==value]
        return sum(vals)/len(vals)
    return {"marker_effect_px":mean("marker",True)-mean("marker",False),
            "contact_effect_px":mean("contact",True)-mean("contact",False)}

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    training=group(root,"train",TRAIN)
    training_effects=effects(training)
    # Before looking at TEST, infer the responsive factor from the TRAIN factorial.
    marker_informative=abs(training_effects["marker_effect_px"])>2
    contact_informative=abs(training_effects["contact_effect_px"])>2
    policy=seal({"schema":"BRODY_F1G_FACTORIAL_POLICY_V1",
        "marker_effect_px":training_effects["marker_effect_px"],
        "contact_effect_px":training_effects["contact_effect_px"],
        "marker_informative":marker_informative,
        "contact_informative":contact_informative,
        "intervention_evidence":"CONTROLLED_SYNTHETIC_FACTORIAL",
        "contact_visible_to_perception":False,
        "contact_available_to_inference":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"})
    save(root/"candidate_factorial_policy.json",policy)
    exams=group(root,"test",TEST)
    # Evaluate paired interventions, not pretend contact can be inferred visually.
    observed_effects=effects(exams)
    train_sources={r["source_sha256"] for r in training}
    if any(r["source_sha256"] in train_sources for r in exams):
        raise ValueError("TRAIN_TEST_TRUTH_LEAK")
    outcome={"schema":"BRODY_F1G_FACTORIAL_CAUSAL_AUDIT_V1",
        "training_effects":training_effects,"test_effects":observed_effects,
        "policy":policy,"training_cases":len(training),"heldout_cases":len(exams),
        "marker_discarded_as_causal_factor":not marker_informative,
        "contact_intervention_detected_in_controlled_test":contact_informative,
        "contact_unobservable_at_prediction_time":True,
        "visible_marker_not_assumed_causal":True,
        "factorial_not_real_physics_proof":True,
        "p149_p150_p152_integrated":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"F1G_CONTROLLED_FACTORIAL_ASSOCIATION_AUDIT_ONLY"}
    save(root/"MASTER_REPORT.json",outcome)
    return outcome

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);args=p.parse_args()
    report=run(args.out)
    print(json.dumps({"verdict":report["verdict"],"training_effects":report["training_effects"],
        "test_effects":report["test_effects"]},indent=2))
if __name__=="__main__":main()
