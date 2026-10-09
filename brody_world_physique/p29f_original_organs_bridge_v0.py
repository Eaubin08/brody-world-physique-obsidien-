"""P2.9f verified reuse of actual P1/Reverso and V4.2 experiment outputs.

Different sources: never claim V4.2 2D compositions describe P1 ball video.
No replay bypass: invoke each original verifier with its genuine ancestors.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from hashlib import sha256
from . import multirepresentation_ball_bridge_v5 as p1
from . import world_orientation_school_v4_2 as v42

SCHEMA="BRODY_P29F_ORIGINAL_ORGANS_VERIFIED_BRIDGE_V0"

def digest(p):
    return sha256(Path(p).read_bytes()).hexdigest()

def assemble(*,suite,forecasts,preview,p1_out,v42_out,v3,v4,v41):
    replay_p1=p1.verify(Path(suite),Path(forecasts),Path(preview),Path(p1_out))
    replay_v42=v42.verify(Path(v42_out),v3=Path(v3),v4=Path(v4),v41=Path(v41))
    if replay_p1.get("status")!="PASS_P1_MULTIREPRESENTATION_BOUNDED_REPLAY":
        raise ValueError("P1 not verified")
    if replay_v42.get("status")!="PASS_V4_2_BOUNDED_ORIENTATION_AND_RECIPROCITY_REPLAY":
        raise ValueError("V4.2 not verified")
    a=json.loads((Path(p1_out)/"evaluation.json").read_text(encoding="utf-8"))
    b=json.loads((Path(v42_out)/"evaluation.json").read_text(encoding="utf-8"))
    episode=a["experiment_candidate"]
    required={"RASTER","SPATIAL","TEMPORAL","MOTION"}
    views=episode["representation_views"]
    if not required.issubset(views):
        raise ValueError("missing P1 views")
    if a["source_kind"]!="SIMULATED" or b["source_kind"]!="SIMULATED":
        raise ValueError("source type")
    if a["decision_authority"]!="KX108_ONLY" or b["decision_authority"]!="KX108_ONLY":
        raise ValueError("authority")
    if a["native_memory_write_allowed"] is not False or b["native_memory_write_allowed"] is not False:
        raise ValueError("memory write")
    # V4.2 is an independent synthetic exercise in 2D. It cannot be
    # treated as an additional observation of the P1 source video.
    return {"schema":SCHEMA,"source_kind":"TWO_SEPARATE_SYNTHETIC_EXPERIMENTS",
            "p1_replay":replay_p1["status"],"v42_replay":replay_v42["status"],
            "p1_source_video_sha256":a["video_sha256"],
            "p1_representation_views":sorted(required),
            "p1_temporal_frame":views["TEMPORAL"]["clock_kind"],
            "p1_spatial_frame":views["SPATIAL"]["frame_ref"],
            "p1_full_frame_mae":episode["comparisons"]["full_frame_mae"],
            "p1_center_error_px":episode["comparisons"]["center_error_px"],
            "v42_rotation_frame":b["rotation_frame"],
            "v42_reciprocal_relation_derived_by_reverse_vector":
                b["reciprocal_relation_derived_by_reverse_vector"],
            "v42_lessons":len(b["lessons"]) if isinstance(b.get("lessons"),list) else len(b["candidate_relation_model"].get("directions",[])),
            "source_count_as_one_experiment":False,
            "same_scene_cross_modal_inference":False,
            "joint_physical_understanding_proven":False,
            "b8_promotion":False,"native_memory_write":False,
            "decision_authority":"KX108_ONLY",
            "p1_evaluation_sha256":digest(Path(p1_out)/"evaluation.json"),
            "v42_evaluation_sha256":digest(Path(v42_out)/"evaluation.json")}

def run(out,**kwargs):
    p=Path(out)
    if p.exists():raise ValueError("output already exists")
    result=assemble(**kwargs)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def verify(out,**kwargs):
    saved=json.loads(Path(out).read_text(encoding="utf-8"))
    if saved!=assemble(**kwargs):raise ValueError("P2.9f joint replay mismatch")
    return {"verified":True,"source_join":False}

def main():
    ap=argparse.ArgumentParser()
    for arg in ("suite","forecasts","preview","p1-out","v42-out","v3","v4","v41","out"):
        ap.add_argument("--"+arg,required=True)
    ap.add_argument("--verify",action="store_true")
    a=vars(ap.parse_args());check=a.pop("verify");out=a.pop("out")
    kwargs={k.replace("-","_"):v for k,v in a.items()}
    response=verify(out,**kwargs) if check else run(out,**kwargs)
    print(json.dumps(response,ensure_ascii=False))
if __name__=="__main__":
    main()
