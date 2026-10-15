"""Unified, restartable local identity school: lessons, discovery, doubt, exam.

This is a bounded bridge over existing Brody modules, not semantic AGI.
Teacher labels are explicit; no unauthorized network crawling.
"""
from __future__ import annotations
import argparse,hashlib,json,os
from pathlib import Path
from .image_external_source_school_v0 import reference
from .image_blind_identity_transfer_v1 import signature,classify
from .image_persistent_identity_teacher_loop_v1 import new_state,remember
from .image_structural_observation_v1 import describe
from .fusion_f9_intensive_education_v0 import digest,verify_chain

EXT={".png",".jpg",".jpeg",".webp",".bmp"}
def atomic(path,obj):
    tmp=path.with_name(path.name+".tmp")
    with tmp.open("w",encoding="utf-8") as f:
        json.dump(obj,f,sort_keys=True);f.write("\n");f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def curriculum(root,labels_path):
    """Local-source discovery: only approved folders with teacher labels."""
    labels=json.loads(Path(labels_path).read_text(encoding="utf-8-sig"))
    if not isinstance(labels,dict):raise ValueError("LABEL_MAPPING_REQUIRED")
    p=Path(root)
    if not p.is_dir():raise ValueError("MISSING_APPROVED_SOURCE_DIRECTORY")
    discovered=sorted(x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in EXT)
    tasks=[]
    for item in discovered:
        relative=item.relative_to(p).as_posix()
        label=labels.get(relative)
        if label is None:continue
        if not isinstance(label,str) or not label.strip():raise ValueError("INVALID_TEACHER_LABEL")
        tasks.append({"file":str(item.resolve()),"relative":relative,
                      "teacher_identity":label,"source_sha256":sha(item)})
    if not tasks:raise ValueError("NO_LABELED_LOCAL_SOURCES")
    return tasks

def validate_state(state):
    if state.get("native_memory_write") is not False or state.get("canonical_promotion") is not False or state.get("decision_authority")!="KX108_ONLY":
        raise ValueError("UNAUTHORIZED_STATE")
    if not isinstance(state.get("identities"),dict) or not isinstance(state.get("seen_hashes"),dict):
        raise ValueError("BAD_MEMORY_SHAPE")
def save_checkpoint(path,state,done,tip,config):
    body={"schema":"BRODY_UNIFIED_CHECKPOINT_V1","completed":done,
          "receipt_tip":tip,"config_digest":config,"state":state}
    atomic(path,{**body,"digest":digest(body)})
def begin(out,tasks,previous):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    receipts=out/"receipts.jsonl";check=out/"checkpoint.json"
    config=digest({"tasks":tasks,"previous":str(previous) if previous else None})
    if check.exists():
        c=json.loads(check.read_text(encoding="utf-8"))
        sealed=c.pop("digest",None)
        if sealed!=digest(c) or c.get("config_digest")!=config:raise ValueError("CHECKPOINT_TAMPER")
        n,tip=verify_chain(receipts)
        if n!=c["completed"] or tip!=c["receipt_tip"]:raise ValueError("CHECKPOINT_RECEIPTS_DIVERGENCE")
        validate_state(c["state"]);return c["state"],n,tip,config
    if receipts.exists() or (out/"MASTER_REPORT.json").exists():
        raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    if previous:
        state=json.loads(Path(previous).read_text(encoding="utf-8"))
        seal=state.pop("digest",None)
        if seal!=digest(state):raise ValueError("PREVIOUS_MEMORY_TAMPER")
    else:state=new_state()
    validate_state(state)
    return state,0,None,config
def learn(root,labels,out,previous=None,max_new=None):
    tasks=curriculum(root,labels)
    state,completed,tip,config=begin(out,tasks,previous)
    base=Path(out);receipts=base/"receipts.jsonl"
    for idx in range(completed,len(tasks)):
        item=tasks[idx];h=item["source_sha256"]
        # Always classify first. No access to teacher_identity before seal.
        im=reference(item["file"]);facts=describe(im)
        choice=classify(state["identities"],im)
        seal=digest({"sha":h,"choice":choice,"context":facts["context"]})
        teacher=item["teacher_identity"]
        outcome=remember(state,h,teacher,im,"LOCAL_TEACHER_LABEL_UNVERIFIED")
        record={"index":idx+1,"previous":tip,"source_sha256":h,
            "context":facts["context"],"parts":facts["parts"],
            "relations":facts["relations"],"sealed_choice":choice,
            "pre_feedback_seal":seal,"teacher_feedback":teacher,
            "learning_outcome":outcome,"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
        record["digest"]=digest(record)
        with receipts.open("a",encoding="utf-8") as f:
            f.write(json.dumps(record,sort_keys=True)+"\n");f.flush();os.fsync(f.fileno())
        tip=record["digest"]
        save_checkpoint(base/"checkpoint.json",state,idx+1,tip,config)
        if max_new is not None and idx+1-completed>=max_new and idx+1<len(tasks):
            return {"status":"PAUSED_CHECKPOINTED","completed":idx+1,"total":len(tasks)}
    n,tip=verify_chain(receipts)
    snapshot={**state,"digest":digest(state)}
    atomic(base/"identity_memory_candidate.json",snapshot)
    report={"schema":"BRODY_UNIFIED_LOCAL_SCHOOL_V1","lessons":n,
        "identities":len(state["identities"]),
        "observations":len(state["seen_hashes"]),
        "contradictions":len(state["contradictions"]),
        "receipt_tip":tip,"durable_checkpoint_after_each_lesson":True,
        "blind_pre_feedback":True,"max_hypotheses":3,
        "local_labeled_discovery":True,"external_web_discovery":False,
        "teacher_authenticated":False,"semantic_recognition_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "status":"UNIFIED_LOCAL_CANDIDATE_SCHOOL"}
    atomic(base/"MASTER_REPORT.json",report)
    return report

def exam(state_path,images,out):
    state=json.loads(Path(state_path).read_text(encoding="utf-8"))
    seal=state.pop("digest",None)
    if seal!=digest(state):raise ValueError("PREVIOUS_MEMORY_TAMPER")
    validate_state(state)
    files=sorted(p for p in Path(images).rglob("*") if p.is_file() and p.suffix.lower() in EXT)
    if not files:raise ValueError("NO_EXAM_IMAGES")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    dest.mkdir(parents=True)
    tip=None;records=[]
    with (dest/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i,path in enumerate(files,1):
            h=sha(path)
            if h in state["seen_hashes"]:raise ValueError("EXAM_LEAKAGE")
            choice=classify(state["identities"],reference(path))
            rec={"index":i,"previous":tip,"source_sha256":h,
                 "blind_decision":choice,"native_memory_write":False,
                 "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
            rec["digest"]=digest(rec);tip=rec["digest"];records.append(rec)
            f.write(json.dumps(rec,sort_keys=True)+"\n")
    n,tip=verify_chain(dest/"receipts.jsonl")
    result={"schema":"BRODY_UNIFIED_BLIND_RECALL_EXAM_V1","cases":n,
            "candidate_predictions":sum(bool(x["blind_decision"]["prediction"]) for x in records),
            "holds":sum(x["blind_decision"]["prediction"] is None for x in records),
            "receipt_tip":tip,"memory_updated":False,
            "semantic_recognition_proven":False,"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    atomic(dest/"MASTER_REPORT.json",result)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("learn","exam"),required=True)
    p.add_argument("--images",required=True);p.add_argument("--out",required=True)
    p.add_argument("--labels");p.add_argument("--previous");p.add_argument("--max-new",type=int)
    a=p.parse_args()
    if a.mode=="learn":
        if not a.labels:raise ValueError("LABELS_REQUIRED")
        result=learn(a.images,a.labels,a.out,a.previous,a.max_new)
    else:
        if not a.previous:raise ValueError("PREVIOUS_REQUIRED")
        result=exam(a.previous,a.images,a.out)
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
