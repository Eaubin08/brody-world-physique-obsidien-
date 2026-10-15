"""P149 multi-angle temporal identity laboratory.

Separate observability, tracking and prediction. The simulation preserves
two hidden object IDs; the tracker never receives them. Paired histories may
have exactly identical final pixels yet opposite latent velocities.
"""
from __future__ import annotations
import argparse,json,random,time,hashlib,statistics
from pathlib import Path
from PIL import Image,ImageDraw
KINDS=("cross_identical","cross_distinct","occlude_one","occlude_both",
       "reverse","accelerate","stop","color_swap","distractor",
       "same_frame_opposite_history","long_gap","camera_offset")
def positions(rng,kind):
    va=rng.choice((3,4,5));vb=rng.choice((3,4,5))
    a=10+rng.randint(0,4);b=82-rng.randint(0,4)
    aa=[];bb=[]
    for t in range(7):
        aa.append(a);bb.append(b)
        sa=va;sb=-vb
        if kind=="reverse" and t>=3:sa=-va
        if kind=="stop" and t>=3:sa=0
        if kind=="accelerate":sa=va+t//2
        if kind=="same_frame_opposite_history":
            # Converge at t=4 with opposite motion depending on hidden trial bit
            direction=rng.choice((-1,1)) if t==0 else direction
            a=48+(t-4)*4*direction
            b=48-(t-4)*4*direction
            continue
        a+=sa;b+=sb
    return aa,bb
def render(a,b,t,kind,rng=None):
    im=Image.new("RGB",(96,64),(248,247,245));d=ImageDraw.Draw(im)
    camera=t*2 if kind=="camera_offset" else 0
    def dot(x,y,c):d.ellipse((x-3-camera,y-3,x+3-camera,y+3),fill=c)
    ca=(225,45,55);cb=(40,75,230) if kind=="cross_distinct" else ca
    if kind=="color_swap" and t>=4:ca,cb=cb,(30,165,65)
    dot(a,26,ca);dot(b,38,cb)
    if kind=="distractor":dot(15+t*7,52,(45,185,65))
    if kind in ("occlude_one","occlude_both","long_gap"):
        if kind=="occlude_one":d.rectangle((35,0,60,33),fill=(95,95,95))
        else:d.rectangle((30,0,65,63),fill=(95,95,95))
    return im
def observed(im):
    px=im.load();ys={}
    for row in (26,38):
        coords=[]
        for y in range(row-3,row+4):
            for x in range(96):
                r,g,b=px[x,y]
                if r>190 and g<100 and b<120:coords.append(x)
        ys[str(row)]=(min(coords)+max(coords))/2 if coords else None
    return ys
def estimator(history):
    # Tracks separated by known observation lanes, not real identity discovery.
    center=[h["26"] for h in history]
    avail=[(i,x) for i,x in enumerate(center) if x is not None]
    if len(avail)<2:return None,"HOLD_INSUFFICIENT_HISTORY"
    (u,x),(v,y)=avail[-2:]
    if v-u>3:return None,"HOLD_LONG_GAP"
    return y+(y-x)/(v-u)*(len(center)-v),"TRACK_LINEAR_EXTRAPOLATION"
def experiment(rng,kind):
    aa,bb=positions(rng,kind)
    imgs=[render(aa[t],bb[t],t,kind) for t in range(7)]
    observed_history=[observed(im) for im in imgs[:6]]
    prediction,why=estimator(observed_history)
    last=observed_history[-1]["26"]
    target=aa[6]
    # Camera shift is deliberately not compensated: this is a stress test.
    return imgs,{"truth":target,"prediction":prediction,"reason":why,
      "snapshot":last,"mae":abs(prediction-target) if prediction is not None else None,
      "snapshot_mae":abs(last-target) if last is not None else None,
      "history":observed_history}
def paired_counterfactual():
    # At the center crossing both objects have identical pixels, while
    # their latent future ID trajectories differ.
    def sequence(direction):
        frames=[]
        for t in range(5):
            a=48+(t-4)*5*direction;b=48-(t-4)*5*direction
            frames.append(render(a,b,t,"cross_identical"))
        return frames
    left=sequence(1);right=sequence(-1)
    same=left[4].tobytes()==right[4].tobytes()
    different_past=left[0].tobytes()!=right[0].tobytes()
    h1=[observed(x) for x in left[:5]]
    h2=[observed(x) for x in right[:5]]
    for im in left+right:im.close()
    proof=render(48,48,4,"cross_identical");digest=hashlib.sha256(proof.tobytes()).hexdigest();proof.close()
    return {"same_final_pixels":same,"different_histories":different_past,
      "different_hidden_identity_futures":(48+5)!=(48-5),
      "history_observations_differ":h1!=h2,
      "pixel_sha256":digest}
def run(out,minutes=20,seed=149,episodes_per_kind=800):
    if not (2<=minutes<=60 and 20<=episodes_per_kind<=5000):raise ValueError("INVALID_BOUNDS")
    path=Path(out)
    if path.exists():raise ValueError("PRESERVE_EVIDENCE")
    path.mkdir(parents=True)
    rng=random.Random(seed+999)
    start=time.monotonic();deadline=start+60*minutes
    cf=paired_counterfactual()
    (path/"COUNTERFACTUAL.json").write_text(json.dumps(cf,indent=2),encoding="utf8")
    rows={};total=0;stop=False;sample_dir=path/"samples";sample_dir.mkdir()
    with (path/"EPISODES.jsonl").open("w",encoding="utf8") as log:
        for kind in KINDS:
            record={"n":0,"answered":0,"holds":0,"history_sum_abs_error":0.,
                    "snapshot_answered":0,"snapshot_sum_abs_error":0.,
                    "within_3px":0}
            for i in range(episodes_per_kind):
                if time.monotonic()>=deadline:stop=True;break
                images,r=experiment(rng,kind)
                record["n"]+=1;total+=1
                if r["prediction"] is None:record["holds"]+=1
                else:
                    record["answered"]+=1;record["history_sum_abs_error"]+=r["mae"]
                    record["within_3px"]+=int(r["mae"]<=3)
                if r["snapshot_mae"] is not None:
                    record["snapshot_answered"]+=1
                    record["snapshot_sum_abs_error"]+=r["snapshot_mae"]
                if i==0:
                    for j,im in enumerate(images):im.save(sample_dir/f"{kind}_{j}.png")
                log.write(json.dumps({"kind":kind,"i":i,**r},sort_keys=True)+"\n")
                for im in images:im.close()
            record["history_mae"]=round(record["history_sum_abs_error"]/record["answered"],4) if record["answered"] else None
            record["snapshot_mae"]=round(record["snapshot_sum_abs_error"]/record["snapshot_answered"],4) if record["snapshot_answered"] else None
            record["coverage"]=round(record["answered"]/record["n"],4) if record["n"] else None
            rows[kind]=record
            if stop:break
    result={"schema":"BRODY_P149_MULTIANGLE_TEMPORAL_IDENTITY","episodes":total,
      "scenarios_expected":len(KINDS),"scenarios_completed":sum(r["n"]==episodes_per_kind for r in rows.values()),
      "elapsed_seconds":round(time.monotonic()-start,3),
      "counterfactual":cf,"scenario_results":rows,
      "stopped_by":"TIME_BUDGET" if stop else "EPISODE_CAP",
      "identity_resolution_proven":False,"physical_learning_proven":False,
      "lane_is_given_by_detector":True,"independent_real_world_sources":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (path/"MASTER_REPORT.json").write_text(json.dumps(result,indent=2),encoding="utf8")
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20);p.add_argument("--seed",type=int,default=149)
    p.add_argument("--episodes-per-kind",type=int,default=800)
    a=p.parse_args()
    report=run(a.out,a.minutes,a.seed,a.episodes_per_kind)
    print(json.dumps({k:v for k,v in report.items() if k!="scenario_results"},indent=2))
    print("Per-scenario results: "+str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
