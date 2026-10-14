"""F1C paired memory-utility audit, including negative transfer and ambiguity.

Uses existing contextual motion forecast/correction APIs. No forced benefit,
no law discovery; reports coverage, model choices and realized selected errors.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from .f1b_physical_memory_bridge_v1 import episode, measured_forecast
from .image_experience_guided_motion_v2 import forecast, correct, load
from .image_multihypothesis_motion_memory_v1 import read

TRAIN=(
    ("train_accel_1",(10,14,20,28,38)),
    ("train_accel_2",(17,21,27,35,45)),
    ("train_steady_1",(11,16,21,26,31)),
    ("train_steady_2",(15,20,25,30,35)),
)
TEST=(
    ("heldout_accel",(24,28,34,42,52)),
    ("heldout_accel_shift",(9,13,19,27,37)),
    ("heldout_reversal",(21,25,31,39,35)),
    ("heldout_steady",(12,17,22,27,32)),
    ("heldout_stop",(18,23,28,33,33)),
)
def _selected_error(report,errors):
    key=report["selected"]
    return None if key is None else errors[key]
def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    memory=None
    train_rows=[]
    train_hashes=set()
    for name,ys in TRAIN:
        manifest,truth=episode(root,name,ys)
        observations=read(manifest)["observations"]
        train_hashes.update(hashlib.sha256(Path(x["file"]).read_bytes()).hexdigest() for x in observations)
        train_hashes.add(hashlib.sha256(truth.read_bytes()).hexdigest())
        folder=root/("pred_"+name)
        predicted=forecast(manifest,folder,previous=memory)
        correction=root/("teach_"+name)
        corrected=correct(folder/"sealed_forecast.json",truth,correction,previous=memory)
        memory=correction/"candidate_physics_memory.json"
        train_rows.append({"lesson":name,"context":predicted["context"],
                           "experiences":corrected["experiences"]})
    state=load(memory)
    if len({x["forecast_digest"] for x in state["experiences"]}) != len(TRAIN):
        raise ValueError("TRAIN_INDEPENDENCE_FAILED")
    records=[]
    for name,ys in TEST:
        manifest,truth=episode(root,name,ys,x=39)
        obs=read(manifest)["observations"]
        hashes={hashlib.sha256(Path(x["file"]).read_bytes()).hexdigest() for x in obs}
        truth_hash=hashlib.sha256(truth.read_bytes()).hexdigest()
        if truth_hash in train_hashes or hashes.intersection(train_hashes):
            raise ValueError("TRAIN_TEST_HASH_LEAK")
        base_folder=root/("no_memory_"+name)
        mem_folder=root/("with_memory_"+name)
        base=forecast(manifest,base_folder)
        guided=forecast(manifest,mem_folder,previous=memory)
        sealed_bytes=( (base_folder/"sealed_forecast.json").read_bytes(),
                       (mem_folder/"sealed_forecast.json").read_bytes() )
        errors_base=measured_forecast(base_folder,truth)
        errors_guided=measured_forecast(mem_folder,truth)
        if sealed_bytes != ((base_folder/"sealed_forecast.json").read_bytes(),
                            (mem_folder/"sealed_forecast.json").read_bytes()):
            raise ValueError("SEALED_FORECAST_CHANGED")
        eb=_selected_error(base,errors_base)
        eg=_selected_error(guided,errors_guided)
        records.append({"case":name,"context":base["context"],
          "no_memory":{"selected":base["selected"],"mode":base["mode"],
                       "source":base["evidence_source"],"errors_by_model_px":errors_base,
                       "selected_error_px":eb},
          "with_memory":{"selected":guided["selected"],"mode":guided["mode"],
                         "source":guided["evidence_source"],
                         "eligible_episodes":guided["eligible_episodes"],
                         "errors_by_model_px":errors_guided,"selected_error_px":eg},
          "choice_changed":base["selected"]!=guided["selected"],
          "utility_px":None if eb is None or eg is None else round(eb-eg,5),
          "forecast_sealed_before_truth":True})
    comparable=[x for x in records if x["utility_px"] is not None]
    positives=sum(x["utility_px"]>0 for x in comparable)
    negatives=sum(x["utility_px"]<0 for x in comparable)
    ties=sum(x["utility_px"]==0 for x in comparable)
    report={"schema":"BRODY_F1C_MEMORY_UTILITY_AUDIT_V1","train":train_rows,
      "test":records,"paired_cases":len(records),
      "comparable_cases":len(comparable),"improved_cases":positives,
      "degraded_cases":negatives,"unchanged_cases":ties,
      "changed_model_choices":sum(x["choice_changed"] for x in records),
      "mean_memory_utility_px":round(sum(x["utility_px"] for x in comparable)/len(comparable),5) if comparable else None,
      "all_forecasts_sealed":True,"source_hash_separation_checked":True,
      "synthetic_cases":True,"physics_discovery_proven":False,
      "reciprocal_generation_integrated":False,"cumulative_p156_integrated":False,
      "unified_education_e2e":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY",
      "verdict":"F1C_PAIRED_AUDIT_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    return report
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    result=run(args.out)
    print(json.dumps({k:result[k] for k in ("verdict","paired_cases","comparable_cases",
        "improved_cases","degraded_cases","unchanged_cases","changed_model_choices","mean_memory_utility_px")},indent=2))
if __name__=="__main__":main()
