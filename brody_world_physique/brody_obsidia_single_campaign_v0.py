"""Single-shot Brody Image × Obsidia consolidated acceptance.

Executes real available runs, exposes unmet capability gates without fake PASS.
No changes to Obsidia, kernel, Sigma, Native Memory or main.
"""
from __future__ import annotations
import argparse,json,subprocess,sys,hashlib,datetime
from pathlib import Path

STEPS=[
 ("f15", "brody_world_physique.fusion_f15_periphery_contract_bridge_v0",
  lambda r,o:["--f14-receipts",str(r/"f14"/"receipts.jsonl"),
             "--obsidia-repo",str(o),"--out",str(r/"f15")]),
 ("f15b","brody_world_physique.fusion_f15b_real_guard_sigma_diagnostic_v0",
  lambda r,o:["--f14-receipts",str(r/"f14"/"receipts.jsonl"),
             "--obsidia-repo",str(o),"--out",str(r/"f15b")]),
 ("f16","brody_world_physique.fusion_f16_canonical_route_inventory_v0",
  lambda r,o:["--obsidia-repo",str(o),"--out",str(r/"f16")]),
 ("f17","brody_world_physique.fusion_f17_agent_context_dryrun_v0",
  lambda r,o:["--f15-packets",str(r/"f15"/"periphery_packets.jsonl"),
             "--obsidia-repo",str(o),"--out",str(r/"f17")]),
]
def read_json(path):
 return json.loads(path.read_text(encoding="utf-8"))
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--obsidia-repo",default=r"C:\OBSIDIA_WORK\obsidia-x108-proofs")
 p.add_argument("--out",required=True)
 p.add_argument("--f14-receipts",default="build/fusion-f14-multisource-001/receipts.jsonl")
 p.add_argument("--skip-tests",action="store_true")
 a=p.parse_args();root=Path(a.out);obsidia=Path(a.obsidia_repo)
 if root.exists():raise SystemExit("Output already exists: preserve old evidence")
 if not obsidia.is_dir():raise SystemExit("Obsidia repo missing")
 src=Path(a.f14_receipts)
 if not src.is_file():raise SystemExit("F14 receipts missing")
 root.mkdir(parents=True)
 (root/"f14").mkdir()
 # Avoid copying secrets or rewriting source; symlinks problematic on Windows.
 # Pass external F14 source as explicit input in step argument replacement.
 ledger=[]
 def launch(label,args):
  proc=subprocess.run(args,capture_output=True,text=True,encoding="utf-8",errors="replace")
  (root/(label+".stdout.txt")).write_text(proc.stdout,encoding="utf-8")
  (root/(label+".stderr.txt")).write_text(proc.stderr,encoding="utf-8")
  ledger.append({"step":label,"exit_code":proc.returncode})
  return proc.returncode==0
 if not a.skip_tests:
  ok=launch("regression",
    [sys.executable,"-m","unittest","discover","-s","tests","-p","test_fusion_f*.py"])
  if not ok:
   (root/"INCOMPLETE.json").write_text(json.dumps({"ledger":ledger},indent=2),encoding="utf-8")
   raise SystemExit("Regression failed: inspect stderr")
 # Validate F14 source using original proof verifier rather than relabel a copy.
 from brody_world_physique.fusion_f9_intensive_education_v0 import verify_chain
 count,tip=verify_chain(src)
 if count!=1000:raise SystemExit("Expected exactly 1000 F14 receipts")
 for label,module,make_args in STEPS:
  args=make_args(root,obsidia)
  if label in ("f15","f15b"):
   args[1]=str(src.resolve())
  ok=launch(label,[sys.executable,"-m",module,*args])
  if not ok:
   (root/"INCOMPLETE.json").write_text(json.dumps({"ledger":ledger},indent=2),encoding="utf-8")
   raise SystemExit(label+" failed: inspect log")
 reports={k:read_json(root/k/"report.json") for k in ("f15","f15b","f16","f17")}
 danger=reports["f15b"]["counts"]["unsafe_authorizations"]
 counts=reports["f17"]["dryrun_results"]
 if danger or counts["ALLOW_CONTEXT_ONLY"]:
  status="UNSAFE_UNEXPECTED_ADMISSION"
 elif any(r["source_receipts"]!=1000 for r in [reports["f15"]]) or reports["f17"]["count"]!=1000:
  status="INCOMPLETE_REPLAY"
 else:
  status="DIAGNOSTICS_PASS_FULL_LEARNING_NOT_VALIDATED"
 # Distinguish completeness dimensions and do not infer successful sensing from synthetic receipts.
 capabilities={
  "synthetic_receipts_integrity":True,
  "canonical_periphery_packet":True,
  "real_guard_sigma_diagnostic_only":True,
  "canonical_context_dryrun":True,
  "verified_real_sensor_provenance":False,
  "visual_perception_real_world_test":False,
  "physical_generalization_independent_exam":False,
  "learning_improvement_real_data":False,
  "native_memory_promotion":False,
  "brody_action_domain_certified":False,
  "controlled_actuation":False}
 report={"schema":"BRODY_IMAGE_OBSIDIA_SINGLE_CAMPAIGN_V0","status":status,
   "receipt_cases":count,"receipt_tip":tip,"source_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),
   "diagnostic_guard_counts":reports["f15b"]["counts"],
   "context_dryrun_counts":counts,"capabilities":capabilities,
   "steps":ledger,"immutable_existing_outputs":True,
   "no_obisdia_patch":True,"no_main_patch":True,
   "decision_authority":"KX108_ONLY"}
 (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,indent=2))
 if status!="DIAGNOSTICS_PASS_FULL_LEARNING_NOT_VALIDATED":raise SystemExit(2)
if __name__=="__main__":main()
