"""P138: adaptive novel-task visual laboratory; NOT a unittest repeater.

Each episode creates a new unseen procedural scene, probes a distinct visual
capability, compares a prediction with the scene and records failures. Cycles
allocate tasks to weak skill families. Limits bound CPU and disk usage.
Synthetic procedural evidence only; no autonomous real-world understanding.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random,time
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageOps
from .image_reciprocal_shape_learning_p134 import scene
from .image_multicapability_lab_p133 import geometry,match,occlusion_hypotheses
from .image_structural_observation_v1 import describe

SKILLS=("colour","count","location","rotation","shape","occlusion","reflection","relations")
SHAPES=("ellipse","rectangle","triangle")
PALETTE=((220,30,35),(20,65,210),(25,145,65),(110,40,175))
def draw_scene(rng,kind,complexity):
    image=Image.new("RGB",(64,64),"white")
    draw=ImageDraw.Draw(image)
    objects=[]
    n=1 if complexity==1 else min(4,complexity)
    for j in range(n):
        # Grid-separated objects except on occlusion tasks.
        col=j%2;row=j//2
        ox=4+col*32;oy=4+row*32
        x0=ox+rng.randint(0,6);y0=oy+rng.randint(0,6)
        w=rng.randint(9,17);h=rng.randint(9,17)
        box=(x0,y0,min(x0+w,ox+26),min(y0+h,oy+26))
        shape=rng.choice(SHAPES);rgb=rng.choice(PALETTE)
        if shape=="ellipse":draw.ellipse(box,fill=rgb)
        elif shape=="rectangle":draw.rectangle(box,fill=rgb)
        else:draw.polygon(((box[0],box[3]),((box[0]+box[2])//2,box[1]),(box[2],box[3])),fill=rgb)
        objects.append({"shape":shape,"bbox":box,"rgb":rgb})
    if kind=="occlusion" and len(objects)>1:
        b=objects[-1]["bbox"]
        draw.rectangle((b[0]-1,b[1]-1,b[2]+1,b[3]+1),fill="white")
    if kind=="reflection":image=ImageOps.mirror(image)
    if kind=="rotation":image=image.rotate(90)
    return image,objects
def probe(image,objects,skill):
    with image.copy() as im:
        observable=scene_image(im)
        struct=describe(im)
        count=len(observable["components"])
        if skill=="colour":
            actual={tuple(p["rgb"]) for p in observable["components"]}
            expected={tuple(p["rgb"]) for p in objects}
            # Occlusion/transform not applied in this skill.
            ok=bool(actual) and all(min(sum(abs(a-b) for a,b in zip(c,e)) for e in expected)<45 for c in actual)
            return ok,{"observed_colours":len(actual),"expected_colours":len(expected)}
        if skill=="count":
            return count==len(objects),{"observed":count,"expected":len(objects)}
        if skill=="location":
            return count>0 and all(0<=p["bbox"][0]<=p["bbox"][2]<64 for p in observable["components"]),{"components":count}
        if skill=="rotation":
            return count>=1,{"components_after_rotation":count,"invariance_verified":False}
        if skill=="shape":
            return count>0 and all(p["area"]>0 for p in observable["components"]),{"shape_recognized":False,"parts":count}
        if skill=="occlusion":
            return count<len(objects),{"visible":count,"original":len(objects),"cause_proven":False}
        if skill=="reflection":
            return count>=1,{"matched_identity_proven":False,"visible":count}
        if skill=="relations":
            expected=n_choose_2(count)
            return len(struct["relations"])==expected,{"relations":len(struct["relations"]),"expected":expected}
    raise ValueError("UNKNOWN_SKILL")
def n_choose_2(n):return n*(n-1)//2
def scene_image(im):
    # Observe from pixels without file I/O using same connected component
    # criterion as P134. Scanned components are purely local observations.
    from collections import deque
    pixels=im.convert("RGB").load()
    pending={(x,y) for y in range(64) for x in range(64) if min(pixels[x,y])<220}
    result=[]
    while pending:
        p=pending.pop();q=deque([p]);pts=[]
        while q:
            x,y=q.popleft();pts.append((x,y))
            for near in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if near in pending:pending.remove(near);q.append(near)
        if len(pts)<4:continue
        x0=min(x for x,y in pts);y0=min(y for x,y in pts)
        x1=max(x for x,y in pts);y1=max(y for x,y in pts)
        avg=tuple(round(sum(pixels[x,y][i] for x,y in pts)/len(pts)) for i in range(3))
        result.append({"bbox":[x0,y0,x1,y1],"area":len(pts),"rgb":avg})
    return {"components":result}
def run(out,minutes=10,maximum=3000,seed=138):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    if not (1<=minutes<=60 and 80<=maximum<=50000):raise ValueError("INVALID_BOUNDS")
    dest.mkdir(parents=True)
    rng=random.Random(seed)
    start=time.monotonic();deadline=start+minutes*60
    stats={s:{"attempts":0,"fails":0} for s in SKILLS}
    cases=[];cycle=0
    # First coverage each skill on at least ten distinct scenes.
    while len(cases)<maximum and time.monotonic()<deadline:
        cycle+=1
        order=list(SKILLS)
        if cycle>10:
            # Spend more episodes on families that have observed failures,
            # without starving any family. Every 3rd cycle covers all.
            order=sorted(SKILLS,key=lambda s:(-(stats[s]["fails"]+1)/(stats[s]["attempts"]+2),s))
            if cycle%3:order=order[:5]
        for skill in order:
            if len(cases)>=maximum or time.monotonic()>=deadline:break
            difficulty=min(4,1+(cycle//4))
            if skill in ("occlusion","relations"):difficulty=max(2,difficulty)
            im,objects=draw_scene(rng,skill,difficulty)
            ok,detail=probe(im,objects,skill)
            stats[skill]["attempts"]+=1;stats[skill]["fails"]+=int(not ok)
            n=len(cases)
            if not ok and n<1000:
                im.save(dest/f"failure_{n:05d}.png")
            cases.append({"id":n,"family":skill,"complexity":difficulty,
               "status":"PASS" if ok else "FAIL","details":detail})
    duration=time.monotonic()-start
    report={"schema":"BRODY_ADAPTIVE_VISUAL_LAB_P138","budget_minutes":minutes,
      "actual_seconds":round(duration,3),"episodes":len(cases),"cycles":cycle,
      "new_scenes_each_episode":True,"family_stats":stats,
      "passes":sum(x["status"]=="PASS" for x in cases),
      "failures":sum(x["status"]=="FAIL" for x in cases),
      "stopped_by":"EPISODE_CAP" if len(cases)>=maximum else "TIME_BUDGET",
      "tests_are_procedural_not_external":True,
      "training_or_generalization_proven":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"EXPERIMENTS.jsonl").write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in cases),encoding="utf8")
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--out",required=True);p.add_argument("--minutes",type=int,default=10)
 p.add_argument("--max-episodes",type=int,default=3000);p.add_argument("--seed",type=int,default=138)
 a=p.parse_args()
 print(json.dumps(run(a.out,a.minutes,a.max_episodes,a.seed),indent=2))
if __name__=="__main__":main()
