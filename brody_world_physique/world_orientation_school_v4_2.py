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
        name: mean(row.get("observed_features",row.get("features"))[f"{name}_fill_ratio"] for row in lessons)
        for name in ("pointed","block")
    }
    vecs = {}
    for direction in DIRS:
        vals = [row.get("observed_features",row.get("features"))["unit_xy"] for row in lessons
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
    draw.rectangle((0,0,63,30),fill=255)
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
        "observed_geometry":obs,
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
    """Recombine observed part masks from lessons, using learned displacement.

    The motor that rotates/repositions stored pixels is engineered; only
    the role/direction prototypes are learned from teacher feedback.
    No target image or instructor position boxes reach this function.
    """
    if requested_direction not in DIRS:
        raise ValueError("unknown relative direction")
    lesson=training[0]
    observation=lesson["observed_geometry"]
    roles=lesson["teacher_role_annotation"]
    direction=policy["direction_unit_prototypes"][requested_direction]
    separation=lesson["observed_features"]["distance_px"]
    img=Image.new("L",(64,64),255)
    pixels=img.load()
    centers={
        "pointed":(32+direction[0]*separation/2,
                   32+direction[1]*separation/2),
        "block":(32-direction[0]*separation/2,
                 32-direction[1]*separation/2),
    }
    # Rotate each learned mask to the intended cardinal pose. These
    # transforms are hardcoded raster motors, not inferred world dynamics.
    angle=0 if requested_direction=="TOP" else (
        90 if requested_direction=="LEFT" else (
        180 if requested_direction=="BOTTOM" else 270))
    from math import cos, sin, pi
    theta=angle*pi/180
    for role in ("pointed","block"):
        component=observation["components"][roles[role+"_component_index"]]
        ox,oy=component["centroid_xy"]
        nx,ny=centers[role]
        for x,y in component["pixel_points"]:
            rx=x-ox;ry=y-oy
            # Image-frame CCW rotation: positive source y points down.
            xx=round(nx+rx*cos(theta)+ry*sin(theta))
            yy=round(ny-rx*sin(theta)+ry*cos(theta))
            if 0<=xx<64 and 0<=yy<64:
                pixels[xx,yy]=0
    return img


def pixel_score(reference:Image.Image,student:Image.Image)->dict:
    ref={i for i,p in enumerate(reference.convert("L").tobytes()) if p<128}
    pred={i for i,p in enumerate(student.convert("L").tobytes()) if p<128}
    error=len(ref^pred)
    return {"pixel_xor":error,"blank_error":len(ref),
            "better_than_blank":error<len(ref),
            "pixel_iou":len(ref&pred)/len(ref|pred) if ref|pred else 1.0}


def relation_score(target:Image.Image,student:Image.Image,policy:dict,goal:str)->dict:
    """World-level relation metric, separate from raw raster coincidence.

    It is evaluated AFTER the student image was written. It never changes the
    committed raster or selection. Separate pixel_xor is retained unchanged.
    """
    teacher=classify_oriented(inspect_pixels(target),policy)
    pupil=classify_oriented(inspect_pixels(student),policy)
    return {
        "intended_orientation":goal,
        "student_candidate":pupil["candidate"],
        "teacher_candidate":teacher["candidate"],
        "student_recipient_reciprocal":pupil["reciprocal"],
        "teacher_recipient_reciprocal":teacher["reciprocal"],
        "both_match_direction": (
            pupil.get("direction")==goal and teacher.get("direction")==goal
        ),
        "both_match_reciprocal": (
            pupil.get("reciprocal_direction")==teacher.get("reciprocal_direction")
            and pupil.get("reciprocal_direction") is not None
        ),
        "semantic_object_recognition_proven":False,
        "canonical_world_state_proven":False,
    }


def _load_upstream(v3:Path,v4:Path,v41:Path)->dict:
    prior=verify_v41(v41,prior_v3=v3,prior_v4=v4)
    if (prior["exams_verified"]!=6 or
        prior["native_memory_write_allowed"] is not False):
        raise ValueError("V4.1 evidence prerequisite not met")
    return json.loads((v41/"world_relation_memory_candidate.json").read_text(encoding="utf-8"))["policy"]


def _expected_lessons(root:Path)->list[dict]:
    lessons=[]
    for name,orientation,img in training_fixtures():
        path=root/"images"/("lesson_"+name+".png")
        if sha(path)!=digest_bytes(_image_bytes_as_png(img)):
            raise ValueError("lesson source hash does not replay")
        lessons.append(_make_lesson(name,orientation,img,sha(path)))
    return lessons


def _image_bytes_as_png(img:Image.Image)->bytes:
    from io import BytesIO
    buff=BytesIO()
    img.save(buff,format="PNG")
    return buff.getvalue()


def _score_decision(choice:dict,expected:str|None)->bool:
    return ((choice.get("direction")==expected and
             choice.get("status")=="CANDIDATE_ONLY") if expected is not None
            else choice.get("candidate") is None and
                 choice.get("status","").startswith("HOLD_"))


def build(out:str|Path,*,v3:str|Path,v4:str|Path,v41:str|Path)->dict:
    root=Path(out).resolve()
    if root.exists() and any(root.iterdir()):
        raise ValueError("new V4.2 experiment output directory required")
    p3=Path(v3).resolve(strict=True)
    p4=Path(v4).resolve(strict=True)
    p41=Path(v41).resolve(strict=True)
    previous_policy=_load_upstream(p3,p4,p41)
    root.mkdir(parents=True,exist_ok=True)
    images=root/"images"
    images.mkdir()
    training=[]
    for name,orientation,img in training_fixtures():
        path=images/("lesson_"+name+".png")
        sh=write_png(path,img)
        training.append(_make_lesson(name,orientation,img,sh))
    policy=learn_frame_policy(training,previous_policy)
    memory=root/"world_orientation_memory_candidate.json"
    write_json(memory,{
        "schema":SCHEMA,"training":training,"policy":policy,
        "prior_v4_1_sha256":sha(p41/"evaluation.json"),
        "source_kind":SYNTHETIC,"readonly":True,
        "memory_eligibility":"CANDIDATE_ONLY",
        "native_memory_write_allowed":False,
        "model_weights_trained":False,
        "sens_runtime_executed":False,
    })
    memory_hash=sha(memory)
    tests=[]
    worlds=[]
    commit_path=root/"decisions_before_feedback.jsonl"
    with commit_path.open("x",encoding="utf-8") as receipt:
        for i,(name,expected,img) in enumerate(test_fixtures()):
            filepath=images/("exam_"+name+".png")
            source_hash=write_png(filepath,img)
            obs=inspect_pixels(img)
            choice=classify_oriented(obs,policy)
            sealed={
                "id":name,
                "source_sha256":source_hash,
                "observation_sha256":digest_bytes(stable_bytes(obs)),
                "memory_sha256":memory_hash,
                "choice":choice,
                "teacher_feedback_unavailable_to_student":True,
                "teacher_part_boxes_unavailable_to_student":True,
                "source_kind":SYNTHETIC,
                "decision_authority":"KX108_ONLY",
            }
            receipt.write(json.dumps(sealed,sort_keys=True)+"\n")
            receipt.flush()
            # A teacher label must first appear AFTER this line is written.
            correct=_score_decision(choice,expected)
            row={"id":name,"expected":expected,"decision":choice,
                 "correct":correct,"image_sha256":source_hash,
                 "feedback_after_precommit":True,
                 "world_knowledge_validated":False}
            tests.append(row)
            worlds.append(memory_candidates(row,obs,choice,i))
    goal="LEFT"   # Only abstract relation goal, not teacher boxes/pixels.
    student=student_reconstruct(training,policy,goal)
    student_ref=images/"composition_student.png"
    student_sha=write_png(student_ref,student)
    precommit=root/"composition_before_teacher_reveal.json"
    write_json(precommit,{
        "requested_relation":goal,
        "source_training_refs":[x["id"] for x in training],
        "student_image_ref":"images/composition_student.png",
        "student_image_sha256":student_sha,
        "student_procedure":"ROTATE_STORED_COMPONENT_MASKS_AND_APPLY_LEARNED_RELATIVE_DIRECTION",
        "code_sha256":sha(MODULE),
        "memory_sha256":memory_hash,
        "teacher_target_read_before_student_commit":False,
        "teacher_box_coordinates_supplied":False,
        "real_world_identity_claimed":False,
        "native_memory_write_allowed":False,
    })
    # The target is generated AFTER the student image and sealed receipt.
    target=turn_scene(90,dx=4,dy=-3,scale=1.08)
    truth_ref=images/"composition_teacher_revealed.png"
    truth_sha=write_png(truth_ref,target)
    composition={
        "student_ref":"images/composition_student.png",
        "student_sha256":student_sha,
        "teacher_ref":"images/composition_teacher_revealed.png",
        "teacher_sha256":truth_sha,
        "score":pixel_score(target,student),
        "relation_score":relation_score(target,student,policy,goal),
        "student_saw_target_before_render":False,
        "role_masks_transformed_by_programmed_motor":True,
        "semantic_understanding_proven":False,
    }
    index={
        "schema":SCHEMA,"source_kind":SYNTHETIC,
        "prior_v3_eval_sha256":sha(p3/"evaluation.json"),
        "prior_v4_sha256":sha(p4),
        "prior_v41_eval_sha256":sha(p41/"evaluation.json"),
        "code_sha256":sha(MODULE),
        "memory_sha256":memory_hash,
        "decisions_sha256":sha(commit_path),
        "composition_precommit_sha256":sha(precommit),
        "lessons":len(training),
        "exams":tests,
        "world_experience_candidates":worlds,
        "candidate_relation_model":policy,
        "composition":composition,
        "range_of_rotations_tested":[0,90,180,270],
        "rotation_frame":"SYNTHETIC_2D_CANVAS_NOT_3D_360",
        "independent_object_identity_tracking":False,
        "reciprocal_relation_derived_by_reverse_vector":True,
        "orientation_labels_learned_from_teacher":True,
        "world_state_is_memory":False,
        "sens_runtime_executed":False,
        "native_memory_write_allowed":False,
        "auto_promotion_allowed":False,
        "decision_authority":"KX108_ONLY",
    }
    write_json(root/"evaluation.json",index)
    checked=verify(root,v3=p3,v4=p4,v41=p41)
    return {"evaluation":str(root/"evaluation.json"),
            "lessons":len(training),"exams":len(tests),
            "correct":sum(x["correct"] for x in tests),
            "held_unknown":sum(x["expected"] is None and x["correct"] for x in tests),
            "reciprocal_predictions":sum(x["decision"]["reciprocal"] is not None for x in tests),
            "composition_pixel_xor":composition["score"]["pixel_xor"],
            "composition_better_than_blank":composition["score"]["better_than_blank"],
            "composition_relation_match":composition["relation_score"]["both_match_direction"],
            "status":checked["status"],
            "native_memory_write_allowed":False}


def verify(folder:str|Path,*,v3:str|Path,v4:str|Path,v41:str|Path)->dict:
    root=Path(folder).resolve(strict=True)
    p3=Path(v3).resolve(strict=True)
    p4=Path(v4).resolve(strict=True)
    p41=Path(v41).resolve(strict=True)
    previous_policy=_load_upstream(p3,p4,p41)
    index=json.loads((root/"evaluation.json").read_text(encoding="utf-8"))
    if (index.get("schema")!=SCHEMA or index.get("source_kind")!=SYNTHETIC
        or index.get("code_sha256")!=sha(MODULE)
        or index.get("native_memory_write_allowed") is not False
        or index.get("auto_promotion_allowed") is not False
        or index.get("sens_runtime_executed") is not False
        or index.get("world_state_is_memory") is not False
        or index.get("decision_authority")!="KX108_ONLY"
        or index.get("rotation_frame")!="SYNTHETIC_2D_CANVAS_NOT_3D_360"):
        raise ValueError("untrusted orientation experiment or procedure")
    if (index["prior_v3_eval_sha256"]!=sha(p3/"evaluation.json")
        or index["prior_v4_sha256"]!=sha(p4)
        or index["prior_v41_eval_sha256"]!=sha(p41/"evaluation.json")):
        raise ValueError("ancestor experiment or memory receipt changed")
    memory=root/"world_orientation_memory_candidate.json"
    receipt=root/"decisions_before_feedback.jsonl"
    precommit=root/"composition_before_teacher_reveal.json"
    if (index["memory_sha256"]!=sha(memory)
        or index["decisions_sha256"]!=sha(receipt)
        or index["composition_precommit_sha256"]!=sha(precommit)):
        raise ValueError("candidate memory / decision receipts modified")
    saved=json.loads(memory.read_text(encoding="utf-8"))
    if (saved.get("schema")!=SCHEMA or saved.get("source_kind")!=SYNTHETIC
        or saved.get("native_memory_write_allowed") is not False
        or saved.get("memory_eligibility")!="CANDIDATE_ONLY"
        or saved.get("model_weights_trained") is not False
        or saved["prior_v4_1_sha256"]!=sha(p41/"evaluation.json")):
        raise ValueError("candidate memory asserted a false authority")
    lessons=saved["training"]
    recomputed=_expected_lessons(root)
    if stable_bytes(lessons)!=stable_bytes(recomputed):
        raise ValueError("lesson model changed")
    policy=learn_frame_policy(lessons,previous_policy)
    if (stable_bytes(policy)!=stable_bytes(saved["policy"])
        or stable_bytes(policy)!=stable_bytes(index["candidate_relation_model"])):
        raise ValueError("policy cannot be learned from declared lessons")
    sealed=[json.loads(line) for line in receipt.read_text(encoding="utf-8").splitlines()]
    expected_cases=test_fixtures()
    if len(index["exams"])!=len(expected_cases) or len(sealed)!=len(expected_cases):
        raise ValueError("missing exam evidence")
    for i,(row,receipt_row,(name,label,img)) in enumerate(
        zip(index["exams"],sealed,expected_cases)
    ):
        source=root/"images"/("exam_"+name+".png")
        obs=inspect_pixels(img)
        choice=classify_oriented(obs,policy)
        correct=_score_decision(choice,label)
        expected_world=memory_candidates(
            {"id":name,"expected":label,"correct":correct,
             "image_sha256":sha(source)},obs,choice,i)
        actual={
            "id":name,"expected":label,"decision":choice,
            "correct":correct,"image_sha256":sha(source),
            "feedback_after_precommit":True,
            "world_knowledge_validated":False,
        }
        proper_receipt={
            "id":name,"source_sha256":sha(source),
            "observation_sha256":digest_bytes(stable_bytes(obs)),
            "memory_sha256":sha(memory),"choice":choice,
            "teacher_feedback_unavailable_to_student":True,
            "teacher_part_boxes_unavailable_to_student":True,
            "source_kind":SYNTHETIC,
            "decision_authority":"KX108_ONLY",
        }
        if (sha(source)!=digest_bytes(_image_bytes_as_png(img))
            or stable_bytes(row)!=stable_bytes(actual)
            or stable_bytes(receipt_row)!=stable_bytes(proper_receipt)
            or stable_bytes(index["world_experience_candidates"][i])!=stable_bytes(expected_world)):
            raise ValueError("exam or candidate world evidence cannot be replayed")
    prior=json.loads(precommit.read_text(encoding="utf-8"))
    student=student_reconstruct(lessons,policy,"LEFT")
    target=turn_scene(90,dx=4,dy=-3,scale=1.08)
    art=root/"images"/"composition_student.png"
    teacher=root/"images"/"composition_teacher_revealed.png"
    expected_precommit={
        "requested_relation":"LEFT",
        "source_training_refs":[x["id"] for x in lessons],
        "student_image_ref":"images/composition_student.png",
        "student_image_sha256":sha(art),
        "student_procedure":"ROTATE_STORED_COMPONENT_MASKS_AND_APPLY_LEARNED_RELATIVE_DIRECTION",
        "code_sha256":sha(MODULE),
        "memory_sha256":sha(memory),
        "teacher_target_read_before_student_commit":False,
        "teacher_box_coordinates_supplied":False,
        "real_world_identity_claimed":False,
        "native_memory_write_allowed":False,
    }
    expected_comp={
        "student_ref":"images/composition_student.png",
        "student_sha256":sha(art),
        "teacher_ref":"images/composition_teacher_revealed.png",
        "teacher_sha256":sha(teacher),
        "score":pixel_score(target,student),
        "relation_score":relation_score(target,student,policy,"LEFT"),
        "student_saw_target_before_render":False,
        "role_masks_transformed_by_programmed_motor":True,
        "semantic_understanding_proven":False,
    }
    if (sha(art)!=digest_bytes(_image_bytes_as_png(student))
        or sha(teacher)!=digest_bytes(_image_bytes_as_png(target))
        or stable_bytes(prior)!=stable_bytes(expected_precommit)
        or stable_bytes(index["composition"])!=stable_bytes(expected_comp)):
        raise ValueError("student proposal or teacher holdout altered")
    return {"status":"PASS_V4_2_BOUNDED_ORIENTATION_AND_RECIPROCITY_REPLAY",
            "lessons_verified":len(lessons),
            "exams_verified":len(index["exams"]),
            "correct":sum(t["correct"] for t in index["exams"]),
            "candidate_world_experiences_verified":len(index["world_experience_candidates"]),
            "no_teacher_boxes_given_to_student":True,
            "world_semantics_proven":False,
            "sens_runtime_executed":False,
            "native_memory_write_allowed":False}


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
