"""P165-D6: reappearance auditing of multi-track hypotheses.

All ground truth is evaluation-only. No fabricated certainty of identity.
"""
import argparse,json,time
from pathlib import Path
from .hard_scene_angles_p165d2 import spec_from_index,draw
from .image_persistent_tracks_p165d5 import associate,adjudicate,state_from_path

def evaluate_tracks(tracks,truth,threshold=6):
    # Seven frames, gap at indices 3-4 in full-occlusion fixtures.
    def score(p):
        xs=p["xs"]
        before=sum(xs[i] is not None and abs(xs[i]-truth[i])<=threshold for i in (0,1,2))
        after=sum(xs[i] is not None and abs(xs[i]-truth[i])<=threshold for i in (5,6))
        return before,after
    ranked=[score(t) for t in tracks]
    pre=any(a>=2 for a,b in ranked)
    post=any(b>=2 for a,b in ranked)
    same=any(a>=2 and b>=2 for a,b in ranked)
    return {"pre_visible_recall":pre,"post_reappearance_recall":post,
            "same_path_pre_post_recall":same,
            "topk_four_frame_recall":any(sum(x is not None and abs(x-y)<=threshold for x,y in zip(t["xs"],truth))>=4 for t in tracks),
            "oracle_for_scoring_only":True}

def infer(frames,beam=8):
    raw=associate(frames,beam)
    verdict=adjudicate(raw)
    states=[state_from_path(path["xs"]) for path in raw["tracks"]]
    return {"raw":raw,"verdict":verdict,"persistent_hypotheses":states,
            "unique_identity_proven":False,"fixture_label_used":False}

def run(out,seeds=2,limit=0,beam=8):
    if not(1<=seeds<=20 and 0<=limit<=675 and 2<=beam<=32):raise ValueError("INVALID_BOUNDS")
    total=675 if not limit else limit;p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True);start=time.monotonic();groups={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for j in range(total):
            spec=spec_from_index(j)
            for k in range(seeds):
                frames,truth=draw(spec,1009+104729*j+k)
                try:result=infer(frames,beam)
                finally:
                    for im in frames:im.close()
                scores=evaluate_tracks(result["raw"]["tracks"],truth)
                key=spec["appearance"]+"/"+spec["occlusion"]
                g=groups.setdefault(key,{"n":0,"pre_recall":0,"post_recall":0,
                    "same_path_pre_post":0,"topk_four_recall":0,"hypotheses_sum":0,
                    "HOLD":0,"MULTI":0,"CANDIDATE":0})
                g["n"]+=1
                g["pre_recall"]+=int(scores["pre_visible_recall"])
                g["post_recall"]+=int(scores["post_reappearance_recall"])
                g["same_path_pre_post"]+=int(scores["same_path_pre_post_recall"])
                g["topk_four_recall"]+=int(scores["topk_four_frame_recall"])
                g["hypotheses_sum"]+=len(result["persistent_hypotheses"])
                g[result["verdict"]["status"]]+=1
                f.write(json.dumps({"fixture_eval_only":spec,"seed":k,"scores":scores,
                    "verdict":result["verdict"],"tracks":result["raw"]["tracks"],
                    "persistent_hypotheses":result["persistent_hypotheses"],
                    "truth_eval_only":truth})+"\n")
    report={"schema":"BRODY_P165D6_REAPPEARANCE_GATE","conditions":total,
            "episodes":total*seeds,"full_matrix_complete":total==675,
            "beam_size":beam,"groups":groups,"all_tracks_propagated_to_d4":True,
            "reappearance_identity_proven":False,
            "metrics_use_hidden_oracle_only_after_inference":True,
            "camera_scene_graph_and_rf_sensors_connected":False,
            "real_physical_causality_proven":False,
            "runtime_seconds":round(time.monotonic()-start,3),
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out",required=True)
    a.add_argument("--seeds",type=int,default=2)
    a.add_argument("--beam",type=int,default=8)
    a.add_argument("--limit",type=int,default=0)
    v=a.parse_args();data=run(v.out,v.seeds,v.limit,v.beam)
    print(json.dumps({k:v for k,v in data.items() if k!="groups"},indent=2))
    print("Report:",str(Path(v.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
