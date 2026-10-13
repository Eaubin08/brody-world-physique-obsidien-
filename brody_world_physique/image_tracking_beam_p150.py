"""P150 — image-only multi-object tracking, camera correction, ambiguity.

No lane positions or object ID in inference. Two equally red moving dots may
become unidentifiable after overlap; HOLD is a valid result. Independent
truth is retained by simulation for exam grading only.
"""
import argparse,json,random,time,math
from pathlib import Path
from PIL import Image,ImageDraw

SCENARIOS=("separate","cross","overlap","occlude_one","occlude_both","camera_pan","appearance_swap","distractor")
W,H=112,72
def build(rng,scenario):
    speed=rng.choice((3,4,5))
    x1=rng.randint(10,16);x2=rng.randint(93,100)
    y=rng.randint(29,41)
    sign=rng.choice((-1,1)) if scenario=="overlap" else 1
    positions=[]
    for t in range(9):
        a=x1+speed*t
        b=x2-speed*t
        if scenario=="separate":b=x2+speed*t//2
        if scenario=="appearance_swap" and t>=5:a=x1+speed*5-speed*(t-5)
        if scenario=="overlap":a=56+(t-4)*speed*sign;b=56-(t-4)*speed*sign
        positions.append((a,b))
    camera=rng.choice((-2,-1,1,2)) if scenario=="camera_pan" else 0
    frames=[]
    for t,(a,b) in enumerate(positions):
        im=Image.new("RGB",(W,H),(246,245,242))
        d=ImageDraw.Draw(im)
        offset=t*camera
        # Three fixed landmarks provide an *observed* camera-motion cue.
        for sx,sy in ((7,7),(104,9),(96,63)):
            d.rectangle((sx-offset-2,sy-2,sx-offset+2,sy+2),fill=(15,155,15))
        c1=(225,35,45);c2=(35,75,225) if scenario in ("appearance_swap","separate") else c1
        if scenario=="appearance_swap" and t>=4:c1,c2=c2,c1
        for x,col in ((a,c1),(b,c2)):
            d.ellipse((x-offset-3,y-3,x-offset+3,y+3),fill=col)
        if scenario=="distractor":
            x=15+6*t-offset;d.ellipse((x-2,58,x+2,62),fill=(220,35,45))
        if scenario in ("occlude_one","occlude_both"):
            left,right=(30,49) if scenario=="occlude_one" else (36,76)
            top,bottom=(y-5,y+1) if scenario=="occlude_one" else (y-9,y+9)
            d.rectangle((left-offset,top,right-offset,bottom),fill=(105,105,110))
        frames.append(im)
    return frames,positions,camera
def components(im,predicate):
    p=im.load();found=set()
    for y in range(H):
        for x in range(W):
            if predicate(*p[x,y]):found.add((x,y))
    blobs=[]
    while found:
        seed=found.pop();stack=[seed];blob=[seed]
        while stack:
            x,y=stack.pop()
            for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if q in found:found.remove(q);stack.append(q);blob.append(q)
        if len(blob)>=4:
            blobs.append((sum(x for x,y in blob)/len(blob),sum(y for x,y in blob)/len(blob),len(blob)))
    return blobs
def observe(im):
    red=components(im,lambda r,g,b:r>175 and g<110 and b<120)
    blue=components(im,lambda r,g,b:b>150 and r<100 and g<130)
    marks=components(im,lambda r,g,b:g>110 and r<65 and b<90)
    return sorted([(x,y,0) for x,y,n in red]+[(x,y,1) for x,y,n in blue]),sorted((x,y) for x,y,n in marks)
def camera_from_marks(marks):
    # Landmark at the top left; no use of simulator-provided offset.
    top=[(x,y) for x,y in marks if y<16 and x<25]
    return 7-min(top,key=lambda q:abs(q[1]-7))[0] if top else None
def candidates(track,obs,dt=1):
    if not track:return [(o,0.) for o in obs]
    px,py,vx,vy,cost=track
    return sorted(((o,math.hypot(o[0]-(px+vx*dt),o[1]-(py+vy*dt))) for o in obs),key=lambda v:v[1])
def infer(images):
    # Beam over two target identities; detector itself uses no fixed lanes.
    states=[];history=[];camera_info=[]
    for t,im in enumerate(images):
        objects,marks=observe(im)
        cam=camera_from_marks(marks);camera_info.append(cam)
        corrected=[(x+cam,y,c) for x,y,c in objects] if cam is not None else objects
        if t==0:
            # Assignment at birth is arbitrary but reproducible: leftmost is A.
            ordered=sorted(corrected,key=lambda o:o[0])
            if len(ordered)<2:continue
            states=[(ordered[0][:2]+(0.,0.,0.),ordered[1][:2]+(0.,0.,0.),0.)]
            history.append({"t":t,"observations":len(corrected),"beam":len(states)})
            continue
        next_states=[]
        for a,b,loss in states:
            for ia in range(-1,len(corrected)):
                for ib in range(-1,len(corrected)):
                    if ia==ib and ia!=-1:continue
                    assigned=[]
                    for tr,idx in ((a,ia),(b,ib)):
                        x,y,vx,vy,err=tr
                        if idx<0:
                            assigned.append((x+vx,y+vy,vx,vy,err+3.5))
                        else:
                            nx,ny,_=corrected[idx]
                            e=math.hypot(nx-x-vx,ny-y-vy)
                            assigned.append((nx,ny,nx-x,ny-y,err+e))
                    next_states.append((assigned[0],assigned[1],loss+sum(z[4] for z in assigned)-a[4]-b[4]))
        states=sorted(next_states,key=lambda q:q[2])[:6]
        history.append({"t":t,"observations":len(corrected),"beam":len(states)})
    if not states:return {"prediction":None,"reason":"HOLD_NO_TRACK","margin":None,"camera_observed":all(c is not None for c in camera_info)}
    best=states[0];second=states[1] if len(states)>1 else None
    margin=(second[2]-best[2]) if second else float("inf")
    # Close competitive association indicates unresolved identity, not certainty.
    if second and margin<0.6:
        pred=None;reason="HOLD_IDENTITY_AMBIGUOUS"
    else:
        a=best[0];pred=a[0]+a[2];reason="TRACK_PREDICTION"
    return {"prediction":pred,"reason":reason,"margin":round(margin,4) if math.isfinite(margin) else None,
            "camera_observed":all(c is not None for c in camera_info),"history":history}
def run(out,minutes=15,seed=150,episodes_each=300):
    if not 2<=minutes<=60 or not 10<=episodes_each<=10000:raise ValueError("BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);examples=root/"examples";examples.mkdir()
    rng=random.Random(seed+8173)
    begun=time.monotonic();deadline=begun+minutes*60;results={};cut=False
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for scenario in SCENARIOS:
            metric={"n":0,"answered":0,"holds":0,"mae_sum":0.,"within_4px":0,"camera_seen":0}
            for i in range(episodes_each):
                if time.monotonic()>=deadline:cut=True;break
                frames,truth,cam=build(rng,scenario)
                prediction=infer(frames[:8])
                actual=truth[8][0]
                error=abs(prediction["prediction"]-actual) if prediction["prediction"] is not None else None
                metric["n"]+=1
                metric["camera_seen"]+=int(prediction["camera_observed"])
                if error is None:metric["holds"]+=1
                else:
                    metric["answered"]+=1;metric["mae_sum"]+=error;metric["within_4px"]+=int(error<=4)
                if i==0:
                    for j,im in enumerate(frames):im.save(examples/f"{scenario}_{j}.png")
                log.write(json.dumps({"scenario":scenario,"index":i,
                    "prediction":prediction["prediction"],"reason":prediction["reason"],
                    "margin":prediction["margin"],"target":actual,"error":error})+"\n")
                for im in frames:im.close()
            metric["mae"]=round(metric["mae_sum"]/metric["answered"],4) if metric["answered"] else None
            metric["coverage"]=round(metric["answered"]/metric["n"],4) if metric["n"] else None
            results[scenario]=metric
            if cut:break
    final={"schema":"BRODY_P150_IMAGE_ONLY_MULTI_OBJECT_BEAM","episodes":sum(x["n"] for x in results.values()),
      "scenarios_expected":len(SCENARIOS),"scenarios_completed":sum(x["n"]==episodes_each for x in results.values()),
      "duration_seconds":round(time.monotonic()-begun,3),"scenarios":results,
      "stopped_by":"TIME_BUDGET" if cut else "EPISODE_CAP",
      "real_identity_proven":False,"learned_dynamics":False,"observed_camera_landmarks":True,
      "real_world_generalization_proven":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(final,indent=2),encoding="utf8")
    return final
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=150)
    p.add_argument("--episodes-each",type=int,default=300)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.episodes_each)
    print(json.dumps({k:v for k,v in r.items() if k!="scenarios"},indent=2))
    print("Detailed metrics: "+str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
