"""G1 persistence/restart replay integrity for Brody experimental skill state.

Reads a previously sealed candidate memory, verifies its digest without
mutating it, and tests new independently seeded heldout episodes after restart.
Never trains on the heldout future; never touches canonical/native memory.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .consolidated_education_replay_v1 import evaluate
from .experiential_skill_learning_v1 import save,seal

def resume(memory_file,out):
    src=Path(memory_file);dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    envelope=json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(envelope,dict) or "digest" not in envelope:
        raise ValueError("UNSEALED_MEMORY")
    state={k:v for k,v in envelope.items() if k!="digest"}
    if seal(state)["digest"]!=envelope["digest"]:
        raise ValueError("MEMORY_TAMPER")
    if state.get("decision_authority")!="KX108_ONLY" or state.get("native_memory_write") is not False or state.get("canonical_promotion") is not False:
        raise ValueError("AUTHORITY_BOUNDARY_FAILURE")
    if set(state["motion"])!={"clean","intervention"} or "shape" not in state:
        raise ValueError("UNKNOWN_MEMORY_SCHEMA")
    before=hashlib.sha256(src.read_bytes()).hexdigest()
    dest.mkdir(parents=True)
    (dest/"CANDIDATE_MEMORY.json").write_bytes(src.read_bytes())
    trials=[evaluate(dest,"restarted_clean",state,"flat",8302),
            evaluate(dest,"restarted_intervention",state,"slope",8403),
            evaluate(dest,"restarted_unknown",state,"spring",8504)]
    report={"schema":"BRODY_SESSION_RESTART_REPLAY_V1","source_memory_sha256":before,
       "memory_bytes_unchanged":hashlib.sha256(src.read_bytes()).hexdigest()==before,
       "tests":trials,"separate_process_restart_supported":True,
       "multi_day_retention_proven":False,
       "real_world_transfer_proven":False,"native_memory_write":False,
       "canonical_promotion":False,"decision_authority":"KX108_ONLY",
       "verdict":"SEALED_MEMORY_RELOADED_AND_REPLAYED"}
    save(dest/"MASTER_REPORT.json",report);return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--memory",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();r=resume(a.memory,a.out)
    print(json.dumps({"verdict":r["verdict"],"tests":r["tests"]},indent=2))
if __name__=="__main__":main()
