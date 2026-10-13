"""F15B diagnostic: real GuardX108 + Sigma call, no Brody domain certification.

Forces fail-closed due to UNREGISTERED_BRODY_DOMAIN and no verified
source provenance. Never interprets sovereign kernel ALLOW as permission.
"""
import argparse,dataclasses,json,sys,os
from pathlib import Path
from .fusion_f9_intensive_education_v0 import verify_chain,digest
from .fusion_f15_periphery_contract_bridge_v0 import packet_fields,check_real_contract

def run(f14_receipts,obsidia_repo,out):
    source=Path(f14_receipts);root=Path(obsidia_repo).resolve();output=Path(out)
    if output.exists():raise ValueError("preserve prior evidence")
    n,tip=verify_chain(source)
    contract=check_real_contract(root)
    sys.path.insert(0,str(root))
    try:
        from sigma.contracts import Domain,DomainAggregate
        from sigma.guard import GuardX108
        from sigma.run_pipeline import apply_sigma
        from sigma.obsidia_sigma_v130 import ObsidiaSigmaMonitor
        from periphery.sigma_bridge import _merge_periphery_into_aggregate
        if not hasattr(Domain,"META"):raise RuntimeError("NO_META_DOMAIN")
        # Importing the authentic code proves this is not a mock;
        # the META domain is used only for negative diagnostic tests.
        imported={"guard":GuardX108.__module__,"sigma":apply_sigma.__module__,
                  "merge":_merge_periphery_into_aggregate.__module__}
        if imported!={"guard":"sigma.guard","sigma":"sigma.run_pipeline",
                       "merge":"periphery.sigma_bridge"}:
            raise RuntimeError("UNEXPECTED_RUNTIME_MODULE")
        results=[];counts={"guard_allow":0,"guard_hold":0,"guard_block":0,
                           "sigma_veto":0,"unsafe_authorizations":0,"errors":0}
        for line in source.read_text(encoding="utf-8").splitlines():
            evidence=json.loads(line)
            fields=packet_fields(evidence)
            packet=contract(**fields)
            packet.assert_non_sovereign()
            # Critical: real Guard may ALLOW with only one unknown.
            # Explicit domain nonregistration and unavailable trusted attestation
            # are separate facts. No invented positive confidence.
            aggregate=DomainAggregate(domain=Domain.META,market_verdict="HOLD",
                                      confidence=0.0,
                                      unknowns=["BRODY_DOMAIN_UNREGISTERED",
                                                "BRODY_NO_VERIFIED_PROVENANCE"],
                                      evidence_refs=fields["evidence_refs"])
            merged=_merge_periphery_into_aggregate(aggregate,packet)
            decision=GuardX108().decide(merged)
            raw=dataclasses.asdict(decision)
            guard_gate=str(raw.get("x108_gate"))
            counts["guard_"+guard_gate.lower()]=counts.get("guard_"+guard_gate.lower(),0)+1
            # Fresh monitor per case: avoid making test order a hidden input.
            sigma=ObsidiaSigmaMonitor(config_path=str(root/"sigma"/"sigma_config.json"))
            final=apply_sigma(raw,sigma)
            counts["sigma_veto"]+=int(final.get("sigma_override") is True)
            unsafe=guard_gate=="ALLOW" or final.get("x108_gate")=="ALLOW"
            counts["unsafe_authorizations"]+=int(unsafe)
            results.append({"index":evidence["index"],
                            "f14_digest":evidence["digest"],
                            "guard_gate":guard_gate,
                            "guard_reason":final.get("reason_code"),
                            "sigma_authority":final.get("sigma_authority"),
                            "sigma_override":final.get("sigma_override"),
                            "final_market_verdict":final.get("market_verdict"),
                            "unsafe_authorization":unsafe,
                            "no_domain_action":True,
                            "native_memory_write":False})
    finally:
        sys.path.pop(0)
    output.mkdir(parents=True)
    with (output/"replay.jsonl").open("x",encoding="utf-8") as handle:
        for item in results:handle.write(json.dumps(item,sort_keys=True)+"\n")
    report={"schema":"BRODY_F15B_REAL_GUARD_SIGMA_DIAGNOSTIC_V0",
            "cases":n,"f14_receipt_tip":tip,"calls":imported,"counts":counts,
            "real_guard_invoked":True,"real_sigma_invoked":True,
            "brody_domain_registered":False,"domain_used_for_diagnostic":"META",
            "domain_decision_authorized":False,
            "binder_route_certified":False,"native_memory_write":False,
            "kernel_mutation":False,"status":"DIAGNOSTIC_FAIL_CLOSED" if counts["unsafe_authorizations"]==0 else "UNSAFE_GUARD_ALLOW_DETECTED"}
    (output/"report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--f14-receipts",required=True)
    p.add_argument("--obsidia-repo",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    r=run(a.f14_receipts,a.obsidia_repo,a.out)
    print(json.dumps(r,indent=2))
    if r["counts"]["unsafe_authorizations"]:raise SystemExit(2)
if __name__=="__main__":main()
