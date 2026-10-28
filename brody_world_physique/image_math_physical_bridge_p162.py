"""P162: time-indexed physical representation, reversible preview and P161 ablation.
Experimental read-only adapter; NOT a canonical F12/F16/MMonde integration.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random,time,statistics
from pathlib import Path
from PIL import Image,ImageDraw
from .image_hard_visual_ood_p161 import STYLES,TEST_LAWS,TRAIN_LAWS,positions,draw_frames,extract,fit_bank,predict as p161_predict

def features(xs):
    pairs=[(t,float(x)) for t,x in enumerate(xs) if x is not None]
    if len(pairs)<4:return {"status":"HOLD","reason":"VISIBILITY","positions":pairs}
    velocities=[(t,(xs[t]-xs[t-1])) for t in range(1,len(xs))
                if xs[t] is not None and xs[t-1] is not None]
    accelerations=[(t,xs[t]-2*xs[t-1]+xs[t-2]) for t in range(2,len(xs))
                   if all(xs[z] is not None for z in (t,t-1,t-2))]
    if len(velocities)<2:return {"status":"HOLD","reason":"MOTION_UNOBSERVED","positions":pairs}
    return {"status":"OK","positions":pairs,"velocity":velocities,
            "acceleration":accelerations,"last_velocity":velocities[-1][1],
            "median_abs_velocity":statistics.median(abs(v) for _,v in velocities),
            "direction_changes":sum(velocities[k][1]*velocities[k-1][1]<0
                                    for k in range(1,len(velocities))),
            "max_jump":max((abs(velocities[k][1]-velocities[k-1][1])
                             for k in range(1,len(velocities))),default=0.)}
def classify(f,threshold=.65):
    if f["status"]!="OK":return {"status":"HOLD","reason":f["reason"]}
    v=f["median_abs_velocity"];a=[x for _,x in f["acceleration"]]
    if f["direction_changes"]>0 or f["max_jump"]>=7:
        return {"status":"NOVELTY_CANDIDATE","reason":"UNSEEN_TEMPORAL_EVENT"}
    if not a:return {"status":"HOLD","reason":"NO_ACCELERATION"}
    ac=statistics.median(a)
    if abs(ac)>1.65:return {"status":"NOVELTY_CANDIDATE","reason":"UNSEEN_ACCELERATION"}
    if abs(ac)<.35:
        return {"status":"SELECT","selected":"still" if v<.75 else "linear"}
    if abs(ac+1)<threshold:return {"status":"SELECT","selected":"brake"}
    if abs(ac-1)<threshold:return {"status":"SELECT","selected":"boost"}
    return {"status":"HOLD","reason":"UNRESOLVED_DYNAMICS"}
def infer_velocity(xs):
    for i in range(len(xs)-1,0,-1):
        if xs[i] is not None and xs[i-1] is not None:
            return (xs[i],xs[i]-xs[i-1],i)
    return None
def predict_next(xs,f,cls):
    if cls["status"]!="SELECT":return None
    last=infer_velocity(xs)
    if last is None:return None
    x,v,t=last
    delta={"still":0.,"linear":0.,"brake":-1.,"boost":1.}[cls["selected"]]
    return x+v+delta
def render_projection(x,width=168,height=96):
    im=Image.new("RGB",(width,height),(235,233,225))
    if x is not None:
        d=ImageDraw.Draw(im);p=round(x)
        d.ellipse((p-6,42,p+6,54),fill=(220,45,55))
    return im
def reverse_check(x):
    if x is None:return None
    im=render_projection(x)
    recovered=extract([im])[0]
    im.close()
    return {"predicted_x":x,"reread_x":recovered,
            "reread_abs_error":abs(x-recovered) if recovered is not None else None}
def run(out,minutes=20,seed=162,exam_each=30):
    if not (2<=minutes<=90 and 10<=exam_each<=200):raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True)
    started=time.monotonic();deadline=started+minutes*60;rng=random.Random(seed+37)
    baseline=fit_bank(seed+11,35)
    (root/"FROZEN_P161_BASELINE.json").write_text(json.dumps(baseline,indent=2),encoding="utf8")
    results={};stop=False
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as journal:
        for style in STYLES:
            for law in TEST_LAWS:
                key=style+"/"+law
                m={"n":0,"new_correct_known":0,"new_wrong_known":0,"baseline_correct_known":0,
                   "baseline_wrong_known":0,"new_novelty_unknown":0,"new_select_unknown":0,
                   "baseline_select_unknown":0,"new_hold":0,"new_multi":0,
                   "perception_abs_sum":0.,"perception_pairs":0,"projection_abs_sum":0.,
                   "projection_scored":0,"reverse_abs_sum":0.,"reverse_scored":0}
                for case in range(exam_each):
                    if time.monotonic()>=deadline:stop=True;break
                    seq=positions(law,rng);imgs,truth,cam=draw_frames(seq,style,rng)
                    seen=extract(imgs);f=features(seen);ans=classify(f)
                    baseline_ans=p161_predict(seen,baseline)
                    projection=predict_next(seen,f,ans)
                    reverse=reverse_check(projection)
                    pairs=[(a,b) for a,b in zip(seen,truth) if a is not None]
                    m["perception_abs_sum"]+=sum(abs(a-b) for a,b in pairs);m["perception_pairs"]+=len(pairs)
                    m["n"]+=1
                    if law in TRAIN_LAWS:
                        m["new_correct_known"]+=int(ans["status"]=="SELECT" and ans.get("selected")==law)
                        m["new_wrong_known"]+=int(ans["status"]=="SELECT" and ans.get("selected")!=law)
                        m["baseline_correct_known"]+=int(baseline_ans["decision"]=="SELECT" and baseline_ans.get("selected")==law)
                        m["baseline_wrong_known"]+=int(baseline_ans["decision"]=="SELECT" and baseline_ans.get("selected")!=law)
                    else:
                        m["new_novelty_unknown"]+=int(ans["status"]=="NOVELTY_CANDIDATE")
                        m["new_select_unknown"]+=int(ans["status"]=="SELECT")
                        m["baseline_select_unknown"]+=int(baseline_ans["decision"]=="SELECT")
                    m["new_hold"]+=int(ans["status"]=="HOLD")
                    m["new_multi"]+=int(ans["status"]=="MULTI")
                    if projection is not None:
                        m["projection_abs_sum"]+=abs(projection-seq[7]) if style not in ("camera","combined") else abs(projection-(seq[7]+cam*7))
                        m["projection_scored"]+=1
                    if reverse is not None and reverse["reread_abs_error"] is not None:
                        m["reverse_abs_sum"]+=reverse["reread_abs_error"];m["reverse_scored"]+=1
                    journal.write(json.dumps({"cell":key,"case":case,"camera_truth_exam_only":cam,
                        "truth_law_exam_only":law,"observed_centers":seen,
                        "derived_state":f,"decision":ans,"baseline":baseline_ans,
                        "candidate_projection":projection,"reverse":reverse})+"\n")
                    for img in imgs:img.close()
                results[key]=m
                if stop:break
            if stop:break
    report={"schema":"BRODY_P162_MATH_PHYSICAL_REPRESENTATION_FIRST_BRIDGE",
     "cells_expected":len(STYLES)*len(TEST_LAWS),
     "cells_completed":sum(z["n"]==exam_each for z in results.values()),
     "episodes":sum(z["n"] for z in results.values()),
     "duration_seconds":round(time.monotonic()-started,3),
     "stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP","cells":results,
     "physical_state_has_position_velocity_acceleration_events":True,
     "reverse_projection_from_prediction":True,"real_f12_f16_runtime_connected":False,
     "camera_correction_connected":False,"world_generation_connected":False,
     "independent_physical_truth_proven":False,"model_params_frozen":True,
     "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20);p.add_argument("--seed",type=int,default=162)
    p.add_argument("--exam-each",type=int,default=30)
    a=p.parse_args();result=run(a.out,a.minutes,a.seed,a.exam_each)
    print(json.dumps({k:v for k,v in result.items() if k!="cells"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
