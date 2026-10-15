"""P142 geometric descriptors and domain-shift stress tests.

All predictors are fitted on training examples only. The geometric candidate
uses foreground geometry, never teacher labels or generator object metadata.
Grey images explicitly HOLD colour, since chroma was removed.
"""
from __future__ import annotations
import argparse,collections,json,random,time,math
from pathlib import Path
from PIL import Image
from .image_long_curriculum_p140 import FAMILIES,LABELS,make,features,predict
from .image_transfer_stress_p141 import SHIFTS,shift_image,centroid_predict,majority

def descriptor(image):
    im=image.convert("RGB").resize((48,48))
    p=im.load();visited=set();components=[]
    for y in range(48):
        for x in range(48):
            if (x,y) in visited or min(p[x,y])>=220:continue
            todo=[(x,y)];visited.add((x,y));points=[]
            while todo:
                px,py=todo.pop();points.append((px,py))
                for q in ((px-1,py),(px+1,py),(px,py-1),(px,py+1)):
                    qx,qy=q
                    if 0<=qx<48 and 0<=qy<48 and q not in visited and min(p[qx,qy])<220:
                        visited.add(q);todo.append(q)
            if len(points)<6:continue
            xs=[v[0] for v in points];ys=[v[1] for v in points]
            width=max(xs)-min(xs)+1;height=max(ys)-min(ys)+1
            components.append((len(points),width,height,
                sum(xs)/len(xs)/48,sum(ys)/len(ys)/48))
    components.sort(reverse=True)
    n=len(components)
    area=sum(c[0] for c in components)/2304
    occupancy=sum(c[0]/(c[1]*c[2]) for c in components)/n if n else 0
    aspect=sum(math.log(c[1]/c[2]) for c in components)/n if n else 0
    centx=sum(c[3] for c in components)/n if n else .5
    centy=sum(c[4] for c in components)/n if n else .5
    sx=math.sqrt(sum((c[3]-centx)**2 for c in components)/n) if n else 0
    sy=math.sqrt(sum((c[4]-centy)**2 for c in components)/n) if n else 0
    foreground=[p[x,y] for y in range(48) for x in range(48) if min(p[x,y])<220]
    mean=[sum(rgb[channel] for rgb in foreground)/(255*len(foreground)) for channel in range(3)] if foreground else [0,0,0]
    return [n/3,area,occupancy,aspect,abs(aspect),centx,centy,sx,sy]+mean
def feat_for(im,family):
    v=descriptor(im)
    if family=="shape":return [v[i] for i in (2,3,4,0)]
    if family=="orientation":return [v[i] for i in (3,4)]
    if family=="count":return [v[i] for i in (0,1,7,8)]
    if family=="arrangement":return [v[i] for i in (0,7,8)]
    return v[9:12]
def confidence_predict(memory,vec,labels,unknown=False):
    if unknown:return "HOLD","DESTROYED_CHROMATIC_INFORMATION"
    if not memory:return "HOLD","NO_MEMORY"
    pred=centroid_predict(memory,vec,labels)
    return pred,"GEOMETRIC_CENTROID"
def run(out,minutes=15,seed=142,train_per_family=300,exam_per_cell=1000):
    if not 2<=minutes<=60 or not 30<=train_per_family<=1000 or not 20<=exam_per_cell<=100000:raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    t=time.monotonic();deadline=t+minutes*60
    rng=random.Random(seed);exam_rng=random.Random(seed+9587)
    train={}
    for fam in FAMILIES:
        train[fam]={"rgb":[],"geometric":[]}
        for i in range(train_per_family):
            im,label=make(rng,fam,1+i%3)
            train[fam]["rgb"].append((features(im),label))
            train[fam]["geometric"].append((feat_for(im,fam),label));im.close()
    stats={};stopped=False
    with (dest/"EXAMS.jsonl").open("w",encoding="utf8") as output:
        for transform in SHIFTS:
            for fam in FAMILIES:
                c=collections.Counter();n=0
                for i in range(exam_per_cell):
                    if time.monotonic()>deadline:stopped=True;break
                    im,answer=make(exam_rng,fam,1+i%3)
                    exam=shift_image(im,transform);im.close()
                    rgb=features(exam);geo=feat_for(exam,fam);exam.close()
                    rgbpred=predict(train[fam]["rgb"],rgb,fam)[0]
                    geopred,reason=confidence_predict(train[fam]["geometric"],geo,LABELS[fam],
                        unknown=fam=="colour" and transform=="greyscale")
                    baseline=majority(train[fam]["rgb"],LABELS[fam])
                    preds={"rgb_knn":rgbpred,"geometric":geopred,"majority":baseline}
                    for method,guess in preds.items():
                        if guess=="HOLD":c[method+"_hold"]+=1
                        elif guess==answer:c[method+"_correct"]+=1
                    n+=1
                    output.write(json.dumps({"condition":fam+"/"+transform,"i":i,
                        "predictions":preds,"actual":answer,"geometric_reason":reason},sort_keys=True)+"\n")
                stats[fam+"/"+transform]={"n":n,**{m:{"correct":c[m+"_correct"],"holds":c[m+"_hold"],
                    "accuracy_attempted":round(c[m+"_correct"]/(n-c[m+"_hold"]),4) if n-c[m+"_hold"] else None,
                    "coverage":round((n-c[m+"_hold"])/n,4) if n else None} for m in ("rgb_knn","geometric","majority")}}
                if stopped:break
            if stopped:break
    (dest/"CELL_REPORT.json").write_text(json.dumps(stats,indent=2),encoding="utf8")
    summary={"schema":"BRODY_P142_GEOMETRIC_TRANSFER","exam_cases":sum(s["n"] for s in stats.values()),
        "expected_cells":30,"completed_cells":sum(s["n"]==exam_per_cell for s in stats.values()),
        "elapsed_seconds":round(time.monotonic()-t,3),"budget_seconds":minutes*60,
        "models":["rgb_knn","geometric","majority"],"stopped_by":"TIME_BUDGET" if stopped else "EXAM_CAP",
        "greyscale_colour_holds_explicit":True,"real_world_transfer_proven":False,
        "trained_on_exam":False,"native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=142)
    p.add_argument("--train-per-family",type=int,default=300);p.add_argument("--exam-per-cell",type=int,default=1000)
    a=p.parse_args();print(json.dumps(run(a.out,a.minutes,a.seed,a.train_per_family,a.exam_per_cell),indent=2))
if __name__=="__main__":main()
