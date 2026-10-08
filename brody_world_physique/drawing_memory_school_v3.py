"""Brody Drawing School V3: immediate, intervening-exercise, and novel-composition recall.

Protocol isolation:
- observer receives reference pixels, emits a bounded stroke representation;
- student receives ONLY this persisted representation and frozen V2 scores;
- teacher reference is reopened ONLY AFTER student's image SHA is precommitted;
- delayed recall loads the same representation from disk after 3 distractors;
- novel composition has NO target observation; it composes named prior V1
  motor candidates into requested boxes, then reveals an independently drawn
  teacher target.

This is a falsifiable synthetic memory-routing test, NOT human-like visual
understanding: stroke extraction is engineered and captures much of the
reference; the delay is interference, not time; composition is teacher-guided.
No Native Memory mutation or arbitrary execution of stored code.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from .drawing_school_v0 import (
    SIDE, CandidateExperienceLedgerV0, black_pixels, bbox_of, digest_bytes,
    signature_for, verify_candidate_ledger,
)
from .drawing_school_v1 import (
    GestureV1, teacher_exams, suggest_gestures_from_reference,
)
from .experience_memory_v1 import (
    checked_gesture, code_fingerprint, verify_memory_bundle, stable_bytes,
)
from .instrument_school_v2 import (
    TOOLS, select_tool, render_instrument, verify_school,
)

SCHEMA="BRODY_DRAWING_HIDDEN_REFERENCE_V3"
MAX_GESTURES=128
DISTRACTORS=("examen_croix","examen_courbe","examen_carre")
LEVELS=("immediate","delayed","transfer")
MODULE=Path(__file__).resolve()
MODULE_REL="brody_world_physique/drawing_memory_school_v3.py"


def _sha(path:Path)->str:
    return digest_bytes(path.read_bytes())


def _source_image(source:Image.Image)->Image.Image:
    gray=source.convert("L")
    if gray.size!=(SIDE,SIDE):raise ValueError("unsupported observation geometry")
    if not black_pixels(gray):raise ValueError("cannot encode blank reference")
    return gray


def _gestures(raw:list[dict]|tuple[dict,...])->tuple[GestureV1,...]:
    if not isinstance(raw,(list,tuple)) or not 1<=len(raw)<=MAX_GESTURES:
        raise ValueError("unbounded or empty gesture representation")
    return tuple(checked_gesture(x) for x in raw)


def _snapshot(gestures:tuple[GestureV1,...])->list[dict]:
    return [{"kind":g.kind,"points":[list(p) for p in g.points]} for g in gestures]


def observe_only(reference:Image.Image, ref:str, source_sha256:str)->dict:
    """Observer boundary: the only function that sees teacher reference."""
    image=_source_image(reference)
    ink=black_pixels(image)
    gestures=suggest_gestures_from_reference(image)
    if not gestures or len(gestures)>MAX_GESTURES:
        raise ValueError("observer failed to propose bounded motor representation")
    record={
        "schema":SCHEMA,"source_ref":ref,"observed_source_sha256":source_sha256,
        "context":"TEACHER_VISIBLE_ONLY_DURING_ENCODING",
        "representation_type":"RASTER_SKELETON_TO_MOTOR_STROKES",
        "bbox":list(bbox_of(ink)),
        "signature":list(signature_for(ink,bbox_of(ink))),
        "observed_ink_count":len(ink),
        "gestures":_snapshot(gestures),
        "source_pixels_in_memory":False,
        "representation_contains_detailed_contour":True,
        "learning_algorithm_autonomously_discovered":False,
        "interpretation_semantic":False,
        "memory_write_allowed":False,
    }
    record["representation_sha256"]=digest_bytes(stable_bytes(record))
    return record


def _verify_representation(rep:dict,expected_source:str)->tuple[GestureV1,...]:
    if rep.get("schema")!=SCHEMA or rep.get("observed_source_sha256")!=expected_source:
        raise ValueError("unexpected/altered observation source")
    body={k:v for k,v in rep.items() if k!="representation_sha256"}
    if digest_bytes(stable_bytes(body))!=rep.get("representation_sha256"):
        raise ValueError("observation representation receipt modified")
    if rep.get("source_pixels_in_memory") is not False or rep.get("representation_contains_detailed_contour") is not True:
        raise ValueError("memory encoding is misrepresented")
    return _gestures(rep["gestures"])


def _load_v2(prior:Path)->tuple[tuple[dict,...],dict]:
    info=verify_school(prior)
    episode=json.loads((prior/"instrument_skill_memory.json").read_text(encoding="utf-8"))
    lessons=episode["episodes"]
    if len(lessons)!=9 or len({x["id"] for x in lessons})!=9:
        raise ValueError("a complete frozen nine-lesson instrument school is required")
    return tuple(lessons),info


def _choose(frozen:tuple[dict,...],goal:str)->dict:
    selection=select_tool(frozen,goal)
    if selection["chosen_tool"] not in TOOLS:
        raise ValueError("known classroom intent unexpectedly unsupported")
    return selection


def draw_from_snapshot(rep:dict,choice:dict,expected_source_sha:str)->Image.Image:
    """Student boundary: receives no reference file, source image or scorer."""
    gestures=_verify_representation(rep,expected_source_sha)
    if choice["chosen_tool"] not in TOOLS:
        raise ValueError("no authorised drawing instrument")
    return render_instrument(gestures,choice["chosen_tool"])


def _fit_gestures(strokes:tuple[GestureV1,...], rect:tuple[int,int,int,int])->tuple[GestureV1,...]:
    if not all(type(x) is int for x in rect) or not (0<=rect[0]<rect[2]<SIDE and 0<=rect[1]<rect[3]<SIDE):
        raise ValueError("invalid composition bounds")
    points=[p for g in strokes for p in g.points]
    sx0=min(x for x,y in points);sy0=min(y for x,y in points)
    sx1=max(x for x,y in points);sy1=max(y for x,y in points)
    dx=max(1,sx1-sx0);dy=max(1,sy1-sy0)
    a,b,c,d=rect
    return tuple(GestureV1(points=tuple(
        (max(0,min(SIDE-1,round(a+(x-sx0)/dx*(c-a)))),
         max(0,min(SIDE-1,round(b+(y-sy0)/dy*(d-b))))
        for x,y in g.points),kind=g.kind) for g in strokes)


def assemble_from_prior_skills(prior_v1:Path, composition:list[dict])->tuple[GestureV1,...]:
    """No target bitmap is supplied. Components/bounds come from teacher task."""
    memory=json.loads((prior_v1/"candidate_skill_memory.json").read_text(encoding="utf-8"))
    approved={x["lesson_ref"]:x for x in memory["skills"]}
    output=[]
    for part in composition:
        name=part["skill_ref"]
        if name not in ("cours_carre","cours_triangle","cours_cercle","cours_trait"):
            raise ValueError("unknown primitive procedure")
        if name not in approved:raise ValueError("missing demonstrated skill")
        strokes=_gestures(approved[name]["gestures"])
        box=part["box"]
        if not isinstance(box,list) or len(box)!=4:raise ValueError("invalid task placement")
        output.extend(_fit_gestures(strokes,tuple(box)))
    if not output or len(output)>MAX_GESTURES:
        raise ValueError("invalid combined gesture count")
    return tuple(output)


def teacher_hidden_model()->Image.Image:
    """Fresh pentagon: not one of V1's teaching/exam raster fixtures."""
    img=Image.new("L",(SIDE,SIDE),255)
    d=ImageDraw.Draw(img)
    d.line(((14,49),(10,26),(30,9),(50,26),(46,49),(14,49)),
           fill=0,width=3)
    return img


def teacher_new_composition()->Image.Image:
    """Held-out source, created after commitment, independent of learner gestures."""
    img=Image.new("L",(SIDE,SIDE),255)
    d=ImageDraw.Draw(img)
    d.line(((14,31),(46,31),(46,55),(14,55),(14,31)),fill=0,width=3)
    d.line(((10,31),(30,9),(50,31)),fill=0,width=3)
    return img


def _save_image_once(image:Image.Image,dest:Path)->str:
    if dest.exists():raise ValueError("image evidence overwrite forbidden")
    image.save(dest)
    return _sha(dest)


def _score(source:Image.Image,proposed:Image.Image)->dict:
    ref=black_pixels(_source_image(source))
    predicted=black_pixels(proposed.convert("L"))
    wrong=len(ref.symmetric_difference(predicted))
    return {"pixel_xor":wrong,"blank_pixel_xor":len(ref),
            "recall_improves_over_blank":wrong<len(ref),
            "pixel_iou":len(ref&predicted)/max(1,len(ref|predicted))}


def _write_json(path:Path,data:dict)->str:
    if path.exists():raise ValueError("cannot overwrite memory trace")
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return _sha(path)


def _sealed_line(destination, event:dict):
    destination.write(json.dumps(event,ensure_ascii=False,sort_keys=True)+"\n")
    destination.flush()


def _commit_student(root:Path,episode:str,level:str,goal:str,representation:dict|None,
                    strokes:tuple[GestureV1,...],frozen:tuple[dict,...],
                    *, distractors:list[dict],task:list[dict]|None=None)->dict:
    """Student path cannot read any teacher source image or heldout target."""
    choice=_choose(frozen,goal)
    image=render_instrument(strokes,choice["chosen_tool"])
    output=root/"student_images"/(episode+"_drawing.png")
    drawing_sha=_save_image_once(image,output)
    procedure={
        "module":MODULE_REL,
        "code_sha256":_sha(MODULE),
        "instrument_renderer_module_sha256":_sha(Path(__file__).with_name("instrument_school_v2.py")),
        "image_to_gesture_code":code_fingerprint("image-thinning"),
        "motor_selection":"MIN_PRIOR_MEAN_PIXEL_ERROR_BY_DECLARED_INTENT",
        "no_dynamic_code_from_memory":True,
    }
    return {
        "episode":episode,"level":level,"goal":goal,
        "representation_ref":f"representations/{episode}.json" if representation else None,
        "representation_sha256":representation["representation_sha256"] if representation else None,
        "gestures":_snapshot(strokes),
        "composition_task":task,
        "distractor_records":distractors,
        "distractor_count":len(distractors),
        "instrument_selection":choice,
        "procedures":procedure,
        "output_ref":"student_images/"+output.name,
        "output_sha256":drawing_sha,
        "teacher_reference_available_to_student_during_drawing":False,
        "teacher_reference_read_during_student_step":False,
        "source_kind":"SIMULATED",
        "native_memory_write_allowed":False,
        "auto_promotion_allowed":False,
        "decision_authority":"KX108_ONLY",
    }


def run_school(out:str|Path,*,prior_v2:str|Path)->dict:
    root=Path(out).resolve()
    if root.exists() and any(root.iterdir()):raise ValueError("output folder must be fresh")
    prior=Path(prior_v2).resolve(strict=True)
    frozen,verified=_load_v2(prior)
    prior_v1=Path(json.loads((prior/"instrument_experience_index.json").read_text())["prior_school_source"]).resolve(strict=True)
    verify_memory_bundle(prior_v1)
    root.mkdir(parents=True,exist_ok=True)
    for d in ("representations","teacher_revealed","student_images","interference"):
        (root/d).mkdir()
    ledger=CandidateExperienceLedgerV0(root/"candidate_experience_ledger.jsonl")
    precommit=root/"committed_before_teacher_reveal.jsonl"
    teacher_refs=dict(teacher_exams())
    # The fresh teacher model is absent from ALL V1 lesson/exam fixtures.
    source=_source_image(teacher_hidden_model())
    source_sha=digest_bytes(source.tobytes())
    original_rep=observe_only(source,"teacher:hidden_pentagon_v3",source_sha)
    # Representation is serialized and reloaded before rendering.
    # No original PNG or teacher pixels are part of the student interface.
    records=[]
    evals=[]
    with precommit.open("x",encoding="utf-8") as receipt:
        for level in ("immediate","delayed"):
            ep=level+"_pentagon"
            snapshot=dict(original_rep)
            path=root/"representations"/(ep+".json")
            _write_json(path,snapshot)
            distractions=[]
            if level=="delayed":
                for i,name in enumerate(DISTRACTORS,1):
                    scene=_source_image(teacher_refs[name])
                    exposed=observe_only(scene,"distractor:"+name,digest_bytes(scene.tobytes()))
                    p=root/"interference"/(f"task_{i:02d}.json")
                    _write_json(p,exposed)
                    distractions.append({"source_ref":exposed["source_ref"],
                                         "representation_sha256":exposed["representation_sha256"],
                                         "task_index":i})
            # The drawing function receives ONLY the disk-loaded representation,
            # not the source. This is an API separation, NOT process isolation.
            loaded=json.loads(path.read_text(encoding="utf-8"))
            strokes=_verify_representation(loaded,source_sha)
            student=_commit_student(root,ep,level,"UNIFORM",loaded,strokes,
                                    frozen,distractors=distractions)
            _sealed_line(receipt,student) # before teacher comparison / reveal
            if level=="delayed" and len(distractions)!=3:
                raise ValueError("delayed trial did not complete interference")
            # Evaluation phase: teacher opens the exact reference AFTER receipt.
            target=root/"teacher_revealed"/(ep+"_reference.png")
            _save_image_once(source,target)
            outcome=_score(source,render_instrument(strokes,student["instrument_selection"]["chosen_tool"]))
            records.append(student)
            evals.append({"episode":ep,"level":level,"teacher_sha256":_sha(target),
                          "source_observation_sha256":source_sha,
                          "score":outcome,"memory_revisions_from_test":0})
            ledger.append({"event":"HIDDEN_REFERENCE_DRAWING_EVALUATED",
                           "episode":ep,"level":level,
                           "student_output_sha256":student["output_sha256"],
                           "teacher_target_sha256":_sha(target),
                           "pixel_xor":outcome["pixel_xor"],"memory_write_allowed":False})
        # NEW composition: only components + boxes, NOT example image.
        ep="transfer_house"
        task=[{"skill_ref":"cours_carre","box":[14,31,46,55]},
              {"skill_ref":"cours_triangle","box":[10,9,50,31]}]
        strokes=assemble_from_prior_skills(prior_v1,task)
        student=_commit_student(root,ep,"transfer","UNIFORM",None,strokes,
                                frozen,distractors=[],task=task)
        _sealed_line(receipt,student)
        # The target below was not seen by the learner, nor used to
        # select strokes, tools, or construct the composition.
        target_image=teacher_new_composition()
        target=root/"teacher_revealed"/(ep+"_reference.png")
        _save_image_once(target_image,target)
        outcome=_score(target_image,render_instrument(strokes,student["instrument_selection"]["chosen_tool"]))
        records.append(student)
        evals.append({"episode":ep,"level":"transfer","teacher_sha256":_sha(target),
                      "source_observation_sha256":None,
                      "score":outcome,"memory_revisions_from_test":0})
        ledger.append({"event":"HELDOUT_COMPOSITION_EVALUATED","episode":ep,
                       "source_kind":"SIMULATED","student_output_sha256":student["output_sha256"],
                       "teacher_target_sha256":_sha(target),
                       "pixel_xor":outcome["pixel_xor"],"memory_write_allowed":False})
    index={
        "schema":SCHEMA,"episodes":len(records),
        "results":evals,
        "reference_visible_during_drawing":False,
        "representation_kept_after_observation":True,
        "detailed_contour_in_representation":True,
        "delayed_trial_has_three_interference_exposures":True,
        "physical_delay_seconds":None,
        "source_kind":"SIMULATED",
        "prior_v2_source":str(prior),
        "prior_v2_memory_sha256":_sha(prior/"instrument_skill_memory.json"),
        "prior_v2_verified":True,
        "student_precommit_sha256":_sha(precommit),
        "ledger_sha256":_sha(ledger.filename),
        "student_outputs":[{"ref":r["output_ref"],"sha256":r["output_sha256"]} for r in records],
        "code_sha256":_sha(MODULE),
        "native_memory_write_allowed":False,
        "auto_promotion_allowed":False,
        "decision_authority":"KX108_ONLY",
    }
    _write_json(root/"evaluation.json",index)
    check=verify_school(root)
    return {"evaluation":str(root/"evaluation.json"),
            "episodes":len(records),
            "results":[{"level":e["level"],"pixel_xor":e["score"]["pixel_xor"],
                        "better_than_blank":e["score"]["recall_improves_over_blank"]} for e in evals],
            "verified_precommits":check["episodes_verified"],
            "reference_hidden_during_drawing":True,
            "native_memory_write_allowed":False}


def verify_school(folder:str|Path)->dict:
    root=Path(folder).resolve(strict=True)
    info=json.loads((root/"evaluation.json").read_text(encoding="utf-8"))
    if (info.get("schema")!=SCHEMA or info.get("source_kind")!="SIMULATED"
        or info.get("reference_visible_during_drawing") is not False
        or info.get("native_memory_write_allowed") is not False
        or info.get("auto_promotion_allowed") is not False
        or info.get("decision_authority")!="KX108_ONLY"):
        raise ValueError("untrusted school contract")
    prior=Path(info["prior_v2_source"]).resolve(strict=True)
    verify_school_v2(prior)
    frozen=tuple(json.loads((prior/"instrument_skill_memory.json").read_text())["episodes"])
    if _sha(prior/"instrument_skill_memory.json")!=info["prior_v2_memory_sha256"]:
        raise ValueError("prior instrument memory changed")
    if _sha(MODULE)!=info["code_sha256"]:
        raise ValueError("student procedure changed")
    receipt=root/"committed_before_teacher_reveal.jsonl"
    if _sha(receipt)!=info["student_precommit_sha256"]:
        raise ValueError("student commitment modified")
    events=[json.loads(x) for x in receipt.read_text(encoding="utf-8").splitlines()]
    if len(events)!=3 or [e.get("level") for e in events]!=list(LEVELS):
        raise ValueError("missing trial or reordered proof")
    if _sha(root/"candidate_experience_ledger.jsonl")!=info["ledger_sha256"]:
        raise ValueError("corrupted evaluation ledger")
    ledger=verify_candidate_ledger(root/"candidate_experience_ledger.jsonl")
    if len(info.get("results",[]))!=3:
        raise ValueError("evaluation table incomplete")
    source=teacher_hidden_model()
    source_sha=digest_bytes(source.tobytes())
    prior_v1=Path(json.loads((prior/"instrument_experience_index.json").read_text())["prior_school_source"]).resolve(strict=True)
    verify_memory_bundle(prior_v1)
    for i,(event,evaluation) in enumerate(zip(events,info["results"])):
        ep=event["episode"]
        if event["level"]!=evaluation["level"] or event["source_kind"]!="SIMULATED":
            raise ValueError("source or level contradiction")
        for attr in ("native_memory_write_allowed","auto_promotion_allowed",
                     "teacher_reference_available_to_student_during_drawing",
                     "teacher_reference_read_during_student_step"):
            if event[attr] is not False:raise ValueError("permission/future access escalation")
        if event["decision_authority"]!="KX108_ONLY":
            raise ValueError("authority contradiction")
        procedure=event["procedures"]
        if (procedure["code_sha256"]!=_sha(MODULE)
            or procedure["instrument_renderer_module_sha256"]!=_sha(Path(__file__).with_name("instrument_school_v2.py"))
            or procedure["image_to_gesture_code"]!=code_fingerprint("image-thinning")
            or procedure["no_dynamic_code_from_memory"] is not True):
            raise ValueError("code identity mismatch")
        selection=_choose(frozen,event["goal"])
        if selection!=event["instrument_selection"]:
            raise ValueError("tool selection does not replay from prior lessons")
        if event["level"] in ("immediate","delayed"):
            p=root/"representations"/(ep+".json")
            if event["representation_ref"]!="representations/"+p.name:
                raise ValueError("representation path contradiction")
            rep=json.loads(p.read_text(encoding="utf-8"))
            gestures=_verify_representation(rep,source_sha)
            if (event["representation_sha256"]!=rep["representation_sha256"]
                or stable_bytes(event["gestures"])!=stable_bytes(_snapshot(gestures))):
                raise ValueError("representation content mismatch")
            if event["level"]=="delayed":
                if len(event["distractor_records"])!=3 or event["distractor_count"]!=3:
                    raise ValueError("no delayed interference trials")
                for j,name in enumerate(DISTRACTORS,1):
                    q=root/"interference"/(f"task_{j:02d}.json")
                    d=json.loads(q.read_text(encoding="utf-8"))
                    expected=teacher_exams_dict()[name]
                    _verify_representation(d,digest_bytes(expected.tobytes()))
                    if event["distractor_records"][j-1]["representation_sha256"]!=d["representation_sha256"]:
                        raise ValueError("distractor memory altered")
            elif event["distractor_records"] or event["distractor_count"]!=0:
                raise ValueError("unexpected intermediate exercises")
            expected_teacher=source
            if evaluation["source_observation_sha256"]!=source_sha:
                raise ValueError("observation source changed")
        else:
            if event["representation_ref"] is not None or event["representation_sha256"] is not None:
                raise ValueError("transfer source must not be observed in advance")
            if event["composition_task"]!=[
                {"skill_ref":"cours_carre","box":[14,31,46,55]},
                {"skill_ref":"cours_triangle","box":[10,9,50,31]},
            ] or event["distractor_records"] or event["distractor_count"]:
                raise ValueError("composition task contract modified")
            gestures=assemble_from_prior_skills(prior_v1,event["composition_task"])
            if stable_bytes(_snapshot(gestures))!=stable_bytes(event["gestures"]):
                raise ValueError("transfer gestures were not composed from stored skills")
            expected_teacher=teacher_new_composition()
        student=render_instrument(gestures,selection["chosen_tool"])
        image_path=root/"student_images"/(ep+"_drawing.png")
        if event["output_ref"]!="student_images/"+image_path.name or _sha(image_path)!=event["output_sha256"]:
            raise ValueError("student output SHA changed")
        with Image.open(image_path) as actual:
            if actual.convert("L").tobytes()!=student.tobytes():
                raise ValueError("student drawing cannot be reproduced")
        teacher_path=root/"teacher_revealed"/(ep+"_reference.png")
        if _sha(teacher_path)!=evaluation["teacher_sha256"]:
            raise ValueError("teacher reference changed")
        with Image.open(teacher_path) as actual:
            if actual.convert("L").tobytes()!=expected_teacher.tobytes():
                raise ValueError("teacher reference was not the approved source")
        measured=_score(expected_teacher,student)
        if measured!=evaluation["score"] or evaluation["memory_revisions_from_test"]!=0:
            raise ValueError("stored visual score does not replay")
    return {"status":"PASS_HIDDEN_REFERENCE_EPISODIC_REPLAY",
            "episodes_verified":len(events),
            "ledger_events_verified":ledger["verified_records"],
            "prior_v2_verified":True,"prior_v1_verified":True,
            "native_memory_modified":False,"world_knowledge_validated":False}


# Do not shadow this module's verification function.
from .instrument_school_v2 import verify_school as verify_school_v2


def teacher_exams_dict()->dict[str,Image.Image]:
    return {name:img.convert("L") for name,img in teacher_exams()}


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(description="Brody V3 hidden-reference memory: immediate, distractor-delayed, prior-skill composition")
    p.add_argument("--out",type=Path)
    p.add_argument("--prior-v2",type=Path)
    p.add_argument("--verify",type=Path)
    a=p.parse_args(argv)
    if a.verify:
        if a.out or a.prior_v2:p.error("--verify excludes --out and --prior-v2")
        result=verify_school(a.verify)
    else:
        if not a.out or not a.prior_v2:p.error("--out and --prior-v2 required")
        result=run_school(a.out,prior_v2=a.prior_v2)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
