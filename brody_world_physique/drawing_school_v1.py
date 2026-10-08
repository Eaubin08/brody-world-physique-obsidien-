"""Image-first drawing workshop V1: remove, replace, line and curved gesture.

The pupil sees a pixel reference in every lesson and examination: this is
guided VISUAL COPYING (not unseen-image generation). No shape names, teacher
construction code or physical formulas are input to the tracing mechanism.
A generic thinning / point-path procedure supplies the suggested gestures,
so the motor procedure is ENGINEERED rather than discovered by an AI model.
Episodic errors, negative recall and image outputs are local candidates only.
No Native Memory writes, promotion, model weights, API or kernel mutation.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from math import hypot
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw

from .drawing_school_v0 import (
    SIDE, CandidateExperienceLedgerV0, bbox_of, black_pixels,
    digest_bytes, signature_for, verify_candidate_ledger,
)

Point = tuple[int,int]
Edge = tuple[Point,Point]


@dataclass(frozen=True)
class GestureV1:
    points: tuple[Point,...]
    kind: str  # STRAIGHT_STROKE or CURVED_STROKE, not shape class


@dataclass(frozen=True)
class SkillV1:
    source_sha256: str
    lesson_ref: str
    bbox: tuple[int,int,int,int]
    signature: tuple[int,...]
    gestures: tuple[GestureV1,...]
    last_error_pixels: int
    status: str = "EXPERIENTIAL_SKILL_CANDIDATE_ONLY"


def _neighbors(point:Point, pixels:set[Point])->list[Point]:
    x,y=point
    card=[(x,y-1),(x+1,y),(x,y+1),(x-1,y)]
    diag=[(x+1,y-1),(x+1,y+1),(x-1,y+1),(x-1,y-1)]
    found=[p for p in card if p in pixels]
    for a,b in diag:
        if (a,b) not in pixels:continue
        # Keep 8-neighbor connectivity, but do not create redundant triangles
        # for diagonal touching pixels with an existing orthogonal route.
        if (a,y) in pixels or (x,b) in pixels:
            continue
        found.append((a,b))
    return sorted(found)


def _skeletonize(ink:set[int], *, iterations:int=50)->set[Point]:
    """Zhang-Suen thinning; general raster morphology, not circle templates."""
    pts={(k%SIDE,k//SIDE) for k in ink}
    offsets=((0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1))
    for _ in range(iterations):
        changed=False
        for pass_no in (0,1):
            remove=set()
            for x,y in pts:
                ns=[(x+dx,y+dy) in pts for dx,dy in offsets]
                neighbors=sum(ns)
                if not 2<=neighbors<=6:continue
                transitions=sum(not ns[i] and ns[(i+1)%8] for i in range(8))
                if transitions!=1:continue
                p2,p4,p6,p8=ns[0],ns[2],ns[4],ns[6]
                if pass_no==0:
                    cond=(not(p2 and p4 and p6) and not(p4 and p6 and p8))
                else:
                    cond=(not(p2 and p4 and p8) and not(p2 and p6 and p8))
                if cond:remove.add((x,y))
            if remove:
                pts.difference_update(remove)
                changed=True
        if not changed:break
    return pts


def _edge(a:Point,b:Point)->Edge:
    return tuple(sorted((a,b)))  # type: ignore[return-value]


def _trace_paths(pixels:set[Point])->list[list[Point]]:
    """Split one-pixel traces at junctions, preserving cycles."""
    if not pixels:return []
    adjacency={p:_neighbors(p,pixels) for p in pixels}
    used:set[Edge]=set()
    paths:list[list[Point]]=[]
    starts=sorted(p for p,nbrs in adjacency.items() if len(nbrs)!=2)
    ordered=starts+sorted(p for p in pixels if p not in set(starts))
    for start in ordered:
        for next_pt in adjacency[start]:
            if _edge(start,next_pt) in used:continue
            chain=[start,next_pt];used.add(_edge(start,next_pt))
            prior,current=start,next_pt
            while len(chain) < SIDE*SIDE:
                if len(adjacency[current])!=2 or current==start:
                    break
                unused=[p for p in adjacency[current] if p!=prior and _edge(current,p) not in used]
                if not unused:break
                following=unused[0]
                used.add(_edge(current,following))
                chain.append(following)
                prior,current=current,following
            if len(chain)>=2:paths.append(chain)
    # Single-pixel specks cannot be reliably reconstructed as a stroke.
    return paths


def _point_to_line_distance(p:Point,a:Point,b:Point)->float:
    x0,y0=a;x1,y1=b;x,y=p
    dx,dy=x1-x0,y1-y0
    denom=dx*dx+dy*dy
    if denom==0:return hypot(x-x0,y-y0)
    t=max(0.0,min(1.0,((x-x0)*dx+(y-y0)*dy)/denom))
    return hypot(x-(x0+t*dx),y-(y0+t*dy))


def _simplify(points:list[Point],tolerance:float=.8)->list[Point]:
    if len(points)<3:return points
    if points[0]==points[-1]:
        # Avoid collapsing a closed curve to a point.
        quarter=max(1,(len(points)-1)//4)
        return sum(
            (_simplify(points[i:j+1],tolerance)[:-1]
             for i,j in ((0,quarter),(quarter,2*quarter),
                         (2*quarter,3*quarter),(3*quarter,len(points)-1))),
            [],
        )+[points[0]]
    maximum=-1.
    middle=-1
    for i in range(1,len(points)-1):
        distance=_point_to_line_distance(points[i],points[0],points[-1])
        if distance>maximum:maximum,middle=distance,i
    if maximum<=tolerance:return [points[0],points[-1]]
    left=_simplify(points[:middle+1],tolerance)
    right=_simplify(points[middle:],tolerance)
    return left[:-1]+right


def suggest_gestures_from_reference(reference:Image.Image)->tuple[GestureV1,...]:
    """Generic bitmap->thin path->stroke motor proposals, no lesson labels."""
    original=black_pixels(reference)
    skeleton=_skeletonize(original)
    paths=_trace_paths(skeleton)
    gestures=[]
    for path in paths:
        simplified=_simplify(path)
        if len(simplified)<2:continue
        kind="CURVED_STROKE" if len(simplified)>2 else "STRAIGHT_STROKE"
        gestures.append(GestureV1(points=tuple(simplified),kind=kind))
    return tuple(gestures[:128])


def raster_stroke(gesture:GestureV1)->set[int]:
    canvas=Image.new("L",(SIDE,SIDE),255)
    ImageDraw.Draw(canvas).line(gesture.points,fill=0,width=3,joint="curve")
    return black_pixels(canvas)


def render(gestures:Iterable[GestureV1])->Image.Image:
    image=Image.new("L",(SIDE,SIDE),255)
    pen=ImageDraw.Draw(image)
    for gesture in gestures:
        pen.line(gesture.points,fill=0,width=3,joint="curve")
    return image


def _error(reference:set[int],gestures:Iterable[GestureV1])->int:
    return len(reference.symmetric_difference(black_pixels(render(gestures))))


def _scaled(value:int,amin:int,amax:int,bmin:int,bmax:int)->int:
    return max(0,min(SIDE-1,round(bmin+((value-amin)/max(1,amax-amin))*(bmax-bmin))))


def recall(memory:tuple[SkillV1,...],reference:set[int])->tuple[GestureV1,...]:
    if not memory:return ()
    bounds=bbox_of(reference)
    feature=signature_for(reference,bounds)
    skill=min(memory,key=lambda item:sum(x!=y for x,y in zip(feature,item.signature)))
    a,b,c,d=skill.bbox
    e,f,g,h=bounds
    return tuple(GestureV1(
        points=tuple((_scaled(x,a,c,e,g),_scaled(y,b,d,f,h))
                     for x,y in stroke.points),
        kind=stroke.kind,
    ) for stroke in skill.gestures)


def correct_drawing(reference:Image.Image, initial:tuple[GestureV1,...]=(),
                    *, max_revisions:int=24) -> dict:
    """Local motor correction: add / ERASE / REPLACE stored strokes.

    Uses visual reference pixels to score each edit. A bad memory replay
    remains an explicit recorded failure, never silently accepted as truth.
    """
    if not 0<=max_revisions<=64:raise ValueError("bounded revision budget")
    truth=black_pixels(reference)
    raw_error=_error(truth,initial)
    blank_error=len(truth)
    rejected=bool(initial and raw_error>blank_error)
    gestures=list(() if rejected else initial)
    error=_error(truth,gestures)
    proposals=suggest_gestures_from_reference(reference)
    changes=[]
    rejected_proposals=0
    for iteration in range(max_revisions):
        best=(error,None,None)
        # Always preserve source and label of the proposal. No teacher class
        # name, formula or generator parameter enters the trace extractor.
        alternatives_evaluated=0
        for i,candidate in enumerate(proposals):
            if candidate in gestures:continue
            candidate_set=gestures+[candidate]
            score=_error(truth,candidate_set)
            alternatives_evaluated+=1
            if score<best[0]:best=(score,"ADD",i)
        for existing in range(len(gestures)):
            score=_error(truth,gestures[:existing]+gestures[existing+1:])
            alternatives_evaluated+=1
            if score<best[0]:best=(score,"ERASE",existing)
            for i,candidate in enumerate(proposals):
                if candidate==gestures[existing]:continue
                trial=gestures[:existing]+[candidate]+gestures[existing+1:]
                score=_error(truth,trial)
                alternatives_evaluated+=1
                if score<best[0]:best=(score,"REPLACE",(existing,i))
        score,operation,idx=best
        rejected_proposals+=alternatives_evaluated-int(operation is not None)
        if operation is None:break
        previous=error
        before_gesture=None
        applied_gesture=None
        if operation=="ADD":
            applied_gesture=proposals[idx]
            gestures.append(applied_gesture)
        elif operation=="ERASE":
            before_gesture=gestures.pop(idx)
        else:
            old,new=idx
            before_gesture=gestures[old]
            applied_gesture=proposals[new]
            gestures[old]=applied_gesture
        error=score
        changes.append({"revision":iteration+1,"action":operation,
                        "target_index":len(gestures)-1 if operation=="ADD" else
                                       idx if operation=="ERASE" else idx[0],
                        "gesture_before":asdict(before_gesture) if before_gesture else None,
                        "gesture_applied":asdict(applied_gesture) if applied_gesture else None,
                        "alternatives_evaluated":alternatives_evaluated,
                        "choice_rule":"MIN_PIXEL_XOR_STRICT_IMPROVEMENT_FIRST_TIE",
                        "error_before":previous,"error_after":score,
                        "strict_improvement":score<previous})
        if score==0:break
    return {"raw_recall_error":raw_error if initial else None,
            "memory_rejected":rejected,
            "initial_gestures":[asdict(g) for g in initial],
            "rejected_alternative_evaluations":rejected_proposals,
            "proposed_gesture_count":len(proposals),
            "algorithm_choice_reason":"PIXEL_ERROR_MINIMIZATION_GIVEN_VISIBLE_REFERENCE",
            "blank_error":blank_error,
            "error_after_recall_gate":blank_error if rejected else raw_error,
            "final_error":error,"changes":changes,
            "gestures":tuple(gestures),
            "image":render(gestures),
            "contains_curved_strokes":any(g.kind=="CURVED_STROKE" for g in gestures),
            "source_known_in_feedback":True}


def teacher_lessons()->list[tuple[str,Image.Image]]:
    """Only drawing references; geometric labels stay outside student calls."""
    def picture(lines:list[tuple[Point,...]], *, ellipse=None):
        img=Image.new("L",(SIDE,SIDE),255)
        draw=ImageDraw.Draw(img)
        for pts in lines:draw.line(pts,fill=0,width=3,joint="curve")
        if ellipse:draw.ellipse(ellipse,outline=0,width=3)
        return img
    return [
        ("cours_trait",picture([((8,16),(48,16))])),
        ("cours_carre",picture([((12,12),(44,12),(44,44),(12,44),(12,12))])),
        ("cours_triangle",picture([((12,48),(32,8),(52,48),(12,48))])),
        ("cours_cercle",picture([],ellipse=(10,10,52,52))),
    ]


def teacher_exams()->list[tuple[str,Image.Image]]:
    def picture(lines:list[tuple[Point,...]], *, ellipse=None):
        img=Image.new("L",(SIDE,SIDE),255);d=ImageDraw.Draw(img)
        for pts in lines:d.line(pts,fill=0,width=3,joint="curve")
        if ellipse:d.ellipse(ellipse,outline=0,width=3)
        return img
    return [
        ("examen_trait",picture([((10,45),(53,45))])),
        ("examen_carre",picture([((18,15),(50,15),(50,47),(18,47),(18,15))])),
        ("examen_triangle",picture([((8,51),(29,10),(53,51),(8,51))])),
        ("examen_cercle",picture([],ellipse=(15,12,48,45))),
        ("examen_croix",picture([((10,10),(52,52)),((10,52),(52,10))])),
        ("examen_courbe",picture([((5,35),(13,29),(24,18),(35,25),(46,36),(57,22))])),
    ]


def _open_fresh(destination:str|Path)->Path:
    root=Path(destination).resolve()
    if root.exists() and any(root.iterdir()):
        raise ValueError("new output directory required")
    root.mkdir(parents=True,exist_ok=True)
    return root


def run_school(out:str|Path)->dict:
    root=_open_fresh(out)
    teacher_dir=root/"teacher_images"
    attempts=root/"attempts"
    teacher_dir.mkdir();attempts.mkdir()
    ledger=CandidateExperienceLedgerV0(root/"candidate_experience_ledger.jsonl")
    skills=[]
    training=[]
    for name,source in teacher_lessons():
        original=teacher_dir/(name+".png")
        source.save(original)
        digest=digest_bytes(original.read_bytes())
        trial=correct_drawing(source)
        trial["image"].save(attempts/(name+"_dessin.png"))
        ledger.append({"event":"TEACHER_SOURCE_REFERENCE",
                       "source_ref":name,"source_sha256":digest,
                       "source_kind":"SIMULATED","memory_write_allowed":False})
        for item in trial["changes"]:
            ledger.append({"event":"MOTOR_CORRECTION_EXPERIENCE",
                           "source_ref":name,"source_sha256":digest,
                           "edit":item,"memory_write_allowed":False})
        ink=black_pixels(source)
        candidate=SkillV1(digest,name,bbox_of(ink),
                          signature_for(ink,bbox_of(ink)),
                          trial["gestures"],trial["final_error"])
        skills.append(candidate)
        ledger.append({"event":"CANDIDATE_MOTOR_SKILL",
                       "source_ref":name,"source_sha256":digest,
                       "final_error":trial["final_error"],
                       "canonically_validated":False,
                       "memory_write_allowed":False})
        training.append({"lesson":name,"blank_error":trial["blank_error"],
                         "final_error":trial["final_error"],
                         "edit_actions":[s["action"] for s in trial["changes"]],
                         "curved_gesture_candidate":trial["contains_curved_strokes"]})
    frozen=tuple(skills)
    memory_file=root/"candidate_skill_memory.json"
    memory_file.write_text(json.dumps({
        "schema":"BRODY_DRAWING_SCHOOL_SKILL_MEMORY_V1",
        "source_kind":"SIMULATED","native_memory_write_allowed":False,
        "canonical_memory":False,"skills":[asdict(s) for s in frozen],
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    results=[]
    for name,source in teacher_exams():
        original=teacher_dir/(name+".png")
        source.save(original)
        digest=digest_bytes(original.read_bytes())
        ink=black_pixels(source)
        proposed=recall(frozen,ink)
        raw=render(proposed)
        raw.save(attempts/(name+"_souvenir_brut.png"))
        transferred=correct_drawing(source,proposed,max_revisions=0)
        transferred["image"].save(attempts/(name+"_memoire_filtrée.png"))
        repaired=correct_drawing(source,proposed)
        repaired["image"].save(attempts/(name+"_apres_correction.png"))
        ledger.append({"event":"UNSEEN_EXAM_WITH_REFERENCE_VISIBLE",
                       "source_ref":name,"source_sha256":digest,
                       "blank_error":repaired["blank_error"],
                       "raw_recall_error":repaired["raw_recall_error"],
                       "memory_rejected":repaired["memory_rejected"],
                       "final_error":repaired["final_error"],
                       "memory_write_allowed":False})
        if repaired["memory_rejected"]:
            ledger.append({"event":"NEGATIVE_TRANSFER_SKILL_CANDIDATE",
                           "source_ref":name,"source_sha256":digest,
                           "raw_recall_error":repaired["raw_recall_error"],
                           "failure": "MEMORY_WORSE_THAN_BLANK",
                           "recovery":"RESTART_WITHOUT_BAD_GESTURES",
                           "memory_write_allowed":False})
        for edit in repaired["changes"]:
            ledger.append({"event":"EXAM_CORRECTION_CANDIDATE",
                           "source_ref":name,"edit":edit,
                           "memory_write_allowed":False})
        results.append({"exercise_ref":name,
                        "blank_error_pixels":repaired["blank_error"],
                        "raw_memory_error_pixels":repaired["raw_recall_error"],
                        "memory_rejected":repaired["memory_rejected"],
                        "initial_after_memory_gate":repaired["error_after_recall_gate"],
                        "after_correction_error_pixels":repaired["final_error"],
                        "correction_actions":[c["action"] for c in repaired["changes"]],
                        "curved_gestures":repaired["contains_curved_strokes"],
                        "seen_by_learner_at_exam":True})
    verification=verify_candidate_ledger(ledger.filename)
    report={
        "schema":"BRODY_DRAWING_STUDENT_V1",
        "kind":"SUPERVISED_DRAWING_FROM_VISIBLE_SOURCE",
        "curriculum": ["TRAITS","CONTOURS","TRIANGLES","CERCLES","RECOUVREMENT","COURBES"],
        "train_lessons":training,"unseen_exams":results,
        "candidate_skills":len(skills),
        "candidate_memory_file":str(memory_file),
        "ledger_integrity":verification,
        "truth_evaluator":"KNOWN_REFERENCE_PIXEL_ERROR",
        "semantic_object_understanding":False,
        "autonomous_image_generation":False,
        "trained_vision_model":False,
        "native_memory_write_allowed":False,
        "memory_promotion_allowed":False,
        "kernel_mutation":False,"decision_authority":"KX108_ONLY",
        "limitations":[
            "The reference image is visible during training and tests",
            "Generic morphology, gesture catalog and edit search are coded by humans",
            "Drawing score is binary pixel agreement, not composition or artistic quality",
            "Candidate memory reuses raster-derived gestures, not object meaning",
            "Local chained JSONL is not Native Memory or an authenticated Merkle seal",
        ],
    }
    (root/"evaluation.json").write_text(json.dumps(
        report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {"evaluation":str(root/"evaluation.json"),
            "train":len(training),"exams":len(results),
            "results":[{k:r[k] for k in ("exercise_ref","blank_error_pixels",
                      "initial_after_memory_gate","after_correction_error_pixels",
                      "memory_rejected")} for r in results],
            "ledger_events":verification["verified_records"],
            "native_memory_write_allowed":False}


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Draw from reference, erase bad strokes, acquire curved motor gestures and replay experiences")
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args(argv)
    print(json.dumps(run_school(args.out),indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
