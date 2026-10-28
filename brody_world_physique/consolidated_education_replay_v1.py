"""Brody consolidation: immutable candidate skill snapshots and replay gates.

Learns from pixel-derived dynamic episodes, retains synthetic visual prototype,
rejects harmful global corrections, predicts future images from a sealed state.
This is a bounded offline experiment; NEVER Native Memory or external action.
"""
from __future__ import annotations
import argparse,hashlib,json,random
from pathlib import Path
from .image_active_context_probe_p158 import trajectory
from .image_context_coexistence_p157 import observed
from .image_education_retention_gate_p155 import choose
from .image_reciprocal_shape_learning_p134 import scene,compare
from .u8_shared_shape_motion_generation_v1 import teaching_shape,draw_candidate,motion_features,predict
from .experiential_skill_learning_v1 import save,seal

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def episode(kind,seed):
    imgs=trajectory(kind,"discriminating",random.Random(seed))
    try:return observed(imgs)
    finally:
        for image in imgs:image.close()

def evaluate(root,label,state,kind,seed):
    xs=episode(kind,seed)
    history=xs[:6]
    acceleration=motion_features(history)
    memory=state["motion"]
    context=("intervention" if acceleration is not None and abs(acceleration-memory["intervention"])<.25
             else "clean" if acceleration is not None and abs(acceleration-memory["clean"])<.25 else None)
    future=predict(history,memory[context]) if context else None
    proof=seal({"trial":label,"history":history,"context":context,"prediction":future,
        "state_sha256":digest(root/"CANDIDATE_MEMORY.json"),
        "source_kind":"SIMULATED","native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY"})
    save(root/(label+"_PRECOMMIT.json"),proof)
    result={"case":label,"context":context,"prediction_generated":future is not None}
    if future is not None:
        render=root/(label+"_prediction.png")
        draw_candidate(state["shape"],future,render)
        actual=xs[6]
        truth=root/(label+"_target.png")
        draw_candidate(state["shape"],actual,truth)
        result["position_error"]=abs(future-actual)
        result["image_mae"]=compare(render,truth)["mae_rgb"]
    else:
        result["position_error"]=None;result["image_mae"]=None
    return result

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    shape_path=root/"shape_source.png";teaching_shape(shape_path)
    shape=scene(shape_path)["components"][0]
    old=episode("flat",100)
    new=episode("slope",101)
    a_old=motion_features(old[:6]);a_new=motion_features(new[:6])
    if a_old is None or a_new is None:raise ValueError("MISSING_OBSERVATIONS")
    accepted,reason=choose(a_new,[(10.,10.+a_new),(20.,20.+a_new)],
                           [(10.,10.),(20.,20.)],.03)
    if accepted:raise ValueError("RETENTION_GATE_UNEXPECTEDLY_PERMITTED_GLOBAL_MUTATION")
    state={"schema":"BRODY_CONSOLIDATED_SKILL_STATE_V1","version":1,
           "shape":shape,"motion":{"clean":a_old,"intervention":a_new},
           "source_provenance":{"shape":digest(shape_path),
                 "motion":"P158_RENDERED_PIXELS_P157_OBSERVER"},
           "global_mutation_denied":reason,
           "native_memory_write":False,"canonical_promotion":False,
           "decision_authority":"KX108_ONLY"}
    save(root/"CANDIDATE_MEMORY.json",seal(state))
    # Replay old competency before and after new lesson, with separate exam seeds.
    rows=[evaluate(root,"old_clean_replay",state,"flat",302),
          evaluate(root,"new_slope_transfer",state,"slope",403),
          evaluate(root,"unknown_novel",state,"spring",504)]
    report={"schema":"BRODY_CONSOLIDATED_EDUCATION_REPLAY_V1",
        "retention_gate_global_update":"BLOCKED",
        "retention_reason":reason,
        "candidate_memory_sha256":digest(root/"CANDIDATE_MEMORY.json"),
        "precommit_count":len(rows),"replays":rows,
        "source_groups_independent_proven":False,
        "long_term_memory_retention_proven":False,
        "multi_day_learning_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"SHARED_CANDIDATE_REPLAY_WITH_RETENTION_GUARD"}
    save(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"replays":r["replays"]},indent=2))
if __name__=="__main__":main()
