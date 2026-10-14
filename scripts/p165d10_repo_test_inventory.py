"""Read-only repository test inventory; AST only, no test execution.

Lists all test*.py files, test methods/functions, unittest classes, imports,
and P161-P165 historical presence. Writes new audit folder (no overwrite).
"""
import argparse,ast,hashlib,json,subprocess
from pathlib import Path

LEGACY=("p161","p162","p163","p164","p165a","p165b","p165c","p165d")
def inventory(root):
    root=Path(root).resolve()
    files=sorted((root/"tests").rglob("test*.py"))
    records=[]
    for file in files:
        rel=file.relative_to(root).as_posix()
        content=file.read_bytes()
        try:
            tree=ast.parse(content.decode("utf-8-sig"),filename=rel)
            tests=[]
            for n in ast.walk(tree):
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith("test_"):
                    tests.append({"name":n.name,"line":n.lineno})
            classes=[n.name for n in tree.body if isinstance(n,ast.ClassDef)]
            imports=sorted(set(
                (n.module or "") for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)
            )|set(a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names))
            record={"file":rel,"sha256":hashlib.sha256(content).hexdigest(),
                    "declared_tests":len(tests),"tests":sorted(tests,key=lambda t:t["line"]),
                    "classes":classes,"imports":imports,"syntax":"OK"}
        except (SyntaxError,UnicodeError) as exc:
            record={"file":rel,"sha256":hashlib.sha256(content).hexdigest(),
                    "syntax":"ERROR","error":str(exc),"declared_tests":0}
        records.append(record)
    legacy={tag:{"files":[r["file"] for r in records if tag in Path(r["file"]).stem.lower()],
                  "declared_tests":sum(r["declared_tests"] for r in records if tag in Path(r["file"]).stem.lower())}
            for tag in LEGACY}
    return {"schema":"BRODY_P165D10_REPOSITORY_AST_TEST_INVENTORY",
       "files":records,"test_files":len(records),
       "declared_tests":sum(r["declared_tests"] for r in records),
       "syntax_errors":sum(r["syntax"]=="ERROR" for r in records),
       "legacy":legacy,
       "discovery_caveat":"AST declared test_ methods/functions != unittest collected counts",
       "scope":"ONLY tests/test*.py under current checked out repository",
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY"}
def run(root,out):
    d=Path(out)
    if d.exists():raise ValueError("PRESERVE_EVIDENCE")
    result=inventory(root)
    d.mkdir(parents=True)
    (d/"MASTER_REPORT.json").write_text(json.dumps(result,indent=2),encoding="utf8")
    summary={k:v for k,v in result.items() if k!="files"}
    (d/"SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--root",default=".")
    p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.root,a.out),indent=2))
if __name__=="__main__":main()
