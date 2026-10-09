"""P2.9i: paired evaluation of P2.9h saved predictions, never retuning on TEST.

The P2.9h report is a post-hoc evaluation of precommitted candidate proposals.
This analyzer audits accepted overlap versus HOLD without modifying them.
"""
from __future__ import annotations
import argparse,json,hashlib
from collections import defaultdict
from pathlib import Path
from statistics import mean

SCHEMA="BRODY_P29I_PAIRED_ABLATION_AUDIT_V0"
BASE="A1_SPATIAL_DELTA"
MEM="A4_FROZEN_MEMORY"

def _metrics(values):
    return {"accepted":len(values),"mae_px":mean(values) if values else None,
            "errors_over_10px":sum(v>10 for v in values)}

def analyze(report):
    if report.get("schema")!="BRODY_P29H_PRECOMMITTED_POSITION_ABLATION_V0":
        raise ValueError("wrong P2.9h report schema")
    if report.get("test_feedback_used_for_learning") is not False or report.get("native_memory_write") is not False or report.get("decision_authority")!="KX108_ONLY":
        raise ValueError("invalid provenance or authority")
    rows=defaultdict(dict)
    for row in report["scores"]:
        key=(row["clip"],row["frame"])
        if row["arm"] in rows[key]:
            raise ValueError("duplicate arm on episode")
        rows[key][row["arm"]]=row["error_px"]
    precommit={(p["clip"],p["future_frame"]):p for p in report["precommit"]}
    if len(precommit)!=len(report["precommit"]) or len(rows)!=report["shared_test_cases"]:
        raise ValueError("missing or duplicated future episodes")
    if set(rows)!=set(precommit):raise ValueError("scores/precommit episode mismatch")
    arms=set(report["arms"])
    if any(set(episode)!=arms or set(p["predictions"])!=arms for key,episode in rows.items() for p in (precommit[key],)):
        raise ValueError("incomplete arms")
    groups={"both_accepted":[],"memory_hold_spatial_accepted":[],"both_hold":[],"memory_accepted_spatial_hold":[]}
    paired=[]
    for key in sorted(rows):
        episode=rows[key]
        s,m=episode[BASE],episode[MEM]
        if s is not None and m is not None:
            groups["both_accepted"].append(key)
            paired.append({"clip":key[0],"frame":key[1],"spatial_error_px":s,
                           "memory_error_px":m,"memory_minus_spatial_px":m-s})
        elif s is not None:
            groups["memory_hold_spatial_accepted"].append(key)
        elif m is not None:
            groups["memory_accepted_spatial_hold"].append(key)
        else:groups["both_hold"].append(key)
    paired_spatial=[x["spatial_error_px"] for x in paired]
    paired_memory=[x["memory_error_px"] for x in paired]
    refused_spatial=[rows[k][BASE] for k in groups["memory_hold_spatial_accepted"]]
    all_spatial=[e[BASE] for e in rows.values() if e[BASE] is not None]
    return {"schema":SCHEMA,"total_episodes":len(rows),
            "paired_episodes":len(paired),
            "groups":{name:len(keys) for name,keys in groups.items()},
            "same_case_spatial":_metrics(paired_spatial),
            "same_case_memory":_metrics(paired_memory),
            "mean_paired_memory_minus_spatial_px":
                mean(x["memory_minus_spatial_px"] for x in paired) if paired else None,
            "spatial_on_memory_hold_cases":_metrics(refused_spatial),
            "spatial_on_all_accepted_cases":_metrics(all_spatial),
            "pairs":paired,
            "held_case_keys":[{"clip":clip,"frame":frame} for clip,frame in groups["memory_hold_spatial_accepted"]],
            "changed_predictions":False,"test_labels_used_for_training":False,
            "independent_test_sources_added":False,"joint_multirepresentation_proven":False,
            "b8_promotion":False,"native_memory_write":False,"decision_authority":"KX108_ONLY"}

def run(source,out):
    s=Path(source);d=Path(out)
    if d.exists():raise ValueError("refuse overwrite")
    raw=s.read_bytes()
    report=json.loads(raw)
    result=analyze(report)
    result["source_report_sha256"]=hashlib.sha256(raw).hexdigest()
    d.parent.mkdir(parents=True,exist_ok=True)
    d.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def verify(source,out):
    raw=Path(source).read_bytes()
    result=analyze(json.loads(raw))
    result["source_report_sha256"]=hashlib.sha256(raw).hexdigest()
    if result!=json.loads(Path(out).read_text(encoding="utf-8")):
        raise ValueError("paired replay mismatch")
    return {"verified":True,"paired_episodes":result["paired_episodes"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    result=verify(args.source,args.out) if args.verify else run(args.source,args.out)
    print(json.dumps(result if args.verify else {k:result[k] for k in
      ("total_episodes","groups","same_case_spatial","same_case_memory",
       "mean_paired_memory_minus_spatial_px","spatial_on_memory_hold_cases")}))
if __name__=="__main__":main()
