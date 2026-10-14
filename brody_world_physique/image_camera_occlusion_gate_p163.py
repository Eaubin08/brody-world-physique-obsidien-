"""P163 camera/frame and occlusion integrity gate; paired P162.
A readable deterministic lab fixture, not actual canonical F12/F16 integration.
"""
import argparse,json,random,time,statistics
from pathlib import Path
from PIL import Image,ImageDraw
from .image_hard_visual_ood_p161 import STYLES,TEST_LAWS,TRAIN_LAWS,positions,draw_frames,extract
from .image_math_physical_bridge_p162 import features,classify as p162_classify,predict_next as p162_next
def camera_evidence(frames):
    # Infer common background motion from three unchanging fiducials in a
    # dedicated canvas margin, without using simulator camera truth.
    # Existing P161 renders no fiducials: absence must trigger HOLD, not oracle.
    offsets=[]
    for im in frames:
        pix=im.load();xs=[]
        for x in range(168):
            r,g,b=pix[x,13]
            if 30<r<90 and g>155 and b<110:xs.append(x)
        offsets.append(statistics.median(xs) if xs else None)
    if len(offsets)<3 or offsets[0] is None or any(v is None for v in offsets):
        return None
    return [v-offsets[0] for v in offsets]
def annotate_fiducials(frames,style,camera):
    # P163 fixture version: background landmarks move with the camera. Unlike
    # P161, background geometry now makes the camera shift observable.
    out=[]
    for t,im in enumerate(frames):
        cp=im.copy()
        shift=camera*t if style in ("camera","combined") else 0
        d=ImageDraw.Draw(cp)
        for base in (12,92,148):
            x=round(base+shift)
            if 0<=x<168:d.rectangle((x-1,11,x+1,15),fill=(54,190,65))
        out.append(cp)
    return out
def normalize(xs,cam):
    if cam is None:return {"status":"UNOBSERVABLE_FRAME","xs":xs}
    return {"status":"FRAME_ESTIMATED","xs":[(x-shift if x is not None else None)
                                           for x,shift in zip(xs,cam)]}
def track_gate(xs):
    # Gaps cannot be silently interpolated across a discontinuous event.
    missing=[i for i,x in enumerate(xs) if x is None]
    if not missing:return {"status":"COMPLETE"}
    if any(3<=i<=5 for i in missing):
        return {"status":"HOLD","reason":"EVENT_MAY_BE_HIDDEN","missing":missing}
    return {"status":"HOLD","reason":"INCOMPLETE_TRACK","missing":missing}
def decide(xs,frame_status):
    if frame_status!="FRAME_ESTIMATED":
        return {"status":"HOLD","reason":"UNOBSERVABLE_CAMERA_FRAME"}
    gate=track_gate(xs)
    if gate["status"]!="COMPLETE":return {"status":"HOLD","reason":gate["reason"]}
    return p162_classify(features(xs))
def future_projection(xs,answer):
    if answer["status"]!="SELECT":return None
    return p162_next(xs,features(xs),answer)
def run(out,minutes=20,seed=163,exam_each=30):
    if not (2<=minutes<=90 and 10<=exam_each<=200):raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);start=time.monotonic();deadline=start+minutes*60
    rng=random.Random(seed+37);results={};stop=False
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as evidence:
        for style in STYLES:
            for law in TEST_LAWS:
                row={"n":0,"correct_known":0,"false_known":0,"unknown_select":0,
                     "unknown_novelty":0,"unknown_hold":0,"HOLD":0,
                     "frame_observed":0,"occlusion_hold":0,
                     "paired_p162_correct":0,"paired_p162_false":0,
                     "projection_scored":0,"projection_abs_sum":0.,
                     "perception_abs_sum":0.,"perception_pairs":0}
                for case in range(exam_each):
                    if time.monotonic()>=deadline:stop=True;break
                    xs=positions(law,rng);raw,truth,sim_camera=draw_frames(xs,style,rng)
                    frames=annotate_fiducials(raw,style,sim_camera)
                    for im in raw:im.close()
                    seen=extract(frames);cam=camera_evidence(frames)
                    aligned=normalize(seen,cam)
                    answer=decide(aligned["xs"],aligned["status"])
                    baseline=p162_classify(features(seen))
                    projection=future_projection(aligned["xs"],answer)
                    row["n"]+=1;row["frame_observed"]+=int(cam is not None)
                    row["occlusion_hold"]+=int(answer.get("reason")=="EVENT_MAY_BE_HIDDEN")
                    row["HOLD"]+=int(answer["status"]=="HOLD")
                    pairs=[(p,t) for p,t in zip(seen,truth) if p is not None]
                    row["perception_abs_sum"]+=sum(abs(p-t) for p,t in pairs)
                    row["perception_pairs"]+=len(pairs)
                    if law in TRAIN_LAWS:
                        row["correct_known"]+=int(answer["status"]=="SELECT" and answer.get("selected")==law)
                        row["false_known"]+=int(answer["status"]=="SELECT" and answer.get("selected")!=law)
                        row["paired_p162_correct"]+=int(baseline["status"]=="SELECT" and baseline.get("selected")==law)
                        row["paired_p162_false"]+=int(baseline["status"]=="SELECT" and baseline.get("selected")!=law)
                    else:
                        row["unknown_select"]+=int(answer["status"]=="SELECT")
                        row["unknown_novelty"]+=int(answer["status"]=="NOVELTY_CANDIDATE")
                        row["unknown_hold"]+=int(answer["status"]=="HOLD")
                    if projection is not None:
                        row["projection_scored"]+=1;row["projection_abs_sum"]+=abs(projection-xs[7])
                    evidence.write(json.dumps({"style":style,"episode":case,"law_exam_only":law,
                        "camera_truth_exam_only":sim_camera,"pixel_measurements":seen,
                        "camera_estimate":cam,"aligned":aligned,"answer":answer,
                        "p162_baseline":baseline,"future_candidate":projection,
                        "heldout_future_exam_only":xs[7]})+"\n")
                    for im in frames:im.close()
                results[style+"/"+law]=row
                if stop:break
            if stop:break
    report={"schema":"BRODY_P163_CAMERA_OCCLUSION_GATE",
      "cells_expected":len(STYLES)*len(TEST_LAWS),
      "cells_completed":sum(v["n"]==exam_each for v in results.values()),
      "episodes":sum(v["n"] for v in results.values()),
      "duration_seconds":round(time.monotonic()-start,3),
      "stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP","cells":results,
      "frame_estimation_uses_pixels_only":True,
      "occluded_critical_event_fails_closed":True,
      "p162_baseline_uses_same_annotated_images":True,
      "fixture_has_programmed_fiducials":True,
      "natural_scene_camera_reconstruction_proven":False,
      "real_f12_f16_runtime_connected":False,
      "real_image_generator_connected":False,
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20)
    p.add_argument("--seed",type=int,default=163);p.add_argument("--exam-each",type=int,default=30)
    a=p.parse_args();report=run(a.out,a.minutes,a.seed,a.exam_each)
    print(json.dumps({k:v for k,v in report.items() if k!="cells"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
