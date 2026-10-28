"""P2.9g one-source video representation + reciprocal motion and Reverso evidence.

Uses P1's original full replay before making any new claims. Direction is a
coordinate relation, not a learned V4.2 classifier and not physical causality.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from hashlib import sha256
from math import hypot,isclose
from . import multirepresentation_ball_bridge_v5 as p1
from .contracts_v0 import WorldStateDeltaV0,WorldExperienceCandidateV0
from .reverso_learning_v0 import LearningEpisodeSignalV0,triage_learning

SCHEMA="BRODY_P29G_SAME_VIDEO_MULTIVIEW_V0"

def evidence(*,suite,forecasts,preview,p1_out):
    verified=p1.verify(Path(suite),Path(forecasts),Path(preview),Path(p1_out))
    if verified.get("status")!="PASS_P1_MULTIREPRESENTATION_BOUNDED_REPLAY":
        raise ValueError("P1 replay failed")
    base=json.loads((Path(p1_out)/"evaluation.json").read_text(encoding="utf-8"))
    ep=base["experiment_candidate"]
    views=ep["representation_views"]
    if set(views)!={"RASTER","SPATIAL","TEMPORAL","MOTION"}:
        raise ValueError("exact four bounded views required")
    if ep["shared_source_sha256"]!=base["video_sha256"] or ep["independent_source_count"]!=1:
        raise ValueError("independent source inflation")
    if ep["contract_refs"]["memory_write_allowed"] or ep["contract_refs"]["decision_authority"]!="KX108_ONLY":
        raise ValueError("authority boundary")
    space,time,motion=views["SPATIAL"],views["TEMPORAL"],views["MOTION"]
    if space["unit"]!="px" or time["clock_kind"]!="SIMULATED_FRAME_TIME":
        raise ValueError("unsupported unit/clock")
    coords=space["history_xy"]
    times=time["history_t_s"]
    if len(coords)!=3 or len(times)!=3 or any(t2<=t1 for t1,t2 in zip(times,times[1:])):
        raise ValueError("invalid temporal source")
    last=coords[-1]; prev=coords[-2];dt=times[-1]-times[-2]
    velocity=[(last[k]-prev[k])/dt for k in range(2)]
    if any(not isclose(velocity[k],motion["estimated_velocity_px_per_s"][k],abs_tol=1e-8)
           for k in range(2)):raise ValueError("motion view inconsistent")
    reverse=[-v for v in velocity]
    relative=[last[k]-prev[k] for k in range(2)]
    inverse=[prev[k]-last[k] for k in range(2)]
    residual=hypot(relative[0]+inverse[0],relative[1]+inverse[1])
    if residual>1e-8:raise ValueError("reciprocal mismatch")
    err=ep["comparisons"]["center_error_px"]
    delta=WorldStateDeltaV0(
        delta_id="candidate:p29g:"+base["video_sha256"][:16],
        projected_state_ref=ep["contract_refs"]["projection"],
        observed_world_state_ref=ep["frames"]["heldout_ref"],
        metric_deltas={"center_error_px":err,"raster_mae":ep["comparisons"]["full_frame_mae"]},
        uncertainty=("SIMULATED_RECONSTRUCTION","NO_INDEPENDENT_3D_CAUSAL_INFERENCE"),
        provenance_refs=(ep["frames"]["heldout_ref"],))
    candidate=WorldExperienceCandidateV0(
        experience_id="candidate:p29g-experience:"+base["video_sha256"][:16],
        state_before_ref=ep["frames"]["history_refs"][-1],
        state_after_ref=ep["frames"]["heldout_ref"],outcome="CANDIDATE_POSTCOMMIT_REPLAY",
        projection_ref=ep["contract_refs"]["projection"],delta_ref=delta.delta_id,
        context_refs=tuple(ep["frames"]["history_refs"]),
        evidence_refs=("sha256:"+base["video_sha256"],))
    triage=triage_learning(LearningEpisodeSignalV0(
        kind="HYPOTHESIS",route_ref="P29G_ONE_VIDEO",source_ref="sha256:"+base["video_sha256"],
        outcome="UNKNOWN"))
    return {"schema":SCHEMA,"video_sha256":base["video_sha256"],
        "p1_evaluation_sha256":sha256((Path(p1_out)/"evaluation.json").read_bytes()).hexdigest(),
        "view_names":sorted(views),"spatial_frame":space["frame_ref"],
        "clock_kind":time["clock_kind"],"unit":"px",
        "velocity_px_per_s":velocity,"inverse_velocity_px_per_s":reverse,
        "reciprocal_residual":residual,
        "raster_predicted_sha256":views["RASTER"]["predicted_generated_sha256"],
        "raster_heldout_sha256":views["RASTER"]["heldout_source_frame_sha256"],
        "center_error_px":err,"raster_mae":ep["comparisons"]["full_frame_mae"],
        "delta_id":delta.delta_id,"experience_id":candidate.experience_id,
        "triage":triage["proposed_action"],"same_source_view_count":4,
        "independent_source_count":1,"v42_classifier_called":False,
        "new_prediction_made":False,"joint_improvement_proven":False,
        "causal_proof":False,"b8_promotion":False,"native_memory_write":False,
        "decision_authority":"KX108_ONLY"}

def run(out,**kwargs):
    dest=Path(out)
    if dest.exists():raise ValueError("output file exists")
    result=evidence(**kwargs)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def verify(out,**kwargs):
    saved=json.loads(Path(out).read_text(encoding="utf-8"))
    if saved!=evidence(**kwargs):raise ValueError("P2.9g replay mismatch")
    return {"verified":True,"same_source_view_count":4}

def main():
    ap=argparse.ArgumentParser()
    for name in ("suite","forecasts","preview","p1-out","out"):
        ap.add_argument("--"+name,required=True)
    ap.add_argument("--verify",action="store_true")
    a=vars(ap.parse_args())
    check=a.pop("verify");out=a.pop("out")
    kwargs={k.replace("-","_"):v for k,v in a.items()}
    print(json.dumps(verify(out,**kwargs) if check else run(out,**kwargs)))
if __name__=="__main__":main()
