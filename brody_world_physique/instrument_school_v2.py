"""Brody drawing instrument classroom V2, purely synthetic and noncanonical.

Pencil / pen / nib are *existing simulated computer tools*. The teacher
provides an intent and evaluates three instruments during TRAIN. Brody
learns empirical error per intent, then selects from those observations
before any TEST target is opened. It does not learn art, physics, semantic
intent, tool design, or model weights. New instrument choice is *routing*.

The original V1 drawing/memory bundle is verified and reused for gesture
plans, including code fingerprints. Test geometry may use existing generic
raster-to-gesture code; only the *instrument* choice is learned here.
All outputs are local, sha-linked candidate receipts; no native memory write.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from math import hypot
from pathlib import Path
from statistics import mean
from typing import Any

from PIL import Image, ImageDraw, ImageFilter
import PIL

from .drawing_school_v0 import (
    SIDE, CandidateExperienceLedgerV0, black_pixels, bbox_of, digest_bytes,
    signature_for, verify_candidate_ledger,
)
from .drawing_school_v1 import GestureV1, teacher_exams, teacher_lessons, suggest_gestures_from_reference
from .experience_memory_v1 import (
    checked_gesture, code_fingerprint, verify_memory_bundle,
)

SCHEMA="BRODY_INSTRUMENT_SCHOOL_V2"
TRAIN_GOALS=("LIGHT","UNIFORM","EXPRESSIVE")
TOOLS=("PENCIL","PEN","NIB")
# Teacher-only synthetic targets. Learner selection never calls this map.
TEACHER_ONLY_STYLE_TARGET={"LIGHT":"PENCIL","UNIFORM":"PEN","EXPRESSIVE":"NIB"}
MAX_LESSONS=9
UNFAMILIAR="UNSEEN_INTENT"
SOURCE_KIND="SIMULATED"
MODULE=Path(__file__).resolve()


def source_hash(path:Path)->str:
    return digest_bytes(path.read_bytes())


def _safe_tool(name:str)->str:
    if name not in TOOLS:
        raise ValueError("unknown/untrusted drawing instrument")
    return name


def _gray_pixel_loss(a:Image.Image,b:Image.Image)->float:
    if a.size!=(SIDE,SIDE) or b.size!=(SIDE,SIDE):
        raise ValueError("only 64x64 grayscale classroom images")
    aa=a.convert("L").tobytes();bb=b.convert("L").tobytes()
    return sum(abs(x-y) for x,y in zip(aa,bb))/len(aa)


def render_instrument(gestures:tuple[GestureV1,...],tool:str)->Image.Image:
    """Whitelisted computer pens; tool stroke physics is PREPROGRAMMED."""
    tool=_safe_tool(tool)
    img=Image.new("L",(SIDE,SIDE),255)
    pen=ImageDraw.Draw(img)
    for g in gestures:
        if g.kind not in ("STRAIGHT_STROKE","CURVED_STROKE"):
            raise ValueError("untrusted gesture kind")
        if len(g.points)<2 or len(g.points)>256:
            raise ValueError("invalid number of gesture points")
        for a,b in zip(g.points,g.points[1:]):
            x0,y0=a;x1,y1=b
            if any(type(v) is not int or v<0 or v>=SIDE for v in (x0,y0,x1,y1)):
                raise ValueError("gesture coordinate beyond canvas")
            if tool=="PENCIL":
                pen.line((a,b),fill=125,width=3)
            elif tool=="PEN":
                pen.line((a,b),fill=0,width=2)
            else:
                # Synthetic broad nib: line varies with direction. NOT
                # a physically measured fountain pen or fluid simulation.
                dx,dy=abs(x1-x0),abs(y1-y0)
                weight=1+round(3*dx/max(1,dx+dy))
                pen.line((a,b),fill=20,width=weight)
    if tool=="PENCIL":
        img=img.filter(ImageFilter.GaussianBlur(radius=0.32))
    return img


def _print_kind(image:Image.Image)->tuple[int,...]:
    ink=black_pixels(image)
    return signature_for(ink,bbox_of(ink))


def _demo_spec(ref:str,goal:str,teacher:Image.Image,gestures:tuple[GestureV1,...])->dict:
    if goal not in TRAIN_GOALS and goal!=UNFAMILIAR:
        raise ValueError("unrecognized intent")
    return {"id":ref,"goal":goal,"image":teacher,"gestures":gestures}


def _teacher_targets(spec:dict)->Image.Image:
    """Called only during feedback AFTER choice; never by select_tool()."""
    goal=spec["goal"]
    # UNFAMILIAR has a teacher target for evaluation but never a goal label
    # the pupil had seen in training.
    oracle_tool=TEACHER_ONLY_STYLE_TARGET.get(goal,"PEN")
    return render_instrument(spec["gestures"],oracle_tool)


def _training_specs(prior:Path)->list[dict]:
    skills=json.loads((prior/"candidate_skill_memory.json").read_text(encoding="utf-8"))
    by_lesson={s["lesson_ref"]:s for s in skills["skills"]}
    # Use V1 gestures stored in the *actual*, independently verified memory.
    source_names=("cours_trait","cours_triangle","cours_cercle")
    result=[]
    for goal in TRAIN_GOALS:
        for name in source_names:
            art=Image.open(prior/"teacher_images"/(name+".png")).convert("L")
            gestures=tuple(checked_gesture(g) for g in by_lesson[name]["gestures"])
            result.append(_demo_spec("training_%02d"%(len(result)+1),goal,art,gestures))
    return result


def _exam_specs()->list[dict]:
    examples=dict(teacher_exams())
    choices=(("examen_trait","LIGHT"),("examen_cercle","UNIFORM"),
             ("examen_triangle","EXPRESSIVE"),("examen_courbe",UNFAMILIAR))
    return [_demo_spec("exam_%02d"%(i+1),goal,examples[shape],
                       suggest_gestures_from_reference(examples[shape]))
            for i,(shape,goal) in enumerate(choices)]


def select_tool(experiences:tuple[dict,...],goal:str, *,
                min_episodes:int=1)->dict:
    """Empirical mean reward; no tool/style mapping and no heldout target."""
    if goal not in TRAIN_GOALS+(UNFAMILIAR,):
        raise ValueError("unknown intent value")
    if not 1<=min_episodes<=MAX_LESSONS:
        raise ValueError("invalid confidence data threshold")
    matches=[x for x in experiences if x["goal"]==goal]
    if len(matches)<min_episodes:
        return {"status":"HOLD_NO_MATCHING_EXPERIENCE",
                "chosen_tool":None,"based_on_training_ids":[],
                "candidate_losses":None,
                "selection_rule":"MIN_PRIOR_MEAN_PIXEL_ERROR_BY_DECLARED_INTENT",
                "confidence_calibrated":False}
    table={}
    for tool in TOOLS:
        values=[]
        for x in matches:
            trials=x.get("trial_losses")
            if not isinstance(trials,dict) or set(trials)!=set(TOOLS):
                raise ValueError("incomplete teacher training feedback")
            value=trials[tool]
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=255:
                raise ValueError("invalid empirical loss")
            values.append(value)
        table[tool]=mean(values)
    # Stable deterministic tie break; confidence is NOT calibrated.
    chosen=min(TOOLS,key=lambda tool:(table[tool],TOOLS.index(tool)))
    return {"status":"INSTRUMENT_CANDIDATE_FROM_PRIOR_EXPERIENCE",
            "chosen_tool":chosen,"based_on_training_ids":[x["id"] for x in matches],
            "candidate_losses":table,
            "selection_rule":"MIN_PRIOR_MEAN_PIXEL_ERROR_BY_DECLARED_INTENT",
            "confidence_calibrated":False}


def _emit_image(image:Image.Image,folder:Path,name:str)->dict:
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/(name+".png")
    if path.exists():raise ValueError("no overwrite of art evidence")
    image.save(path)
    return {"ref":str(path.name),"sha256":source_hash(path)}


def _record_candidate(ledger:CandidateExperienceLedgerV0,event:dict):
    ledger.append({"event":event.pop("event"),**event,
                   "source_kind":SOURCE_KIND,"memory_write_allowed":False,
                   "auto_promotion_allowed":False})


def run_school(output:str|Path, *, prior_school:str|Path|None=None,
               training_lessons:int=MAX_LESSONS)->dict:
    if type(training_lessons) is not int or not 0<=training_lessons<=MAX_LESSONS:
        raise ValueError("training_lessons must be an integer 0..9")
    out=Path(output).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("fresh output required")
    # The prior-school V1 has already been executed; use verified gestures.
    # For convenience, create one inside the V2 experiment if not supplied.
    out.mkdir(parents=True,exist_ok=True)
    if prior_school is None:
        from .drawing_school_v1 import run_school as make_prior
        prior=out/"prior_drawing_school_v1"
        make_prior(prior)
    else:
        prior=Path(prior_school).resolve(strict=True)
    audited=verify_memory_bundle(prior)
    folder=out/"instrument_art"
    folder.mkdir()
    ledger=CandidateExperienceLedgerV0(out/"instrument_ledger.jsonl")
    all_lessons=_training_specs(prior)
    episodes=[]
    module_identity={"module_path":"brody_world_physique/instrument_school_v2.py",
                     "module_sha256":source_hash(MODULE),
                     "renderer":"render_instrument",
                     "selector":"select_tool",
                     "preexisting_drawing_code":code_fingerprint("image-thinning"),
                     "pillow_version":PIL.__version__}
    training=[]
    for item in all_lessons[:training_lessons]:
        ident=item["id"]
        sketch=_emit_image(item["image"],folder,ident+"_sketch")
        # This teacher image is NOT made available to learner selection.
        target=_teacher_targets(item)
        target_meta=_emit_image(target,folder,ident+"_teacher_target")
        trials={}
        for tool in TOOLS:
            artwork=render_instrument(item["gestures"],tool)
            trials[tool]=_gray_pixel_loss(artwork,target)
            artifact=_emit_image(artwork,folder,ident+"_"+tool.lower())
            if artifact["sha256"]!=source_hash(folder/artifact["ref"]):
                raise ValueError("unverifiable practice drawing")
        entry={"id":ident,"goal":item["goal"],"sketch_sha256":sketch["sha256"],
               "teacher_target_sha256":target_meta["sha256"],
               "trial_losses":trials,"all_three_tools_tried":True,
               "teacher_feedback_visible_during_train":True}
        training.append(entry)
        _record_candidate(ledger,{"event":"INSTRUMENT_PRACTICE",
            "episode_id":ident,"intent":item["goal"],"context_sketch_sha256":sketch["sha256"],
            "tool_comparisons":trials,"code_sha256":module_identity["module_sha256"],
            "outcome":"LOCAL_EPISODIC_CANDIDATE"})
    frozen=tuple(training)
    memories=out/"instrument_skill_memory.json"
    memories.write_text(json.dumps({
        "schema":"BRODY_INSTRUMENT_EPISODIC_CANDIDATES_V2",
        "episodes":training,"candidate_only":True,
        "native_memory_write_allowed":False,
        "no_auto_promotion":True,"code_identity":module_identity,
        "prior_v1_episode_count":audited["episodes"],
    },indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    memory_sha=source_hash(memories)
    forecasts=out/"choices_before_heldout.jsonl"
    results=[]
    with forecasts.open("x",encoding="utf-8") as receipt:
        for item in _exam_specs():
            ident=item["id"]
            sketch_meta=_emit_image(item["image"],folder,ident+"_sketch")
            # FROZEN experiences only, never previous exam successes.
            decision=select_tool(frozen,item["goal"])
            precommit={
                "schema":SCHEMA,"episode_id":ident,"goal":item["goal"],
                "source_kind":SOURCE_KIND,"sketch_sha256":sketch_meta["sha256"],
                "instrument_memory_sha256":memory_sha,
                "procedure_code_sha256":module_identity["module_sha256"],
                "decision":decision,
                "target_accessed_before_decision":False,
                "author":"DETERMINISTIC_EMPIRICAL_POLICY",
                "native_memory_write_allowed":False}
            receipt.write(json.dumps(precommit,sort_keys=True)+"\n")
            receipt.flush()
            # Teacher target must be obtained ONLY AFTER flush above.
            target=_teacher_targets(item)
            target_meta=_emit_image(target,folder,ident+"_heldout_target")
            blank=Image.new("L",(SIDE,SIDE),255)
            trial={}
            for tool in TOOLS:
                drawing=render_instrument(item["gestures"],tool)
                trial[tool]=_gray_pixel_loss(drawing,target)
                _emit_image(drawing,folder,ident+"_tool_"+tool.lower())
            candidate=decision["chosen_tool"]
            if candidate:
                image=render_instrument(item["gestures"],candidate)
                output_meta=_emit_image(image,folder,ident+"_prediction")
                err=_gray_pixel_loss(image,target)
            else:
                output_meta=None
                err=None
            baseline_loss=_gray_pixel_loss(blank,target)
            r={"id":ident,"goal":item["goal"],"decision":decision,
               "heldout_target_sha256":target_meta["sha256"],
               "prediction_artifact":output_meta,
               "chosen_error_px_mean":err,"blank_error_px_mean":baseline_loss,
               "available_tool_errors_after_holdout":trial,
               "winner_after_holdout":min(TOOLS,key=lambda tool:(trial[tool],TOOLS.index(tool))),
               "decision_sealed_before_target_rendered":True,
               "memory_mutations_from_test":0,"world_knowledge_validated":False}
            results.append(r)
            _record_candidate(ledger,{"event":"SEALED_TEST_DECISION_EVALUATED",
                "episode_id":ident,"intent":item["goal"],"status":decision["status"],
                "chosen_tool":candidate,"heldout_result_px_mean":err,
                "read_only_test_feedback":True,"do_not_learn_during_test":True})
    index=out/"instrument_experience_index.json"
    index.write_text(json.dumps({
        "schema":SCHEMA,"source_kind":SOURCE_KIND,"training_lessons":len(training),
        "test_exams":len(results),"trained_experience_count":len(frozen),
        "memory_ref":memories.name,"memory_sha256":memory_sha,
        "procedure":module_identity,
        "precommitted_choice_ref":forecasts.name,
        "precommitted_choice_sha256":source_hash(forecasts),
        "prior_school_replay_verified":True,
        "prior_school_source":str(prior),
        "ledger_ref":ledger.filename.name,"ledger_sha256":source_hash(ledger.filename),
        "native_memory_write_allowed":False,"auto_promotion_allowed":False,
        "decision_authority":"KX108_ONLY",
    },indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    scores=out/"evaluation.json"
    report={
        "schema":SCHEMA,"instrument_choices":"EXPERIENCE_ASSOCIATION_BY_GOAL",
        "train":training,"exams":results,"hold_count":sum(x["decision"]["chosen_tool"] is None for x in results),
        "chosen_count":sum(x["decision"]["chosen_tool"] is not None for x in results),
        "training_lessons":len(training),
        "prior_v1_verified_episodes":audited["episodes"],
        "ledger_integrity":verify_candidate_ledger(ledger.filename),
        "instrument_artificial_models":True,
        "teacher_targets_from_same_renderer":True,
        "semantic_tool_comprehension_proven":False,
        "new_model_weights_trained":False,
        "real_world_generalization_proven":False,
        "native_memory_write_allowed":False,
        "memory_promotion_allowed":False,
        "decision_authority":"KX108_ONLY",
    }
    scores.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    verified=verify_school(out)
    return {
        "evaluation":str(scores),"train":len(training),"exams":len(results),
        "chosen":report["chosen_count"],"hold":report["hold_count"],
        "sealed_decisions_replayed":verified["decisions_verified"],
        "choices":[{"id":r["id"],"goal":r["goal"],
                    "choice":r["decision"]["chosen_tool"],
                    "error":r["chosen_error_px_mean"],
                    "winner_after_holdout":r["winner_after_holdout"]} for r in results],
        "native_memory_write_allowed":False,
    }


def verify_school(root:str|Path)->dict:
    root=Path(root).resolve(strict=True)
    meta=json.loads((root/"instrument_experience_index.json").read_text(encoding="utf-8"))
    if meta.get("schema")!=SCHEMA or meta.get("native_memory_write_allowed") is not False or meta.get("auto_promotion_allowed") is not False or meta.get("decision_authority")!="KX108_ONLY":
        raise ValueError("memory authority violated")
    if meta.get("procedure")!={
        "module_path":"brody_world_physique/instrument_school_v2.py",
        "module_sha256":source_hash(MODULE),
        "renderer":"render_instrument","selector":"select_tool",
        "preexisting_drawing_code":code_fingerprint("image-thinning"),
        "pillow_version":PIL.__version__}:
        raise ValueError("code/source version changed; replay prohibited")
    memory=root/"instrument_skill_memory.json"
    forecast=root/"choices_before_heldout.jsonl"
    ledger=root/"instrument_ledger.jsonl"
    if (meta.get("memory_ref")!=memory.name or meta.get("memory_sha256")!=source_hash(memory)
        or meta.get("precommitted_choice_ref")!=forecast.name or meta.get("precommitted_choice_sha256")!=source_hash(forecast)
        or meta.get("ledger_ref")!=ledger.name or meta.get("ledger_sha256")!=source_hash(ledger)):
        raise ValueError("sealed instrument evidence modified")
    candidate=json.loads(memory.read_text(encoding="utf-8"))
    if candidate.get("schema")!="BRODY_INSTRUMENT_EPISODIC_CANDIDATES_V2" or candidate.get("native_memory_write_allowed") is not False or candidate.get("no_auto_promotion") is not True:
        raise ValueError("memory promotion boundary missing")
    # Bind instrument experiences to the exact, independently replayed prior
    # drawing lessons: reject a changed training source instead of trusting
    # the self-reported source hash in the V2 report.
    prior=Path(meta["prior_school_source"]).resolve(strict=True)
    prior_proof=verify_memory_bundle(prior)
    if meta.get("prior_school_replay_verified") is not True or (
        candidate.get("prior_v1_episode_count")!=prior_proof["episodes"]
        or candidate.get("code_identity")!=meta["procedure"]
    ):
        raise ValueError("prior lesson source/code chain unverified")
    original_training=_training_specs(prior)
    verify_candidate_ledger(ledger)
    report=json.loads((root/"evaluation.json").read_text(encoding="utf-8"))
    if report.get("schema")!=SCHEMA or report.get("native_memory_write_allowed") is not False:
        raise ValueError("evaluation provenance invalid")
    training=tuple(candidate["episodes"])
    if len(training)!=meta["training_lessons"] or len(training)>MAX_LESSONS:
        raise ValueError("training count mismatch")
    rows=[json.loads(x) for x in forecast.read_text(encoding="utf-8").splitlines()]
    if len(rows)!=meta["test_exams"] or len(rows)!=len(report["exams"]):
        raise ValueError("test count mismatch")
    images=root/"instrument_art"
    if any(s["id"]!=f"training_{i+1:02d}" for i,s in enumerate(training)):
        raise ValueError("training order corruption")
    for i,entry in enumerate(training):
        source=original_training[i]
        goal=entry["goal"]
        if (entry["id"]!=source["id"] or goal!=source["goal"]
            or goal not in TRAIN_GOALS or set(entry["trial_losses"])!=set(TOOLS)
            or entry.get("all_three_tools_tried") is not True):
            raise ValueError("training feedback corrupted")
        teacher_path=images/(entry["id"]+"_teacher_target.png")
        sketch_path=images/(entry["id"]+"_sketch.png")
        if entry["teacher_target_sha256"]!=source_hash(teacher_path):
            raise ValueError("training target altered")
        if entry["sketch_sha256"]!=source_hash(sketch_path):
            raise ValueError("training sketch altered")
        if (Image.open(sketch_path).convert("L").tobytes()
            !=source["image"].convert("L").tobytes()):
            raise ValueError("training source does not match the prior V1 lesson")
        actual=Image.open(teacher_path).convert("L")
        if actual.tobytes()!=_teacher_targets(source).tobytes():
            raise ValueError("training teacher target not reproduced from frozen lesson")
        for tool in TOOLS:
            path=images/(entry["id"]+"_"+tool.lower()+".png")
            art=Image.open(path).convert("L")
            if art.tobytes()!=render_instrument(source["gestures"],tool).tobytes():
                raise ValueError("stored instrument trial cannot be replayed")
            if abs(_gray_pixel_loss(art,actual)-entry["trial_losses"][tool])>1e-10:
                raise ValueError("training loss does not match archived tool trial")
    frozen=tuple(training)
    original_exams=_exam_specs()
    for ix,(receipt,r) in enumerate(zip(rows,report["exams"])):
        true_scene=original_exams[ix]
        if (receipt.get("episode_id")!=f"exam_{ix+1:02d}" or r["id"]!=receipt["episode_id"]
            or receipt.get("schema")!=SCHEMA or receipt.get("target_accessed_before_decision") is not False
            or receipt.get("instrument_memory_sha256")!=meta["memory_sha256"]
            or receipt.get("procedure_code_sha256")!=meta["procedure"]["module_sha256"]
            or receipt.get("native_memory_write_allowed") is not False
            or receipt.get("sketch_sha256")!=source_hash(images/(r["id"]+"_sketch.png"))):
            raise ValueError("invalid precommitted receipt")
        if receipt["goal"]!=true_scene["goal"]:
            raise ValueError("test goal changed after source preparation")
        sketch=Image.open(images/(r["id"]+"_sketch.png")).convert("L")
        if sketch.tobytes()!=true_scene["image"].convert("L").tobytes():
            raise ValueError("heldout test source cannot be reproduced")
        decision=select_tool(frozen,receipt["goal"])
        if receipt["decision"]!=decision or r["decision"]!=decision or receipt["goal"]!=r["goal"]:
            raise ValueError("stored decision is not reproducible from frozen memory")
        target_path=images/(r["id"]+"_heldout_target.png")
        if source_hash(target_path)!=r["heldout_target_sha256"]:
            raise ValueError("heldout artifact was modified")
        target=Image.open(target_path).convert("L")
        if target.tobytes()!=_teacher_targets(true_scene).tobytes():
            raise ValueError("heldout target cannot be reproduced from fixture")
        test_art={}
        for tool in TOOLS:
            path=images/(r["id"]+"_tool_"+tool.lower()+".png")
            if not path.is_file():raise ValueError("tool trial missing")
            tool_art=Image.open(path).convert("L")
            if tool_art.tobytes()!=render_instrument(true_scene["gestures"],tool).tobytes():
                raise ValueError("heldout tool trial was altered")
            loss=_gray_pixel_loss(tool_art,target)
            if abs(loss-r["available_tool_errors_after_holdout"][tool])>1e-10:
                raise ValueError("heldout feedback modified")
            test_art[tool]=loss
        expected_winner=min(TOOLS,key=lambda tool:(test_art[tool],TOOLS.index(tool)))
        if expected_winner!=r["winner_after_holdout"]:
            raise ValueError("false winning instrument")
        chosen=decision["chosen_tool"]
        if chosen is not None:
            artifact=r["prediction_artifact"]
            p=images/(r["id"]+"_prediction.png")
            if (artifact.get("ref")!=p.name or artifact["sha256"]!=source_hash(p)
                or abs(_gray_pixel_loss(Image.open(p),target)-r["chosen_error_px_mean"])>1e-10
                or Image.open(p).convert("L").tobytes()!=Image.open(images/(r["id"]+"_tool_"+chosen.lower()+".png")).convert("L").tobytes()):
                raise ValueError("prediction does not match chosen real tool")
        elif r["prediction_artifact"] is not None or r["chosen_error_px_mean"] is not None:
            raise ValueError("HOLD cannot forge an output")
    return {
        "status":"PASS_BOUNDED_EPISODIC_TOOL_REPLAY",
        "decisions_verified":len(rows),
        "lessons_verified":len(training),
        "code_identity_verified":True,
        "native_memory_write_allowed":False,
        "model_weights_trained":False,
        "world_knowledge_validated":False,
    }


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(description="Brody instrument class: learn to route simulated pencil, pen and nib")
    p.add_argument("--out",type=Path)
    p.add_argument("--prior-school",type=Path)
    p.add_argument("--training-lessons",type=int,default=MAX_LESSONS)
    p.add_argument("--verify",type=Path)
    a=p.parse_args(argv)
    if a.verify:
        if a.out: p.error("--verify and --out are mutually exclusive")
        result=verify_school(a.verify)
    else:
        if not a.out:p.error("--out is required to teach")
        result=run_school(a.out,prior_school=a.prior_school,training_lessons=a.training_lessons)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
