"""Auditable motion campaign: source provenance, train/test split, blind A/B.

One trajectory per scene/recording group; whole groups belong to exactly one
partition. Exam data never train memory. The output is an executable plan and
a strict manifest, not claims of proven generalization.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .image_multihypothesis_motion_memory_v1 import track,read,write
from .image_observed_motion_school_v1 import analyze
from .fusion_f9_intensive_education_v0 import digest
ALLOWED={"train","exam"}
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def audit(manifest,out):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    spec=read(manifest)
    if not isinstance(spec,list) or not spec:raise ValueError("NO_CAMPAIGN_EPISODES")
    groups={};all_hashes={};splits={"train":[],"exam":[]}
    for i,row in enumerate(spec,1):
        split=row.get("split");group=row.get("source_group")
        origin=row.get("origin")
        if split not in ALLOWED or not isinstance(group,str) or not group.strip():
            raise ValueError("SPLIT_AND_SOURCE_GROUP_REQUIRED")
        if origin not in ("camera","video","synthetic","unknown"):
            raise ValueError("EXPLICIT_ORIGIN_REQUIRED")
        if group in groups and groups[group]!=split:raise ValueError("SOURCE_GROUP_LEAK")
        groups[group]=split
        observations=track(row)
        t=float(row["predict_t"])
        if t<=observations[-1]["t"]:raise ValueError("BAD_FORECAST_TIME")
        actual=analyze(row["actual"])
        if actual["source_sha256"] in {x["source_sha256"] for x in observations}:
            raise ValueError("EXAM_IS_COURSE_FRAME")
        hashes=[x["source_sha256"] for x in observations]+[actual["source_sha256"]]
        if len(set(hashes))!=len(hashes):raise ValueError("REPEATED_IMAGE_IN_EPISODE")
        for h in hashes:
            if h in all_hashes and all_hashes[h]["split"]!=split:
                raise ValueError("BYTE_LEAK_BETWEEN_SPLITS")
            all_hashes[h]={"split":split,"group":group}
        clean={"observations":row["observations"],"predict_t":t,
               "actual":row["actual"],"source_group":group,"origin":origin}
        splits[split].append(clean)
    if not splits["train"] or not splits["exam"]:raise ValueError("TRAIN_EXAM_BOTH_REQUIRED")
    # Provenance is self-reported; no claim that photographic independence was verified.
    report={"schema":"BRODY_SOURCE_GROUPED_MOTION_CAMPAIGN_V1",
      "episodes":len(spec),"train":len(splits["train"]),"exam":len(splits["exam"]),
      "train_groups":len({x["source_group"] for x in splits["train"]}),
      "exam_groups":len({x["source_group"] for x in splits["exam"]}),
      "origin_counts":{k:sum(r["origin"]==k for r in spec) for k in ("camera","video","synthetic","unknown")},
      "cross_split_byte_leak":False,"cross_split_source_group_leak":False,
      "provenance_verified_independently":False,
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY",
      "status":"SOURCE_DECLARED_GROUP_SPLIT_AUDITED"}
    dest.mkdir(parents=True)
    write(dest/"train_cases.json",splits["train"])
    write(dest/"exam_cases.json",splits["exam"])
    evidence={"report":report,"sha256_manifest":sha(manifest),
        "groups":groups,"source_hashes":all_hashes,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    evidence["digest"]=digest(evidence)
    write(dest/"SPLIT_EVIDENCE.json",evidence);write(dest/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(audit(a.manifest,a.out),indent=2))
if __name__=="__main__":main()
