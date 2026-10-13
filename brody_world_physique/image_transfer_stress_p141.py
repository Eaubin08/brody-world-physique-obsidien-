"""P141: cross-distribution transfer with teacher-free exam and strong baselines.

Built on P140, tests domain shifts that do NOT alter semantic targets.
Holds source labels out of prediction. A/B includes no-memory majority,
RGB kNN memory and class-centroid memory. Data are still synthetic 2-D.
"""
from __future__ import annotations
import argparse,collections,json,random,time
from pathlib import Path
from PIL import Image,ImageEnhance,ImageOps,ImageFilter
from .image_long_curriculum_p140 import FAMILIES,LABELS,make,features,predict,distance

SHIFTS=("native","mirror","greyscale","posterize","blur","contrast")
def shift_image(im,kind):
    if kind=="native":return im.copy()
    if kind=="mirror":return ImageOps.mirror(im)
    if kind=="greyscale":return ImageOps.grayscale(im).convert("RGB")
    if kind=="posterize":return ImageOps.posterize(im,3)
    if kind=="blur":return im.filter(ImageFilter.GaussianBlur(1.4))
    if kind=="contrast":return ImageEnhance.Contrast(im).enhance(0.35)
    raise ValueError("INVALID_SHIFT")
def centroid_predict(memory,vector,labels):
    if not memory:return labels[0]
    groups=collections.defaultdict(list)
    for feat,label in memory:groups[label].append(feat)
    means={label:[sum(row[i] for row in rows)/len(rows) for i in range(len(vector))] for label,rows in groups.items()}
    return min(means,key=lambda label:(distance(means[label],vector),label))
def majority(memory,labels):
    counts=collections.Counter(label for _,label in memory)
    return sorted(labels,key=lambda label:(-counts[label],label))[0]
def run(out,minutes=15,seed=141,train_per_family=300,exam_per_cell=1000):
    if not 2<=minutes<=60 or not 30<=train_per_family<=1000 or not 20<=exam_per_cell<=100000:
        raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    start=time.monotonic();deadline=start+60*minutes
    train_rng=random.Random(seed)
    exam_rng=random.Random(seed+7737)
    memory={}
    for family in FAMILIES:
        memory[family]=[]
        for i in range(train_per_family):
            im,label=make(train_rng,family,1+(i%3))
            memory[family].append((features(im),label))
            im.close()
    rows=[];counters={}
    stop=False
    with (dest/"EXAMS.jsonl").open("w",encoding="utf8") as fp:
        for shift in SHIFTS:
            for family in FAMILIES:
                key=family+"/"+shift
                correct={"knn":0,"centroid":0,"majority":0}
                done=0
                for i in range(exam_per_cell):
                    if time.monotonic()>=deadline:
                        stop=True;break
                    im,truth=make(exam_rng,family,1+(i%3))
                    transformed=shift_image(im,shift);im.close()
                    vector=features(transformed);transformed.close()
                    # Prediction computed independently of label, only compared after.
                    preds={"knn":predict(memory[family],vector,family)[0],
                           "centroid":centroid_predict(memory[family],vector,LABELS[family]),
                           "majority":majority(memory[family],LABELS[family])}
                    for method in correct:correct[method]+=int(preds[method]==truth)
                    done+=1
                    fp.write(json.dumps({"group":key,"episode":i,"predictions":preds,"actual":truth,
                        "correct":{method:preds[method]==truth for method in preds}},sort_keys=True)+"\n")
                counters[key]={"n":done,"correct":correct,
                    "accuracies":{k:round(v/done,4) if done else None for k,v in correct.items()}}
                if stop:break
            if stop:break
    with (dest/"CELL_REPORT.json").open("w",encoding="utf8") as fp:json.dump(counters,fp,indent=2)
    total=sum(v["n"] for v in counters.values())
    totals={method:sum(v["correct"][method] for v in counters.values()) for method in ("knn","centroid","majority")}
    report={"schema":"BRODY_P141_TRANSFER_STRESS","elapsed_seconds":round(time.monotonic()-start,3),
        "budget_seconds":minutes*60,"exam_cases":total,"train_examples":len(FAMILIES)*train_per_family,
        "cells_completed":sum(v["n"]==exam_per_cell for v in counters.values()),
        "cells_expected":len(FAMILIES)*len(SHIFTS),
        "shift_types":list(SHIFTS),"families":list(FAMILIES),
        "global_accuracy":{m:round(v/total,4) if total else None for m,v in totals.items()},
        "stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP",
        "exam_feedback_used_in_learning":False,"unseen_generator_family":False,
        "real_world_transfer_proven":False,"native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);p.add_argument("--minutes",type=int,default=15)
    p.add_argument("--train-per-family",type=int,default=300)
    p.add_argument("--exam-per-cell",type=int,default=1000)
    p.add_argument("--seed",type=int,default=141)
    a=p.parse_args()
    print(json.dumps(run(a.out,a.minutes,a.seed,a.train_per_family,a.exam_per_cell),indent=2))
if __name__=="__main__":main()
