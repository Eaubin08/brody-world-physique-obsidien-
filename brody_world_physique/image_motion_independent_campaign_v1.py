"""Run grouped independent-episode ablation without teaching from exam data."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .image_motion_campaign_split_v1 import audit
from .image_experience_guided_motion_v2 import forecast,correct
from .image_motion_memory_ablation_v1 import run as ablate
from .image_multihypothesis_motion_memory_v1 import read,write

def campaign(manifest,out):
    target=Path(out)
    if target.exists():raise ValueError("PRESERVE_PRIOR_CAMPAIGN")
    if not Path(manifest).is_file():raise ValueError("CAMPAIGN_MANIFEST_MISSING")
    target.mkdir(parents=True)
    audit(manifest,target/"split")
    lessons=read(target/"split"/"train_cases.json")
    previous=None
    for i,case in enumerate(lessons,1):
        spec={"observations":case["observations"],"predict_t":case["predict_t"]}
        manifest_i=target/f"course_{i:03d}.json"
        write(manifest_i,spec)
        pred=target/f"train_forecast_{i:03d}"
        graded=target/f"train_feedback_{i:03d}"
        forecast(manifest_i,pred,previous)
        correct(pred/"sealed_forecast.json",case["actual"],graded,previous)
        previous=graded/"candidate_physics_memory.json"
    evaluation=ablate(target/"split"/"exam_cases.json",previous,target/"heldout_ablation")
    summary={"schema":"BRODY_INDEPENDENT_MOTION_CAMPAIGN_V1",
        "train_episodes":len(lessons),"exam_episodes":evaluation["cases"],
        "paired_selected":evaluation["paired_selected"],
        "paired_memory_advantage_px":evaluation["mean_paired_advantage_px"],
        "memory_outperforms_baseline_on_paired_cases":evaluation["memory_outperforms_baseline_on_paired_cases"],
        "memory_frozen_for_heldout":True,
        "real_world_generalization_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    write(target/"MASTER_REPORT.json",summary)
    return summary
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(campaign(a.manifest,a.out),indent=2))
if __name__=="__main__":main()
