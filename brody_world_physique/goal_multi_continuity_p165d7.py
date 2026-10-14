"""P165-D7: goal-conditioned multi-continuity epistemic arbitration.

Read-only decision-support on declared evidence; NOT discovery of physical truth.
"""
import argparse,json
from pathlib import Path

CONTINUITIES=("physical","temporal","spatial","identity","causal","experiential","symbolic","conceptual")
GOALS={
 "LOCATE":("spatial","physical","temporal"),
 "REIDENTIFY":("identity","temporal","experiential"),
 "EXPLAIN_CAUSE":("causal","physical","temporal"),
 "PREDICT":("physical","temporal","causal"),
 "RENDER":("spatial","physical","conceptual"),
 "INTERPRET_SYMBOL":("symbolic","conceptual","experiential"),
 "EXPLORE":CONTINUITIES,
}
STATUS=("OBSERVED","INFERRED","PREDICTED","INTERPRETED","UNKNOWN")
def claim(identifier,continuity,status,statement,source,confidence=None,contradicts=()):
    if continuity not in CONTINUITIES or status not in STATUS:raise ValueError("INVALID_CLAIM")
    if not identifier or not statement or not source:raise ValueError("EMPTY_PROVENANCE")
    if confidence is not None and not (0<=confidence<=1):raise ValueError("INVALID_CONFIDENCE")
    return {"id":identifier,"continuity":continuity,"status":status,
            "statement":statement,"source":source,"confidence":confidence,
            "contradicts":list(contradicts)}
def arbitrate(goal,claims):
    if goal not in GOALS:raise ValueError("UNREGISTERED_GOAL")
    if len({c["id"] for c in claims})!=len(claims):raise ValueError("DUPLICATE_ID")
    for c in claims:
        if c["continuity"] not in CONTINUITIES or c["status"] not in STATUS or not c["source"]:
            raise ValueError("INVALID_EVIDENCE")
    priority=GOALS[goal]
    def order(c):
        return (priority.index(c["continuity"]) if c["continuity"] in priority else len(priority),
                {"OBSERVED":0,"INFERRED":1,"PREDICTED":2,"INTERPRETED":3,"UNKNOWN":4}[c["status"]],
                c["id"])
    ranked=sorted(claims,key=order)
    selected=[c["id"] for c in ranked if c["continuity"] in priority]
    contradiction_ids=sorted({x for c in claims for x in c["contradicts"]}|{c["id"] for c in claims if c["contradicts"]})
    unresolved=bool(contradiction_ids) or not selected
    return {"goal":goal,"priority":list(priority),"relevance_order":[c["id"] for c in ranked],
      "focused":selected,"retained_all_claims":ranked,"contradiction_ids":contradiction_ids,
      "status":"MULTI" if contradiction_ids else ("HOLD" if not selected else "CONTEXTUAL_VIEW"),
      "epistemically_resolved":False,"unresolved":unresolved,
      "priority_is_evidence":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
def fixtures():
    return [
     claim("seen","spatial","OBSERVED","Object detected at x=14","SIMULATED_IMAGE"),
     claim("predicted","temporal","PREDICTED","Object may move behind obstacle","MODEL_1D",.5,("alternative",)),
     claim("alternative","identity","UNKNOWN","Reappeared object may be another entity","ASSOCIATION_HYPOTHESIS",None,("predicted",)),
     claim("symbol","symbolic","INTERPRETED","Disappearance can symbolize transition","USER_INTERPRETATION"),
     claim("causal","causal","UNKNOWN","Occlusion or replacement undecidable","MODEL_LIMIT"),
     claim("physical","physical","INFERRED","Constant velocity holds only provisionally","MODEL_1D",.4)]
def run(out):
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    evidence=fixtures();reports={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for goal in GOALS:
            result=arbitrate(goal,evidence)
            reports[goal]={"focused":result["focused"],"status":result["status"],
                          "contradictions_preserved":bool(result["contradiction_ids"])}
            f.write(json.dumps(result)+"\n")
    report={"schema":"BRODY_P165D7_GOAL_MULTI_CONTINUITY",
      "goal_count":len(GOALS),"claim_count":len(evidence),"goals":reports,
      "all_claims_retained_per_goal":True,"priority_promotes_truth":False,
      "real_sensor_evidence":False,"automatic_goal_understanding":False,
      "d6_tracker_connected":False,"physical_or_metaphysical_truth_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--out",required=True)
    args=parser.parse_args();print(json.dumps(run(args.out),indent=2))
if __name__=="__main__":main()
