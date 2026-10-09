"""F15 experimental evidence-to-periphery adapter. No fake Guard/Sigma verdicts.

Requires installed obsidia-x108-proofs periphery in a separate path.
Read-only F14 receipts => PeripheralSignalPacket => non-sovereign contract.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from .fusion_f9_intensive_education_v0 import verify_chain,digest

def packet_fields(receipt):
    evidence=receipt.get("observations",[])
    decision=receipt.get("decision",{})
    reasons=[];contradictions=[];risks=[]
    origins={}
    for o in evidence:
        origin=o.get("origin_id")
        if not o.get("attested_by_harness") is True:
            reasons.append("BRODY_UNVERIFIED_ORIGIN")
        if not origin:
            reasons.append("BRODY_MISSING_ORIGIN")
        if origin:
            origins.setdefault(origin,set()).add(o.get("value"))
    if any(len(v)>1 for v in origins.values()):
        contradictions.append("BRODY_SAME_ORIGIN_CONTRADICTION")
    if len(origins)<2:
        reasons.append("BRODY_INDEPENDENCE_NOT_ESTABLISHED")
    if len({o.get("value") for o in evidence if o.get("value") in ("OLD","NEW")})>1:
        contradictions.append("BRODY_OBSERVATION_CONTRADICTION")
    if decision.get("accepted") is not None:
        # A simulated source attestation is never enough to authorize anything.
        reasons.append("BRODY_SIMULATED_PROVENANCE_NOT_AUTHENTICATED")
    if receipt.get("case_type")=="all_spoof":
        risks.append("BRODY_COORDINATED_SPOOFING_TEST_CASE")
    return {"action_id":"brody-f15-"+str(receipt["index"]),"domain":"brody_image",
      "extra_metrics":{"case_type":receipt["case_type"],"evidence_count":len(evidence),
                       "source_attestation":"HARNESS_ONLY"},
      "unknowns":sorted(set(reasons)),
      "contradictions":sorted(set(contradictions)),
      "risk_flags":sorted(set(risks)),
      "evidence_refs":["f14:receipt:"+str(receipt["index"])+":"+receipt["digest"]],
      "recommended_gate":"HOLD","can_emit_act":False}

def check_real_contract(repo):
    import importlib.util
    root=Path(repo).resolve()
    for rel in ("periphery/common.py","periphery/sigma_bridge.py",
                "sigma/guard.py","sigma/run_pipeline.py"):
        if not (root/rel).is_file():
            raise RuntimeError("MISSING_REAL_OBSIDIA_CONTRACT:"+rel)
    # Load ONLY non-sovereign packet contract; do not mutate kernel or sigma.
    spec=importlib.util.spec_from_file_location("f15_periphery_common",root/"periphery/common.py")
    mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    return mod.PeripheralSignalPacket

def run(f14,out,obsidia_repo):
    src=Path(f14)
    if not src.exists():raise ValueError("MISSING_F14_RECEIPTS")
    n,tip=verify_chain(src)
    klass=check_real_contract(obsidia_repo)
    folder=Path(out)
    if folder.exists():raise ValueError("PRESERVE_EVIDENCE_EXISTING_OUTPUT")
    # Ensure mapping works before emitting artifacts.
    lines=src.read_text(encoding="utf-8").splitlines()
    packets=[]
    for line in lines:
        entry=json.loads(line)
        fields=packet_fields(entry)
        packet=klass(**fields)
        packet.assert_non_sovereign()
        packets.append(fields)
    folder.mkdir(parents=True)
    (folder/"periphery_packets.jsonl").write_text(
        "".join(json.dumps(x,sort_keys=True)+"\n" for x in packets),encoding="utf-8")
    summary={"schema":"BRODY_F15_PERIPHERY_PACKET_CONTRACT_V0",
      "source_receipts":n,"source_tip":tip,"mapped_packets":len(packets),
      "periphery_class_loaded_from_real_repo":True,
      "real_guard_invoked":False,"real_sigma_invoked":False,
      "reason_not_invoked":"NO_CERTIFIED_BRODY_DOMAIN_STATE_OR_BINDER_ROUTE",
      "simulation_cannot_authorize":True,"native_memory_write":False,
      "kernel_mutation":False,"decision_authority":"KX108_ONLY",
      "status":"PACKET_CONTRACT_ONLY_NOT_RUNTIME_INTEGRATION"}
    (folder/"report.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--f14-receipts",required=True)
    p.add_argument("--obsidia-repo",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    print(json.dumps(run(a.f14_receipts,a.out,a.obsidia_repo),indent=2))
if __name__=="__main__":main()
