"""Brody integrated education V0: one experience across perception, motion and rendering.

An isolated experimental integration, not canonical cognition, not a physical-law
discovery. This module reuses existing tracking, memory and drawing APIs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

from .f1b_physical_memory_bridge_v1 import episode
from .image_experience_guided_motion_v2 import forecast, correct, load
from .image_multihypothesis_motion_memory_v1 import read
from .image_observed_motion_school_v1 import analyze

LESSONS=(
    ("ball_falling_A",(10,14,20,28,38)),
    ("ball_falling_B",(17,21,27,35,45)),
    ("different_skill_steady",(9,14,19,24,29)),
)
EXAMS=(
    ("unseen_fall",(22,26,32,40,50)),
    ("contradictory_reversal",(11,15,21,29,25)),
)
LOCK=("identity_candidate","object_count","temporal_order")
FLEX=("screen_position","illumination","context","viewpoint")
IGNORE=("background_unrelated_to_motion",)

def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _write(path,obj):
    with Path(path).open("x",encoding="utf8") as f:
        json.dump(obj,f,indent=2,sort_keys=True);f.write("\n")

def _evidence(forecast_dir,observed):
    sealed_path=forecast_dir/"sealed_forecast.json"
    sealed=read(sealed_path)
    original_digest=sealed["digest"]
    true=analyze(observed)
    variants={}
    for name,position in sealed["hypotheses"].items():
        drawn=forecast_dir/(name.lower()+".png")
        visual=analyze(drawn)
        variants[name]={
            "predicted_xy":[position["x"],position["y"]],
            "roundtrip_xy":[visual["x"],visual["y"]],
            "roundtrip_error_px":round(math.hypot(visual["x"]-position["x"],visual["y"]-position["y"]),5),
            "truth_error_px":round(math.hypot(true["x"]-position["x"],true["y"]-position["y"]),5),
            "generated_sha256":_sha(drawn)}
    if read(sealed_path)["digest"]!=original_digest:
        raise ValueError("PREDICTION_CHANGED_AFTER_FEEDBACK")
    return variants

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    memory=None
    journal=[]
    candidates={}
    for idx,(label,ys) in enumerate(LESSONS):
        manifest,target=episode(root,label,ys,x=25+idx*3)
        folder=root/("prediction_"+label)
        prediction=forecast(manifest,folder,previous=memory)
        prior_memory_sha=_sha(memory) if memory else None
        comparison=_evidence(folder,target)
        correction_dir=root/("feedback_"+label)
        learned=correct(folder/"sealed_forecast.json",target,correction_dir,previous=memory)
        memory=correction_dir/"candidate_physics_memory.json"
        candidates[label]=_sha(memory)
        journal.append({"phase":"TRAIN","lesson":label,"predicted_before_feedback":True,
                        "evidence_source":prediction["evidence_source"],
                        "selected":prediction["selected"],
                        "memory_before_sha":prior_memory_sha,
                        "memory_after_sha":candidates[label],
                        "feedback":learned,"representation_roundtrip":comparison,
                        "status":"EXPERIENCE_CANDIDATE"})
    checkpoint=root/"education_checkpoint.json"
    _write(checkpoint,{"schema":"BRODY_EDUCATION_CHECKPOINT_V0",
        "candidate_memory_file":str(memory.relative_to(root)),
        "candidate_memory_sha256":_sha(memory),
        "skill_preconditions":{"ball_motion":"four ordered observable frames",
                              "camera_correction":"not supported in this harness"},
        "skill_dependencies":{"prediction":["object_localization","time_order"],
                              "render_reconstruction":["motion_prediction"]},
        "lock":LOCK,"flex":FLEX,"ignore":IGNORE,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"})
    # Restore/check the serialized experimental skill state before examination.
    restored=read(checkpoint)
    restored_path=root/restored["candidate_memory_file"]
    if _sha(restored_path)!=restored["candidate_memory_sha256"]:
        raise ValueError("CHECKPOINT_TAMPER")
    restored_memory=load(restored_path)
    if len(restored_memory["experiences"])!=len(LESSONS):
        raise ValueError("EXPERIENCES_LOST_AFTER_RESTORE")
    baseline_cases=[]
    for label,ys in EXAMS:
        manifest,target=episode(root,label,ys,x=41)
        baseline_dir=root/("baseline_"+label)
        learned_dir=root/("learned_"+label)
        b=forecast(manifest,baseline_dir)
        m=forecast(manifest,learned_dir,previous=restored_path)
        # Both output commitments precede opening the evaluation reference.
        b_sha=_sha(baseline_dir/"sealed_forecast.json")
        m_sha=_sha(learned_dir/"sealed_forecast.json")
        base_scores=_evidence(baseline_dir,target)
        learned_scores=_evidence(learned_dir,target)
        if b_sha!=_sha(baseline_dir/"sealed_forecast.json") or m_sha!=_sha(learned_dir/"sealed_forecast.json"):
            raise ValueError("EXAM_COMMIT_MUTATION")
        selected_base=b["selected"];selected_mem=m["selected"]
        base_error=base_scores[selected_base]["truth_error_px"] if selected_base else None
        mem_error=learned_scores[selected_mem]["truth_error_px"] if selected_mem else None
        baseline_cases.append({"exam":label,"baseline_choice":selected_base,
            "memory_choice":selected_mem,"memory_evidence_source":m["evidence_source"],
            "memory_eligible_episodes":m["eligible_episodes"],
            "baseline_error_px":base_error,"memory_error_px":mem_error,
            "delta_px":round(base_error-mem_error,5) if base_error is not None and mem_error is not None else None,
            "baseline_visual_roundtrip":base_scores,
            "learned_visual_roundtrip":learned_scores,
            "observation_vs_prediction_distinct":True,
            "exam_feedback_reused_for_training":False})
    report={"schema":"BRODY_INTEGRATED_EDUCATION_V0","curriculum":journal,
            "exams":baseline_cases,
            "checkpoint_sha256":_sha(checkpoint),
            "checkpoint_restore_verified":True,
            "skill_history_dependencies_explicit":True,
            "lock_flex_ignore_contract":{"LOCK":LOCK,"FLEX":FLEX,"IGNORE":IGNORE},
            "roundtrip_is_programmatic_reanalysis":True,
            "generated_images_are_existing_model_renderings":True,
            "same_experience_perception_prediction_render_comparison":True,
            "full_reverse_360":False,"sens_cognition_mmonde_connected":False,
            "p156_shared_skill_state":False,"learned_physical_law_proven":False,
            "generalization_proven":False,"education_integrated_full":False,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY",
            "verdict":"INTEGRATED_EDUCATION_V0_CANDIDATE_ONLY"}
    _write(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args()
    r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],
        "lessons":len(r["curriculum"]),"exams":len(r["exams"]),
        "checkpoint_restore_verified":r["checkpoint_restore_verified"]},indent=2))
if __name__=="__main__":main()
