"""P1: link existing simulated video forecasts and Reverso render to candidate world views.

NOT a new video predictor/decoder, MMonde WorldState, memory system, physics
solver, causal proof or F16 real image. Forecasts are precommitted by the
existing streaming world_transfer_probe_v1; this module only assembles evidence
AFTER its held-out video observation and Reverso rendered comparison exist.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from math import hypot, isclose
from pathlib import Path
from shutil import copyfile
from types import SimpleNamespace

from PIL import Image, ImageChops, ImageStat

from .contracts_v0 import (
    WorldTransformationV0, WorldStateProjectionV0, ProjectionKindV0,
    WorldStateDeltaV0, WorldExperienceCandidateV0,
    TransformationEpistemicClassV0,
)
from .preverbal_prediction_v0 import PositionMeasurementV0
from .world_transfer_probe_v1 import _load_probe_suite, iter_video_points
from .video_observation_v0 import video_sha256

SCHEMA = "BRODY_MULTIREPRESENTATION_BALL_BRIDGE_P1_V0"
CODE = Path(__file__).resolve()
IMAGES = ("last_observed.png", "predicted_reverso_candidate.png",
          "heldout_frame.png", "difference.png")


@dataclass(frozen=True)
class _SyntheticTime:
    observed_at: str


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    if path.exists():
        raise ValueError("refuse overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False,
                               sort_keys=True) + "\n", encoding="utf-8")


def _assert_synthetic_suite(manifest: Path, video_name: str) -> tuple[Path, str]:
    _train, tests = _load_probe_suite(manifest)
    found = [(p, h) for n,p,h in tests if n == video_name]
    if len(found) != 1 or video_name != "test_01.mp4":
        raise ValueError("P1 is bounded to withheld test_01.mp4")
    video, source_sha = found[0]
    if video_sha256(video) != source_sha:
        raise ValueError("source video mismatch")
    return video, source_sha


def _selected_precommit(receipts: Path, video_name: str) -> tuple[dict, str]:
    if receipts.stat().st_size > 2_000_000:
        raise ValueError("oversized receipts")
    lines = receipts.read_text(encoding="utf-8").splitlines()
    if len(lines) > 1000:
        raise ValueError("too many receipts")
    candidates = [json.loads(line) for line in lines]
    matched = [x for x in candidates
               if x.get("clip") == video_name
               and x.get("camera_mode") == "anchored"
               and x.get("proposal",{}).get("status") == "PREDICTION_CANDIDATE"
               and x.get("proposal",{}).get("candidate_xy") is not None]
    if not matched:
        raise ValueError("no eligible precommitted prediction")
    chosen = matched[0]  # exactly the selection used in existing Reverso adapter
    future = chosen.get("next_frame_index")
    history_refs = chosen.get("history_refs")
    if (not isinstance(future, int) or future not in range(6,72,6)
        or not isinstance(history_refs,list) or len(history_refs)!=3
        or any(f"#frame:{future}#" in r for r in history_refs)):
        raise ValueError("invalid held-out / history ordering")
    return chosen, digest(receipts)


def _images_and_metric(preview_dir:Path, report:dict)->dict:
    expected = ("BRODY_REVERSE_FUTURE_IMAGE_CANDIDATE_V1", "SIMULATED")
    if (report.get("schema"),report.get("source_kind")) != expected:
        raise ValueError("invalid Reverso preview")
    sha_by_name = {}
    for name in IMAGES:
        path=preview_dir/name
        with Image.open(path) as image:
            if image.size != (480,320):
                raise ValueError("unexpected synthetic preview size")
        sha_by_name[name] = digest(path)
    with Image.open(preview_dir/"predicted_reverso_candidate.png") as p:
        with Image.open(preview_dir/"heldout_frame.png") as t:
            diff=ImageChops.difference(p.convert("RGB"),t.convert("RGB"))
            mae=sum(ImageStat.Stat(diff).mean)/3
    if not isclose(mae,report["full_frame_mean_absolute_pixel_difference"],
                   rel_tol=0,abs_tol=1e-6):
        raise ValueError("Reverso score and stored images disagree")
    with Image.open(preview_dir/"difference.png") as stored:
        if ImageChops.difference(diff, stored.convert("RGB")).getbbox() is not None:
            raise ValueError("altered image difference")
    return {"artifact_sha256":sha_by_name, "full_frame_pixel_mae":mae,
            "generated_is_observation":False,
            "image_source_independence_count":1}


def _history_by_refs(video:Path, video_sha:str, receipt:dict):
    observed=list(iter_video_points(video,video_sha,camera_mode="anchored"))
    known={p.source_ref:p for p in observed if p is not None}
    history_refs=receipt["history_refs"]
    if len(set(history_refs))!=3 or any(ref not in known for ref in history_refs):
        raise ValueError("history references not present in source")
    history=[known[ref] for ref in history_refs]
    if not all(a.time_s < b.time_s for a,b in zip(history,history[1:])):
        raise ValueError("history order incorrect")
    future=receipt["next_frame_index"]
    target_ref=f"sha256:{video_sha}#frame:{future}#visual_candidate"
    heldout=known.get(target_ref)
    if heldout is None:
        raise ValueError("heldout observation missing; cannot claim measured future")
    if heldout.time_s <= history[-1].time_s:
        raise ValueError("future is not after history")
    return history,heldout


def candidate_episode(history:list[PositionMeasurementV0],
                      future:PositionMeasurementV0, forecast:dict,
                      preview_metric:dict, video_sha:str,
                      preview_hash:str)->dict:
    """Pure F0 contract adapter; receives nothing from the simulation's law."""
    if len(history)!=3 or any(p.source_kind!="SIMULATED" for p in (*history,future)):
        raise ValueError("requires three same-simulator history measurements")
    if len({p.frame_ref for p in (*history,future)})!=1:
        raise ValueError("cannot fuse incompatible reference frames")
    if {p.unit for p in (*history,future)}!={"px"}:
        raise ValueError("unsupported physical units")
    if not history[0].time_s<history[1].time_s<history[2].time_s<future.time_s:
        raise ValueError("nonmonotonic timeline")
    xy=forecast.get("candidate_xy")
    if not isinstance(xy,list) or len(xy)!=2 or not all(isinstance(x,(int,float)) and not isinstance(x,bool) for x in xy):
        raise ValueError("missing candidate position")
    spatial_error=hypot(xy[0]-future.x,xy[1]-future.y)
    dt=history[-1].time_s-history[-2].time_s
    if dt<=0:raise ValueError("nonpositive time")
    vx=(history[-1].x-history[-2].x)/dt
    vy=(history[-1].y-history[-2].y)/dt
    last_dt=future.time_s-history[-1].time_s
    linear_xy=[history[-1].x+vx*last_dt,history[-1].y+vy*last_dt]
    linear_error=hypot(linear_xy[0]-future.x,linear_xy[1]-future.y)
    before=f"world-view:simulated:{video_sha}:frame:{int(round(history[-1].time_s*24))}"
    after=f"world-view:simulated:{video_sha}:frame:{int(round(future.time_s*24))}"
    projected_id="projected:"+after
    trans=WorldTransformationV0(
        transformation_id="candidate:prediction-transition:"+video_sha[:16],
        transformation_kind="EXPERIENTIAL_2D_MOTION_FORECAST",
        time=_SyntheticTime(str(history[-1].time_s)),
        target_refs=(before,),parameters={"frame":history[-1].frame_ref,"unit":"px"},
        provenance_refs=tuple(x.source_ref for x in history),
        evidence_refs=("sha256:"+video_sha,),
        epistemic_class=TransformationEpistemicClassV0.INFERRED,
    )
    # Shape-only view required by existing F0 contract; this is NOT a new
    # WorldStateV0 root nor a canonical realization of MMonde.
    projected_view=SimpleNamespace(world_state_id=projected_id,
                                   candidate_reality=True,memory_object=False)
    projection=WorldStateProjectionV0(
        projection_id="candidate:projection:"+video_sha[:16],
        base_state_ref=before,projected_state=projected_view,
        projection_kind=ProjectionKindV0.PREDICTED,
        model_or_rule_ref="brody_world_physique.world_transfer_probe_v1:propose_with_conflict_gate",
        generated_at=str(history[-1].time_s),
        transformation_ref=trans.transformation_id,
        prediction_horizon=str(last_dt)+" s",
        uncertainty=("IMAGE_PLANE_PIXEL_UNITS_ONLY","SIMULATED_SOURCE",
                     "NO_PHYSICAL_LAW_PROVEN"),
        provenance_refs=tuple(x.source_ref for x in history),
        evidence_refs=("sha256:"+video_sha,),
    )
    delta=WorldStateDeltaV0(
        delta_id="candidate:delta:"+video_sha[:16],
        projected_state_ref=projection.projection_id,
        observed_world_state_ref=after,
        metric_deltas={"center_error_px":spatial_error,
                       "matched_linear_center_error_px":linear_error,
                       "reverso_full_frame_mae":preview_metric["full_frame_pixel_mae"]},
        continuity_status="UNKNOWN",
        uncertainty=("VISUAL_OBSERVATION_NOT_PHYSICAL_AUTHENTICITY",
                     "RENDERING_NOT_REAL_IMAGE_OBSERVATION"),
        provenance_refs=(future.source_ref,"sha256:"+preview_hash),
    )
    exp=WorldExperienceCandidateV0(
        experience_id="candidate:world-experience:"+video_sha[:16],
        state_before_ref=before,state_after_ref=after,
        outcome="MEASURED_POSTCOMMIT_VISUAL_DIFFERENCE",
        transformation_ref=trans.transformation_id,
        projection_ref=projection.projection_id,delta_ref=delta.delta_id,
        context_refs=tuple(p.source_ref for p in history),
        replay_refs=("sha256:"+preview_hash,),
        evidence_refs=(future.source_ref,"sha256:"+video_sha),
    )
    return {
        "source_kind":"SIMULATED","shared_source_sha256":video_sha,
        "independent_source_count":1,
        "frames":{"history_refs":[p.source_ref for p in history],
                  "heldout_ref":future.source_ref,
                  "future_observed_after_precommit_by_upstream_protocol":True},
        "representation_views":{
            "RASTER":{"observed_past_sha256":preview_metric["artifact_sha256"]["last_observed.png"],
                      "predicted_generated_sha256":preview_metric["artifact_sha256"]["predicted_reverso_candidate.png"],
                      "heldout_source_frame_sha256":preview_metric["artifact_sha256"]["heldout_frame.png"],
                      "kind":"SIMULATED_RENDERED_FRAMES_NOT_REAL_F16"},
            "SPATIAL":{"frame_ref":history[-1].frame_ref,
                       "unit":"px","history_xy":[[p.x,p.y] for p in history],
                       "predicted_xy":list(xy),"heldout_xy":[future.x,future.y]},
            "TEMPORAL":{"history_t_s":[p.time_s for p in history],
                        "predicted_future_t_s":future.time_s,
                        "clock_kind":"SIMULATED_FRAME_TIME"},
            "MOTION":{"estimated_velocity_px_per_s":[vx,vy],
                      "linear_baseline_xy":linear_xy,
                      "law_identity_proven":False},
        },
        "comparisons":{"center_error_px":spatial_error,
                       "matched_linear_center_error_px":linear_error,
                       "full_frame_mae":preview_metric["full_frame_pixel_mae"],
                       "joint_representation_improvement_proven":False,
                       "ablation_experiment_completed":False},
        "contract_refs":{"transformation":trans.transformation_id,
                         "projection":projection.projection_id,
                         "delta":delta.delta_id,
                         "experience":exp.experience_id,
                         "schema_versions":[trans.schema_version,projection.schema_version,
                                            delta.schema_version,exp.schema_version],
                         "canonical_world_state_instantiated":False,
                         "memory_eligibility":exp.memory_eligibility.value,
                         "memory_write_allowed":exp.memory_write_allowed,
                         "auto_promotion_allowed":exp.auto_promotion_allowed,
                         "causal_proof":delta.causal_proof,
                         "decision_authority":exp.decision_authority},
    }


def _recompute(suite:Path,forecasts:Path,preview:Path)->dict:
    manifest=suite.resolve(strict=True)
    video,source_hash=_assert_synthetic_suite(manifest,"test_01.mp4")
    chosen,precommit_sha=_selected_precommit(forecasts.resolve(strict=True),"test_01.mp4")
    pre=_json(preview/"evaluation.json")
    if (pre.get("video_sha256")!=source_hash
        or pre.get("forecast_receipt_sha256")!=precommit_sha
        or pre.get("future_index")!=chosen["next_frame_index"]
        or pre.get("past_index")!=chosen["next_frame_index"]-6
        or pre.get("candidate_center_xy")!=chosen["proposal"]["candidate_xy"]
        or pre.get("native_memory_write_allowed") is not False):
        raise ValueError("preview and sealed forecast not linked")
    pixel_metrics=_images_and_metric(preview,pre)
    history,future=_history_by_refs(video,source_hash,chosen)
    episode=candidate_episode(history,future,chosen["proposal"],pixel_metrics,
                              source_hash,digest(preview/"evaluation.json"))
    return {
        "schema":SCHEMA,"source_kind":"SIMULATED",
        "source_manifest_sha256":digest(manifest),
        "video_sha256":source_hash,
        "forecast_precommit_sha256":precommit_sha,
        "preview_evaluation_sha256":digest(preview/"evaluation.json"),
        "code_sha256":digest(CODE),
        "upstream_video_decoder":"world_transfer_probe_v1.iter_video_points",
        "upstream_predictor":"world_transfer_probe_v1.propose_with_conflict_gate",
        "upstream_renderer":"examples.reverso_future_preview_v1.create_preview",
        "experiment_candidate":episode,
        "pixel_evidence":pixel_metrics,
        "ablation_results_claimed":False,"physical_truth_proven":False,
        "sens_runtime_executed":False,"native_memory_write_allowed":False,
        "auto_promotion_allowed":False,"emits_act":False,
        "kernel_mutation":False,"decision_authority":"KX108_ONLY",
    }


def build(suite:Path,forecasts:Path,preview:Path,out:Path)->dict:
    root=Path(out).resolve()
    if root.exists() and any(root.iterdir()):
        raise ValueError("output must be fresh")
    proposal=_recompute(suite,forecasts,preview)
    images_dir=root/"images"
    images_dir.mkdir(parents=True,exist_ok=False)
    for name in IMAGES:
        original=Path(preview).resolve(strict=True)/name
        copied=images_dir/name
        copyfile(original,copied)
        if digest(copied)!=proposal["pixel_evidence"]["artifact_sha256"][name]:
            raise ValueError("copied synthetic image changed")
    _write_json(root/"evaluation.json",proposal)
    return {"status":"P1_MULTIREPRESENTATION_BOUNDED_BRIDGE_CREATED",
            "evaluation":str(root/"evaluation.json"),
            "center_error_px":proposal["experiment_candidate"]["comparisons"]["center_error_px"],
            "joint_improvement_proven":False,
            "memory_write_allowed":False}


def verify(suite:Path,forecasts:Path,preview:Path,out:Path)->dict:
    actual=_json(Path(out).resolve(strict=True)/"evaluation.json")
    expected=_recompute(suite,forecasts,preview)
    if actual!=expected:
        raise ValueError("world representation evidence does not replay")
    for name in IMAGES:
        copied=Path(out).resolve(strict=True)/"images"/name
        if (digest(copied)!=actual["pixel_evidence"]["artifact_sha256"][name]
            or digest(copied)!=digest(Path(preview).resolve(strict=True)/name)):
            raise ValueError("published candidate images are inconsistent")
    return {"status":"PASS_P1_MULTIREPRESENTATION_BOUNDED_REPLAY",
            "view_count":len(actual["experiment_candidate"]["representation_views"]),
            "independent_source_count":actual["experiment_candidate"]["independent_source_count"],
            "source_kind":actual["source_kind"],
            "native_memory_write_allowed":False,"joint_improvement_proven":False}


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(description="P1: join precommitted visual prediction, space, time, motion, and Reverso into one readonly candidate episode")
    p.add_argument("--suite",type=Path,required=True)
    p.add_argument("--forecasts",type=Path,required=True)
    p.add_argument("--preview",type=Path,required=True)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--out",type=Path)
    g.add_argument("--verify",type=Path)
    a=p.parse_args(argv)
    res=build(a.suite,a.forecasts,a.preview,a.out) if a.out else verify(a.suite,a.forecasts,a.preview,a.verify)
    print(json.dumps(res,indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
