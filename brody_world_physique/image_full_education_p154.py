"""P154: integrated five-gate education, sealed curriculum and visual prediction.

Models infer constant acceleration from measured pixels of a few past frames;
the simulator never gives physics parameters to the learner. Three stages:
lessons -> seal -> out-of-distribution exam -> supervised feedback -> retest.
Retest compares against a frozen pre-feedback copy, on identical heldout cases.
"""
from __future__ import annotations
import argparse,copy,json,math,random,time
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
WORLD=("clean","dark","camera","noise","large","occluded")
LAWS=("stationary","constant_speed","constant_acceleration","reverse")
W,H=128,80
def simulate(rng,law,world,length=9):
    x=rng.uniform(23,39);y=rng.randint(27,50)
    vx=rng.choice((-4,-3,3,4));acc=rng.choice((-1.,1.))
    if law=="stationary":vx=0;acc=0
    if law=="constant_speed":acc=0
    if law=="reverse":acc=0
    offset=rng.choice((-1,1)) if world=="camera" else 0
    truth=[];imgs=[]
    for t in range(length):
        truth.append(x)
        bg=(25,27,34) if world=="dark" else (245,246,242)
        im=Image.new("RGB",(W,H),bg);d=ImageDraw.Draw(im)
        if world=="camera":
            for px,py in ((8,9),(119,10),(114,70)):
                d.rectangle((px-offset*t-2,py-2,px-offset*t+2,py+2),fill=(35,185,65))
        size=5 if world=="large" else 3
        d.ellipse((int(round(x-offset*t))-size,y-size,int(round(x-offset*t))+size,y+size),fill=(225,42,52))
        if world=="occluded":
            d.rectangle((60,0,74,79),fill=(99,100,105))
        if world=="noise":
            for _ in range(28):
                px=rng.randrange(W);py=rng.randrange(H)
                d.point((px,py),fill=(rng.randint(60,200),rng.randint(80,220),rng.randint(80,210)))
        imgs.append(im)
        if law=="reverse" and t==3:vx=-vx
        x+=vx
        if law=="constant_acceleration":vx+=acc
    return imgs,truth
def detect(im):
    pix=im.load();hits=[]
    for yy in range(H):
        for xx in range(W):
            r,g,b=pix[xx,yy]
            if r>210 and g<75 and b<90:hits.append(xx)
    return round(sum(hits)/len(hits),3) if hits else None
def camera_mark(im):
    p=im.load();hits=[]
    for yy in range(5,15):
        for xx in range(W):
            r,g,b=p[xx,yy]
            if g>140 and r<85 and b<110:hits.append(xx)
    # Rightmost marker at y~10; use broad search robust to clipping of left.
    return max(hits) if hits else None
def observations(images,world):
    cam0=camera_mark(images[0]) if world=="camera" else None
    result=[]
    for im in images:
        x=detect(im)
        if x is not None and world=="camera":
            cm=camera_mark(im)
            x=x+(cam0-cm) if cm is not None and cam0 is not None else x
        result.append(x)
    return result
def infer_rule(samples):
    """Induce best rule via estimated mean first and second differences."""
    options=[]
    for xs in samples:
        valid=[v for v in xs if v is not None]
        if len(valid)>=3:
            velocity=[valid[i+1]-valid[i] for i in range(len(valid)-1)]
            accel=[velocity[i+1]-velocity[i] for i in range(len(velocity)-1)]
            options.append((sum(velocity)/len(velocity),sum(accel)/len(accel)))
    if not options:return None
    v=sum(x[0] for x in options)/len(options)
    a=sum(x[1] for x in options)/len(options)
    return {"mean_velocity":v,"mean_accel":a}
def forecast(xs,rule):
    pairs=[(i,x) for i,x in enumerate(xs) if x is not None]
    if len(pairs)<2:return None
    i,x=pairs[-1];j,y=pairs[-2]
    speed=(x-y)/(i-j)
    # The acceleration term is learned from observations, not oracle.
    return x+speed+rule["mean_accel"]
def rasterize(x,background=(245,246,242)):
    im=Image.new("RGB",(W,H),background)
    if x is not None:
        d=ImageDraw.Draw(im);cx=int(round(x))
        d.ellipse((cx-3,37,cx+3,43),fill=(225,42,52))
    return im
def grade_visual(pred,actual):
    # Pixel comparison after each image has been transformed to its canonical
    # prediction target representation. Exact pixel IoU complements position.
    if pred is None:return None
    a=rasterize(pred);b=rasterize(actual)
    pa=a.load();pb=b.load();inter=union=0
    for yy in range(H):
        for xx in range(W):
            ac=pa[xx,yy][0]>200 and pa[xx,yy][1]<80
            bc=pb[xx,yy][0]>200 and pb[xx,yy][1]<80
            inter+=int(ac and bc);union+=int(ac or bc)
    a.close();b.close()
    return round(inter/union,4) if union else 1.
def evaluate_sequence(images,truth,world,rule):
    xs=observations(images[:6],world)
    pred=forecast(xs,rule)
    actual=truth[6]
    return {"prediction":pred,"actual":actual,"error":abs(pred-actual) if pred is not None else None,
      "visual_iou":grade_visual(pred,actual),"answered":pred is not None}
def run(out,minutes=20,seed=154,lessons_each=32,exam_each=120,feedback_each=24,retest_each=120):
    if not (3<=minutes<=90 and 8<=lessons_each<=300 and 20<=exam_each<=1000 and 8<=feedback_each<=300 and 20<=retest_each<=1000):
        raise ValueError("INVALID_BOUNDS")
    dst=Path(out)
    if dst.exists():raise ValueError("PRESERVE_EVIDENCE")
    dst.mkdir(parents=True);samples=dst/"samples";samples.mkdir()
    start=time.monotonic();deadline=start+minutes*60
    tr=random.Random(seed);ex=random.Random(seed+13013);fb=random.Random(seed+21917);re=random.Random(seed+49201)
    # Every learning subject sees only unlabeled observed trajectories. Law
    # names select the teacher's task, but no law parameters are supplied.
    models={};lesson_evidence={}
    for law in LAWS:
        vectors=[]
        for n in range(lessons_each):
            imgs,truth=simulate(tr,law,"clean")
            vectors.append(observations(imgs[:5],"clean"))
            for img in imgs:img.close()
        models[law]=infer_rule(vectors)
        lesson_evidence[law]={"frames_observed":sum(len(v) for v in vectors),"rule":models[law]}
    frozen=copy.deepcopy(models)
    (dst/"FROZEN_BEFORE_EXAM.json").write_text(json.dumps({"laws":lesson_evidence,
      "seed_train":seed,"seed_exam":seed+13013,"seed_feedback":seed+21917,
      "seed_retest":seed+49201,"exam_feedback_leakage":False},indent=2),encoding="utf8")
    report_cells={};cut=False
    with (dst/"EXAM.jsonl").open("w",encoding="utf8") as log:
        for law in LAWS:
            for world in WORLD:
                key=law+"/"+world
                s={"n":0,"answered":0,"within3":0,"sum_abs_error":0.,"visual_iou_total":0.}
                for j in range(exam_each):
                    if time.monotonic()>=deadline:cut=True;break
                    imgs,truth=simulate(ex,law,world)
                    outcome=evaluate_sequence(imgs,truth,world,frozen[law])
                    s["n"]+=1;s["answered"]+=int(outcome["answered"])
                    if outcome["answered"]:
                        s["sum_abs_error"]+=outcome["error"]
                        s["within3"]+=int(outcome["error"]<=3)
                        s["visual_iou_total"]+=outcome["visual_iou"]
                    if j==0 and law=="constant_acceleration":
                        imgs[5].save(samples/f"{world}_observed.png")
                        rasterize(outcome["prediction"]).save(samples/f"{world}_prediction.png")
                    log.write(json.dumps({"stage":"exam","law":law,"world":world,"j":j,**outcome})+"\n")
                    for im in imgs:im.close()
                s["mae"]=round(s["sum_abs_error"]/s["answered"],3) if s["answered"] else None
                s["mean_visual_iou"]=round(s["visual_iou_total"]/s["answered"],4) if s["answered"] else None
                report_cells[key]=s
                if cut:break
            if cut:break
    # Feedback phase is teaching on separate sequences. Estimate persistent
    # residual correction for each law/world: never touch existing frozen rules.
    corrections={}
    if not cut:
        for law in LAWS:
            for world in WORLD:
                residuals=[]
                for j in range(feedback_each):
                    imgs,truth=simulate(fb,law,world)
                    v=evaluate_sequence(imgs,truth,world,frozen[law])
                    if v["answered"]:residuals.append(v["actual"]-v["prediction"])
                    for im in imgs:im.close()
                corrections[law+"/"+world]=sum(residuals)/len(residuals) if residuals else 0.
        (dst/"LEARNED_CORRECTIONS.json").write_text(json.dumps(corrections,indent=2),encoding="utf8")
    retests={}
    if not cut:
        with (dst/"RETEST.jsonl").open("w",encoding="utf8") as log:
            for law in LAWS:
                for world in WORLD:
                    key=law+"/"+world
                    s={"n":0,"before_abs_error":0.,"after_abs_error":0.,"responded":0,
                       "after_within3":0,"retention_reference":world=="clean"}
                    for j in range(retest_each):
                        if time.monotonic()>=deadline:cut=True;break
                        imgs,truth=simulate(re,law,world)
                        outcome=evaluate_sequence(imgs,truth,world,frozen[law])
                        if outcome["answered"]:
                            before=outcome["error"]
                            after=abs(outcome["prediction"]+corrections[key]-outcome["actual"])
                            s["responded"]+=1;s["before_abs_error"]+=before
                            s["after_abs_error"]+=after;s["after_within3"]+=int(after<=3)
                            log.write(json.dumps({"law":law,"world":world,"j":j,"before":before,"after":after})+"\n")
                        s["n"]+=1
                        for im in imgs:im.close()
                    s["before_mae"]=round(s["before_abs_error"]/s["responded"],3) if s["responded"] else None
                    s["after_mae"]=round(s["after_abs_error"]/s["responded"],3) if s["responded"] else None
                    retests[key]=s
                    if cut:break
                if cut:break
    summary={"schema":"BRODY_P154_FIVE_GATE_EDUCATION","duration_seconds":round(time.monotonic()-start,3),
      "exam_cases":sum(v["n"] for v in report_cells.values()),
      "exam_cells_complete":sum(v["n"]==exam_each for v in report_cells.values()),
      "exam_cells_expected":len(LAWS)*len(WORLD),
      "retest_cases":sum(v["n"] for v in retests.values()),
      "retest_cells_complete":sum(v["n"]==retest_each for v in retests.values()),
      "retest_cells_expected":len(LAWS)*len(WORLD),
      "frozen_rule_parameters":lesson_evidence,"exam_results":report_cells,"retest_results":retests,
      "stopped_by":"TIME_BUDGET" if cut else "RETEST_CAP",
      "learning_rule_from_pixel_observations":True,
      "retention_frozen_model":True,"feedback_separate_from_exam":True,
      "canonical_visual_prediction_rendered":True,
      "real_world_observation":False,"full_autonomous_education_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dst/"MASTER_REPORT.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20);p.add_argument("--seed",type=int,default=154)
    p.add_argument("--lessons-each",type=int,default=32)
    p.add_argument("--exam-each",type=int,default=120)
    p.add_argument("--feedback-each",type=int,default=24)
    p.add_argument("--retest-each",type=int,default=120)
    a=p.parse_args()
    r=run(a.out,a.minutes,a.seed,a.lessons_each,a.exam_each,a.feedback_each,a.retest_each)
    print(json.dumps({k:v for k,v in r.items() if k not in ("frozen_rule_parameters","exam_results","retest_results")},indent=2))
    print("Full report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
