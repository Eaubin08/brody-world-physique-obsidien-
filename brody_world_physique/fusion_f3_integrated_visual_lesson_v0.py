"""FUSION-F3 first integrated visual lesson: observe, encode, hide, compose, reveal.

Combines the *existing* V3 observer and P2.11 verified gesture memory/motor.
The new target is not opened until after the candidate is written and hashed.
Synthetic teacher for optional demo is labeled SIMULATED. Not object semantics.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from .drawing_school_v0 import SIDE
from .drawing_memory_school_v3 import observe_only
from .p211b_frozen_gesture_transfer_v0 import learn,read
from .p211c_gesture_recomposition_v0 import compose,_remap
from .drawing_school_v1 import render
from .p210a_visual_loop_contract_v0 import digest,open_rgba,pixel_error
from .fusion_historical_evidence_v0 import mismatch

def lesson(train_image,layout,out_dir,teacher=None):
    out=Path(out_dir)
    if out.exists():raise ValueError("refuse overwrite")
    source=open_rgba(train_image)
    if source.size!=(SIDE,SIDE):raise ValueError("training size")
    spec=json.loads(Path(layout).read_text(encoding="utf-8"))
    if spec.get("schema")!="BRODY_P211C_LAYOUT_V0" or not isinstance(spec.get("boxes"),list) or not 1<=len(spec["boxes"])<=12:
        raise ValueError("layout")
    # Observe original TRAIN reference, retain engineered visual representation;
    # this is NOT semantic interpretation of the image.
    rep=observe_only(source,"TRAIN:teacher_observed",digest(train_image))
    out.mkdir(parents=True)
    memory=out/"memory.json"
    learn(train_image,memory)
    _,motor=read(memory)
    # Generate a new composition from the IN layout without reading teacher.
    candidate=out/"candidate.png"
    summary=compose(memory,layout,candidate)
    blank=candidate.with_name(candidate.stem+"-blank.png")
    final={"schema":"BRODY_FUSION_F3_LESSON_V0",
           "train_sha256":digest(train_image),"layout_sha256":digest(layout),
           "representation_digest":rep["representation_sha256"],
           "memory_sha256":digest(memory),
           "candidate_sha256":digest(candidate),"baseline_sha256":digest(blank),
           "gesture_count":len(motor),"boxes":len(spec["boxes"]),
           "target_hidden_until_after_candidate_sealed":True,
           "observe_only_is_engineered_extraction":True,
           "novel_object_recognition":False,
           "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    if teacher is not None:
        if digest(teacher)==digest(train_image):raise ValueError("TEST target duplicates training source")
        target=open_rgba(teacher)
        if target.size!=(SIDE,SIDE):raise ValueError("target size")
        actual=open_rgba(candidate);baseline=open_rgba(blank)
        a=pixel_error(target,actual);b=pixel_error(target,baseline)
        final.update({"teacher_sha256":digest(teacher),"candidate_error_px":a,
                      "baseline_error_px":b,"gain_px":b-a,
                      "verdict":"IMPROVED" if a<b else "WORSENED" if a>b else "TIE"})
        sheet=Image.new("RGB",(SIDE*3,(SIDE+20)),"white")
        painter=ImageDraw.Draw(sheet)
        for j,(caption,im) in enumerate((("TEACHER",target),("BLANK",baseline),("STUDENT",actual))):
            painter.text((j*SIDE+2,2),caption,fill="black")
            sheet.paste(im.convert("RGB"),(j*SIDE,20))
        sheet.save(out/"comparison.png")
        final["comparison_sha256"]=digest(out/"comparison.png")
    (out/"episode.json").write_text(json.dumps(final,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return final

def demo(out_dir):
    # Demo ground truth is created separately from the pupil by a synthetic
    # teacher generator, then held aside until the attempt has been sealed.
    root=Path(out_dir)
    if root.exists():raise ValueError("output exists")
    inputs=root.parent/(root.name+"-inputs")
    if inputs.exists():raise ValueError("input exists")
    inputs.mkdir(parents=True)
    train=inputs/"train.png";im=Image.new("L",(SIDE,SIDE),255)
    ImageDraw.Draw(im).rectangle((9,11,29,31),outline=0,width=2)
    im.save(train)
    layout=inputs/"layout.json"
    boxes=[[5,5,27,27],[36,34,57,55]]
    layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":boxes}))
    # Teacher independently draws instructed rectangles (not generated via learner).
    gold=Image.new("L",(SIDE,SIDE),255);pen=ImageDraw.Draw(gold)
    for box in boxes:pen.rectangle(box,outline=0,width=2)
    target=inputs/"teacher.png";gold.save(target)
    result=lesson(train,layout,root,target)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--demo",action="store_true")
    p.add_argument("--train");p.add_argument("--layout");p.add_argument("--teacher")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    if a.demo and not a.train and not a.layout and not a.teacher:r=demo(a.out)
    elif not a.demo and a.train and a.layout:r=lesson(a.train,a.layout,a.out,a.teacher)
    else:p.error("use --demo or --train --layout [--teacher]")
    print(json.dumps({k:r[k] for k in ("schema","gesture_count","boxes","target_hidden_until_after_candidate_sealed")}))
    if "candidate_error_px" in r:print(json.dumps({k:r[k] for k in ("candidate_error_px","baseline_error_px","gain_px","verdict")}))
if __name__=="__main__":main()
