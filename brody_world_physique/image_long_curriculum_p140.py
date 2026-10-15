"""P140: long-running train/exam school with actual incremental memory updates.

Five independent visual questions and three education phases. An exam is
predicted BEFORE its label is revealed. No exam feedback enters the memory.
Baseline is a fixed prior; learned predictor is example-based. This module is
a controlled procedural 2-D experiment, not a real-world science claim.
"""
from __future__ import annotations
import argparse,json,math,random,time,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFilter

FAMILIES=("shape","colour","count","arrangement","orientation")
SHAPES=("rectangle","ellipse","triangle")
COLORS=((230,40,45),(25,75,220),(30,165,55),(130,45,180))
LABELS={"shape":SHAPES,"colour":("red","blue","green","purple"),
        "count":("one","two","three"),"arrangement":("horizontal","vertical","diagonal"),
        "orientation":("wide","tall","balanced")}
def make(rng,family,difficulty):
    """Labels follow the procedural world; images have uncontrolled nuisance shifts."""
    y=Image.new("RGB",(96,96),"white");d=ImageDraw.Draw(y)
    shape=rng.choice(SHAPES);colour=rng.randrange(4);n=rng.randint(1,3)
    orient=rng.choice(("wide","tall","balanced"))
    arrangement=rng.choice(("horizontal","vertical","diagonal"))
    if family=="count":n=rng.randint(1,3)
    if family=="arrangement":n=3
    for i in range(n):
        if arrangement=="horizontal":cx=22+i*25;cy=48
        elif arrangement=="vertical":cx=48;cy=22+i*25
        else:cx=22+i*25;cy=22+i*25
        jitter=2+difficulty*2
        cx+=rng.randint(-jitter,jitter);cy+=rng.randint(-jitter,jitter)
        if orient=="wide":w,h=22,11
        elif orient=="tall":w,h=11,22
        else:w,h=18,18
        w+=rng.randint(-2,2);h+=rng.randint(-2,2)
        bbox=(cx-w//2,cy-h//2,cx+w//2,cy+h//2)
        rgb=COLORS[colour]
        if shape=="rectangle":d.rectangle(bbox,fill=rgb)
        elif shape=="ellipse":d.ellipse(bbox,fill=rgb)
        else:d.polygon(((cx,bbox[1]),(bbox[0],bbox[3]),(bbox[2],bbox[3])),fill=rgb)
    if difficulty>=2:
        y=y.filter(ImageFilter.GaussianBlur(radius=0.45))
    if difficulty>=3:
        p=y.load()
        for _ in range(12):
            x=rng.randrange(96);yy=rng.randrange(96)
            old=p[x,yy];p[x,yy]=tuple(max(0,min(255,c+rng.randint(-15,15))) for c in old)
    answer={"shape":shape,"colour":LABELS["colour"][colour],
       "count":LABELS["count"][n-1],"arrangement":arrangement,
       "orientation":orient}[family]
    return y,answer
def features(image):
    # Fixed, inexpensive visual descriptor; no target labels/metadata used.
    im=image.resize((24,24)).convert("RGB")
    pix=list(im.getdata())
    vec=[]
    for by in range(6):
        for bx in range(6):
            cells=[pix[(by*4+y)*24+bx*4+x] for y in range(4) for x in range(4)]
            for c in range(3):vec.append(sum(q[c] for q in cells)/(len(cells)*255))
    return vec
def distance(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def predict(exemplars,vec,family):
    if not exemplars:return LABELS[family][0],"NO_EXPERIENCE"
    neighbors=sorted(((distance(v,vec),label) for v,label in exemplars),key=lambda p:p[0])[:5]
    votes={}
    for dist,label in neighbors:votes[label]=votes.get(label,0)+1/max(1e-5,dist)
    return sorted(votes.items(),key=lambda x:(-x[1],x[0]))[0][0],"LEARNED_NEAREST_EXAMPLES"
def run(out,minutes=10,max_episodes=60000,seed=140):
    if not 2<=minutes<=60 or not 100<=max_episodes<=250000:raise ValueError("INVALID_RESOURCE_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    rng=random.Random(seed)
    # Holdout groups are generated with a separate private random stream.
    exam_rng=random.Random(seed+10391)
    state={family:[] for family in FAMILIES}
    stats={fam:{"train":0,"exam":0,"correct":0,"baseline_correct":0} for fam in FAMILIES}
    started=time.monotonic();deadline=started+minutes*60
    cases=0;epochs=0
    log=(dest/"EPISODES.jsonl").open("w",encoding="utf8")
    try:
        while cases<max_episodes and time.monotonic()<deadline:
            epochs+=1
            # Every cycle learns on fresh cases, then holds out independent
            # cases; exam ground truth is read only AFTER prediction.
            for family in FAMILIES:
                if cases>=max_episodes or time.monotonic()>=deadline:break
                difficulty=min(3,1+epochs//80)
                image,teacher=make(rng,family,difficulty)
                vec=features(image)
                before,_=predict(state[family],vec,family)
                state[family].append((vec,teacher))
                # Ring buffer bounds RAM use; earlier observations are
                # deliberately forgotten, counted in report as limitation.
                if len(state[family])>400:state[family].pop(0)
                stats[family]["train"]+=1
                log.write(json.dumps({"id":cases,"family":family,"phase":"train",
                    "difficulty":difficulty,"prior_prediction":before,"teacher":teacher,
                    "corrected":before!=teacher})+"\n")
                cases+=1
            for family in FAMILIES:
                if cases>=max_episodes or time.monotonic()>=deadline:break
                difficulty=min(3,1+epochs//80)
                exam_image,hidden_teacher=make(exam_rng,family,difficulty)
                prediction,source=predict(state[family],features(exam_image),family)
                baseline=LABELS[family][0]
                # A sealed prediction is appended before the revealed grade.
                log.write(json.dumps({"id":cases,"family":family,"phase":"forecast",
                    "prediction":prediction,"baseline":baseline,"source":source})+"\n")
                graded=(prediction==hidden_teacher);base=(baseline==hidden_teacher)
                log.write(json.dumps({"id":cases,"family":family,"phase":"grade",
                    "actual":hidden_teacher,"correct":graded,"baseline_correct":base})+"\n")
                stats[family]["exam"]+=1;stats[family]["correct"]+=graded
                stats[family]["baseline_correct"]+=base
                cases+=1
            if epochs%10==0:
                log.flush()
                (dest/"CHECKPOINT.json").write_text(json.dumps({"epoch":epochs,"episodes":cases,"elapsed_s":round(time.monotonic()-started,2),
                    "stats":stats},indent=2),encoding="utf8")
    finally:log.close()
    report={"schema":"BRODY_TRAIN_EXAM_CURRICULUM_P140","budget_seconds":minutes*60,
      "elapsed_seconds":round(time.monotonic()-started,3),"epochs":epochs,"episodes":cases,
      "family_stats":{fam:{**d,"accuracy":round(d["correct"]/d["exam"],4) if d["exam"] else None,
                            "baseline_accuracy":round(d["baseline_correct"]/d["exam"],4) if d["exam"] else None} for fam,d in stats.items()},
      "stopped_by":"EPISODE_CAP" if cases>=max_episodes else "TIME_BUDGET",
      "real_independent_sources":False,"procedural_synthetic_only":True,
      "no_exam_feedback_to_memory":True,"bounded_memory_examples_per_family":400,
      "generalization_to_real_world_proven":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--minutes",type=int,default=10);p.add_argument("--max-episodes",type=int,default=60000)
    p.add_argument("--seed",type=int,default=140);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.out,a.minutes,a.max_episodes,a.seed),indent=2))
if __name__=="__main__":main()
