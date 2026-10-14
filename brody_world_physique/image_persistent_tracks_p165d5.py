"""P165-D5: image candidates to persistent multi-track hypotheses (synthetic lab).

Inference receives raster pixels only, no fixture labels nor truth positions.
Hypotheses are NOT proof of unique identity, true physics or camera cause.
"""
import argparse,json,math,time
from pathlib import Path
from .hard_scene_angles_p165d2 import spec_from_index,draw
from .color_agnostic_perception_p165d3 import detect_sequence

def associate(frames, beam_size=8):
    observations=detect_sequence(frames)
    paths=[{"xs":[],"last":None,"velocity":None,"score":0.0,"observed":0}]
    for t,spots in enumerate(observations):
        successors=[]
        for path in paths:
            last=path["last"];v=path["velocity"]
            guess=None if last is None else last+(v if v is not None else 0.)
            # Include missing-data branch; avoid inventing ground-truth positions.
            options=[None]+spots
            for item in options:
                h={"xs":path["xs"][:],"last":last,"velocity":v,
                   "score":path["score"],"observed":path["observed"]}
                if item is None:
                    h["xs"].append(None);h["score"]+=8.
                else:
                    x=item["x"]
                    if guess is not None:
                        h["score"]+=min(abs(x-guess),60.)
                    h["score"]+=max(0,30-item["size"])/20.
                    if last is not None:h["velocity"]=x-last
                    h["last"]=x;h["xs"].append(x);h["observed"]+=1
                successors.append(h)
        # Retain distinct histories, rather than the highest-scoring duplicate.
        dedup={}
        for h in sorted(successors,key=lambda p:(p["score"],-p["observed"])):
            key=tuple(None if x is None else round(x,1) for x in h["xs"])
            if key not in dedup:dedup[key]=h
            if len(dedup)>=beam_size:break
        paths=list(dedup.values())
    return {"tracks":paths,"candidate_counts":[len(s) for s in observations],
            "uses_fixture_labels":False,"uses_oracle":False}

def adjudicate(result):
    tracks=result["tracks"];counts=result["candidate_counts"]
    if not tracks:return {"status":"HOLD","reason":"NO_TRACK"}
    valid=[p for p in tracks if p["observed"]>=4]
    if not valid:return {"status":"HOLD","reason":"LOW_COVERAGE"}
    if any(n>1 for n in counts):
        status="MULTI";reason="MULTIPLE_ASSOCIATION_HYPOTHESES"
    elif any(n==0 for n in counts):
        status="MULTI";reason="OCCLUSION_GAP"
    else:
        status="CANDIDATE";reason="VISIBLE_PATH_NOT_IDENTITY_PROOF"
    return {"status":status,"reason":reason,
            "best_path":valid[0]["xs"],"hypothesis_count":len(valid),
            "unique_identity_proven":False}

def run(out,seeds=2,limit=0,beam=8):
    if not(1<=seeds<=20 and 0<=limit<=675 and 2<=beam<=32):
        raise ValueError("INVALID_BOUNDS")
    total=675 if limit==0 else limit;p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True);start=time.monotonic();groups={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for j in range(total):
            spec=spec_from_index(j)
            for seed in range(seeds):
                images,truth=draw(spec,1009+104729*j+seed)
                try:result=associate(images,beam)
                finally:
                    for im in images:im.close()
                decision=adjudicate(result)
                name=spec["appearance"]+"/"+spec["occlusion"]
                m=groups.setdefault(name,{"n":0,"holds":0,"multis":0,
                                          "candidates":0,"topk_truth_recall":0,
                                          "top1_position_error_sum":0.,
                                          "top1_position_pairs":0})
                m["n"]+=1
                m["holds"]+=int(decision["status"]=="HOLD")
                m["multis"]+=int(decision["status"]=="MULTI")
                m["candidates"]+=int(decision["status"]=="CANDIDATE")
                # Scoring ONLY: do not pass truth to inferencer.
                best=result["tracks"][0]["xs"]
                pairs=[(x,y) for x,y in zip(best,truth) if x is not None]
                m["top1_position_error_sum"]+=sum(abs(x-y) for x,y in pairs)
                m["top1_position_pairs"]+=len(pairs)
                recall=any(sum(x is not None and abs(x-y)<=6 for x,y in zip(tr["xs"],truth))>=4
                           for tr in result["tracks"])
                m["topk_truth_recall"]+=int(recall)
                f.write(json.dumps({"spec":spec,"seed":seed,"decision":decision,
                                    "tracks":result["tracks"],"truth_exam_only":truth})+"\n")
    report={"schema":"BRODY_P165D5_IMAGE_TO_PERSISTENT_HYPOTHESES",
            "conditions":total,"episodes":total*seeds,"run_complete":total==675,
            "beam_size":beam,"groups":groups,
            "inference_receives_truth":False,"inference_receives_fixture_labels":False,
            "track_positions_persist_across_frames":True,
            "true_identity_established":False,
            "camera_and_scene_graph_connected":False,
            "physical_event_causality_proven":False,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY",
            "duration_seconds":round(time.monotonic()-start,3)}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    a=argparse.ArgumentParser();a.add_argument("--out",required=True)
    a.add_argument("--seeds",type=int,default=2)
    a.add_argument("--limit",type=int,default=0)
    a.add_argument("--beam",type=int,default=8)
    q=a.parse_args();d=run(q.out,q.seeds,q.limit,q.beam)
    print(json.dumps({k:v for k,v in d.items() if k!="groups"},indent=2))
    print("Report:",str(Path(q.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
