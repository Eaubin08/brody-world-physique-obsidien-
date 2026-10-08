"""Strict same-frames comparison for zero/one/multiple memory experiments.

Reads existing results; never trains, modifies weights, or promotes memory.
Coverage and errors are separate because an abstention is not an error of 0.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean


def compare(cold: dict, one: dict, many: dict) -> dict:
    reports=(cold,one,many)
    if any(r.get("schema")!="BRODY_COLD_START_EXPERIENTIAL_SUITE_V0" for r in reports):
        raise ValueError("invalid result schema")
    if any(r.get("source_kind")!="SIMULATED" or r.get("world_knowledge_validated") is not False for r in reports):
        raise ValueError("reports must be simulated candidates only")
    def keyed(report:dict)->dict:
        out={}
        for clip in report["test_measures"]:
            for event in clip["errors"]:
                label=(clip["source_sha256"],event["heldout_ref"])
                if label in out: raise ValueError("duplicate heldout source")
                out[label]=event
        return out
    c,o,m=(keyed(x) for x in reports)
    if set(c)!=set(o) or set(c)!=set(m):
        raise ValueError("stages must use exactly the same heldout sources")
    if cold["test_predictions"]!=0 or one["training_candidate_transitions"]>many["training_candidate_transitions"]:
        raise ValueError("invalid cold or accumulated experience ordering")
    one_preds={k for k,v in o.items() if v["learned_error_px"] is not None}
    many_preds={k for k,v in m.items() if v["learned_error_px"] is not None}
    shared=sorted(one_preds & many_preds)
    def avg(keys,lookup,key):
        return mean(lookup[k][key] for k in keys) if keys else None
    report={
        "schema_version":"BRODY_MATCHED_EXPERIENTIAL_COMPARISON_V0",
        "total_heldout_positions":len(c),
        "cold_predictions":cold["test_predictions"],
        "one_experience_predictions":len(one_preds),
        "many_experience_predictions":len(many_preds),
        "shared_predicted_positions":len(shared),
        "one_error_on_shared_px":avg(shared,o,"learned_error_px"),
        "many_error_on_shared_px":avg(shared,m,"learned_error_px"),
        "linear_error_on_shared_px":avg(shared,m,"linear_error_px"),
        "acceleration_error_on_shared_px":avg(shared,m,"fixed_accel_error_px"),
        "paired_many_wins":sum(m[k]["learned_error_px"] < o[k]["learned_error_px"] for k in shared),
        "paired_one_wins":sum(o[k]["learned_error_px"] < m[k]["learned_error_px"] for k in shared),
        "paired_ties":sum(o[k]["learned_error_px"] == m[k]["learned_error_px"] for k in shared),
        "comparison_scope":"SHARED_HELDOUT_POSITIONS_ONLY",
        "physical_causality_proven":False,
        "adaptive_world_model_validated":False,
        "source_kind":"SIMULATED",
        "native_memory_write_allowed":False,
        "decision_authority":"KX108_ONLY",
    }
    return report


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Score zero/one/many learned experiences on exactly the same heldout frames")
    parser.add_argument("--cold",type=Path,required=True)
    parser.add_argument("--one",type=Path,required=True)
    parser.add_argument("--many",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args(argv)
    paths=(args.cold,args.one,args.many)
    results=[json.loads(x.read_text(encoding="utf-8")) for x in paths]
    compared=compare(*results)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(compared,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(compared,indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
