"""P165-D8: D6 raster hypotheses to D7 goal-conditioned evidence views.
No scenario label/truth to inference. Priority never changes sensor evidence.
"""
import argparse,hashlib,json
from pathlib import Path
from .hard_scene_angles_p165d2 import draw,spec_from_index
from .reappearance_gate_p165d6 import infer,evaluate_tracks
from .goal_multi_continuity_p165d7 import claim,arbitrate

GOALS=("LOCATE","REIDENTIFY","RENDER","EXPLAIN_CAUSE","PREDICT","INTERPRET_SYMBOL")
def evidence_from_inference(d6):
    raw=d6["raw"]; paths=raw["tracks"]; states=d6["persistent_hypotheses"]
    counts=raw["candidate_counts"]
    claims=[claim("visible_candidates","spatial","OBSERVED",
                  "Detected component counts per frame: "+repr(counts),
                  "P165D3_IMAGE_DETECTOR")]
    if paths:
        best=paths[0]
        claims.append(claim("track_0","temporal","INFERRED",
                            "Candidate path "+repr(best["xs"]),
                            "P165D6_ASSOCIATION"))
        st=states[0]["state"]
        claims.append(claim("persist_0","physical","PREDICTED" if st["mode"]=="PREDICTED" else "INFERRED",
                            "Synthetic 1D candidate state "+repr(st["position"]),
                            "P165D4_ADAPTER"))
        if len(paths)>1:
            claims.append(claim("alternative_tracks","identity","UNKNOWN",
                                str(len(paths))+" mutually unverified path hypotheses",
                                "P165D6_BEAM",contradicts=("track_0",)))
    claims.append(claim("unknown_cause","causal","UNKNOWN",
                         "Visibility or association cause is not established",
                         "P165D6_LIMIT"))
    # Symbolism requires user evidence; no synthetic interpretation fabricated.
    return claims
def views_from_frames(frames,beam=8):
    d6=infer(frames,beam=beam)
    ev=evidence_from_inference(d6)
    digest=hashlib.sha256(json.dumps(ev,sort_keys=True).encode()).hexdigest()
    views={g:arbitrate(g,ev) for g in GOALS}
    return {"digest":digest,"claims":ev,"views":views,"d6":d6,
            "unchanged_under_goals":all(hashlib.sha256(json.dumps(ev,sort_keys=True).encode()).hexdigest()==digest for g in GOALS)}
def run(out,seeds=2,limit=0,beam=8):
    if not(1<=seeds<=20 and 0<=limit<=675 and 2<=beam<=32):raise ValueError("INVALID_BOUNDS")
    count=675 if not limit else limit;root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True)
    summary={"cases":0,"stable_across_goals":0,"different_goal_focus":0,
             "continuity_failure":0,"continuity_success":0,"symbolic_hold":0}
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for i in range(count):
            spec=spec_from_index(i)
            for seed in range(seeds):
                frames,truth=draw(spec,1009+104729*i+seed)
                try:r=views_from_frames(frames,beam=beam)
                finally:
                    for im in frames:im.close()
                score=evaluate_tracks(r["d6"]["raw"]["tracks"],truth)
                relevant={g:v["focused"] for g,v in r["views"].items()}
                summary["cases"]+=1
                summary["stable_across_goals"]+=int(r["unchanged_under_goals"])
                summary["different_goal_focus"]+=int(relevant["LOCATE"]!=relevant["REIDENTIFY"])
                summary["continuity_failure"]+=int(not score["same_path_pre_post_recall"])
                summary["continuity_success"]+=int(score["same_path_pre_post_recall"])
                summary["symbolic_hold"]+=int(r["views"]["INTERPRET_SYMBOL"]["status"]=="HOLD")
                f.write(json.dumps({"fixture_only_for_evaluation":spec,"seed":seed,"evidence_digest":r["digest"],
                   "claims":r["claims"],"views":{g:{"focus":v["focused"],"status":v["status"],
                      "contradictions":v["contradiction_ids"]} for g,v in r["views"].items()},
                   "d6_verdict":r["d6"]["verdict"],"reappearance_eval_only":score})+"\n")
    report={"schema":"BRODY_P165D8_D6_D7_BRIDGE","conditions":count,"episodes":count*seeds,
        "summary":summary,"fixture_labels_to_inference":False,
        "physical_state_mutated_by_goal":False,"semantic_goal_parsing_connected":False,
        "symbolic_claim_fabrication":False,"continuity_improvement_claimed":False,
        "real_multimodal_sensors_connected":False,
        "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);p.add_argument("--seeds",type=int,default=2)
    p.add_argument("--limit",type=int,default=0);p.add_argument("--beam",type=int,default=8)
    a=p.parse_args();print(json.dumps(run(a.out,a.seeds,a.limit,a.beam),indent=2))
if __name__=="__main__":main()
