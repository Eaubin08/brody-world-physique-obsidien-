"""Paired held-out ablation: local backtest versus previously corrected memory.

Uses the SAME unseen trajectories and their withheld next images. No learning,
model fitting or feedback is performed during scoring. Fail-closed on leakage.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from .image_experience_guided_motion_v2 import load,decision,backtest,context
from .image_multihypothesis_motion_memory_v1 import track,position,read,write,KINDS
from .image_observed_motion_school_v1 import analyze
from .fusion_f9_intensive_education_v0 import digest

def run(manifest,memory_path,out):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    memory=load(memory_path)
    cases=read(manifest)
    if not isinstance(cases,list) or not cases:raise ValueError("NO_HELDOUT_CASES")
    rows=[];train_set=set()
    for episode in memory["experiences"]:
        train_set.add(episode["feedback_sha256"])
    for idx,case in enumerate(cases,1):
        obs=track(case)
        if any(x["source_sha256"] in train_set for x in obs):
            raise ValueError("TRAINING_SEQUENCE_LEAKAGE")
        t=float(case["predict_t"])
        if t<=obs[-1]["t"]:raise ValueError("BAD_PREDICT_TIME")
        raw=decision(obs,{"experiences":[]})
        guided=decision(obs,memory)
        futures={k:position(obs,k,t) for k in KINDS}
        # Evaluate withheld truth only AFTER both prediction choices are fixed.
        actual=analyze(case["actual"])
        if actual["source_sha256"] in train_set or actual["source_sha256"] in {x["source_sha256"] for x in obs}:
            raise ValueError("HELDOUT_LEAKAGE")
        model_errors={k:round(math.hypot(p["x"]-actual["x"],p["y"]-actual["y"]),5)
                      for k,p in futures.items()}
        def result(choice):
            name=choice["selected"]
            return {"selected":name,"mode":choice["mode"],
                    "error_px":model_errors[name] if name else None,
                    "evidence_source":choice["evidence_source"]}
        rows.append({"case":idx,"context":context(obs),"models_error_px":model_errors,
                     "no_memory":result(raw),"with_memory":result(guided),
                     "source_sha256":actual["source_sha256"]})
    def summarize(key):
        observed=[r[key]["error_px"] for r in rows if r[key]["error_px"] is not None]
        return {"selected":len(observed),"holds":len(rows)-len(observed),
                "mean_error_px":round(sum(observed)/len(observed),5) if observed else None,
                "errors_include_holds":False}
    baseline=summarize("no_memory");guided=summarize("with_memory")
    paired=[(r["no_memory"]["error_px"],r["with_memory"]["error_px"]) for r in rows
            if r["no_memory"]["error_px"] is not None and r["with_memory"]["error_px"] is not None]
    delta=round(sum(a-b for a,b in paired)/len(paired),5) if paired else None
    report={"schema":"BRODY_PAIRED_PHYSICAL_MEMORY_ABLATION_V1",
        "cases":len(rows),"paired_selected":len(paired),
        "no_memory":baseline,"with_memory":guided,"mean_paired_advantage_px":delta,
        "memory_outperforms_baseline_on_paired_cases":delta>0 if delta is not None else None,
        "episodes_available":len(memory["experiences"]),
        "identical_heldout_cases":True,"memory_frozen_during_exam":True,
        "independent_scene_proven":False,"native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY",
        "status":"HELDOUT_PAIRED_COMPARISON_ONLY"}
    dest.mkdir(parents=True)
    evidence={"schema":"BRODY_PAIRED_ABLATION_EVIDENCE_V1","rows":rows,
         "report":report,"memory_digest":digest(memory),
         "native_memory_write":False,"canonical_promotion":False,
         "decision_authority":"KX108_ONLY"}
    evidence["digest"]=digest(evidence)
    write(dest/"EVIDENCE.json",evidence)
    write(dest/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cases",required=True);p.add_argument("--memory",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.cases,a.memory,a.out),indent=2))
if __name__=="__main__":main()
