"""Read-only, provenance-preserving historical school scorecard.

Reads original evaluation.json files from a local build directory.
It does not rerun training, compare incompatible metrics, or use TEST to learn.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path

SCHOOLS={
"V0":"ecole-dessin-20261008-225534",
"V1":"ecole-dessin-v1-20261008-231554",
"V3":"dessin-memoire-v3-20261009-000320",
"V4.1":"relations-v4-1-20261009-003945",
"V4.2":"orientation-v4-2-20261009-012020",
}
def scorecard(build_dir,out):
    base=Path(build_dir);target=Path(out)
    if target.exists():raise ValueError("output already exists")
    rows=[]
    for level,folder in SCHOOLS.items():
        path=base/folder/"evaluation.json"
        if not path.is_file():
            rows.append({"level":level,"status":"MISSING","scores":[]})
            continue
        payload=path.read_bytes();ev=json.loads(payload)
        scores=[]
        if level=="V0":
            for r in ev.get("exams",[]):
                scores.append({"id":r["exercise_ref"],"metric":"error_pixels",
                    "initial":r.get("initial_error_pixels"),
                    "final":r.get("final_error_pixels"),"raw":r})
        if level=="V1":
            for r in ev.get("unseen_exams",[]):
                scores.append({"id":r["exercise_ref"],"metric":"error_pixels",
                    "initial":r.get("initial_after_memory_gate"),
                    "final":r.get("after_correction_error_pixels")})
        if level=="V3":
            for r in ev.get("results",[]):
                scores.append({"id":r["episode"],"metric":"pixel_iou",
                    "value":r.get("score",{}).get("pixel_iou"),
                    "pixel_xor":r.get("score",{}).get("pixel_xor")})
        if level in ("V4.1","V4.2"):
            for r in ev.get("tests" if level=="V4.1" else "exams",[]):
                scores.append({"id":r.get("test_ref",r.get("id")),"metric":"teacher_label_match",
                    "correct":r.get("correct")})
        rows.append({"level":level,"status":"ARCHIVED_EVALUATION",
            "source":str(path.resolve()),"sha256":hashlib.sha256(payload).hexdigest(),
            "scores":scores,"count":len(scores)})
    target.parent.mkdir(parents=True,exist_ok=True)
    report={"schema":"BRODY_FUSION_F2_HISTORICAL_SCORECARD_V0",
        "source":"ORIGINAL_LOCAL_BUILD_EVALUATIONS","schools":rows,
        "metric_cross_school_comparison_valid":False,
        "recognition_of_real_objects_proven":False,"learning_executed":False,
        "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    target.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--build",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();r=scorecard(a.build,a.out)
    print(json.dumps({row["level"]:{"status":row["status"],"count":row.get("count",0)} for row in r["schools"]}))
if __name__=="__main__":main()
