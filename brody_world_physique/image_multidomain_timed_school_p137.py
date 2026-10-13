"""P137: bounded multi-minute diverse experiment runner.

Executes different existing schools and test suites, never loops one scenario
to inflate coverage. Records failures, seed-independent coverage, runtime.
This is a scheduler, not proof of new cognitive ability.
"""
from __future__ import annotations
import argparse,json,subprocess,sys,time,hashlib
from pathlib import Path
TASKS=[
 ("perception","test_image_heterogeneous_capability_audit_p131.py"),
 ("context","test_image_context_transition_transfer_v1.py"),
 ("scene_memory","test_image_scene_relational_school_p132.py"),
 ("generation","test_image_multicapability_lab_p133.py"),
 ("correction","test_image_reciprocal_shape_learning_p134.py"),
 ("blind_exam","test_image_blind_symbolic_regeneration_p135.py"),
 ("diversity","test_image_forty_distinct_school_p136.py"),
 ("physics","test_image_motion_independent_campaign_v1.py"),
 ("source_provenance","test_image_motion_one_shot_campaign_v1.py"),
]
def run(out,seconds=300,root=None):
 dest=Path(out)
 if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
 if not 30<=seconds<=3600:raise ValueError("BUDGET_BETWEEN_30_AND_3600")
 project=Path(root or Path(__file__).resolve().parent.parent)
 dest.mkdir(parents=True)
 deadline=time.monotonic()+seconds
 reports=[]
 for family,filename in TASKS:
  remaining=deadline-time.monotonic()
  if remaining<2:
   reports.append({"family":family,"test":filename,"status":"NOT_RUN_BUDGET"});continue
  cmd=[sys.executable,"-m","unittest","discover","-s","tests","-p",filename,"-v"]
  start=time.monotonic()
  try:
   p=subprocess.run(cmd,cwd=project,capture_output=True,text=True,
      timeout=min(remaining,120),check=False)
   status="PASS" if p.returncode==0 else "FAIL"
   stdout=p.stdout+("\n"+p.stderr if p.stderr else "")
  except subprocess.TimeoutExpired as e:
   status="TIMEOUT";stdout=str(e)
  record={"family":family,"test":filename,"status":status,
          "duration_s":round(time.monotonic()-start,3),
          "output_sha256":hashlib.sha256(stdout.encode()).hexdigest()}
  (dest/(family+".log")).write_text(stdout,encoding="utf-8")
  reports.append(record)
 counts={status:sum(r["status"]==status for r in reports) for status in ("PASS","FAIL","TIMEOUT","NOT_RUN_BUDGET")}
 result={"schema":"BRODY_MULTIDOMAIN_TIMED_SCHOOL_P137","budget_s":seconds,
  "distinct_families":len(TASKS),"counts":counts,"runs":reports,
  "no_repeated_seed_loops":True,"full_budget_consumption_required":False,
  "real_world_generalization_proven":False,"native_memory_write":False,
  "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
 (dest/"MASTER_REPORT.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
 return result
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True)
 p.add_argument("--minutes",type=float,default=5)
 a=p.parse_args()
 report=run(a.out,int(a.minutes*60))
 print(json.dumps(report,indent=2))
 if report["counts"]["FAIL"] or report["counts"]["TIMEOUT"]:sys.exit(1)
if __name__=="__main__":main()
