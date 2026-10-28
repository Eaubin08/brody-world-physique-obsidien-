"""P165-D3: color-agnostic candidate detection, non-oracle evaluation on D2 suite.
Designed for PIL synthetic laboratory. No semantic recognition or identity proof.
"""
import argparse,json,math,time
from pathlib import Path
from .hard_scene_angles_p165d2 import spec_from_index,draw
from .image_identity_occlusion_p164 import candidates as red_candidates

def components(image):
    im=image.convert("RGB"); w,h=im.size; pix=im.load()
    # Contrast to neighboring horizontal background rather than a fixed RGB.
    # Only saturated chromatic components are accepted; green scene landmarks
    # are filtered by the restricted test-object y-band.
    mask=set()
    for y in range(38,min(60,h)):
        for x in range(w):
            r,g,b=pix[x,y]
            chroma=max(r,g,b)-min(r,g,b)
            if chroma>=65 and max(r,g,b)>=110:
                mask.add((x,y))
    found=[]
    while mask:
        seed=mask.pop(); stack=[seed];cluster=[seed]
        while stack:
            x,y=stack.pop()
            for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if p in mask:
                    mask.remove(p);stack.append(p);cluster.append(p)
        if len(cluster)>=14:
            xs=[p[0] for p in cluster];ys=[p[1] for p in cluster]
            found.append({"x":sum(xs)/len(xs),"y":sum(ys)/len(ys),
                          "size":len(xs)})
    return sorted(found,key=lambda v:(v["x"],v["y"]))

def detect_sequence(frames):
    return [components(im) for im in frames]

def ambiguity_and_motion(sequence):
    counts=[len(x) for x in sequence]
    # This model keeps all candidates and explicitly refuses ID proof.
    jumps=[]; unique=[(i,s[0]["x"]) for i,s in enumerate(sequence) if len(s)==1]
    for (a,x),(b,y) in zip(unique,unique[1:]):
        if b==a+1 and abs(y-x)>15:jumps.append(b)
    status="NOVELTY_CANDIDATE" if jumps else ("MULTI" if any(n>1 for n in counts)
                                             else "HOLD")
    return {"status":status,"candidates":sequence,"visible_jumps":jumps,
            "unique_identity_proven":False,"camera_cause_proven":False}

def run(out,seeds=2,limit=0):
    if not(1<=seeds<=20 and 0<=limit<=675):raise ValueError("INVALID_BOUNDS")
    n=675 if limit==0 else limit;root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True)
    start=time.monotonic();group={};globalstats={"count":0,"truth_frames":0,
          "recall_frames":0,"false_candidates":0,"pixel_abs_sum":0.,
          "pixel_pairs":0,"old_pixel_abs_sum":0.,"old_pixel_pairs":0}
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for j in range(n):
            spec=spec_from_index(j)
            for k in range(seeds):
                frames,truth=draw(spec,1009+104729*j+k)
                try:
                    new=ambiguity_and_motion(detect_sequence(frames))
                    old=[red_candidates(im) for im in frames]
                finally:
                    for im in frames:im.close()
                key=spec["appearance"]+"/"+spec["occlusion"]
                stats=group.setdefault(key,{"exams":0,"truth_frames":0,
                   "recall_frames":0,"false_candidates":0,
                   "pixel_abs_sum":0.,"pixel_pairs":0,
                   "old_pixel_abs_sum":0.,"old_pixel_pairs":0})
                stats["exams"]+=1
                for t,xtrue in enumerate(truth):
                    detected=new["candidates"][t]
                    matched=[d for d in detected if abs(d["x"]-xtrue)<=6]
                    oldmatched=[d for d in old[t] if abs(d[0]-xtrue)<=6]
                    # Under occultation true object not necessarily visible.
                    # Metrics are raw localization/proximity and NOT true
                    # physical object visibility recall.
                    stats["truth_frames"]+=1
                    stats["recall_frames"]+=int(bool(matched))
                    stats["false_candidates"]+=sum(abs(d["x"]-xtrue)>6 for d in detected)
                    if detected:
                        stats["pixel_abs_sum"]+=min(abs(d["x"]-xtrue) for d in detected)
                        stats["pixel_pairs"]+=1
                    if old[t]:
                        stats["old_pixel_abs_sum"]+=min(abs(d[0]-xtrue) for d in old[t])
                        stats["old_pixel_pairs"]+=1
                f.write(json.dumps({"spec":spec,"seed":k,"new":new,
                       "old":old,"truth_exam_only":truth})+"\n")
    for key,stats in group.items():
        for metric in globalstats:
            if metric=="count":continue
            globalstats[metric]+=stats.get(metric,0)
        globalstats["count"]+=stats["exams"]
    report={"schema":"BRODY_P165D3_CHROMATIC_PERCEPTION_LAB",
        "conditions":n,"exams":n*seeds,"run_complete":n==675,
        "groups":group,"overall":globalstats,
        "inference_receives_oracle":False,
        "uses_y_band_prior":True,
        "ground_truth_visibility_available":False,
        "identity_tracking_integrated":False,
        "true_3d_or_scene_graph_integrated":False,
        "real_multisensor_input_connected":False,
        "historical_77_not_replayed":True,
        "runtime_seconds":round(time.monotonic()-start,3),
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--seeds",type=int,default=2)
    p.add_argument("--limit",type=int,default=0)
    a=p.parse_args();r=run(a.out,a.seeds,a.limit)
    print(json.dumps({k:v for k,v in r.items() if k!="groups"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
