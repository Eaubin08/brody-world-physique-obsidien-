"""Brody V4.2 — reciprocal directed relations from synthetic visual experience.

A teacher labels two *visual component roles* and four screen-frame cardinal
directions during lessons. The observer gets pixels only and uses existing V4.1
connected components. The student learns role/angle prototypes from those
lessons, tests held-out translations/scales/rotations and proposes reciprocals
using reversed vectors. It rejects ambiguous/unsupported/occluded input.

This is SUPERVISED GEOMETRIC CLASSIFICATION, not semantic recognition,
3-D 360-degree view invariance, or independent world knowledge. The result
is linked to existing readonly F0 world experience types. Native Memory and
SENS/B8 are not modified or used as authority.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import hypot
from pathlib import Path
from statistics import mean
from typing import Any

from PIL import Image, ImageDraw

from .contracts_v0 import (
    ExperienceValidationStatusV0, MemoryEligibilityV0,
    TransformationEpistemicClassV0, WorldExperienceCandidateV0,
    WorldStateDeltaV0, WorldTransformationV0,
)
from .drawing_school_v0 import digest_bytes
from .experience_memory_v1 import stable_bytes
from .world_relations_school_v4_1 import (
    inspect_pixels, professor_scene, verify_school as verify_v41,
)

SCHEMA = "BRODY_WORLD_ORIENTATION_V4_2"
FRAME = "SYNTHETIC_CANVAS_XY_64"
SYNTHETIC = "SIMULATED"
DIRS = ("TOP", "LEFT", "BOTTOM", "RIGHT")
MODULE = Path(__file__).resolve()


@dataclass(frozen=True)
class _OrdinalTime:
    observed_at: str


def sha(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    if path.exists():
        raise ValueError("refuse evidence overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def write_png(path: Path, img: Image.Image) -> str:
    if path.exists():
        raise ValueError("refuse image overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return sha(path)


def turn_scene(turn: int, *, dx: int = 0, dy: int = 0,
               scale: float = 1.0) -> Image.Image:
    if turn not in (0, 90, 180, 270):
        raise ValueError("only 4 cardinal orientations, not free 360 degrees")
    img = professor_scene("NEAR", dx=dx, dy=dy, scale=scale)
    return img.rotate(turn, resample=Image.Resampling.NEAREST,
                      expand=False, fillcolor=255)


def fill_ratio(comp: dict) -> float:
    x0, y0, x1, y1 = comp["bbox"]
    return comp["area_px"] / ((x1 - x0 + 1) * (y1 - y0 + 1))


def teacher_roles(obs: dict) -> dict:
    """Training teacher identifies morphological roles, never exam coordinates."""
    if obs["component_count"] != 2:
        raise ValueError("invalid labeled lesson")
    ratios = [fill_ratio(c) for c in obs["components"]]
    if abs(ratios[0]-ratios[1]) < .19:
        raise ValueError("lesson lacks distinct visual roles")
    p = min(range(2), key=lambda i: ratios[i])
    return {"pointed_component_index":p, "block_component_index":1-p,
            "role_annotation_source":"TEACHER_GUIDED_LESSON_ONLY"}


def directed_features(obs: dict, pointed_index: int) -> dict:
    if obs["component_count"] != 2:
        raise ValueError("requires exactly two disconnected components")
    pointed = obs["components"][pointed_index]
    block = obs["components"][1-pointed_index]
    dx = pointed["centroid_xy"][0]-block["centroid_xy"][0]
    dy = pointed["centroid_xy"][1]-block["centroid_xy"][1]
    d = hypot(dx,dy)
    if d < 1:
        raise ValueError("coincident component centroids")
    return {"unit_xy":[dx/d,dy/d],"distance_px":d,
            "pointed_fill_ratio":fill_ratio(pointed),
            "block_fill_ratio":fill_ratio(block)}


def training_fixtures() -> list[tuple[str,str,Image.Image]]:
    return [
        ("top_a","TOP",turn_scene(0)),
        ("top_b","TOP",turn_scene(0,dx=3,dy=-1,scale=.9)),
        ("left_a","LEFT",turn_scene(90)),
        ("left_b","LEFT",turn_scene(90,dx=-2,dy=1,scale=1.08)),
        ("bottom_a","BOTTOM",turn_scene(180)),
        ("bottom_b","BOTTOM",turn_scene(180,dx=3,dy=2,scale=.93)),
        ("right_a","RIGHT",turn_scene(270)),
        ("right_b","RIGHT",turn_scene(270,dx=-2,dy=-2,scale=1.05)),
    ]


def learn_frame_policy(lessons: list[dict], prior_v41: dict) -> dict:
    if prior_v41.get("status") != "CANDIDATE_LEARNED_THRESHOLD":
        raise ValueError("missing V4.1 prior learned separation")
    if len(lessons) != 8 or {x["teacher_direction"] for x in lessons} != set(DIRS):
        raise ValueError("must teach all four directions without exam labels")
    fill_proto = {
        name: mean(row["features"][f"{name}_fill_ratio"] for row in lessons)
        for name in ("pointed","block")
    }
    vecs = {}
    for direction in DIRS:
        vals = [row["features"]["unit_xy"] for row in lessons
                if row["teacher_direction"] == direction]
        vx = mean(v[0] for v in vals);vy = mean(v[1] for v in vals)
        n = hypot(vx, vy)
        if n < .65:
            raise ValueError("training direction inconsistent")
        vecs[direction] = [vx/n,vy/n]
    if abs(fill_proto["pointed"]-fill_proto["block"]) < .20:
        raise ValueError("indistinguishable component role models")
    return {
        "status":"SUPERVISED_CANDIDATE_4_CARDINALS",
        "source":"EIGHT_LABELED_SYNTHETIC_EXPERIENCES",
        "role_fill_prototypes":fill_proto,
        "direction_unit_prototypes":vecs,
        "near_threshold_from_v4_1":prior_v41["threshold"],
        "role_margin_min":.12,
        "angular_nearest_distance_max":.48,
        "direction_winner_margin_min":.18,
        "training_refs":[x["id"] for x in lessons],
        "frame":FRAME,"physical_frame":False,
        "confidence_calibrated":False,
        "semantic_shape_recognition":False,
        "learned_continuous_360_invariance":False,
    }


def nearest_direction(unit: list[float], policy: dict) -> tuple[str|None,dict]:
    ranks = sorted(
        [(hypot(unit[0]-v[0], unit[1]-v[1]),name)
         for name,v in policy["direction_unit_prototypes"].items()]
    )
    gap=ranks[1][0]-ranks[0][0]
    detail={"best_distance":ranks[0][0],"runner_up_gap":gap}
    if (ranks[0][0] > policy["angular_nearest_distance_max"] or
        gap < policy["direction_winner_margin_min"]):
        return None,detail
    return ranks[0][1],detail


def classify_oriented(obs: dict, policy: dict, *,
                      frame_ref: str = FRAME) -> dict:
    def hold(reason: str) -> dict:
        return {"status":reason,"candidate":None,"reciprocal":None,
                "source_kind":SYNTHETIC,"semantic_identity_proven":False,
                "causal_proven":False}
    if frame_ref != policy["frame"]:
        return hold("HOLD_UNKNOWN_SPATIAL_FRAME")
    if obs["component_count"] != 2:
        return hold("HOLD_AMBIGUOUS_OR_OCCLUDED_COMPONENTS")
    ratios=[fill_ratio(c) for c in obs["components"]]
    proto=policy["role_fill_prototypes"]
    votes=[]
    for i in (0,1):
        pointed_error=abs(ratios[i]-proto["pointed"])
        block_error=abs(ratios[i]-proto["block"])
        votes.append((pointed_error,block_error))
    role_assignments=[
        (votes[0][0]+votes[1][1], 0),
        (votes[1][0]+votes[0][1], 1),
    ]
    role_assignments.sort()
    if role_assignments[1][0]-role_assignments[0][0] < policy["role_margin_min"]:
        return hold("HOLD_AMBIGUOUS_PART_ROLES")
    pointed_idx=role_assignments[0][1]
    f=directed_features(obs,pointed_idx)
    if obs["features"]["normalized_distance"] > policy["near_threshold_from_v4_1"]:
        return hold("HOLD_COMPONENTS_OUTSIDE_LEARNED_COMPOSITION_RANGE")
    label,rank=nearest_direction(f["unit_xy"],policy)
    if label is None:
        return hold("HOLD_UNLEARNED_OBLIQUE_ORIENTATION")
    reversed_vec=[-f["unit_xy"][0],-f["unit_xy"][1]]
    inverse,inverse_rank=nearest_direction(reversed_vec,policy)
    if inverse is None or label==inverse:
        return hold("HOLD_NONRECIPROCAL_DIRECTION")
    return {
        "status":"CANDIDATE_ONLY",
        "candidate":f"POINTED_{label}_OF_BLOCK",
        "direction":label,
        "reciprocal":f"BLOCK_{inverse}_OF_POINTED",
        "reciprocal_direction":inverse,
        "reciprocal_by_reverse_vector_not_hardcoded_dictionary":True,
        "role_indices":{"pointed":pointed_idx,"block":1-pointed_idx},
        "features":f,"direction_match":rank,
        "inverse_match":inverse_rank,
        "frame_ref":frame_ref,
        "source_kind":SYNTHETIC,
        "semantic_identity_proven":False,"causal_proven":False,
        "confidence_calibrated":False,
    }


def test_fixtures() -> list[tuple[str,str|None,Image.Image]]:
    base=turn_scene(0)
    # The teacher declares labels in its own held-out dataset. The learner
    # does not see these labels until the decision JSONL line is flushed.
    return [
        ("top_shifted","TOP",turn_scene(0,dx=5,dy=3)),
        ("left_scaled","LEFT",turn_scene(90,dx=2,dy=-1,scale=1.17)),
        ("bottom_shifted","BOTTOM",turn_scene(180,dx=-4,dy=3)),
        ("right_scaled","RIGHT",turn_scene(270,dx=-1,dy=2,scale=.83)),
        ("top_mirrored","TOP",base.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ("bottom_reversed_parts","BOTTOM",professor_scene("REVERSED")),
        ("far_top_hold",None,professor_scene("FAR")),
        ("single_component_hold",None,_single_component()),
        ("identical_roles_hold",None,_same_parts()),
        ("diagonal_hold",None,base.rotate(45,resample=Image.Resampling.NEAREST,
                                       expand=False,fillcolor=255)),
        ("occlusion_hold",None,_occluded()),
    ]


def _single_component() -> Image.Image:
    img=Image.new("L",(64,64),255)
    ImageDraw.Draw(img).ellipse((18,15,44,41),fill=0)
    return img


def _same_parts() -> Image.Image:
    img=Image.new("L",(64,64),255)
    draw=ImageDraw.Draw(img)
    draw.rectangle((20,12,40,26),fill=0)
    draw.rectangle((20,37,40,51),fill=0)
    return img


def _occluded() -> Image.Image:
    img=turn_scene(0)
    draw=ImageDraw.Draw(img)
    # Simulate a solid foreground band occluding both shapes. The
    # segmentation becomes unsupported, not an invented ground-truth shape.
    draw.rectangle((0,19,63,42),fill=255)
    return img


def _make_lesson(name:str,label:str,img:Image.Image,ref:str)->dict:
    obs=inspect_pixels(img)
    roles=teacher_roles(obs)
    features=directed_features(obs,roles["pointed_component_index"])
    return {
        "id":name,
        "teacher_direction":label,
        "teacher_role_annotation":roles,
        "observed_features":features,
        "image_sha256":ref,
        "observed_component_count":obs["component_count"],
        "origin":"GUIDED_SYNTHETIC_TRAINING",
        "teacher_roles_accessible_during_lesson":True,
    }


def memory_candidates(row:dict,obs:dict,choice:dict,i:int)->dict:
    name=row["id"]
    before=f"world-candidate:v4-2:{name}:observed"
    after=f"world-candidate:v4-2:{name}:feedback"
    t=WorldTransformationV0(
        transformation_id=f"transformation:v4-2:perceive:{name}",
        transformation_kind="PROPOSE_TYPED_RELATION_FROM_IMAGE",
        time=_OrdinalTime(f"synthetic-sample-{i:02d}"),
        target_refs=(before,),
        parameters={"relation":choice["candidate"],
                    "reciprocal":choice["reciprocal"],
                    "observed_component_count":obs["component_count"]},
        provenance_refs=(f"v4-2:precommitted:{name}",),
        evidence_refs=(f"sha256:{row['image_sha256']}",),
        epistemic_class=TransformationEpistemicClassV0.SIMULATED,
    )
    d=WorldStateDeltaV0(
        delta_id=f"delta:v4-2:{name}",
        baseline_state_ref=before,observed_world_state_ref=after,
        metric_deltas={"matches_teacher_direction":int(row["correct"])},
        continuity_status="UNKNOWN",
        uncertainty=("SYNTHETIC_2D_ONLY","NO_SEMANTIC_TYPE_PROVEN",
                     "FEEDBACK_NOT_WORLD_TRUTH"),
        provenance_refs=(f"sha256:{row['image_sha256']}",),
    )
    x=WorldExperienceCandidateV0(
        experience_id=f"experience:v4-2:{name}",
        state_before_ref=before,state_after_ref=after,
        outcome="MATCHED_TEACHER_FEEDBACK" if row["correct"] else
                ("HELD_UNKNOWN" if row["expected"] is None and choice["candidate"] is None
                 else "CONTRADICTED_BY_TEACHER_FEEDBACK"),
        transformation_ref=t.transformation_id,delta_ref=d.delta_id,
        context_refs=(before,),
        replay_refs=(f"v4-2:precommitted:{name}",),
        evidence_refs=(f"sha256:{row['image_sha256']}",),
        validation_status=ExperienceValidationStatusV0.CANDIDATE,
        memory_eligibility=MemoryEligibilityV0.CANDIDATE_ONLY,
    )
    return {
        "observation_ref":before,
        "source_sha256":row["image_sha256"],
        "source_kind":"SIMULATED",
        "transformation":{"schema_version":t.schema_version,
                          "ref":t.transformation_id,
                          "epistemic_class":t.epistemic_class.value,
                          "decision_authority":t.decision_authority,
                          "execution_authority":t.execution_authority},
        "delta":{"schema_version":d.schema_version,
                 "ref":d.delta_id,"continuity_status":d.continuity_status,
                 "causal_proof":d.causal_proof,
                 "feedback_match":int(row["correct"])},
        "experience":{"schema_version":x.schema_version,
                      "ref":x.experience_id,"outcome":x.outcome,
                      "state_before_ref":x.state_before_ref,
                      "state_after_ref":x.state_after_ref,
                      "validation_status":x.validation_status.value,
                      "memory_eligibility":x.memory_eligibility.value,
                      "canonical_memory":x.canonical_memory,
                      "memory_write_allowed":x.memory_write_allowed,
                      "auto_promotion_allowed":x.auto_promotion_allowed,
                      "decision_authority":x.decision_authority},
    }


def student_reconstruct(training:list[dict],policy:dict,
                        requested_direction:str)->Image.Image:
    """Student receives role masks from lesson images, a *relation goal*
    and learned prototypes, but no teacher output image/position boxes.

    Raster motor: rotate two prior visible pixel patches (programmed) and
    place them by their previously measured relative centroid separation.
    """
    if requested_direction not in DIRS:
        raise ValueError("not a learned relative direction")
    base_image=turn_scene(0)  # ISSUE: source must come from stored lessons
    raise NotImplementedError


def build(out:str|Path,*,v3:str|Path,v4:str|Path,v41:str|Path)->dict:
    raise NotImplementedError


def verify(folder:str|Path,*,v3:str|Path,v4:str|Path,v41:str|Path)->dict:
    raise NotImplementedError


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(description="V4.2 four-direction visual relations, reciprocal tests and blind reconstruction")
    p.add_argument("--prior-v3",type=Path,required=True)
    p.add_argument("--prior-v4",type=Path,required=True)
    p.add_argument("--prior-v4-1",type=Path,required=True)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--out",type=Path)
    group.add_argument("--verify",type=Path)
    a=p.parse_args(argv)
    args={"v3":a.prior_v3,"v4":a.prior_v4,"v41":a.prior_v4_1}
    result=build(a.out,**args) if a.out else verify(a.verify,**args)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
