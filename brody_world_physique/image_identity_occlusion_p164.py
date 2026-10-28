"""P164: multi-hypothesis identity tracking with occlusion replay.
Experimental synthetic pixels; no semantic identity or physical proof.
"""
import argparse,json,random,time,statistics,math
from pathlib import Path
from .image_hard_visual_ood_p161 import STYLES,TEST_LAWS,TRAIN_LAWS,positions,draw_frames,extract
from .image_camera_occlusion_gate_p163 import annotate_fiducials,camera_evidence,normalize,decide
from .image_math_physical_bridge_p162 import features,classify

def candidates(im):
    p=im.load();seen=set();groups=[]
    # Segment candidate saturated pixels in object band. Connected components
    # prevent distant distractors from shifting a global median.
    for y in range(26,70):
        for x in range(168):
            if (x,y) in seen:continue
            r,g,b=p[x,y]
            if not (r>170 and r>g+45 and r>b+30):continue
            stack=[(x,y)];seen.add((x,y));points=[]
            while stack:
                xx,yy=stack.pop();points.append((xx,yy))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=xx+dx,yy+dy
                    if not (0<=nx<168 and 26<=ny<70) or (nx,ny) in seen:continue
                    rr,gg,bb=p[nx,ny]
                    if rr>170 and rr>gg+45 and rr>bb+30:
                        seen.add((nx,ny));stack.append((nx,ny))
            if len(points)>=18:
                center=statistics.median(x for x,_ in points)
                cy=statistics.median(y for _,y in points)
                groups.append((float(center),float(cy),len(points)))
    return sorted(groups,key=lambda a:-a[2])[:8]

def track(frames,offsets=None,beam=4):
    sets=[]
    for im in frames:
        sets.append(candidates(im))
    paths=[{"xs":[],"score":0.,"last":None,"vx":0.,"missing":0}]
    for t,cs in enumerate(sets):
        proposals=[]
        for h in paths:
            # Only use a short, observed history; uncertainty increases on gap.
            predicted=None if h["last"] is None else h["last"]+h["vx"]
            for cx,cy,area in cs:
                x=cx-(offsets[t] if offsets is not None else 0.)
                if predicted is not None and abs(x-predicted)>max(10.,6.+5*h["missing"]):continue
                penalty=0 if predicted is None else abs(x-predicted)
                if abs(cy-48)>9:penalty+=18
                penalty+=max(0,45-area)*.12
                old=h["last"]
                vel=(x-old) if old is not None and h["missing"]==0 else h["vx"]
                proposals.append({"xs":h["xs"]+[x],"score":h["score"]+penalty,
                    "last":x,"vx":vel,"missing":0})
            # Never fill missing images with fabricated observations.
            proposals.append({"xs":h["xs"]+[None],"score":h["score"]+12.,
                "last":h["last"],"vx":h["vx"],"missing":h["missing"]+1})
        proposals.sort(key=lambda h:(h["score"],-sum(v is not None for v in h["xs"])))
        paths=proposals[:beam]
    return paths

def decision(paths):
    if not paths:return {"status":"HOLD","reason":"NO_TRACK"}
    best=paths[0];xs=best["xs"]
    if sum(v is None for v in xs)>2:return {"status":"HOLD","reason":"LOW_COVERAGE"}
    if any(v is None for v in xs[3:6]):
        # Reappearance constrains hypotheses but hidden change is unidentifiable.
        alternatives=[]
        for h in paths:
            f=features(h["xs"])
            if f["status"]=="OK":alternatives.append(classify(f))
        consistent={a.get("selected") for a in alternatives if a["status"]=="SELECT"}
        return {"status":"MULTI" if consistent else "HOLD",
                "reason":"HIDDEN_EVENT_UNRESOLVED","hypotheses":sorted(consistent)}
    return classify(features(xs))

def run(out,minutes=20,seed=164,exam_each=30):
    if not (2<=minutes<=90 and 10<=exam_each<=200):raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);start=time.monotonic();rng=random.Random(seed+37)
    deadline=start+60*minutes;summary={};cut=False
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as outlog:
        for style in STYLES:
            for law in TEST_LAWS:
                row={"n":0,"correct_known":0,"false_known":0,"unknown_select":0,
                     "unknown_novelty":0,"unknown_hold":0,"HOLD":0,"MULTI":0,
                     "baseline_correct":0,"baseline_false":0,
                     "tracked_mae_sum":0.,"tracked_pairs":0,"identity_track_coverage":0,
                     "occluded_hypothesis_cases":0}
                for i in range(exam_each):
                    if time.monotonic()>=deadline:cut=True;break
                    x=positions(law,rng);raw,truth,cam_true=draw_frames(x,style,rng)
                    imgs=annotate_fiducials(raw,style,cam_true)
                    for im in raw:im.close()
                    offsets=camera_evidence(imgs)
                    raw_centers=extract(imgs)
                    baseline=decide(normalize(raw_centers,offsets)["xs"],
                                    normalize(raw_centers,offsets)["status"])
                    paths=track(imgs,offsets=offsets)
                    answer=decision(paths)
                    best=paths[0]["xs"] if paths else [None]*7
                    pairs=[(a,b) for a,b in zip(best,x[:7]) if a is not None]
                    row["tracked_mae_sum"]+=sum(abs(a-b) for a,b in pairs)
                    row["tracked_pairs"]+=len(pairs)
                    row["identity_track_coverage"]+=int(len(pairs)>=5)
                    row["n"]+=1
                    row["HOLD"]+=int(answer["status"]=="HOLD")
                    row["MULTI"]+=int(answer["status"]=="MULTI")
                    row["occluded_hypothesis_cases"]+=int(answer.get("reason")=="HIDDEN_EVENT_UNRESOLVED")
                    if law in TRAIN_LAWS:
                        row["correct_known"]+=int(answer["status"]=="SELECT" and answer.get("selected")==law)
                        row["false_known"]+=int(answer["status"]=="SELECT" and answer.get("selected")!=law)
                        row["baseline_correct"]+=int(baseline["status"]=="SELECT" and baseline.get("selected")==law)
                        row["baseline_false"]+=int(baseline["status"]=="SELECT" and baseline.get("selected")!=law)
                    else:
                        row["unknown_select"]+=int(answer["status"]=="SELECT")
                        row["unknown_novelty"]+=int(answer["status"]=="NOVELTY_CANDIDATE")
                        row["unknown_hold"]+=int(answer["status"]=="HOLD")
                    outlog.write(json.dumps({"cell":style+"/"+law,"case":i,
                         "truth_exam_only":x[:7],"camera_exam_only":cam_true,
                         "pixel_track_candidates":paths,"camera_evidence":offsets,
                         "answer":answer,"p163_baseline":baseline})+"\n")
                    for im in imgs:im.close()
                summary[style+"/"+law]=row
                if cut:break
            if cut:break
    report={"schema":"BRODY_P164_IDENTITY_OCCLUSION_HYPOTHESES",
      "cells_expected":len(STYLES)*len(TEST_LAWS),
      "cells_completed":sum(z["n"]==exam_each for z in summary.values()),
      "episodes":sum(z["n"] for z in summary.values()),
      "duration_seconds":round(time.monotonic()-start,3),
      "stopped_by":"TIME_BUDGET" if cut else "EXAM_CAP",
      "cells":summary,"pixel_connected_components":True,
      "multi_hypothesis_tracking":True,"reappearance_verified_as_unique_identity":False,
      "occluded_event_recovered_as_physical_truth":False,
      "real_f12_f16_runtime_connected":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20);p.add_argument("--seed",type=int,default=164)
    p.add_argument("--exam-each",type=int,default=30)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.exam_each)
    print(json.dumps({k:v for k,v in r.items() if k!="cells"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
