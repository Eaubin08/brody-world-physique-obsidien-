"""FUSION-F3b: five progressive visual drawing exercises with persistent results.

Each exercise invokes the existing V3 observer + P2 memory/recomposition.
Teacher targets are independently rendered and only opened *after* generation.
These are synthetic shape exercises, not semantic object or world learning.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from PIL import Image,ImageDraw
from .drawing_school_v0 import SIDE
from .fusion_f3_integrated_visual_lesson_v0 import lesson

LESSONS=(
 ("01-line","line",[[6,7,51,9]],"E0"),
 ("02-rectangle","rectangle",[[7,8,30,32],[36,33,57,54]],"E0"),
 ("03-triangle","triangle",[[7,5,30,31],[35,34,57,57]],"E1"),
 ("04-circle","ellipse",[[6,10,28,32],[34,31,58,55]],"E1"),
 ("05-composition","rectangle",[[3,4,22,23],[26,6,45,24],[15,34,38,57]],"E2"),
)
def draw_shape(draw,shape,box,width=2):
    if shape=="line":
        x1,y1,x2,y2=box
        draw.line((x1,y1,x2,y2),fill=0,width=width)
    elif shape=="rectangle":draw.rectangle(box,outline=0,width=width)
    elif shape=="ellipse":draw.ellipse(box,outline=0,width=width)
    elif shape=="triangle":
        x1,y1,x2,y2=box
        draw.line([(x1,y2),(round((x1+x2)/2),y1),(x2,y2),(x1,y2)],fill=0,width=width)
    else:raise ValueError("unknown shape")
def school(out_dir):
    root=Path(out_dir)
    if root.exists():raise ValueError("output exists")
    for label,shape,boxes,stage in LESSONS:
        for box in boxes:
            if len(box)!=4 or not (0<=box[0]<box[2]<SIDE and 0<=box[1]<box[3]<SIDE):
                raise ValueError("invalid curriculum box: "+label)
    root.mkdir(parents=True)
    rows=[]
    # Identical learning budget for each exercise: one TRAIN exemplar, one
    # blind composition. Scores are not fed into any later exercise.
    for label,shape,boxes,stage in LESSONS:
        inputs=root/(label+"-inputs");inputs.mkdir()
        train=inputs/"train.png"
        training=Image.new("L",(SIDE,SIDE),255)
        draw_shape(ImageDraw.Draw(training),shape,[12,10,33,31])
        training.save(train)
        layout=inputs/"layout.json"
        layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":boxes}),encoding="utf-8")
        target=inputs/"teacher.png"
        gold=Image.new("L",(SIDE,SIDE),255);pen=ImageDraw.Draw(gold)
        for box in boxes:draw_shape(pen,shape,box)
        gold.save(target)
        report=lesson(train,layout,root/label,target)
        rows.append({"lesson":label,"stage":stage,"shape":shape,
                     "boxes":len(boxes),"gestures":report["gesture_count"],
                     "baseline_error":report["baseline_error_px"],
                     "candidate_error":report["candidate_error_px"],
                     "gain":report["gain_px"],"verdict":report["verdict"],
                     "candidate_sealed_before_teacher":report["target_hidden_until_after_candidate_sealed"]})
    with (root/"scores.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    report={"schema":"BRODY_FUSION_F3B_SCHOOL_V0","lessons":len(rows),
            "improved":sum(r["verdict"]=="IMPROVED" for r in rows),
            "worsened":sum(r["verdict"]=="WORSENED" for r in rows),
            "ties":sum(r["verdict"]=="TIE" for r in rows),
            "total_blank_error":sum(r["baseline_error"] for r in rows),
            "total_candidate_error":sum(r["candidate_error"] for r in rows),
            "rows":rows,"teacher_synthetic":True,
            "learning_is_independent_per_lesson":True,
            "object_semantics_proven":False,"real_world_understanding_proven":False,
            "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (root/"summary.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=school(a.out)
    print(json.dumps({k:r[k] for k in ("lessons","improved","worsened","ties","total_blank_error","total_candidate_error")}))
if __name__=="__main__":main()
