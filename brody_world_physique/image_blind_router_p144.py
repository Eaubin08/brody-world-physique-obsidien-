"""P144: transformation-blind modality routing, controlled evaluation.

The router sees image statistics and the *question family*, never transform
name or target label during exam. Validation fits a nearest-context router;
a condition-aware P143 oracle is only a comparison, not used for selection.
"""
from __future__ import annotations
import argparse,json,random,time,math
from pathlib import Path
from PIL import Image,ImageStat
from .image_long_curriculum_p140 import FAMILIES,LABELS,make,features,predict
from .image_transfer_stress_p141 import SHIFTS,shift_image,majority
from .image_geometric_transfer_p142 import feat_for,confidence_predict

def context_features(im):
    small=im.resize((12,12)).convert("RGB")
    stat=ImageStat.Stat(small)
    means=[x/255 for x in stat.mean]
    variances=[math.sqrt(x)/255 for x in stat.var]
    # No knowledge of the transformation name; descriptive image attributes.
    return means+variances
def distance(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def predictions(mem,fam,im):
    rgb=features(im);geo=feat_for(im,fam)
    gp,_=confidence_predict(mem[fam]["geo"],geo,LABELS[fam])
    return {"rgb":predict(mem[fam]["rgb"],rgb,fam)[0],"geo":gp,
            "majority":majority(mem[fam]["rgb"],LABELS[fam])}
def pick_router(validation,fam,vec,k=24):
    nearest=sorted(((distance(vec,x),method,correct) for x,method,correct in validation[fam]),key=lambda q:q[0])[:k]
    if not nearest:return "majority"
    votes={"rgb":0.0,"geo":0.0,"majority":0.0}
    for dist,method,correct in nearest:
        votes[method]+=correct/max(0.025,dist)
    return max(("geo","rgb","majority"),key=lambda method:(votes[method],method))
def run(out,minutes=15,seed=144,train_per_family=300,validation_per_condition=100,exam_per_condition=1000):
    if not 2<=minutes<=60 or not 30<=train_per_family<=1000 or not 20<=validation_per_condition<=1000 or not 20<=exam_per_condition<=100000:
        raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    start=time.monotonic();deadline=start+60*minutes
    trainrng=random.Random(seed);valrng=random.Random(seed+1901);examrng=random.Random(seed+9209)
    mem={f:{"rgb":[],"geo":[]} for f in FAMILIES}
    for fam in FAMILIES:
        for i in range(train_per_family):
            im,label=make(trainrng,fam,1+i%3)
            mem[fam]["rgb"].append((features(im),label))
            mem[fam]["geo"].append((feat_for(im,fam),label))
            im.close()
    validation={f:[] for f in FAMILIES};known_condition={}
    for shift in SHIFTS:
        for fam in FAMILIES:
            scores={"rgb":0,"geo":0,"majority":0}
            for i in range(validation_per_condition):
                im,label=make(valrng,fam,1+i%3);changed=shift_image(im,shift);im.close()
                vec=context_features(changed)
                opts=predictions(mem,fam,changed);changed.close()
                for method,guess in opts.items():
                    right=int(guess==label);scores[method]+=right
                    validation[fam].append((vec,method,right))
            known_condition[fam+"/"+shift]=max(("geo","rgb","majority"),key=lambda m:(scores[m],m))
    # Route learned exclusively on validation observations. No transformation
    # labels in its runtime input; known_condition only evaluates hindsight gap.
    (dest/"FROZEN_ROUTER.json").write_text(json.dumps({"validation_examples":{f:len(v) for f,v in validation.items()},
      "condition_aware_comparator":known_condition,"exam_labels_used":False,
      "runtime_requires_transform_name":False},indent=2),encoding="utf8")
    cells={};cut=False
    with (dest/"EXAM.jsonl").open("w",encoding="utf8") as log:
        for shift in SHIFTS:
            for fam in FAMILIES:
                stat={"n":0,"blind_correct":0,"aware_correct":0,"rgb_correct":0,"geo_correct":0,"majority_correct":0,"holds":0}
                for i in range(exam_per_condition):
                    if time.monotonic()>=deadline:cut=True;break
                    im,answer=make(examrng,fam,1+i%3);changed=shift_image(im,shift);im.close()
                    vec=context_features(changed);opts=predictions(mem,fam,changed)
                    # Explicit pixel-level achromatic condition, not oracle shift
                    is_gray=all(max(px)-min(px)<2 for px in changed.resize((12,12)).getdata())
                    changed.close()
                    choice=pick_router(validation,fam,vec)
                    blind="HOLD" if fam=="colour" and is_gray else opts[choice]
                    aware_choice=known_condition[fam+"/"+shift]
                    aware="HOLD" if fam=="colour" and shift=="greyscale" else opts[aware_choice]
                    stat["n"]+=1
                    stat["blind_correct"]+=int(blind==answer)
                    stat["aware_correct"]+=int(aware==answer)
                    stat["holds"]+=int(blind=="HOLD")
                    for method in ("rgb","geo","majority"):stat[method+"_correct"]+=int(opts[method]==answer)
                    log.write(json.dumps({"family":fam,"exam_condition":shift,
                      "blind_choice":choice,"blind_prediction":blind,"aware_prediction":aware,
                      "actual":answer,"correct":blind==answer},sort_keys=True)+"\n")
                cells[fam+"/"+shift]=stat
                if cut:break
            if cut:break
    (dest/"CELL_REPORT.json").write_text(json.dumps(cells,indent=2),encoding="utf8")
    n=sum(x["n"] for x in cells.values())
    result={"schema":"BRODY_P144_TRANSFORM_BLIND_ROUTING","exam_cases":n,
       "cells_completed":sum(x["n"]==exam_per_condition for x in cells.values()),
       "cells_expected":30,"elapsed_seconds":round(time.monotonic()-start,3),
       "blind_accuracy":round(sum(x["blind_correct"] for x in cells.values())/n,4) if n else None,
       "aware_accuracy":round(sum(x["aware_correct"] for x in cells.values())/n,4) if n else None,
       "blind_coverage":round(sum(x["n"]-x["holds"] for x in cells.values())/n,4) if n else None,
       "stopped_by":"TIME_BUDGET" if cut else "EXAM_CAP",
       "question_family_known":True,"transform_name_hidden_at_runtime":True,
       "source_generator_independent":False,"native_memory_write":False,
       "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(result,indent=2),encoding="utf8")
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=144)
    p.add_argument("--train-per-family",type=int,default=300)
    p.add_argument("--validation-per-condition",type=int,default=100)
    p.add_argument("--exam-per-condition",type=int,default=1000)
    a=p.parse_args();print(json.dumps(run(a.out,a.minutes,a.seed,a.train_per_family,a.validation_per_condition,a.exam_per_condition),indent=2))
if __name__=="__main__":main()
