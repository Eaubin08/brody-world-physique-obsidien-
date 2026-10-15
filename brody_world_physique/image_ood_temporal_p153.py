"""P153: out-of-distribution temporal stress of frozen P151/P152 estimators.

New independent motion renderer: variable acceleration, jitter, moving camera,
texture, temporary occlusion. No tracker is taught from the exam. Simulated
ground truth solely grades next-position and identity association.
"""
import argparse,json,math,random,time
from pathlib import Path
from PIL import Image,ImageDraw
from .image_identity_beam_p152 import beam_predict
from .image_identity_appearance_p151 import predict as baseline_predict
KINDS=("variable_speed","abrupt_reverse","camera_no_landmarks","camera_with_landmarks",
       "partial_occlusion","long_occlusion","identical_colours","colour_changed",
       "noise_and_distractor","irregular_timestep")
def new_episode(rng,kind):
    x=rng.randint(15,23);bx=rng.randint(83,95)
    y=rng.randint(25,46);by=rng.randint(20,49)
    if abs(by-y)<8:by=20 if y>34 else 50
    v=rng.choice((3,4,5));bv=-rng.choice((2,3,4))
    camera=rng.choice((-2,2)) if kind in ("camera_no_landmarks","camera_with_landmarks") else 0
    xy=[];images=[]
    for t in range(10):
        xy.append(((x,y),(bx,by)))
        im=Image.new("RGB",(112,72),(rng.randint(230,248),rng.randint(225,248),rng.randint(225,248)))
        d=ImageDraw.Draw(im)
        shift=t*camera
        if kind!="camera_no_landmarks":
            for lx,ly in ((7,7),(104,9),(96,63)):
                d.rectangle((lx-2-shift,ly-2,lx+2-shift,ly+2),fill=(15,155,15))
        col=(215,42,50)
        if kind=="colour_changed" and t>=4:col=(35,80,220)
        d.ellipse((x-3-shift,y-3,x+3-shift,y+3),fill=col)
        c2=col if kind=="identical_colours" else (40,80,220)
        d.ellipse((bx-3-shift,by-3,bx+3-shift,by+3),fill=c2)
        if kind=="noise_and_distractor":
            for j in range(4):
                zx=rng.randint(0,111);zy=rng.randint(0,71)
                d.rectangle((zx,zy,zx+1,zy+1),fill=(215,35,45))
        if kind in ("partial_occlusion","long_occlusion"):
            hw=12 if kind=="partial_occlusion" else 26
            d.rectangle((56-hw-shift,0,56+hw-shift,71),fill=(100,100,100))
        images.append(im)
        a=v
        if kind=="variable_speed":a+=rng.choice((-2,-1,0,1,2))
        if kind=="abrupt_reverse" and t>=5:a=-v
        if kind=="irregular_timestep":a*=rng.choice((1,2,3))
        x+=a;bx+=bv
    return images,xy
def run(out,minutes=15,seed=153,episodes_each=200):
    if not (2<=minutes<=60 and 10<=episodes_each<=3000):raise ValueError("INVALID_BOUNDS")
    path=Path(out)
    if path.exists():raise ValueError("PRESERVE_EVIDENCE")
    path.mkdir(parents=True)
    samples=path/"samples";samples.mkdir()
    rng=random.Random(seed+5331);start=time.monotonic();deadline=start+minutes*60
    rows={};stop=False
    with (path/"EXAMS.jsonl").open("w",encoding="utf8") as outlog:
        for kind in KINDS:
            stat={"n":0,"beam_answered":0,"baseline_answered":0,"beam_id_correct":0,"baseline_id_correct":0,
                  "beam_abs_error":0.,"baseline_abs_error":0.,"beam_holds":0,"beam_within4":0}
            for j in range(episodes_each):
                if time.monotonic()>deadline:stop=True;break
                imgs,truth=new_episode(rng,kind)
                pred,why,meta=beam_predict(imgs[:9])
                old,oldreason,_=baseline_predict(imgs[:9],False)
                target,other=truth[9]
                stat["n"]+=1
                for name,guess in (("beam",pred),("baseline",old)):
                    if guess is None:
                        if name=="beam":stat["beam_holds"]+=1
                    else:
                        error=math.dist(guess,target)
                        stat[name+"_answered"]+=1
                        stat[name+"_abs_error"]+=error
                        stat[name+"_id_correct"]+=int(error+0.01<math.dist(guess,other))
                        if name=="beam":stat["beam_within4"]+=int(error<=4)
                if j==0:
                    for t,img in enumerate(imgs):img.save(samples/f"{kind}_{t}.png")
                outlog.write(json.dumps({"kind":kind,"i":j,"beam":pred,"beam_reason":why,"old":old,
                  "target":target,"other":other},sort_keys=True)+"\n")
                for im in imgs:im.close()
            for name in ("beam","baseline"):
                count=stat[name+"_answered"]
                stat[name+"_mae"]=round(stat[name+"_abs_error"]/count,3) if count else None
                stat[name+"_coverage"]=round(count/stat["n"],4) if stat["n"] else None
                stat[name+"_id_all"]=round(stat[name+"_id_correct"]/stat["n"],4) if stat["n"] else None
            rows[kind]=stat
            if stop:break
    summary={"schema":"BRODY_P153_OUT_OF_DISTRIBUTION_TEMPORAL",
      "episodes":sum(s["n"] for s in rows.values()),"conditions_expected":len(KINDS),
      "conditions_completed":sum(s["n"]==episodes_each for s in rows.values()),
      "elapsed_seconds":round(time.monotonic()-start,3),
      "stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP","per_condition":rows,
      "separate_renderer":True,"natural_video_generalization":False,
      "inference_on_pixels_only":True,"new_physics_learned":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (path/"MASTER_REPORT.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=153)
    p.add_argument("--episodes-each",type=int,default=200)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.episodes_each)
    print(json.dumps({k:v for k,v in r.items() if k!="per_condition"},indent=2))
    print("Full report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
