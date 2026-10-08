"""Image-first drawing school: guided motor copying + local candidate memory.

Source intentions: FSO user-authored school, reciprocal image synthesis,
layer order, source preservation; see docs/34. Engineering implementation
below is a bounded, teacher-guided *candidate*, NOT a learned generative AI:
- Pillow supplies the low-level pen/canvas and score.
- Student does not receive the names/shape templates used by the teacher.
- Student greedily improves by comparing raster pixels; this is supervised
  visual feedback, NOT learning from zero input or discovering drawing itself.
- Learned stroke sequences are source-tagged LOCAL candidates, re-used when
  a new visible drawing has a similar normalized raster signature.
- Native Memory never receives writes; all attempts remain auditable.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw

SIDE=64
BRUSH_WIDTH=3
MAX_CANDIDATES=12000
MAX_STROKES=14
Stroke=tuple[int,int,int,int]


def _canonical(value: object)->bytes:
    return json.dumps(value,sort_keys=True,ensure_ascii=False,
                      separators=(",",":")).encode("utf-8")


def digest_bytes(data:bytes)->str:
    return sha256(data).hexdigest()


@dataclass(frozen=True)
class DrawingSkillCandidateV0:
    source_sha256:str
    lesson_ref:str
    source_bbox:tuple[int,int,int,int]
    signature:tuple[int,...]
    strokes:tuple[Stroke,...]
    final_pixel_error:int
    status:str="EPISODIC_SKILL_CANDIDATE_NOT_CANONICAL"


class CandidateExperienceLedgerV0:
    """JSONL append-only hash chain in one isolated experiment output dir.

    This tamper-detection check does NOT provide authenticated signatures or
    Obsidia's historical Merkle Root. Root ownership remains external.
    """
    def __init__(self,filename:Path):
        self.filename=filename
        if filename.exists():
            raise ValueError("candidate ledger must be new; never overwrite prior episodes")
        self.last_hash="0"*64
        self.count=0

    def append(self,event:dict)->str:
        if not isinstance(event,dict) or not event.get("event"):
            raise ValueError("event type required")
        if event.get("memory_write_allowed") is not False:
            raise ValueError("canonical memory mutation is forbidden")
        item={"seq":self.count,"prev_sha256":self.last_hash,"event":event}
        h=digest_bytes(_canonical(item))
        self.filename.parent.mkdir(parents=True,exist_ok=True)
        with self.filename.open("a",encoding="utf-8") as handle:
            handle.write(json.dumps(item|{"record_sha256":h},
                                    ensure_ascii=False,sort_keys=True)+"\n")
        self.last_hash=h
        self.count+=1
        return h


def verify_candidate_ledger(filename:Path)->dict:
    prev="0"*64
    n=0
    for line in filename.read_text(encoding="utf-8").splitlines():
        obj=json.loads(line)
        signature=obj.pop("record_sha256")
        if obj["seq"]!=n or obj["prev_sha256"]!=prev or digest_bytes(_canonical(obj))!=signature:
            raise ValueError("candidate experience chain integrity failure")
        if obj["event"].get("memory_write_allowed") is not False:
            raise ValueError("external mutation permissions found in candidate")
        prev=signature
        n+=1
    return {"verified_records":n,"last_sha256":prev,
            "native_memory_verified":False,"canonical_memory_written":False}


def black_pixels(image:Image.Image)->set[int]:
    if image.size!=(SIDE,SIDE):
        raise ValueError("only 64x64 lessons allowed in V0")
    return {i for i,p in enumerate(image.convert("L").getdata()) if p<128}


def bbox_of(points:set[int])->tuple[int,int,int,int]:
    if not points:raise ValueError("no visible drawing in the teacher source")
    xs=[p%SIDE for p in points]
    ys=[p//SIDE for p in points]
    return min(xs),min(ys),max(xs),max(ys)


def signature_for(points:set[int],bbox:tuple[int,int,int,int])->tuple[int,...]:
    """No semantic label; 8x8 coarse normalized ink occupancy."""
    x0,y0,x1,y1=bbox
    w=max(1,x1-x0)
    h=max(1,y1-y0)
    counts=[0]*64
    for p in points:
        x,y=p%SIDE,p//SIDE
        col=min(7,max(0,int((x-x0)/w*7)))
        row=min(7,max(0,int((y-y0)/h*7)))
        counts[row*8+col]+=1
    threshold=max(1,len(points)//200)
    return tuple(int(v>=threshold) for v in counts)


def stroke_ink(stroke:Stroke)->set[int]:
    im=Image.new("L",(SIDE,SIDE),255)
    ImageDraw.Draw(im).line(stroke,fill=0,width=BRUSH_WIDTH)
    return black_pixels(im)


def _stroke_catalog()->list[tuple[Stroke,set[int]]]:
    """Pencil motor vocabulary, no circle/rectangle/triangle template."""
    directions=((1,0),(0,1),(1,1),(1,-1),(-1,1),(-1,0),
                (0,-1),(-1,-1))
    catalogue=[]
    seen=set()
    for y in range(4,61,4):
        for x in range(4,61,4):
            for length in (8,16,24,32,40):
                for dx,dy in directions:
                    x2,y2=x+length*dx,y+length*dy
                    if not 0<=x2<SIDE or not 0<=y2<SIDE:
                        continue
                    stroke=(x,y,x2,y2)
                    # Segment direction reversed is not another motor skill.
                    key=tuple(sorted(((x,y),(x2,y2))))
                    if key in seen:continue
                    seen.add(key)
                    catalogue.append((stroke,stroke_ink(stroke)))
    if len(catalogue)>MAX_CANDIDATES:
        raise ValueError("stroke catalog too large")
    return catalogue


def draw_strokes(strokes:Iterable[Stroke])->Image.Image:
    image=Image.new("L",(SIDE,SIDE),255)
    pen=ImageDraw.Draw(image)
    for stroke in strokes:
        pen.line(stroke,fill=0,width=BRUSH_WIDTH)
    return image


def _error(target:set[int],ink:set[int])->int:
    return len(target.symmetric_difference(ink))


def _clamp(value:float)->int:
    return max(0,min(SIDE-1,round(value)))


def _transfer_strokes(skill:DrawingSkillCandidateV0,
                      target_bbox:tuple[int,int,int,int])->tuple[Stroke,...]:
    x0,y0,x1,y1=skill.source_bbox
    a,b,c,d=target_bbox
    sx=max(1,x1-x0);sy=max(1,y1-y0)
    tx=max(1,c-a);ty=max(1,d-b)
    result=[]
    for stroke in skill.strokes:
        result.append((_clamp(a+(stroke[0]-x0)/sx*tx),
                       _clamp(b+(stroke[1]-y0)/sy*ty),
                       _clamp(a+(stroke[2]-x0)/sx*tx),
                       _clamp(b+(stroke[3]-y0)/sy*ty)))
    return tuple(result)


def choose_memory_seed(memory:tuple[DrawingSkillCandidateV0,...],
                       target:set[int])->tuple[Stroke,...]:
    """Student sees a NEW reference before deciding which gesture to replay.

    Matching reference features are available, but future corrective feedback
    and heldout pixels were not used to select strokes.
    """
    if not memory:return ()
    wanted=signature_for(target,bbox_of(target))
    skill=min(memory,key=lambda m:sum(a!=b for a,b in zip(m.signature,wanted)))
    return _transfer_strokes(skill,bbox_of(target))


def practice_drawing(image:Image.Image, *,
                     memory:tuple[DrawingSkillCandidateV0,...]=(),
                     max_strokes:int=MAX_STROKES,
                     catalog:list[tuple[Stroke,set[int]]]|None=None)->dict:
    """Visual correction loop with no teacher shape label given to learner."""
    if not 0<=max_strokes<=MAX_STROKES:
        raise ValueError("stroke budget outside bound")
    teacher=black_pixels(image)
    starter=choose_memory_seed(memory,teacher)
    ink=black_pixels(draw_strokes(starter))
    before=_error(teacher,ink)
    original_black=len(teacher)
    steps=[]
    chosen=list(starter)
    catalogue=_stroke_catalog() if catalog is None else catalog
    for iteration in range(max_strokes):
        uncovered=teacher-ink
        if not uncovered:break
        winner=None
        improvement=0
        for proposed,mask in catalogue:
            new=mask-ink
            gain=len(new&uncovered)-len(new-teacher)
            if gain>improvement:
                winner=(proposed,mask)
                improvement=gain
        if winner is None:break
        stroke,pixels=winner
        ink|=pixels
        chosen.append(stroke)
        steps.append({"revision":iteration+1,"stroke":list(stroke),
                      "new_ink_pixels":len(pixels),
                      "error_pixels":_error(teacher,ink),
                      "repaired_by_teacher_feedback":True})
    final_image=draw_strokes(chosen)
    actual=_error(teacher,black_pixels(final_image))
    if actual>before or actual>original_black+len(black_pixels(draw_strokes(starter))):
        raise ValueError("drawing correction unexpectedly worsened")
    return {"initial_error_pixels":before,"blank_error_pixels":original_black,
            "final_error_pixels":actual,"correction_steps":steps,
            "seed_stroke_count":len(starter),"strokes":tuple(chosen),
            "candidate_image":final_image,
            "source_bbox":bbox_of(teacher),
            "source_signature":signature_for(teacher,bbox_of(teacher))}


def _teacher_canvas(parts:list[Stroke])->Image.Image:
    return draw_strokes(parts)


def training_curriculum()->list[tuple[str,Image.Image]]:
    """Teacher-only examples; no class names or geometry given to learner."""
    return [
        ("lesson_01",_teacher_canvas([(8,16,48,16)])),
        ("lesson_02",_teacher_canvas([(12,12,44,12),(44,12,44,44),
                                      (44,44,12,44),(12,44,12,12)])),
        ("lesson_03",_teacher_canvas([(12,48,32,8),(32,8,52,48),
                                      (52,48,12,48)])),
    ]


def test_curriculum()->list[tuple[str,Image.Image]]:
    return [
        ("exam_01",_teacher_canvas([(12,40,52,40)])),
        ("exam_02",_teacher_canvas([(16,16,48,16),(48,16,48,48),
                                    (48,48,16,48),(16,48,16,16)])),
        ("exam_03",_teacher_canvas([(8,52,28,12),(28,12,48,52),
                                    (48,52,8,52)])),
        # A new pair of crossing strokes; no exact training shape.
        ("exam_04",_teacher_canvas([(12,12,52,52),(12,52,52,12)])),
    ]


def run_school(out_dir:str|Path)->dict:
    output=Path(out_dir).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("new output folder required")
    output.mkdir(parents=True,exist_ok=True)
    originals=output/"teacher_images"
    results=output/"attempts"
    originals.mkdir();results.mkdir()
    ledger=CandidateExperienceLedgerV0(output/"candidate_experience_ledger.jsonl")
    catalog=_stroke_catalog()
    learned:list[DrawingSkillCandidateV0]=[]
    train_reports=[]
    for lesson,teacher in training_curriculum():
        ref=originals/(lesson+".png")
        teacher.save(ref)
        digest=digest_bytes(ref.read_bytes())
        initial=practice_drawing(teacher,catalog=catalog)
        image_out=results/(lesson+"_first_drawing.png")
        initial["candidate_image"].save(image_out)
        ledger.append({"event":"LESSON_OBSERVATION",
                       "lesson_ref":lesson,"source_sha256":digest,
                       "source_kind":"SIMULATED",
                       "intent":"DRAW_AS_CLOSE_TO_TEACHER_SOURCE_AS_POSSIBLE",
                       "memory_write_allowed":False})
        for attempt in initial["correction_steps"]:
            ledger.append({"event":"DRAWING_ATTEMPT_CORRECTED",
                           "lesson_ref":lesson,"source_sha256":digest,
                           "revision":attempt["revision"],
                           "error_pixels":attempt["error_pixels"],
                           "stroke":attempt["stroke"],
                           "memory_write_allowed":False})
        candidate=DrawingSkillCandidateV0(
            source_sha256=digest,lesson_ref=lesson,
            source_bbox=initial["source_bbox"],
            signature=initial["source_signature"],
            strokes=initial["strokes"],
            final_pixel_error=initial["final_error_pixels"],
        )
        learned.append(candidate)
        ledger.append({"event":"SKILL_CANDIDATE_LOCAL_ONLY",
                       "lesson_ref":lesson,"source_sha256":digest,
                       "classification":"PROPOSE_FOR_FUTURE_TRANSFER_REVIEW",
                       "final_pixel_error":initial["final_error_pixels"],
                       "memory_write_allowed":False})
        train_reports.append({"lesson_ref":lesson,"source_sha256":digest,
                              "first_error_pixels":initial["blank_error_pixels"],
                              "last_error_pixels":initial["final_error_pixels"],
                              "revisions":len(initial["correction_steps"])})
    frozen=tuple(learned)
    (output/"candidate_skill_memory.json").write_text(
        json.dumps({"schema":"BRODY_DRAWING_SKILL_CANDIDATES_V0",
                    "source_kind":"SIMULATED","canonical_memory":False,
                    "native_memory_write_allowed":False,
                    "skills":[asdict(x) for x in frozen]},
                   ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    exams=[]
    for name,reference in test_curriculum():
        target_path=originals/(name+".png")
        reference.save(target_path)
        digest=digest_bytes(target_path.read_bytes())
        cold=practice_drawing(reference,max_strokes=0,catalog=catalog)
        seed=practice_drawing(reference,memory=frozen,max_strokes=0,catalog=catalog)
        repaired=practice_drawing(reference,memory=frozen,max_strokes=8,catalog=catalog)
        seed["candidate_image"].save(results/(name+"_from_memory.png"))
        repaired["candidate_image"].save(results/(name+"_after_feedback.png"))
        ledger.append({"event":"UNSEEN_EXERCISE_MEMORY_REPLAY",
                       "lesson_ref":name,"source_sha256":digest,
                       "reference_was_visible_before_seed":True,
                       "baseline_blank_error_pixels":cold["final_error_pixels"],
                       "initial_replay_error_pixels":seed["final_error_pixels"],
                       "error_after_feedback_pixels":repaired["final_error_pixels"],
                       "proven_skill_transfer":False,
                       "memory_write_allowed":False})
        exams.append({
            "exercise_ref":name,"source_sha256":digest,
            "cold_blank_error_pixels":cold["final_error_pixels"],
            "candidate_replay_error_pixels":seed["final_error_pixels"],
            "after_feedback_error_pixels":repaired["final_error_pixels"],
            "improved_initially_over_blank":seed["final_error_pixels"] < cold["final_error_pixels"],
            "feedback_revision_count":len(repaired["correction_steps"]),
            "heldout_exercise_prior_to_candidate_memory":True,
        })
    integrity=verify_candidate_ledger(ledger.filename)
    report={"schema":"BRODY_DRAWING_SCHOOL_V0",
            "mode":"GUIDED_VISUAL_COPYING_AND_PENCIL_CORRECTION",
            "learning_source":"LOCAL_SIMULATED_TEACHER_DRAWING",
            "course_sections":["TRAIT","CONTOUR_SIMPLE","ASSEMBLAGE_2D"],
            "labels_accessible_to_learner":False,
            "train_lessons":train_reports,"exams":exams,
            "candidate_skill_count":len(learned),
            "ledger_integrity":integrity,
            "candidate_memory_path":str(output/"candidate_skill_memory.json"),
            "model_weights_trained":False,
            "universal_object_perception":False,
            "physical_understanding_proven":False,
            "novel_view_understanding_proven":False,
            "validated_canonical_skill":False,
            "native_memory_write_allowed":False,
            "decision_authority":"KX108_ONLY",
            "limitations":[
                "Pillow pen motor tools and pixel feedback are provided",
                "Learner sees source pixels; not learning without observations",
                "Training from explicit pixel correction, not learning a world representation",
                "Test seed selects nearest coarse pixel signature; not semantic classification",
                "Local hash chained ledger is NOT authentic Obsidia Merkle sealing",
                "Candidate skills have not passed independent real-world validation",
            ]}
    (output/"evaluation.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"evaluation":str(output/"evaluation.json"),
            "train_lessons":len(train_reports),"unseen_exams":len(exams),
            "exam_scores":[{k:r[k] for k in ("exercise_ref",
                        "cold_blank_error_pixels","candidate_replay_error_pixels",
                        "after_feedback_error_pixels")} for r in exams],
            "ledger_records":integrity["verified_records"],
            "native_memory_write_allowed":False}


def main(argv:list[str]|None=None)->int:
    import argparse
    parser=argparse.ArgumentParser(description="Brody drawing school: observe, trace, correct, candidate memory, unseen exercises")
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args(argv)
    print(json.dumps(run_school(args.out),indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
