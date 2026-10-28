"""P152: persistent multi-hypothesis identity tracking and event-aware dynamics.

The estimator receives pixels only; teacher IDs and future positions are for
grading. Beam diversity is maintained across frames, not recomputed once.
"""
import argparse,itertools,json,math,random,time
from pathlib import Path
from .image_identity_appearance_p151 import CASES,episode,frame_detections,predict as p151_predict

def initial_tracks(obs):
    if len(obs)<2:return []
    a,b=sorted(obs,key=lambda o:o[0])[:2]
    return [((a[0],a[1],0.,0.,0,0),(b[0],b[1],0.,0.,0,0),0.)]

def step(beam,obs,beam_width=12):
    proposed=[]
    for a,b,cost in beam:
        for i,j in itertools.product(range(-1,len(obs)),repeat=2):
            if i>=0 and i==j:continue
            parts=[];penalty=0.
            for tr,k in ((a,i),(b,j)):
                x,y,vx,vy,lost,col=tr
                if k<0:
                    parts.append((x+vx,y+vy,vx,vy,lost+1,col))
                    penalty+=3+min(lost,5)*2
                else:
                    nx,ny,nc=obs[k]
                    residual=math.hypot(nx-(x+vx),ny-(y+vy))
                    # Reversal detection relaxes velocity after a surprising
                    # measurement, but charges for the unexpected transition.
                    newvx=nx-x;newvy=ny-y
                    penalty+=min(residual,25)+(.5 if nc!=col else 0)
                    if lost>=1:penalty+=1.5
                    parts.append((nx,ny,newvx,newvy,0,nc))
            proposed.append((parts[0],parts[1],cost+penalty))
    proposed.sort(key=lambda z:z[2])
    diverse=[];seen=set()
    for item in proposed:
        signature=tuple((round(tr[0]),round(tr[1]),round(tr[2]),tr[4]) for tr in item[:2])
        if signature not in seen:
            diverse.append(item);seen.add(signature)
        if len(diverse)>=beam_width:break
    return diverse

def beam_predict(frames,beam_width=12,uncertainty=2.):
    beam=[];saw_camera=0;ambiguity_frames=0
    for t,im in enumerate(frames):
        obs,seen=frame_detections(im);saw_camera+=int(seen)
        if not beam:
            beam=initial_tracks(obs)
            continue
        beam=step(beam,obs,beam_width)
        if len(beam)>1 and beam[1][2]-beam[0][2]<uncertainty:
            ambiguity_frames+=1
    if not beam:return None,"HOLD_NO_TRACK",{"camera_frames":saw_camera,"ambiguity_frames":ambiguity_frames}
    best=beam[0];track=best[0];guess=(track[0]+track[2],track[1]+track[3])
    # Ambiguity is meaningful only if competitive hypotheses lead to
    # materially different target A predictions.
    alternatives=[]
    for state in beam[1:]:
        if state[2]-best[2]>uncertainty:break
        other=state[0];alt=(other[0]+other[2],other[1]+other[3])
        if math.dist(guess,alt)>4:alternatives.append(alt)
    if track[4]>=4:return None,"HOLD_LONG_OCCLUSION",{"camera_frames":saw_camera,"ambiguity_frames":ambiguity_frames}
    if alternatives:return None,"HOLD_COMPETING_IDENTITIES",{"camera_frames":saw_camera,"ambiguity_frames":ambiguity_frames,"alternatives":len(alternatives)}
    return guess,"TRACK",{"camera_frames":saw_camera,"ambiguity_frames":ambiguity_frames}

def run(out,minutes=15,seed=152,episodes_each=250,beam_width=12):
    if not (2<=minutes<=60 and 10<=episodes_each<=5000 and 2<=beam_width<=32):
        raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    start=time.monotonic();deadline=start+minutes*60;rng=random.Random(seed+9951)
    summary={};stopped=False
    with (dest/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for kind in CASES:
            row={"n":0,"beam_answered":0,"baseline_answered":0,"beam_id_correct":0,
                 "baseline_id_correct":0,"beam_mae_sum":0.,"baseline_mae_sum":0.,
                 "beam_holds":0,"competing_holds":0,"beam_within_4px":0}
            for i in range(episodes_each):
                if time.monotonic()>=deadline:stopped=True;break
                frames,truth=episode(rng,kind)
                beam,reason,diagnostics=beam_predict(frames[:9],beam_width)
                baseline,baseline_reason,_=p151_predict(frames[:9],False)
                a=truth[9]["A"];b=truth[9]["B"]
                row["n"]+=1
                for prefix,result in (("beam",beam),("baseline",baseline)):
                    if result is not None:
                        err=math.dist(result,a)
                        row[prefix+"_answered"]+=1;row[prefix+"_mae_sum"]+=err
                        row[prefix+"_id_correct"]+=int(err+0.01<math.dist(result,b))
                        if prefix=="beam":row["beam_within_4px"]+=int(err<=4)
                    elif prefix=="beam":
                        row["beam_holds"]+=1;row["competing_holds"]+=int(reason=="HOLD_COMPETING_IDENTITIES")
                log.write(json.dumps({"kind":kind,"episode":i,"beam":beam,"beam_reason":reason,
                 "baseline":baseline,"baseline_reason":baseline_reason,
                 "target":a,"other":b,"diagnostics":diagnostics},sort_keys=True)+"\n")
                for im in frames:im.close()
            for method in ("beam","baseline"):
                answered=row[method+"_answered"]
                row[method+"_mae"]=round(row[method+"_mae_sum"]/answered,4) if answered else None
                row[method+"_coverage"]=round(answered/row["n"],4) if row["n"] else None
                row[method+"_id_rate_answered"]=round(row[method+"_id_correct"]/answered,4) if answered else None
                row[method+"_id_rate_all"]=round(row[method+"_id_correct"]/row["n"],4) if row["n"] else None
            summary[kind]=row
            if stopped:break
    report={"schema":"BRODY_P152_PERSISTENT_HYPOTHESES","cases":sum(x["n"] for x in summary.values()),
      "conditions_completed":sum(x["n"]==episodes_each for x in summary.values()),
      "conditions_expected":len(CASES),"elapsed_seconds":round(time.monotonic()-start,3),
      "per_condition":summary,"stopped_by":"TIME_BUDGET" if stopped else "EXAM_CAP",
      "baseline":"P151_MOTION_ASSOCIATION_SAME_FRAMES",
      "oracle_identity_exposed_to_predictors":False,
      "no_exam_feedback":True,"learned_physics":False,"real_world_transfer_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=152)
    p.add_argument("--episodes-each",type=int,default=250)
    p.add_argument("--beam-width",type=int,default=12)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.episodes_each,a.beam_width)
    print(json.dumps({k:v for k,v in r.items() if k!="per_condition"},indent=2))
    print("Détail:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
