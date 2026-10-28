"""E6-E8 integration: external provenance, native contract inventory, candidate loop.

No remote SENS checkout, no real-world auth, no world mutation. E8 links
actual E1/E2-E3 outputs and uses an E4 probe proposal before new evidence.
"""
from __future__ import annotations
import argparse,hashlib,json,random
from pathlib import Path
from . import e1_cumulative_structural_school_v1 as e1
from . import e2_e3_temporal_structural_generation_v1 as e23
from . import image_probe_selection_p159 as p159
from .image_external_source_school_v0 import load_sources,reference,evaluate
from .experiential_skill_learning_v1 import save,seal,sha

def e6(root,folder):
    if folder is None:return {"status":"HOLD_NO_EXTERNAL_CORPUS","examined":0,"real_source_authenticated":False}
    files=load_sources(folder)
    seen=set();rows=[]
    for file in files[:30]:
        digest=hashlib.sha256(file.read_bytes()).hexdigest()
        if digest in seen:raise ValueError("EXTERNAL_DUPLICATE_CONTENT")
        seen.add(digest)
        img=reference(file)
        try:
            assessment=evaluate(img,"identity")
            rows.append({"name":file.name,"sha256":digest,"reconstruction":assessment})
        finally:img.close()
    return {"status":"EXTERNAL_FILE_UNVERIFIED","examined":len(rows),"records":rows,
        "teacher_identity_labels_used":False,"independent_sensor_provenance":False,
        "real_source_authenticated":False,"semantic_transfer_proven":False}

def e7():
    # These are local contracts only; never assert remote dependencies are installed.
    from . import contracts_v0,world_experience_bridge_v4
    existing=("WorldTransformationV0","WorldStateDeltaV0","WorldExperienceCandidateV0")
    found={name:hasattr(contracts_v0,name) for name in existing}
    return {"status":"LOCAL_CONTRACT_AUDITED_UPSTREAM_NOT_CONNECTED",
        "verified_local_contracts":found,
        "v4_compatibility_bridge_exists":hasattr(world_experience_bridge_v4,"SCHEMA"),
        "upstream_sens_runtime_verified":False,"upstream_mmonde_runtime_verified":False,
        "upstream_types_duplicated":False,"decision_authority":"KX108_ONLY"}

def e8(root):
    a=e1.run(root/"E1")
    b=e23.run(root/"E2_E3")
    if not a["retained_after_interference"]:raise ValueError("E1_RETENTION_NOT_PROVEN")
    exam=b["exam"]
    failures=[v for v in exam if v["candidate_mae"] is not None and v["static_mae"] is not None
              and v["candidate_mae"]>v["static_mae"]]
    # An image prediction failure is observed after scoring; it motivates a
    # future information request but does not retroactively rewrite the past.
    probe_bank=p159.learn(random.Random(881),10)
    proposal=p159.choose_probe(probe_bank,["observe","tap","tilt"])
    proposal_doc=seal({"schema":"BRODY_E8_FOLLOWUP_PROBE_CANDIDATE",
        "e1_retained":a["retained_after_interference"],
        "historical_failure_cases":[v["case"] for v in failures],
        "proposed_probe":proposal,
        "probe_not_executed":True,"native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY"})
    save(root/"FOLLOWUP_PROBE_PRECOMMIT.json",proposal_doc)
    return {"status":"LINKED_EDUCATIONAL_EVIDENCE_CANDIDATE",
        "e1_memory_retained":a["retained_after_interference"],
        "e23_regular_generated_exact":sum(x["candidate_mae"]==0 for x in exam),
        "e23_worse_than_static":len(failures),
        "next_experiment_proposed":proposal["decision"],
        "followup_probe_executed":False,
        "shared_latent_world_model":False,
        "shared_multimodal_skill_parameters":False,
        "source_reports":["E1/MASTER_REPORT.json","E2_E3/MASTER_REPORT.json"]}

def run(out,external_images=None):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    report={"schema":"BRODY_E6_E8_EVIDENCE_LINKED_V1",
        "E6":e6(root,external_images),"E7":e7(),"E8":e8(root),
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"E6_E8_BOUNDED_LOCAL_REUSE_NOT_FULL_UNIFICATION"}
    save(root/"MASTER_REPORT.json",report);return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);p.add_argument("--external-images")
    a=p.parse_args();r=run(a.out,a.external_images)
    print(json.dumps({"verdict":r["verdict"],"E6":r["E6"]["status"],
      "E7":r["E7"]["status"],"E8":r["E8"]["status"]},indent=2))
if __name__=="__main__":main()
