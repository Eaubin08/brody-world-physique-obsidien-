"""Append-only education receipts over the existing F3c candidate skill registry.

This is an experimental evidence layer, never Obsidia Native Memory.
"""
import hashlib
import json
from pathlib import Path
from .fusion_f3c_cumulative_skill_archive_v0 import load_registry, teach, exam
from .p210a_visual_loop_contract_v0 import digest

def fingerprint(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()

def verify_journal(root):
    root=Path(root)
    files=sorted((root/"education").glob("event-*.json"))
    history=[]
    tip=None
    for number,path in enumerate(files,1):
        event=json.loads(path.read_text(encoding="utf-8"))
        body={key:value for key,value in event.items() if key!="digest"}
        if (path.name!=f"event-{number:04d}.json" or event.get("index")!=number
                or event.get("previous")!=tip or event.get("digest")!=fingerprint(body)
                or event.get("native_memory_write") is not False
                or event.get("canonical_promotion") is not False
                or event.get("decision_authority")!="KX108_ONLY"):
            raise ValueError("invalid education history")
        history.append(event)
        tip=event["digest"]
    return history

def append_event(root,kind,payload):
    old=verify_journal(root)
    folder=Path(root)/"education"
    folder.mkdir(parents=True,exist_ok=True)
    event={"index":len(old)+1,"previous":old[-1]["digest"] if old else None,
           "kind":kind,"payload":payload,"native_memory_write":False,
           "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    event["digest"]=fingerprint(event)
    destination=folder/f"event-{len(old)+1:04d}.json"
    with destination.open("x",encoding="utf-8") as handle:
        handle.write(json.dumps(event,ensure_ascii=False,indent=2)+"\n")
    verify_journal(root)
    return event

def teach_recorded(root,version,skill_id,training):
    if any(item["kind"]=="TRAIN_CANDIDATE" and item["payload"]["skill_id"]==skill_id
           for item in verify_journal(root)):
        raise ValueError("duplicate taught skill")
    updated=teach(root,version,skill_id,training)
    append_event(root,"TRAIN_CANDIDATE",{
        "skill_id":skill_id,"train_sha256":digest(training),
        "registry_version":updated["version"],"registry_digest":updated["digest"]})
    return updated

def test_recorded(root,version,skill_id,layout,teacher,out):
    history=verify_journal(root)
    if not any(row["kind"]=="TRAIN_CANDIDATE" and row["payload"]["skill_id"]==skill_id
               for row in history):
        raise ValueError("unknown taught skill")
    result=exam(root,version,skill_id,layout,teacher,out)
    append_event(root,"HELD_OUT_TEST",{
        "skill_id":skill_id,"registry_version":version,
        "candidate_sha256":result["candidate_sha256"],"verdict":result["verdict"],
        "candidate_error":result["candidate_error"],
        "baseline_error":result["blank_error"],"test_used_for_training":False})
    return result

def readonly_context(root,version):
    history=verify_journal(root)
    registry=load_registry(root,version)
    return {"schema":"BRODY_EDUCATION_READONLY_VIEW_V0",
            "registry_version":version,"registry_digest":registry["digest"],
            "skill_ids":[item["id"] for item in registry["skills"]],
            "experience_count":len(history),
            "experience_tip":history[-1]["digest"] if history else None,
            "read_only":True,"native_memory_write":False,
            "decision_authority":"KX108_ONLY"}
