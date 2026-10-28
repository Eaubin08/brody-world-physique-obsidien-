"""P165-D9 local epistemic arbitration and D6 diagnostic, experimental.

Local relevance does not imply evidence or unique physical identity.
"""
import argparse,json
from pathlib import Path
from .goal_multi_continuity_p165d7 import arbitrate,claim
from .reappearance_gate_p165d6 import infer,evaluate_tracks
from .hard_scene_angles_p165d2 import spec_from_index,draw
from .goal_track_bridge_p165d8 import evidence_from_inference

def local_view(goal,claims):
    global_view=arbitrate(goal,claims)
    focus=[c for c in global_view["retained_all_claims"] if c["id"] in global_view["focused"]]
    contradictions={x for c in focus for x in c["contradicts"]}
    contradictions.update(c["id"] for c in focus if c["contradicts"])
    for c in claims:
        if c["id"] in {x["id"] for x in focus}:continue
        if any(c["id"] in x["contradicts"] for x in focus):
            contradictions.add(c["id"])
    if not focus: local="HOLD_LOCAL_NO_RELEVANT_EVIDENCE"
    elif contradictions: local="MULTI_LOCAL"
    elif all(c["status"]=="UNKNOWN" for c in focus): local="HOLD_LOCAL_UNKNOWN"
    else:local="SUPPORTED_VIEW_NOT_PROOF"
    return {"goal":goal,"local_status":local,"global_status":global_view["status"],
            "focused_ids":[c["id"] for c in focus],"local_conflicts":sorted(contradictions),
            "retained_all_ids":[c["id"] for c in claims],"priority_promotes_truth":False,
            "unique_identity_proven":False}
def diagnose(frames,truth_eval_only,beam=8):
    result=infer(frames,beam)
    metrics=evaluate_tracks(result["raw"]["tracks"],truth_eval_only)
    views={g:local_view(g,evidence_from_inference(result)) for g in
           ("LOCATE","REIDENTIFY","RENDER","EXPLAIN_CAUSE","INTERPRET_SYMBOL")}
    # Truth ONLY used for diagnostics AFTER infer; causal attribution not proven.
    fail=not metrics["same_path_pre_post_recall"]
    hypotheses=result["raw"]["tracks"]
    post_candidates=any(any(path["xs"][i] is not None for i in (5,6)) for path in hypotheses)
    return {"failed_continuity":fail,"scores_eval_only":metrics,
            "local_views":views,"tracks_count":len(hypotheses),
            "post_candidate_present":post_candidates,
            "cause_established":False}
def run(out,seeds=2,limit=0,beam=8):
    if not(1<=seeds<=20 and 0<=limit<=675 and 2<=beam<=32):raise ValueError("INVALID_BOUNDS")
    count=675 if limit==0 else limit;p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    groups={};local_counts={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for i in range(count):
            spec=spec_from_index(i)
            for k in range(seeds):
                frames,truth=draw(spec,1009+104729*i+k)
                try:outcome=diagnose(frames,truth,beam)
                finally:
                    for im in frames:im.close()
                key=spec["motion"]+"/"+spec["occlusion"]
                d=groups.setdefault(key,{"n":0,"continuity_fail":0,"pre_fail":0,
                                         "post_fail":0,"old_four_pass_new_fail":0})
                m=outcome["scores_eval_only"];d["n"]+=1
                d["continuity_fail"]+=int(outcome["failed_continuity"])
                d["pre_fail"]+=int(not m["pre_visible_recall"])
                d["post_fail"]+=int(not m["post_reappearance_recall"])
                d["old_four_pass_new_fail"]+=int(m["topk_four_frame_recall"] and outcome["failed_continuity"])
                for name,v in outcome["local_views"].items():
                    k2=name+"/"+v["local_status"];local_counts[k2]=local_counts.get(k2,0)+1
                f.write(json.dumps({"fixture_eval_only":spec,"seed":k,
                    "result":outcome})+"\n")
    report={"schema":"BRODY_P165D9_LOCAL_STATUS_AND_FAILURE_DIAGNOSTIC",
            "conditions":count,"episodes":count*seeds,"groups":groups,
            "local_status_counts":local_counts,"goal_priorities_not_truth":True,
            "oracle_for_scoring_only":True,"physical_cause_inferred":False,
            "tracker_algorithm_changed":False,"continuity_improvement_claimed":False,
            "true_multisensor_connected":False,"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--seeds",type=int,default=2);p.add_argument("--limit",type=int,default=0)
    p.add_argument("--beam",type=int,default=8)
    a=p.parse_args();r=run(a.out,a.seeds,a.limit,a.beam)
    print(json.dumps({k:v for k,v in r.items() if k!="groups"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
