"""P146: robust foreground and few-shot adaptation for held-out renderers.

Course: P140. Domain adaptation: teacher-labeled P145 scenes. Exam: independent
P145 scenes, sealed after adaptation. Reports both before/after, including the
reference domain, without oracle model choice at exam.
"""
from __future__ import annotations
import argparse,json,random,time,math
from pathlib import Path
from PIL import Image
from .image_long_curriculum_p140 import FAMILIES,LABELS,make,features,predict
from .image_cross_renderer_world_p145 import WORLD_TYPES,alternative_scene
from .image_blind_router_p144 import predictions
from .image_transfer_stress_p141 import majority,centroid_predict

def robust_features(im,family):
    rgb=im.convert("RGB").resize((48,48))
    pix=rgb.load()
    corners=[pix[x,y] for x,y in ((0,0),(47,0),(0,47),(47,47))]
    bg=tuple(sorted(c[i] for c in corners)[len(corners)//2] for i in range(3))
    points=set()
    for y in range(48):
        for x in range(48):
            if sum(abs(pix[x,y][c]-bg[c]) for c in range(3))>=65:points.add((x,y))
    remaining=set(points);parts=[]
    while remaining:
        start=remaining.pop();stack=[start];component=[start]
        while stack:
            x,y=stack.pop()
            for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if q in remaining:
                    remaining.remove(q);stack.append(q);component.append(q)
        if len(component)<5:continue
        xs=[x for x,y in component];ys=[y for x,y in component]
        x0=min(xs);x1=max(xs);y0=min(ys);y1=max(ys)
        width=x1-x0+1;height=y1-y0+1
        part_rgb=[pix[x,y] for x,y in component]
        avg=tuple(sum(p[i] for p in part_rgb)/(len(part_rgb)*255) for i in range(3))
        parts.append((len(component),width,height,(x0+x1)/94,(y0+y1)/94,avg))
    parts.sort(reverse=True)
    count=len(parts)
    occupancy=sum(p[0]/(p[1]*p[2]) for p in parts)/count if count else 0
    aspect=sum(math.log(p[1]/p[2]) for p in parts)/count if count else 0
    meanx=sum(p[3] for p in parts)/count if count else .5
    meany=sum(p[4] for p in parts)/count if count else .5
    spreadx=math.sqrt(sum((p[3]-meanx)**2 for p in parts)/count) if count else 0
    spready=math.sqrt(sum((p[4]-meany)**2 for p in parts)/count) if count else 0
    colour=tuple(sum(p[5][i]*p[0] for p in parts)/sum(p[0] for p in parts) for i in range(3)) if count else (0,0,0)
    if family=="shape":return [occupancy,abs(aspect),aspect,count/3]
    if family=="orientation":return [aspect,abs(aspect)]
    if family=="count":return [count/3,spreadx,spready]
    if family=="arrangement":return [count/3,spreadx,spready,meanx,meany]
    return list(colour)
def candidate(models,im,family):
    return centroid_predict(models[family],robust_features(im,family),LABELS[family])
def make_world(rng,family,world,idx):
    if world=="reference":return make(rng,family,1+idx%3)
    return alternative_scene(rng,family,world)
def run(out,minutes=15,seed=146,train_each=300,adapt_each=60,exam_each=600):
    if not(2<=minutes<=60 and 30<=train_each<=1000 and 10<=adapt_each<=500 and 20<=exam_each<=30000):
        raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    start=time.monotonic();deadline=start+minutes*60
    tr=random.Random(seed);adapt_rng=random.Random(seed+1111);exam_rng=random.Random(seed+9999)
    original={f:{"rgb":[],"geo":[]} for f in FAMILIES}
    base={f:[] for f in FAMILIES};corrected={f:[] for f in FAMILIES}
    from .image_geometric_transfer_p142 import feat_for
    for family in FAMILIES:
        for i in range(train_each):
            im,label=make(tr,family,1+i%3)
            original[family]["rgb"].append((features(im),label))
            original[family]["geo"].append((feat_for(im,family),label))
            example=(robust_features(im,family),label)
            base[family].append(example);corrected[family].append(example)
            im.close()
    lessons={}
    for world in WORLD_TYPES:
        if world=="reference":continue
        for family in FAMILIES:
            key=family+"/"+world;lessons[key]=0
            for i in range(adapt_each):
                im,label=make_world(adapt_rng,family,world,i)
                corrected[family].append((robust_features(im,family),label))
                lessons[key]+=1;im.close()
    (dest/"SEALED_ADAPTATION.json").write_text(json.dumps({
      "train_per_family":train_each,"adapt_per_world_and_family":adapt_each,
      "lesson_groups":lessons,"exam_seed":seed+9999,
      "exam_feedback_used_in_memory":False},indent=2),encoding="utf8")
    results={};timedout=False
    with (dest/"EXAMS.jsonl").open("w",encoding="utf8") as output:
        for world in WORLD_TYPES:
            for family in FAMILIES:
                counter={"n":0,"p144_correct":0,"robust_before_correct":0,
                         "adapted_correct":0,"adapted_hold":0}
                for i in range(exam_each):
                    if time.monotonic()>=deadline:timedout=True;break
                    im,answer=make_world(exam_rng,family,world,i)
                    # Current P144 representation retained as unchanged comparator,
                    # not an exam-trained router: compare best existing single method.
                    prior=predictions(original,family,im)
                    prior_guess=prior["geo"]
                    before=candidate(base,im,family)
                    after=candidate(corrected,im,family)
                    im.close()
                    counter["n"]+=1
                    counter["p144_correct"]+=int(prior_guess==answer)
                    counter["robust_before_correct"]+=int(before==answer)
                    counter["adapted_correct"]+=int(after==answer)
                    output.write(json.dumps({"world":world,"family":family,"i":i,"actual":answer,
                     "prior_geometric":prior_guess,"robust_before":before,"adapted":after},sort_keys=True)+"\n")
                results[family+"/"+world]=counter
                if timedout:break
            if timedout:break
    (dest/"CELL_REPORT.json").write_text(json.dumps(results,indent=2),encoding="utf8")
    perworld={}
    for world in WORLD_TYPES:
        subset=[c for key,c in results.items() if key.endswith("/"+world)]
        n=sum(c["n"] for c in subset)
        perworld[world]={"n":n,**{method:round(sum(c[method+"_correct"] for c in subset)/n,4) if n else None
            for method in ("p144","robust_before","adapted")}}
    summary={"schema":"BRODY_P146_BACKGROUND_AWARE_FEW_SHOT_ADAPTATION",
      "duration_seconds":round(time.monotonic()-start,3),"budget_seconds":minutes*60,
      "exam_cases":sum(c["n"] for c in results.values()),
      "world_stats":perworld,"cells_expected":25,"cells_completed":sum(c["n"]==exam_each for c in results.values()),
      "adaptation_examples":len(lessons)*adapt_each,"stopped_by":"TIME_BUDGET" if timedout else "EXAM_CAP",
      "hold_calibration_implemented":False,
      "occlusion_reconstruction_implemented":False,
      "independent_real_sources":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=146)
    p.add_argument("--train-each",type=int,default=300)
    p.add_argument("--adapt-each",type=int,default=60)
    p.add_argument("--exam-each",type=int,default=600)
    a=p.parse_args()
    print(json.dumps(run(a.out,a.minutes,a.seed,a.train_each,a.adapt_each,a.exam_each),indent=2))
if __name__=="__main__":main()
