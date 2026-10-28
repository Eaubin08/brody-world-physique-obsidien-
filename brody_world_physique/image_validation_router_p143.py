"""P143: representation routing trained on VALIDATION, evaluated on unseen EXAM.

No oracle selection on exam labels. For every family/shift, choose one method
on disjoint validation images, then freeze choices before the exam loop.
Synthetic-domain benchmark only.
"""
from __future__ import annotations
import argparse,json,random,time,collections
from pathlib import Path
from .image_long_curriculum_p140 import FAMILIES,LABELS,make,features,predict
from .image_transfer_stress_p141 import SHIFTS,shift_image,centroid_predict,majority
from .image_geometric_transfer_p142 import feat_for,confidence_predict

METHODS=("rgb_knn","geometric","majority")
def candidates(mem,fam,image,shift):
    rgb=features(image);geo=feat_for(image,fam)
    g,reason=confidence_predict(mem[fam]["geo"],geo,LABELS[fam],
                               unknown=fam=="colour" and shift=="greyscale")
    return {"rgb_knn":predict(mem[fam]["rgb"],rgb,fam)[0],
            "geometric":g,"majority":majority(mem[fam]["rgb"],LABELS[fam])}
def run(out,minutes=15,seed=143,train_per_family=300,validation_per_cell=120,exam_per_cell=1000):
    if not 2<=minutes<=60 or not 30<=train_per_family<=1000 or not 20<=validation_per_cell<=2000 or not 20<=exam_per_cell<=100000:
        raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    started=time.monotonic();deadline=started+minutes*60
    rng_train=random.Random(seed)
    rng_val=random.Random(seed+11111)
    rng_exam=random.Random(seed+22222)
    mem={f:{"rgb":[],"geo":[]} for f in FAMILIES}
    for fam in FAMILIES:
        for i in range(train_per_family):
            im,label=make(rng_train,fam,1+i%3)
            mem[fam]["rgb"].append((features(im),label))
            mem[fam]["geo"].append((feat_for(im,fam),label))
            im.close()
    # Router's scored validation is sealed BEFORE exam generation.
    router={};validation={}
    for shift in SHIFTS:
        for fam in FAMILIES:
            key=fam+"/"+shift
            scores={m:{"correct":0,"answered":0,"hold":0} for m in METHODS}
            for i in range(validation_per_cell):
                image,label=make(rng_val,fam,1+i%3)
                transformed=shift_image(image,shift);image.close()
                options=candidates(mem,fam,transformed,shift);transformed.close()
                for m,guess in options.items():
                    if guess=="HOLD":scores[m]["hold"]+=1
                    else:
                        scores[m]["answered"]+=1
                        scores[m]["correct"]+=int(guess==label)
            # Reward actual correct answers out of all validation questions,
            # penalize abstentions implicitly (not conditional accuracy).
            ranking=sorted(METHODS,key=lambda m:(-scores[m]["correct"],-scores[m]["answered"],METHODS.index(m)))
            choice=ranking[0]
            # Ground-truth information loss: colour cannot be reconstructed
            # from grey pixels; enforce HOLD irrespective of validation chance.
            if fam=="colour" and shift=="greyscale":choice="HOLD"
            router[key]=choice;validation[key]=scores
    (dest/"FROZEN_ROUTER.json").write_text(json.dumps({"choices":router,"validation_scores":validation,"training_seed":seed,
        "validation_seed":seed+11111,"exam_seed":seed+22222,"frozen_before_exam":True},indent=2),encoding="utf8")
    results={};stopped=False
    with (dest/"EXAM_DECISIONS.jsonl").open("w",encoding="utf8") as outlog:
        for shift in SHIFTS:
            for fam in FAMILIES:
                key=fam+"/"+shift;stat={"n":0,"correct":0,"holds":0,"rgb_correct":0,"geo_correct":0,"majority_correct":0}
                for i in range(exam_per_cell):
                    if time.monotonic()>=deadline:stopped=True;break
                    image,answer=make(rng_exam,fam,1+i%3)
                    transformed=shift_image(image,shift);image.close()
                    options=candidates(mem,fam,transformed,shift);transformed.close()
                    choice=router[key]
                    selected="HOLD" if choice=="HOLD" else options[choice]
                    stat["n"]+=1;stat["holds"]+=int(selected=="HOLD")
                    stat["correct"]+=int(selected==answer)
                    for m in METHODS:stat[{"rgb_knn":"rgb_correct","geometric":"geo_correct","majority":"majority_correct"}[m]]+=int(options[m]==answer)
                    outlog.write(json.dumps({"condition":key,"choice":choice,"predicted":selected,
                       "correct":selected==answer,"actual":answer,"alternatives":options},sort_keys=True)+"\n")
                results[key]=stat
                if stopped:break
            if stopped:break
    (dest/"CELL_REPORT.json").write_text(json.dumps(results,indent=2),encoding="utf8")
    total=sum(s["n"] for s in results.values())
    summary={"schema":"BRODY_P143_VALIDATION_ROUTER","train":train_per_family*len(FAMILIES),
       "validation":validation_per_cell*len(FAMILIES)*len(SHIFTS),"exam":total,
       "cells_expected":len(FAMILIES)*len(SHIFTS),"cells_completed":sum(s["n"]==exam_per_cell for s in results.values()),
       "router_accuracy_all":round(sum(s["correct"] for s in results.values())/total,4) if total else None,
       "router_coverage":round(sum(s["n"]-s["holds"] for s in results.values())/total,4) if total else None,
       "rgb_accuracy_all":round(sum(s["rgb_correct"] for s in results.values())/total,4) if total else None,
       "geometric_accuracy_all":round(sum(s["geo_correct"] for s in results.values())/total,4) if total else None,
       "majority_accuracy_all":round(sum(s["majority_correct"] for s in results.values())/total,4) if total else None,
       "elapsed_seconds":round(time.monotonic()-started,3),"stopped_by":"TIME_BUDGET" if stopped else "EXAM_CAP",
       "validation_precedes_exam":True,"real_world_generalization_proven":False,
       "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=143)
    p.add_argument("--train-per-family",type=int,default=300)
    p.add_argument("--validation-per-cell",type=int,default=120)
    p.add_argument("--exam-per-cell",type=int,default=1000)
    a=p.parse_args()
    print(json.dumps(run(a.out,a.minutes,a.seed,a.train_per_family,a.validation_per_cell,a.exam_per_cell),indent=2))
if __name__=="__main__":main()
