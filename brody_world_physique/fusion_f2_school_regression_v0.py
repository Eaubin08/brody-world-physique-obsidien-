"""FUSION-F2: run legacy and P2 unit-test schools independently, retain honest report.

Runs one test module per subprocess; records failures and does not hide them.
This is a regression audit, not a new training session or evidence of learning.
"""
from __future__ import annotations
import argparse,json,subprocess,sys,time
from pathlib import Path
from .fusion_historical_evidence_v0 import sha

SUITES={
 "E0_DRAWING":"test_drawing_school_v0.py",
 "E1_GESTURES":"test_drawing_school_v1.py",
 "E1_INSTRUMENTS":"test_instrument_school_v2.py",
 "E1_HIDDEN_MEMORY":"test_drawing_memory_school_v3.py",
 "E3_RELATIONS":"test_world_relations_school_v4_1.py",
 "E4_ORIENTATION":"test_world_orientation_school_v4_2.py",
 "E6_REVERSO":"test_reverso_learning_v0.py",
 "P2_CONTEXT":"test_p24_contextual_fluctuation_v0.py",
 "P2_MEMORY":"test_p27_experience_hierarchy_v0.py",
 "P2_GENERATION":"test_p211b_frozen_gesture_transfer_v0.py",
 "P2_COMPOSITION":"test_p211c_gesture_recomposition_v0.py",
 "P2_TRANSFER":"test_p212b_frozen_shift_transfer_v0.py",
 "P2_AUDIT":"test_p212c_mixed_visual_benchmark_v0.py",
 "P2_HOLD":"test_p212d_conservative_correction_gate_v0.py",
 "FUSION_ADAPTER":"test_fusion_historical_evidence_v0.py",
}
def run(repo_root,out_dir,python_executable=None):
    root=Path(repo_root).resolve()
    out=Path(out_dir).resolve()
    if out.exists():raise ValueError("output exists")
    tests=root/"tests"
    missing=[p for p in SUITES.values() if not (tests/p).is_file()]
    if missing:raise ValueError("missing suites: "+", ".join(missing))
    out.mkdir(parents=True)
    rows=[]
    for label,filename in SUITES.items():
        cmd=[str(python_executable or sys.executable),"-m","unittest","discover","-s","tests","-p",filename,"-v"]
        start=time.perf_counter()
        try:
            proc=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=180,errors="replace")
            status="PASS" if proc.returncode==0 else "FAIL"
            log=proc.stdout+"\n"+proc.stderr
            ret=proc.returncode
        except subprocess.TimeoutExpired:
            status="TIMEOUT";log="SUITE_TIMEOUT_180_SECONDS";ret=None
        file=out/(label+".log")
        file.write_text(log,encoding="utf-8")
        rows.append({"suite":label,"path":"tests/"+filename,"status":status,
                     "returncode":ret,"elapsed_seconds":round(time.perf_counter()-start,3),
                     "suite_sha256":sha(tests/filename),
                     "log_sha256":sha(file),"log":str(file)})
    result={"schema":"BRODY_FUSION_F2_REGRESSION_REPORT_V0",
        "suite_count":len(rows),"pass":sum(r["status"]=="PASS" for r in rows),
        "fail":sum(r["status"]=="FAIL" for r in rows),
        "timeout":sum(r["status"]=="TIMEOUT" for r in rows),
        "suites":rows,"tests_per_suite_not_inferred":True,
        "no_visual_quality_inferred":True,"no_training_executed":True,
        "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (out/"report.json").write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",default=".");p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.repo,a.out)
    print(json.dumps({k:r[k] for k in ("suite_count","pass","fail","timeout")}))
    if r["fail"] or r["timeout"]:sys.exit(1)
if __name__=="__main__":main()
