"""F16: audit actual Obsidia Binder/domain capabilities without mutation.

This tool never registers a domain, invokes an action, or synthesizes a gate.
It fails closed on missing or unknown runtime contracts.
"""
from __future__ import annotations
import argparse,ast,hashlib,json
from pathlib import Path

REQUIRED={
 "provider":"scripts/providers/brody_runtime_adapter_v1.py",
 "bridge":"periphery/sigma_bridge.py",
 "domains":"sigma/contracts.py",
 "guard":"sigma/guard.py",
 "sigma":"sigma/run_pipeline.py",
 "cycle":"scripts/obsidia_governed_runtime_cycle_v1.py",
}
def inspect(repo):
 root=Path(repo).resolve()
 files={}
 for name,relative in REQUIRED.items():
  path=root/relative
  if not path.is_file():
   raise RuntimeError("MISSING_CANONICAL_COMPONENT:"+relative)
  raw=path.read_bytes()
  files[name]={"path":relative,"sha256":hashlib.sha256(raw).hexdigest()}
 domain_source=(root/REQUIRED["domains"]).read_text(encoding="utf-8-sig")
 tree=ast.parse(domain_source)
 domain_values=[]
 for node in tree.body:
  if isinstance(node,ast.ClassDef) and node.name=="Domain":
   for item in node.body:
    if isinstance(item,ast.Assign) and isinstance(item.value,ast.Constant) and isinstance(item.value.value,str):
     domain_values.append(item.value.value)
 if not domain_values:raise RuntimeError("UNKNOWN_DOMAIN_REGISTRY")
 provider=(root/REQUIRED["provider"]).read_text(encoding="utf-8-sig")
 bridge=(root/REQUIRED["bridge"]).read_text(encoding="utf-8-sig")
 cycle=(root/REQUIRED["cycle"]).read_text(encoding="utf-8-sig")
 checked={
   "provider_no_decision": "decision_authority: bool = False" in provider,
   "provider_no_memory_write": "memory_write: bool = False" in provider,
   "provider_no_emits_act": "emits_act: bool = False" in provider,
   "bridge_no_brody_route": "def run_brody_with_periphery" not in bridge,
   "cycle_has_unsupported_domain_gate": ("is_supported_domain" in cycle and
                                          "decision_rendered" in cycle),
 }
 # Do not pretend that string/AST inspection proves execution semantics.
 status="SOURCE_CONTRACT_PREFLIGHT" if all(checked.values()) else "CONTRACT_MISMATCH_REVIEW_REQUIRED"
 return {"schema":"BRODY_F16_CANONICAL_ROUTE_INVENTORY_V0",
   "source_files":files,"registered_domains":sorted(domain_values),
   "brody_image_registered":"brody_image" in domain_values,
   "checks":checked,"status":status,
   "real_guard_invoked":False,"real_sigma_invoked":False,
   "runtime_execution":False,"registers_domain":False,
   "native_memory_write":False,"kernel_mutation":False,
   "decision_authority":"KX108_ONLY"}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--obsidia-repo",required=True)
 p.add_argument("--out",required=True)
 args=p.parse_args()
 report=inspect(args.obsidia_repo)
 output=Path(args.out)
 if output.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
 output.mkdir(parents=True)
 (output/"report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":report["status"],
   "brody_image_registered":report["brody_image_registered"],
   "registered_domains":report["registered_domains"]}))
 if report["status"]!="SOURCE_CONTRACT_PREFLIGHT":raise SystemExit(2)
if __name__=="__main__":main()
