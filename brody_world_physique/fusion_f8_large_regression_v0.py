"""F8 full-scale local campaign: independent suites + adverse policy probes.

No forged scores: actual subprocess return codes, durations and stderr are logged.
F2's historical suites are executed using its existing runner (not duplicated).
"""
from __future__ import annotations
import argparse,json,subprocess,time,sys
from pathlib import Path

SUITES=(
("HISTORICAL_V2_INSTRUMENTS","test_instrument_school_v2.py"),
("FUSION_F1","test_fusion_historical_evidence_v0.py"),
("FUSION_F2_REPLAY","test_fusion_f2_school_regression_v0.py"),
("FUSION_F2_SCORECARD","test_fusion_f2_historical_scorecard_v1.py"),
("FUSION_F3","test_fusion_f3_integrated_visual_lesson_v0.py"),
("FUSION_F3B","test_fusion_f3b_multilesson_school_v0.py"),
("FUSION_F3C","test_fusion_f3c_cumulative_skill_archive_v0.py"),
("FUSION_F4","test_fusion_f4_education_journal_v0.py"),
("FUSION_F5","test_fusion_f5_multiskill_course_v0.py"),
("FUSION_F6","test_fusion_f6_instrument_education_v0.py"),
("FUSION_F7","test_fusion_f7_train_only_correction_v0.py"),
("FUSION_F8_ADVERSARIAL","test_fusion_f8_adversarial_v0.py"),
)
def run(repo,out,timeout=240):
    repo=Path(repo).resolve();out=Path(out).resolve()
    if out.exists():raise ValueError("output exists")
    if not (repo/"brody_world_physique").is_dir():raise ValueError("invalid repo")
    out.mkdir(parents=True)
    results=[]
    for key,name in SUITES:
        source=repo/"tests"/name
        if not source.is_file():
            results.append({"name":key,"test_file":name,"status":"MISSING","exit_code":None})
            continue
        cmd=[sys.executable,"-m","unittest","discover","-s","tests","-p",name,"-v"]
        started=time.monotonic()
        try:
            result=subprocess.run(cmd,cwd=repo,capture_output=True,text=True,timeout=timeout,errors="replace")
            status="PASS" if result.returncode==0 else "FAIL"
            stdout=result.stdout;stderr=result.stderr;code=result.returncode
        except subprocess.TimeoutExpired as exc:
            status="TIMEOUT";stdout=str(exc.stdout or "");stderr=str(exc.stderr or "");code=None
        duration=round(time.monotonic()-started,3)
        log=out/(key+".log")
        log.write_text("COMMAND: "+" ".join(cmd)+"\nSTDOUT\n"+stdout+"\nSTDERR\n"+stderr,encoding="utf-8")
        results.append({"name":key,"test_file":name,"status":status,"exit_code":code,
                        "duration_seconds":duration,"log":log.name})
        print(f"{key}: {status} ({duration}s)",flush=True)
    # Execute the fifteen real historical F2 suites after the targeted checks.
    cmd=[sys.executable,"-m","brody_world_physique.fusion_f2_school_regression_v0",
         "--repo",str(repo),"--out",str(out/"f2-historical")]
    started=time.monotonic()
    try:
        replay=subprocess.run(cmd,cwd=repo,capture_output=True,text=True,
                              timeout=max(timeout,360),errors="replace")
        status="PASS" if replay.returncode==0 else "FAIL"
        log_text=replay.stdout+"\n"+replay.stderr
        exit_code=replay.returncode
    except subprocess.TimeoutExpired as exc:
        status="TIMEOUT";log_text=str(exc);exit_code=None
    (out/"F2_HISTORICAL_15.log").write_text(log_text,encoding="utf-8")
    results.append({"name":"F2_HISTORICAL_15","status":status,
                    "exit_code":exit_code,"duration_seconds":round(time.monotonic()-started,3),
                    "log":"F2_HISTORICAL_15.log"})
    print("F2_HISTORICAL_15: "+status,flush=True)
    summary={"schema":"BRODY_F8_LARGE_REGRESSION_V0",
             "suites_run":len(results),"passed":sum(x["status"]=="PASS" for x in results),
             "failed":sum(x["status"]=="FAIL" for x in results),
             "missing":sum(x["status"]=="MISSING" for x in results),
             "timeouts":sum(x["status"]=="TIMEOUT" for x in results),
             "results":results,"full_world_understanding_proven":False,
             "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    summary["verdict"]="PASS" if summary["passed"]==len(results) else "FAIL_CLOSED"
    (out/"report.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",default=".");p.add_argument("--out",required=True)
    p.add_argument("--timeout",type=int,default=240)
    a=p.parse_args()
    report=run(a.repo,a.out,a.timeout)
    print(json.dumps({key:report[key] for key in ("verdict","passed","failed","missing","timeouts")}))
    if report["verdict"]!="PASS":sys.exit(1)
if __name__=="__main__":main()
