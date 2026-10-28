"""P161 hard visual representation transfer and genuinely held-out dynamics.
Frozen learner uses foreground segmentation from pixels, no simulator labels.
Evaluation includes unknown motion families entirely absent from training.
"""
import argparse,json,random,time,statistics,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
TRAIN_LAWS={"still":0.0,"linear":0.0,"brake":-1.0,"boost":1.0}
TEST_LAWS=("still","linear","brake","boost","reverse","oscillate","jump")
STYLES=("canonical","dark","palette_shift","square","triangle","camera","clutter","occluded","blur","scale","combined")
def positions(law,rng):
    x=float(rng.randint(32,55));v=0. if law=="still" else float(rng.choice((3,4)))
    out=[]
    for t in range(9):
        out.append(x)
        if law=="brake" and t>=2:v-=1
        if law=="boost" and t>=2:v+=1
        if law=="reverse" and t==4:v=-v
        if law=="oscillate":v=4 if t%2==0 else -4
        if law=="jump" and t==5:x+=12
        x+=v
    return out
def draw_frames(xs,style,rng):
    frames=[];truth=[]
    camera=rng.choice((-2.,2.)) if style in ("camera","combined") else 0.
    for t,x in enumerate(xs[:7]):
        bg=(29,30,43) if style=="dark" else (235,233,225)
        if style=="palette_shift":bg=(223,225,243)
        im=Image.new("RGB",(168,96),bg);d=ImageDraw.Draw(im)
        if style in ("clutter","combined"):
            for _ in range(12):
                cx=rng.randint(0,160);cy=rng.randint(2,88)
                d.rectangle((cx,cy,cx+3,cy+3),fill=(rng.randint(60,210),rng.randint(60,200),rng.randint(60,200)))
        cx=x+camera*t;cy=48.;size=6 if style!="scale" else 4+t//2
        if style=="palette_shift":fill=(30,135,205)
        else:fill=(220,45,55)
        if style=="square":d.rectangle((round(cx-size),round(cy-size),round(cx+size),round(cy+size)),fill=fill)
        elif style=="triangle":d.polygon([(cx,cy-size),(cx-size,cy+size),(cx+size,cy+size)],fill=fill)
        else:d.ellipse((round(cx-size),round(cy-size),round(cx+size),round(cy+size)),fill=fill)
        if style in ("occluded","combined") and t in (4,5):d.rectangle((int(cx)-9,36,int(cx)+9,62),fill=bg)
        if style=="blur":im=im.filter(ImageFilter.GaussianBlur(1.5))
        frames.append(im);truth.append(cx)
    return frames,truth,camera
def extract(frames):
    centers=[]
    for im in frames:
        pix=im.load();samples=[]
        # Generic saturated foreground detection, without assuming red circle.
        for y in range(24,72):
            for x in range(168):
                r,g,b=pix[x,y];mx=max(r,g,b);mn=min(r,g,b)
                if mx-mn>65 and mx>125 and (r>g+60 or b>r+55):
                    samples.append(x)
        centers.append(float(statistics.median(samples)) if len(samples)>=12 else None)
    return centers
def fit_bank(seed,n):
    rng=random.Random(seed);bank={}
    for law in ("still","linear","brake","boost"):
        acc=[]
        for _ in range(n):
            xs=positions(law,rng)
            ims,_,_=draw_frames(xs,"canonical",rng)
            seen=extract(ims)
            if all(v is not None for v in seen[:4]):
                acc.append(sum(seen[k+2]-2*seen[k+1]+seen[k] for k in (1,2))/2)
            for im in ims:im.close()
        bank[law]={"acceleration":sum(acc)/len(acc) if acc else None,"examples":len(acc)}
    return bank
def predict(seen,bank,threshold=.7):
    valid=[v for v in seen if v is not None]
    if len(valid)<4:return {"decision":"HOLD","reason":"INSUFFICIENT_VISIBILITY"}
    # Recover only temporal samples; never fill an occluded frame with oracle.
    tuples=[(seen[k+2]-2*seen[k+1]+seen[k]) for k in range(1,len(seen)-2)
            if all(seen[j] is not None for j in (k,k+1,k+2))]
    if not tuples:return {"decision":"HOLD","reason":"NO_TEMPORAL_EVIDENCE"}
    acceleration=statistics.median(tuples)
    scored=sorted((abs(acceleration-v["acceleration"]),k) for k,v in bank.items() if v["acceleration"] is not None)
    if not scored:return {"decision":"HOLD","reason":"EMPTY_BANK"}
    if scored[0][0]>threshold:return {"decision":"HOLD","reason":"NOVEL_TEMPORAL_RESPONSE","observed_acceleration":acceleration}
    plausible=[k for err,k in scored if err<=scored[0][0]+.22]
    if len(plausible)>1:return {"decision":"MULTI","hypotheses":plausible,"observed_acceleration":acceleration}
    return {"decision":"SELECT","selected":scored[0][1],"observed_acceleration":acceleration}
def run(out,minutes=20,seed=161,lessons_each=35,exam_each=40):
    if not (2<=minutes<=90 and 10<=lessons_each<=400 and 10<=exam_each<=500):raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);start=time.monotonic();deadline=start+60*minutes
    bank=fit_bank(seed+11,lessons_each)
    (root/"FROZEN_PIXELS_BANK.json").write_text(json.dumps(bank,indent=2),encoding="utf8")
    rng=random.Random(seed+7007);stats={};stop=False
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for style in STYLES:
            for law in TEST_LAWS:
                key=style+"/"+law
                row={"n":0,"perception_coverage":0,"SELECT":0,"MULTI":0,"HOLD":0,
                     "correct_known":0,"wrong_known":0,"unknown_select":0,"unknown_hold":0,
                     "unknown_multi":0,"unknown_total":0,"known_total":0,"abs_position_error_sum":0.,
                     "position_pairs":0}
                for i in range(exam_each):
                    if time.monotonic()>=deadline:stop=True;break
                    true_positions=positions(law,rng)
                    ims,truth,camera=draw_frames(true_positions,style,rng)
                    seen=extract(ims)
                    ans=predict(seen,bank)
                    row["n"]+=1;row[ans["decision"]]+=1
                    valid_pairs=[(p,t) for p,t in zip(seen,truth) if p is not None]
                    row["perception_coverage"]+=int(len(valid_pairs)>=4)
                    row["abs_position_error_sum"]+=sum(abs(p-t) for p,t in valid_pairs)
                    row["position_pairs"]+=len(valid_pairs)
                    known=law in TRAIN_LAWS
                    if known:
                        row["known_total"]+=1
                        row["correct_known"]+=int(ans["decision"]=="SELECT" and ans.get("selected")==law)
                        row["wrong_known"]+=int(ans["decision"]=="SELECT" and ans.get("selected")!=law)
                    else:
                        row["unknown_total"]+=1
                        row["unknown_select"]+=int(ans["decision"]=="SELECT")
                        row["unknown_hold"]+=int(ans["decision"]=="HOLD")
                        row["unknown_multi"]+=int(ans["decision"]=="MULTI")
                    log.write(json.dumps({"style":style,"law_hidden_for_exam":law,"case":i,
                                          "observations":seen,"camera":camera,"answer":ans})+"\n")
                    for im in ims:im.close()
                stats[key]=row
                if stop:break
            if stop:break
    report={"schema":"BRODY_P161_HARD_VISUAL_OOD","cells_expected":len(STYLES)*len(TEST_LAWS),
       "cells_completed":sum(v["n"]==exam_each for v in stats.values()),
       "episodes":sum(v["n"] for v in stats.values()),
       "duration_seconds":round(time.monotonic()-start,3),
       "stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP",
       "learned_on_visual_styles":["canonical"],"evaluated_styles":STYLES,
       "known_laws":list(TRAIN_LAWS),"held_out_laws":["reverse","oscillate","jump"],
       "per_cell":stats,
       "held_out_dynamics_are_truly_absent_from_training":True,
       "camera_correction_implemented":False,"raw_image_to_physics_learned":False,
       "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20);p.add_argument("--seed",type=int,default=161)
    p.add_argument("--lessons-each",type=int,default=35);p.add_argument("--exam-each",type=int,default=40)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.lessons_each,a.exam_each)
    print(json.dumps({k:v for k,v in r.items() if k!="per_cell"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
