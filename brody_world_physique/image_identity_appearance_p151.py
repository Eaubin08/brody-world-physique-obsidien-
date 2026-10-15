"""P151 controlled identity continuity: appearance != motion != identity.

Pixels only at inference. Latent IDs exclusively in independent grading.
Ablation: nearest color vs geometric association, exact ID accuracy vs HOLD.
"""
import argparse,json,random,time,math
from pathlib import Path
from PIL import Image,ImageDraw
from .image_tracking_beam_p150 import observe, camera_from_marks
CASES=("colour_only","motion_reverse_only","colour_and_reverse","cross_equal","cross_color",
       "overlap_equal","occlude_short","occlude_long","camera_and_colour","distractor")
def episode(rng,kind):
    v=rng.choice((3,4,5));xa=rng.randint(12,18);xb=rng.randint(88,96)
    ya=yb=rng.randint(28,42)
    frames=[];truth=[]
    camera=rng.choice((-2,-1,1,2)) if kind=="camera_and_colour" else 0
    for t in range(10):
        a=xa+v*t;b=xb-v*t
        if kind=="motion_reverse_only" and t>5:a=xa+5*v-(t-5)*v
        if kind=="colour_and_reverse" and t>5:a=xa+5*v-(t-5)*v
        if kind=="overlap_equal":a=55+(t-5)*v;b=55-(t-5)*v
        if kind in ("colour_only","motion_reverse_only","colour_and_reverse","camera_and_colour","distractor","occlude_short","occlude_long"):b=xb
        c1=(220,35,45);c2=(35,80,225)
        if kind in ("cross_equal","overlap_equal","occlude_short","occlude_long"):c2=c1
        if kind in ("colour_only","colour_and_reverse","camera_and_colour") and t>=5:c1=(35,80,225);c2=(220,35,45)
        im=Image.new("RGB",(112,72),(246,245,242));d=ImageDraw.Draw(im)
        offset=camera*t
        for xx,yy in ((7,7),(104,9),(96,63)):
            d.rectangle((xx-2-offset,yy-2,xx+2-offset,yy+2),fill=(15,155,15))
        def dot(x,y,c):d.ellipse((x-3-offset,y-3,x+3-offset,y+3),fill=c)
        dot(a,ya,c1);dot(b,yb,c2)
        if kind=="distractor":dot(80-5*t,59,(220,35,45))
        if kind in ("occlude_short","occlude_long"):
            width=14 if kind=="occlude_short" else 38
            d.rectangle((54-width//2-offset,ya-6,54+width//2-offset,ya+6),fill=(100,100,105))
        frames.append(im);truth.append({"A":(a,ya),"B":(b,yb)})
    return frames,truth
def frame_detections(im):
    objs,marks=observe(im)
    correction=camera_from_marks(marks)
    return [(x+(correction or 0),y,c) for x,y,c in objs],correction is not None
def predict(frames,appearance_lock=False):
    tracks=None;ambiguous=0;camera_seen=0;history=[]
    for i,im in enumerate(frames):
        detections,seen=frame_detections(im);camera_seen+=int(seen)
        if tracks is None:
            if len(detections)<2:continue
            arr=sorted(detections,key=lambda d:d[0])[:2]
            tracks=[{"x":a[0],"y":a[1],"color":a[2],"vx":0.,"vy":0.,"lost":0} for a in arr]
            continue
        import itertools
        opts=[]
        for choices in itertools.product(range(-1,len(detections)),repeat=2):
            if choices[0]>=0 and choices[0]==choices[1]:continue
            score=0.;upd=[]
            for tr,which in zip(tracks,choices):
                prior_x=tr["x"]+tr["vx"];prior_y=tr["y"]+tr["vy"]
                if which<0:
                    score+=5+tr["lost"]*2
                    upd.append(dict(tr,x=prior_x,y=prior_y,lost=tr["lost"]+1))
                else:
                    x,y,col=detections[which]
                    dist=math.hypot(x-prior_x,y-prior_y)
                    penalty=(0 if col==tr["color"] else 20) if appearance_lock else 0
                    score+=dist+penalty
                    upd.append({"x":x,"y":y,"vx":x-tr["x"],"vy":y-tr["y"],"color":col,"lost":0})
            opts.append((score,choices,upd))
        if not opts:continue
        opts.sort(key=lambda z:z[0])
        # Ambiguity counted, but continue tracking hypotheses only via best
        # trajectory; end-time ambiguity triggers HOLD rather than a confident ID.
        if len(opts)>1 and opts[1][0]-opts[0][0]<0.2:ambiguous+=1
        tracks=opts[0][2]
        history.append({"t":i,"detections":len(detections),"ambiguous":len(opts)>1 and opts[1][0]-opts[0][0]<0.2})
    if tracks is None:return None,"HOLD_NO_INITIALIZATION",camera_seen
    if ambiguous>=3:return None,"HOLD_IDENTITY_AMBIGUOUS",camera_seen
    if tracks[0]["lost"]>2:return None,"HOLD_TARGET_INVISIBLE",camera_seen
    a=tracks[0]
    return (a["x"]+a["vx"],a["y"]+a["vy"]),"TRACK",camera_seen
def run(out,minutes=15,seed=151,episodes_each=250):
    if not 2<=minutes<=60 or not 10<=episodes_each<=3000:raise ValueError("BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True);samples=dest/"samples";samples.mkdir()
    rng=random.Random(seed+9999);start=time.monotonic();deadline=start+minutes*60
    summary={};stop=False
    with (dest/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for kind in CASES:
            stats={"n":0,"motion_answered":0,"motion_correct_identity":0,"motion_mae_sum":0.,
                   "colour_answered":0,"colour_correct_identity":0,"colour_mae_sum":0.,
                   "motion_holds":0,"camera_seen":0}
            for j in range(episodes_each):
                if time.monotonic()>=deadline:stop=True;break
                frames,truth=episode(rng,kind)
                observations=frames[:9]
                motion,reason,seen=predict(observations,False)
                colour,color_reason,_=predict(observations,True)
                target=truth[9]["A"];other=truth[9]["B"]
                stats["n"]+=1;stats["camera_seen"]+=int(seen==len(observations))
                for prefix,guess in (("motion",motion),("colour",colour)):
                    if guess is not None:
                        error=math.dist(guess,target)
                        stats[prefix+"_answered"]+=1
                        stats[prefix+"_mae_sum"]+=error
                        stats[prefix+"_correct_identity"]+=int(error+0.01<math.dist(guess,other))
                    elif prefix=="motion":stats["motion_holds"]+=1
                if j==0:
                    for idx,im in enumerate(frames):im.save(samples/f"{kind}_{idx}.png")
                log.write(json.dumps({"case":kind,"j":j,"motion":motion,"motion_reason":reason,
                    "colour_baseline":colour,"colour_reason":color_reason,"target":target,"other":other})+"\n")
                for im in frames:im.close()
            for prefix in ("motion","colour"):
                stats[prefix+"_mae"]=round(stats[prefix+"_mae_sum"]/stats[prefix+"_answered"],4) if stats[prefix+"_answered"] else None
                stats[prefix+"_coverage"]=round(stats[prefix+"_answered"]/stats["n"],4) if stats["n"] else None
                stats[prefix+"_id_accuracy_responded"]=round(stats[prefix+"_correct_identity"]/stats[prefix+"_answered"],4) if stats[prefix+"_answered"] else None
            summary[kind]=stats
            if stop:break
    report={"schema":"BRODY_P151_IDENTITY_APPEARANCE_ABLATION",
      "exam_cases":sum(s["n"] for s in summary.values()),"case_groups":len(summary),
      "elapsed_seconds":round(time.monotonic()-start,3),"stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP",
      "per_condition":summary,"identities_are_ground_truth_only":True,
      "tracking_identity_proven":False,"real_world_transfer_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=151)
    p.add_argument("--episodes-each",type=int,default=250)
    a=p.parse_args();result=run(a.out,a.minutes,a.seed,a.episodes_each)
    print(json.dumps({k:v for k,v in result.items() if k!="per_condition"},indent=2))
    print("Results:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
