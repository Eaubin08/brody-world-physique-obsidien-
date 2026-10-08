"""V4.1 - pixel-first structural relation lessons within a *candidate* world.

The professor's coordinates are never provided to the observer, classifier,
or composer. Segmentation uses connected components of dark pixels. Labeled
training feedback teaches a NEAR-vs-FAR distinction from measured normalized
distance, tested on shifted, scaled and 90-degree rotated images.

Novel-composition task asks only for the learned NEAR relation; the student
retrieves observed component patches and an empirical relative offset from
training, and precommits its generated PNG before teacher reveals a new
target. This is a deliberately limited pixel heuristic, NOT semantic object
identity or a general world model. A hard reversed-arrangement negative is
reported even when the model fails. No SENS run, Native Memory write, or KX
action. The V4 source bridge is verified, not modified.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from math import hypot, sqrt
from statistics import mean
from typing import Any

from PIL import Image, ImageDraw

from .drawing_school_v0 import digest_bytes
from .experience_memory_v1 import stable_bytes
from .world_experience_bridge_v4 import verify_world_bundle

SCHEMA="BRODY_WORLD_RELATIONS_SCHOOL_V4_1"
SIDE=64
KINDS=("NEAR","FAR")
MODULE=Path(__file__).resolve()


def digest(path:Path)->str:
    return digest_bytes(path.read_bytes())


def _new_picture()->Image.Image:
    return Image.new("L",(SIDE,SIDE),255)


def professor_scene(kind:str,*,dx:int=0,dy:int=0,scale:float=1.0,
                    turn:int=0)->Image.Image:
    """Teacher-only fixture generator; NEVER fed as parameters to pupil."""
    if kind not in ("NEAR","FAR","REVERSED"):
        raise ValueError("unknown fixture")
    if not .70<=scale<=1.20 or turn not in (0,90):
        raise ValueError("unsupported synthetic transform")
    img=_new_picture()
    d=ImageDraw.Draw(img)
    # Two DISCONNECTED filled bodies so visual segmentation needs no
    # teacher-provided part boxes or semantic labels.
    roof=[(22,25),(32,13),(42,25)]
    body=(22,31,42,45)
    if kind=="FAR":
        roof=[(22,13),(32,3),(42,13)]
        body=(22,43,42,55)
    if kind=="REVERSED":
        roof=[(22,52),(32,40),(42,52)]
        body=(22,9,42,23)
    def map_point(p:tuple[int,int])->tuple[int,int]:
        x,y=p
        return (round(32+(x-32)*scale+dx),round(32+(y-32)*scale+dy))
    d.polygon([map_point(p) for p in roof],fill=0)
    x0,y0=map_point(body[:2]);x1,y1=map_point(body[2:])
    d.rectangle((x0,y0,x1,y1),fill=0)
    if turn:
        img=img.transpose(Image.Transpose.ROTATE_90)
    return img


def inspect_pixels(image:Image.Image)->dict[str,Any]:
    """ONLY image pixels; this function has no fixture or box arguments."""
    img=image.convert("L")
    if img.size!=(SIDE,SIDE):raise ValueError("invalid classroom canvas")
    data=img.tobytes()
    unused={i for i,p in enumerate(data) if p<128}
    components=[]
    while unused:
        seed=min(unused)
        stack=[seed]
        unused.remove(seed)
        group=[]
        while stack:
            cur=stack.pop()
            x,y=cur%SIDE,cur//SIDE
            group.append((x,y))
            for yy in range(max(0,y-1),min(SIDE,y+2)):
                for xx in range(max(0,x-1),min(SIDE,x+2)):
                    q=yy*SIDE+xx
                    if q in unused:
                        unused.remove(q)
                        stack.append(q)
        if len(group)>=8:components.append(group)
    components.sort(key=lambda g:(-len(g), min(p[1] for p in g),
                                  min(p[0] for p in g)))
    observation={
        "component_count":len(components),
        "components":[],
        "segmentation":"BINARY_8_CONNECTED_PIXELS_NO_TEACHER_BOXES",
        "source_kind":"SIMULATED",
    }
    for group in components[:8]:
        x0=min(x for x,y in group);x1=max(x for x,y in group)
        y0=min(y for x,y in group);y1=max(y for x,y in group)
        cx=mean(x for x,y in group);cy=mean(y for x,y in group)
        observation["components"].append({
            "area_px":len(group),"bbox":[x0,y0,x1,y1],
            "centroid_xy":[cx,cy],
            "pixel_points":[[x,y] for x,y in sorted(group)],
        })
    if len(components)==2:
        a,b=observation["components"]
        sep=hypot(a["centroid_xy"][0]-b["centroid_xy"][0],
                  a["centroid_xy"][1]-b["centroid_xy"][1])
        # Approx. scale-invariant; geometrically symmetric under 90°.
        denominator=sqrt(a["area_px"])+sqrt(b["area_px"])
        observation["features"]={
            "normalized_distance":sep/denominator,
            "area_ratio":min(a["area_px"],b["area_px"])/max(a["area_px"],b["area_px"]),
            "normalized_center_dx":(b["centroid_xy"][0]-a["centroid_xy"][0])/denominator,
            "normalized_center_dy":(b["centroid_xy"][1]-a["centroid_xy"][1])/denominator,
        }
    else:
        observation["features"]=None
    return observation


def learn_relation(lessons:list[dict])->dict[str,Any]:
    """Learn a numerical separation rule from feedback, not from class labels."""
    good=[x["features"]["normalized_distance"] for x in lessons
          if x["teacher_feedback"]=="NEAR"]
    bad=[x["features"]["normalized_distance"] for x in lessons
         if x["teacher_feedback"]=="FAR"]
    if not good or not bad or max(good)>=min(bad):
        return {"status":"HOLD_NOT_SEPARABLE","threshold":None,
                "training_example_ids":[x["id"] for x in lessons],
                "confidence_calibrated":False}
    return {"status":"CANDIDATE_LEARNED_THRESHOLD",
            "threshold":(max(good)+min(bad))/2,
            "near_max_observed":max(good),"far_min_observed":min(bad),
            "training_example_ids":[x["id"] for x in lessons],
            "selection_rule":"MIDPOINT_BETWEEN_OBSERVED_CLASSES",
            "confidence_calibrated":False}


def classify(observation:dict,policy:dict)->dict:
    if observation["component_count"]!=2 or not observation["features"]:
        return {"status":"HOLD_UNSUPPORTED_COMPONENT_TOPOLOGY","candidate":None,
                "reason":"REQUIRES_EXACTLY_TWO_DISCONNECTED_COMPONENTS"}
    if policy["status"]!="CANDIDATE_LEARNED_THRESHOLD":
        return {"status":"HOLD_NO_LEARNED_RELATION","candidate":None}
    value=observation["features"]["normalized_distance"]
    return {"status":"CANDIDATE_ONLY",
            "candidate":"NEAR" if value<=policy["threshold"] else "FAR",
            "distance":value,"threshold":policy["threshold"],
            "semantic_label_predicted":None,
            "physical_object_identity_proven":False}


def _write_png(folder:Path,name:str,img:Image.Image)->dict:
    folder.mkdir(parents=True,exist_ok=True)
    p=folder/(name+".png")
    if p.exists():raise ValueError("image evidence overwrite")
    img.save(p)
    return {"ref":p.relative_to(folder.parent).as_posix(),"sha256":digest(p)}


def _write_json(path:Path,value:dict)->str:
    if path.exists():raise ValueError("evidence overwrite")
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return digest(path)


def _teacher_training()->list[tuple[str,str,Image.Image]]:
    return [
        ("lesson01","NEAR",professor_scene("NEAR")),
        ("lesson02","NEAR",professor_scene("NEAR",dx=2,dy=-2,scale=.85)),
        ("lesson03","NEAR",professor_scene("NEAR",dx=-2,dy=2,scale=1.10)),
        ("lesson04","FAR",professor_scene("FAR")),
        ("lesson05","FAR",professor_scene("FAR",dx=1,dy=1,scale=.9)),
        ("lesson06","FAR",professor_scene("FAR",dx=-2,dy=-1,scale=1.05)),
    ]


def _teacher_exams()->list[tuple[str,str,Image.Image]]:
    return [
        ("shifted","NEAR",professor_scene("NEAR",dx=6,dy=4)),
        ("quarter_turn","NEAR",professor_scene("NEAR",turn=90)),
        ("scaled","NEAR",professor_scene("NEAR",scale=1.18)),
        ("far_shifted","FAR",professor_scene("FAR",dx=6,dy=-1)),
        # A known adversarial case: proximity alone does not encode
        # orientation/order. Keep a failure when it happens.
        ("reversed_hard_negative","FAR",professor_scene("REVERSED")),
        ("single_component","HOLD",Image.new("L",(SIDE,SIDE),255)),
    ]


def compose_from_experience(training:list[dict],policy:dict)->Image.Image:
    """Pupil sees experience-derived components/centers, not target boxes."""
    if policy["status"]!="CANDIDATE_LEARNED_THRESHOLD":
        raise ValueError("composition requires a learned policy")
    positive=[row for row in training if row["teacher_feedback"]=="NEAR"]
    if not positive:raise ValueError("no positive experiences")
    # Build from first observed two silhouettes, with centers and their
    # relative placement saved via perception. No target / teacher boxes.
    prototype=positive[0]["observation"]["components"]
    pixels=[c["pixel_points"] for c in prototype]
    all_points=[point for part in pixels for point in part]
    xmin=min(p[0] for p in all_points);xmax=max(p[0] for p in all_points)
    ymin=min(p[1] for p in all_points);ymax=max(p[1] for p in all_points)
    center=((xmin+xmax)/2,(ymin+ymax)/2)
    img=_new_picture()
    pix=img.load()
    # New absolute position chosen by student default canvas center,
    # not by per-exam teacher labels/rectangles.
    offx=32-center[0];offy=32-center[1]
    for p in all_points:
        x=round(p[0]+offx);y=round(p[1]+offy)
        if 0<=x<SIDE and 0<=y<SIDE:pix[x,y]=0
    return img


def _evaluate(source:Image.Image,drawn:Image.Image)->dict:
    t=source.convert("L").tobytes();p=drawn.convert("L").tobytes()
    ref={i for i,x in enumerate(t) if x<128}
    predicted={i for i,x in enumerate(p) if x<128}
    union=ref|predicted
    error=len(ref^predicted)
    return {"pixel_xor":error,"blank_error":len(ref),
            "better_than_blank":error<len(ref),
            "pixel_iou":len(ref&predicted)/len(union) if union else 1.0}


def run_school(out:str|Path,*,prior_v3:str|Path,prior_v4:str|Path)->dict:
    root=Path(out).resolve()
    if root.exists() and any(root.iterdir()):
        raise ValueError("output directory must be fresh")
    prior3=Path(prior_v3).resolve(strict=True)
    prior4=Path(prior_v4).resolve(strict=True)
    upstream=verify_world_bundle(prior3,prior4)
    if upstream["candidate_experiences"]!=3 or upstream["world_understanding_proven"]:
        raise ValueError("upstream candidate state mismatch")
    root.mkdir(parents=True,exist_ok=True)
    images=root/"images"
    images.mkdir()
    training=[]
    for name,category,img in _teacher_training():
        evidence=_write_png(images,"train_"+name,img)
        observation=inspect_pixels(img)
        if observation["component_count"]!=2:
            raise ValueError("invalid classroom fixture segmentation")
        training.append({
            "id":name,"teacher_feedback":category,
            "image":evidence,"features":observation["features"],
            "observation":observation,
            "episode_status":"SIMULATED_EXPERIENCE_CANDIDATE",
        })
    learned=learn_relation(training)
    if learned["status"]!="CANDIDATE_LEARNED_THRESHOLD":
        raise ValueError("teacher examples failed to separate")
    memory=root/"world_relation_memory_candidate.json"
    _write_json(memory,{
        "schema":SCHEMA,"training":training,"policy":learned,
        "root_world_view_sha256":digest(prior4),
        "model_weights_trained":False,
        "native_memory_write_allowed":False,
        "candidate_only":True,
    })
    memory_sha=digest(memory)
    results=[]
    receipt=root/"choices_before_teacher_feedback.jsonl"
    with receipt.open("x",encoding="utf-8") as stream:
        for name,truth,img in _teacher_exams():
            if truth=="HOLD":
                # Construct a single-component example (unseen topology).
                img=_new_picture()
                ImageDraw.Draw(img).ellipse((14,14,45,45),fill=0)
            src=_write_png(images,"exam_"+name,img)
            observed=inspect_pixels(img)
            decision=classify(observed,learned)
            precommit={
                "test_ref":name,"source_sha256":src["sha256"],
                "raster_observation":observed,
                "memory_sha256":memory_sha,"choice":decision,
                "teacher_label_accessed_before_decision":False,
                "no_teacher_boxes_provided":True,
                "decision_authority":"KX108_ONLY",
            }
            stream.write(json.dumps(precommit,sort_keys=True)+"\n")
            stream.flush()
            # Only now look at the teacher's independent answer.
            is_correct=(decision["candidate"]==truth) if truth!="HOLD" else (
                decision["status"]=="HOLD_UNSUPPORTED_COMPONENT_TOPOLOGY")
            results.append({
                "test_ref":name,"truth":truth,"decision":decision,
                "correct":is_correct,
                "reason":"TEACHER_LABEL_REVEALED_AFTER_PRECOMMIT",
                "source_sha256":src["sha256"],
                "world_knowledge_validated":False,
            })
    # Student reconstructs a composite WITHOUT test target, then precommits
    # the student art/hash; the teacher target is produced only afterward.
    pupil=compose_from_experience(training,learned)
    student=_write_png(images,"composition_candidate",pupil)
    composition_receipt=root/"composition_before_reveal.json"
    _write_json(composition_receipt,{
        "procedure":"REUSE_OBSERVED_TWO_COMPONENT_PATCHES_AND_RELATIVE_PLACEMENT",
        "training_refs":[x["id"] for x in training if x["teacher_feedback"]=="NEAR"],
        "memory_sha256":memory_sha,
        "student_artifact":student,
        "target_revealed":False,
        "instructed_component_boxes":None,
        "semantic_object_name_given_to_student":None,
        "code_sha256":digest(MODULE),
        "native_memory_write_allowed":False,
    })
    target=professor_scene("NEAR",dx=-4,dy=3,scale=1.1)
    target_art=_write_png(images,"composition_teacher_revealed",target)
    composition={
        "student":student,"teacher":target_art,
        "score":_evaluate(target,pupil),
        "teacher_target_accessed_after_artifact_commit":True,
        "novel_composition_is_rearranged_stored_pixels":True,
        "semantic_structure_discovered":False,
    }
    candidate_world={
        "schema":SCHEMA,
        "upstream_world_v4_sha256":digest(prior4),
        "upstream_v3_sha256":digest(prior3/"evaluation.json"),
        "code_sha256":digest(MODULE),
        "memory_sha256":memory_sha,
        "choices_sha256":digest(receipt),
        "composition_sha256":digest(composition_receipt),
        "source_kind":"SIMULATED",
        "training_lessons":len(training),
        "tests":results,
        "learned_relation":learned,
        "composition":composition,
        "relation_attribution":"PIXEL_COMPONENT_DISTANCE_LEARNED_FROM_LABELED_TEACHER_EXAMPLES",
        "spatial_direction_understood":False,
        "rotation_invariant_relation":"DISTANCE_ONLY_NOT_ABOVE_BELOW",
        "world_identity_verified":False,
        "sens_executed":False,
        "no_b8_promotion":True,
        "native_memory_write_allowed":False,
        "auto_promotion_allowed":False,
        "decision_authority":"KX108_ONLY",
    }
    _write_json(root/"evaluation.json",candidate_world)
    confirmation=verify_school(root,prior_v3=prior3,prior_v4=prior4)
    return {"evaluation":str(root/"evaluation.json"),
            "tests":len(results),
            "correct":sum(x["correct"] for x in results),
            "known_adversarial_error":not next(x["correct"] for x in results if
                                                x["test_ref"]=="reversed_hard_negative"),
            "candidate_composition_xor":composition["score"]["pixel_xor"],
            "composition_better_than_blank":composition["score"]["better_than_blank"],
            "verified":confirmation["status"],
            "native_memory_write_allowed":False}


def verify_school(folder:str|Path,*,prior_v3:str|Path,prior_v4:str|Path)->dict:
    root=Path(folder).resolve(strict=True)
    p3=Path(prior_v3).resolve(strict=True);p4=Path(prior_v4).resolve(strict=True)
    verify_world_bundle(p3,p4)
    index=json.loads((root/"evaluation.json").read_text(encoding="utf-8"))
    if index.get("schema")!=SCHEMA or index.get("code_sha256")!=digest(MODULE) or (
        index.get("native_memory_write_allowed") is not False
        or index.get("auto_promotion_allowed") is not False
        or index.get("sens_executed") is not False
        or index.get("decision_authority")!="KX108_ONLY"):
        raise ValueError("untrusted world experiment or version changed")
    if index["upstream_world_v4_sha256"]!=digest(p4) or index["upstream_v3_sha256"]!=digest(p3/"evaluation.json"):
        raise ValueError("upstream evidence mismatch")
    memory=root/"world_relation_memory_candidate.json"
    choice=root/"choices_before_teacher_feedback.jsonl"
    composition_ref=root/"composition_before_reveal.json"
    if (index["memory_sha256"]!=digest(memory) or
        index["choices_sha256"]!=digest(choice) or
        index["composition_sha256"]!=digest(composition_ref)):
        raise ValueError("memory or precommitted evidence tampered")
    data=json.loads(memory.read_text(encoding="utf-8"))
    if (data["schema"]!=SCHEMA or data["native_memory_write_allowed"] is not False
        or data["candidate_only"] is not True
        or data["root_world_view_sha256"]!=digest(p4)):
        raise ValueError("untrusted candidate memory")
    training=data["training"]
    if len(training)!=6:raise ValueError("training episode mismatch")
    for row,(name,teacher_label,source) in zip(training,_teacher_training()):
        if row["id"]!=name or row["teacher_feedback"]!=teacher_label:
            raise ValueError("training feedback changed")
        p=root/row["image"]["ref"]
        if digest(p)!=row["image"]["sha256"] or (
            Image.open(p).convert("L").tobytes()!=source.tobytes()):
            raise ValueError("training source image altered")
        observed=inspect_pixels(Image.open(p))
        if stable_bytes(row["observation"])!=stable_bytes(observed) or row["features"]!=observed["features"]:
            raise ValueError("training observation modified")
    policy=learn_relation(training)
    if stable_bytes(policy)!=stable_bytes(data["policy"]) or (
        stable_bytes(policy)!=stable_bytes(index["learned_relation"])):
        raise ValueError("learned model no longer matches experiences")
    recorded=[json.loads(s) for s in choice.read_text(encoding="utf-8").splitlines()]
    exams=_teacher_exams()
    if len(recorded)!=len(exams) or len(index["tests"])!=len(exams):
        raise ValueError("exam count mismatch")
    for rec,eval_row,(name,truth,fixture) in zip(recorded,index["tests"],exams):
        if truth=="HOLD":
            fixture=_new_picture()
            ImageDraw.Draw(fixture).ellipse((14,14,45,45),fill=0)
        path=root/"images"/("exam_"+name+".png")
        obs=inspect_pixels(Image.open(path))
        decision=classify(obs,policy)
        expected_correct=(decision["candidate"]==truth) if truth!="HOLD" else (
            decision["status"]=="HOLD_UNSUPPORTED_COMPONENT_TOPOLOGY")
        if (rec["test_ref"]!=name or rec["source_sha256"]!=digest(path)
            or rec["source_sha256"]!=eval_row["source_sha256"]
            or Image.open(path).convert("L").tobytes()!=fixture.tobytes()
            or rec["teacher_label_accessed_before_decision"] is not False
            or rec["no_teacher_boxes_provided"] is not True
            or rec["decision_authority"]!="KX108_ONLY"
            or rec["memory_sha256"]!=digest(memory)
            or stable_bytes(rec["raster_observation"])!=stable_bytes(obs)
            or stable_bytes(rec["choice"])!=stable_bytes(decision)
            or stable_bytes(eval_row["decision"])!=stable_bytes(decision)
            or eval_row["truth"]!=truth or eval_row["correct"]!=expected_correct):
            raise ValueError("test decision/source/teacher feedback not replayable")
    rec=json.loads(composition_ref.read_text(encoding="utf-8"))
    target=professor_scene("NEAR",dx=-4,dy=3,scale=1.1)
    student=compose_from_experience(training,policy)
    out=root/"images"/"composition_candidate.png"
    truth=root/"images"/"composition_teacher_revealed.png"
    comp=index["composition"]
    if (rec["memory_sha256"]!=digest(memory)
        or rec["target_revealed"] is not False
        or rec["instructed_component_boxes"] is not None
        or rec["semantic_object_name_given_to_student"] is not None
        or rec["code_sha256"]!=digest(MODULE)
        or rec["student_artifact"]["ref"]!="images/"+out.name
        or rec["student_artifact"]["sha256"]!=digest(out)
        or Image.open(out).convert("L").tobytes()!=student.tobytes()
        or comp["student"]!=rec["student_artifact"]
        or comp["teacher"]["sha256"]!=digest(truth)
        or Image.open(truth).convert("L").tobytes()!=target.tobytes()
        or stable_bytes(comp["score"])!=stable_bytes(_evaluate(target,student))):
        raise ValueError("new composition not reproducible independently")
    return {
        "status":"PASS_WORLD_RELATION_V4_1_BOUNDED_REPLAY",
        "training_verified":len(training),"exams_verified":len(exams),
        "positive_tests":sum(r["correct"] for r in index["tests"]),
        "known_failure_count":sum(not r["correct"] for r in index["tests"]),
        "student_has_no_test_teacher_boxes":True,
        "sens_executed":False,
        "native_memory_write_allowed":False,
    }


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(description="V4.1 supervised relation learning from pixels, with transformation and blind composition")
    p.add_argument("--prior-v3",type=Path,required=True)
    p.add_argument("--prior-v4",type=Path,required=True)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--out",type=Path)
    group.add_argument("--verify",type=Path)
    args=p.parse_args(argv)
    result=run_school(args.out,prior_v3=args.prior_v3,prior_v4=args.prior_v4) if args.out else verify_school(args.verify,prior_v3=args.prior_v3,prior_v4=args.prior_v4)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
