"""P148: temporal occlusion, counterfactual ambiguity and memory ablation.

Predict next center after an object crosses opaque screen. Same current pixels
can correspond to differing velocities. Ground truth is only read for grading.
Distinct train and exam random streams; no learned physical laws claimed.
"""
from __future__ import annotations
import argparse,json,random,time,math,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
KINDS=("continuous","reverse","stop","acceleration","enter_occlusion","exit_occlusion",
       "ambiguous_current","two_objects","full_occlusion","out_of_view")
def generate(rng,kind):
    x=rng.randint(12,18);y=rng.randint(24,38)
    vx=rng.choice((3,4,5));acc=0
    if kind=="reverse":velocity=[vx,vx,-vx,-vx]
    elif kind=="stop":velocity=[vx,vx,0,0]
    elif kind=="acceleration":velocity=[vx,vx+1,vx+2,vx+3]
    elif kind=="ambiguous_current":velocity=[rng.choice((-vx,vx))]*4
    else:velocity=[vx]*4
    positions=[x]
    for v in velocity:positions.append(positions[-1]+v)
    if kind=="enter_occlusion":screen=(positions[3]-5,positions[3]+6)
    elif kind=="exit_occlusion":screen=(positions[2]-5,positions[2]+6)
    elif kind in ("full_occlusion","ambiguous_current"):screen=(0,95)
    else:screen=(39,55)
    frames=[]
    for i,p in enumerate(positions):
        im=Image.new("RGB",(96,64),"white");d=ImageDraw.Draw(im)
        d.ellipse((p-3,y-3,p+3,y+3),fill=(220,45,50))
        if kind=="two_objects":d.rectangle((80-i*3,45,85-i*3,50),fill=(30,80,220))
        d.rectangle((screen[0],0,screen[1],63),fill=(100,100,100))
        frames.append(im)
    return frames,positions,screen
def locate(im):
    p=im.load();xs=[]
    for y in range(im.height):
        for x in range(im.width):
            r,g,b=p[x,y]
            if r>160 and g<90 and b<110:xs.append(x)
    return (min(xs)+max(xs))/2 if xs else None
def forecast(observations):
    visible=[(i,x) for i,x in enumerate(observations) if x is not None]
    if len(visible)<2:return None,"HOLD_INSUFFICIENT_OBSERVATION"
    (i1,x1),(i2,x2)=visible[-2:]
    dt=i2-i1
    if dt<=0:return None,"HOLD_INVALID_TIME"
    velocity=(x2-x1)/dt
    return x2+velocity*(len(observations)-i2),"LINEAR_HISTORY_EXTRAPOLATION"
def evaluate(frames,truth):
    observed=[locate(im) for im in frames[:4]]
    history,reason=forecast(observed)
    current=observed[-1]
    snapshot=(current if current is not None else None)
    actual=truth[4]
    def measured(p):return abs(p-actual) if p is not None else None
    return {"visible_centers":observed,"history_prediction":history,"history_reason":reason,
       "snapshot_prediction":snapshot,"history_abs_error":measured(history),
       "snapshot_abs_error":measured(snapshot),"hidden_truth":actual}
def run(out,minutes=15,seed=148,episodes_per_kind=1500):
    if not 2<=minutes<=60 or not 20<=episodes_per_kind<=20000:raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True)
    rng=random.Random(seed+8201)
    start=time.monotonic();deadline=start+60*minutes
    totals={k:{"n":0,"history_answered":0,"snapshot_answered":0,"history_mae_total":0.,
               "snapshot_mae_total":0.,"history_holds":0} for k in KINDS}
    count=0;stopped=False;examples=root/"examples";examples.mkdir()
    with (root/"EPISODES.jsonl").open("w",encoding="utf8") as log:
        for kind in KINDS:
            for j in range(episodes_per_kind):
                if time.monotonic()>=deadline:stopped=True;break
                frames,truth,screen=generate(rng,kind)
                outcome=evaluate(frames,truth)
                stat=totals[kind];stat["n"]+=1;count+=1
                for which in ("history","snapshot"):
                    error=outcome[which+"_abs_error"]
                    if error is not None:
                        stat[which+"_answered"]+=1
                        stat[which+"_mae_total"]+=error
                stat["history_holds"]+=int(outcome["history_prediction"] is None)
                if j==0:
                    for i,frame in enumerate(frames):frame.save(examples/f"{kind}_frame_{i}.png")
                log.write(json.dumps({"kind":kind,"episode":j,"screen":screen,
                    "visible_centers":outcome["visible_centers"],
                    "history_prediction":outcome["history_prediction"],
                    "snapshot_prediction":outcome["snapshot_prediction"],
                    "history_abs_error":outcome["history_abs_error"],
                    "snapshot_abs_error":outcome["snapshot_abs_error"]},sort_keys=True)+"\n")
                for frame in frames:frame.close()
            if stopped:break
    report={"schema":"BRODY_P148_TEMPORAL_OCCLUSION","episodes":count,"elapsed_seconds":round(time.monotonic()-start,3),
      "budget_seconds":minutes*60,"scenarios":{kind:{**stat,
        "history_mae":round(stat["history_mae_total"]/stat["history_answered"],4) if stat["history_answered"] else None,
        "snapshot_mae":round(stat["snapshot_mae_total"]/stat["snapshot_answered"],4) if stat["snapshot_answered"] else None}
        for kind,stat in totals.items()},
      "stopped_by":"TIME_BUDGET" if stopped else "EPISODE_CAP",
      "physics_learning_proven":False,"memory_updates":False,
      "real_world_sources":False,"native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=148)
    p.add_argument("--episodes-per-kind",type=int,default=1500)
    a=p.parse_args();print(json.dumps(run(a.out,a.minutes,a.seed,a.episodes_per_kind),indent=2))
if __name__=="__main__":main()
