"""F17: F15 peripheral packets -> genuine AgentResult -> ContextPacket -> X108 dry-run.

No runtime provider invocation, domain registration, memory promotion or actual action.
"""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path

def run(input_packets,obsidia_repo,out):
    src=Path(input_packets);root=Path(obsidia_repo).resolve();dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    if not src.is_file():raise ValueError("F15_PACKETS_MISSING")
    required=["periphery/agent_contracts.py",
              "periphery/context/agent_result_context_adapter.py",
              "periphery/context/agent_x108_context_flow.py",
              "runtime_wiring/packet_types.py"]
    for rel in required:
        if not (root/rel).is_file():raise RuntimeError("MISSING_OBSIDIA_RUNTIME:"+rel)
    sys.path.insert(0,str(root))
    try:
        from periphery.common import PeripheralSignalPacket
        from periphery.agent_contracts import AgentResult,AgentLayer
        from periphery.context.agent_result_context_adapter import agent_result_to_context_packet
        from periphery.context.agent_x108_context_flow import admit_agent_context
        results=[];totals={"HOLD":0,"BLOCK":0,"ALLOW_CONTEXT_ONLY":0,"other":0}
        input_hash=hashlib.sha256(src.read_bytes()).hexdigest()
        for i,line in enumerate(src.read_text(encoding="utf-8").splitlines()):
            if not line.strip():continue
            fields=json.loads(line)
            if fields.get("can_emit_act") is not False or fields.get("recommended_gate")!="HOLD":
                raise ValueError("UNTRUSTED_PACKET_TRIES_TO_ESCALATE")
            if fields.get("domain")!="brody_image":raise ValueError("WRONG_DOMAIN")
            packet=PeripheralSignalPacket(**fields)
            packet.assert_non_sovereign()
            ar=AgentResult(agent_id="brody-image-f17-readonly",
                           layer=AgentLayer.PROVENANCE,packet=packet,
                           notes=["F14 synthetic proof replay, no origin attestation",
                                  "No domain execution or memory promotion"])
            context=agent_result_to_context_packet(ar)
            result=admit_agent_context(context,ar,critical_action_requested=True)
            result.assert_non_sovereign()
            if result.x108_decision not in totals:totals["other"]+=1
            else:totals[result.x108_decision]+=1
            results.append({"index":i,"action_id":fields["action_id"],
                            "context_id":context.context_id,
                            "decision":result.x108_decision,
                            "gate_status":result.x108_gate_status,
                            "reasons":result.reason_codes,
                            "runtime_allowed_now":result.runtime_allowed_now,
                            "emits_act":result.emits_act,
                            "memory_write":result.memory_write})
        if not results:raise ValueError("NO_INPUT_PACKETS")
        if totals["ALLOW_CONTEXT_ONLY"] or totals["other"]:
            raise RuntimeError("UNEXPECTED_ADMISSION_IN_UNTRUSTED_REPLAY")
    finally:
        sys.path.pop(0)
    dest.mkdir(parents=True)
    with (dest/"context_replay.jsonl").open("x",encoding="utf-8") as f:
        for entry in results:f.write(json.dumps(entry,sort_keys=True)+"\n")
    report={"schema":"BRODY_F17_CANONICAL_AGENT_CONTEXT_DRYRUN_V0",
      "count":len(results),"source_sha256":input_hash,"dryrun_results":totals,
      "real_agent_result_adapter":True,"real_context_packet":True,
      "real_x108_context_dryrun":True,
      "real_guardx108_sovereign_invoked":False,"real_sigma_invoked":False,
      "provider_runtime_invoked":False,"domain_registered":False,
      "source_attestation_verified":False,
      "native_memory_write":False,"kernel_mutation":False,
      "status":"CONTEXT_DRYRUN_FAIL_CLOSED_ONLY"}
    (dest/"report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--f15-packets",required=True)
    p.add_argument("--obsidia-repo",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    print(json.dumps(run(a.f15_packets,a.obsidia_repo,a.out),indent=2))
if __name__=="__main__":main()
