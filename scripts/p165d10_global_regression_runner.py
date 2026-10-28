"""P165-D10 global unittest replay, fail-closed with immutable evidence.

Runs repository unittest discovery in one subprocess, preserving raw stdout,
stderr, exit code and environment summary. Not an all-framework test claim.
"""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
def run(out,root=".",timeout=900):
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    if not 30<=timeout<=3600:raise ValueError("INVALID_TIMEOUT")
    base=Path(root).resolve()
    if not (base/"tests").is_dir():raise ValueError("TEST_DIRECTORY_MISSING")
    p.mkdir(parents=True)
    argv=[sys.executable,"-m","unittest","discover","-s","tests","-p","test*.py","-v"]
    start=time.monotonic()
    try:
        result=subprocess.run(argv,cwd=str(base),capture_output=True,text=True,
                              encoding="utf-8",errors="replace",timeout=timeout)
        stdout=result.stdout;stderr=result.stderr;code=result.returncode;timed_out=False
    except subprocess.TimeoutExpired as exc:
        stdout=(exc.stdout or b"");stderr=(exc.stderr or b"")
        if isinstance(stdout,bytes):stdout=stdout.decode("utf-8","replace")
        if isinstance(stderr,bytes):stderr=stderr.decode("utf-8","replace")
        code=None;timed_out=True
    (p/"STDOUT.txt").write_text(stdout,encoding="utf-8")
    (p/"STDERR.txt").write_text(stderr,encoding="utf-8")
    report={"schema":"BRODY_P165D10_GLOBAL_UNITTEST_DISCOVERY",
       "command":argv,"exit_code":code,"timed_out":timed_out,
       "seconds":round(time.monotonic()-start,3),
       "python":sys.version.split()[0],
       "discovery_scope":"tests/test*.py by unittest only",
       "pytest_and_other_frameworks_not_covered":True,
       "verdict":"GREEN" if code==0 and not timed_out else "RED_OR_INCOMPLETE",
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
def main():
    a=argparse.ArgumentParser();a.add_argument("--out",required=True)
    a.add_argument("--root",default=".");a.add_argument("--timeout",type=int,default=900)
    n=a.parse_args();result=run(n.out,n.root,n.timeout)
    print(json.dumps(result,indent=2))
    if result["verdict"]!="GREEN":sys.exit(1)
if __name__=="__main__":main()
