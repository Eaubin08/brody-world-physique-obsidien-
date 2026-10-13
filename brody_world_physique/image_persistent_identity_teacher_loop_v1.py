"""Persistent candidate identity learning with sealed pre-feedback predictions.

Teacher-confirmed examples update identity knowledge after the prediction.
Contradictions are quarantined; held-out known identities are not forgotten.
No semantic truth, native memory promotion or kernel action.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .image_blind_identity_transfer_v1 import signature,distance,read_manifest,classify
from .image_external_source_school_v0 import reference
from .fusion_f9_intensive_education_v0 import digest,verify_chain

SCHEMA="BRODY_PERSISTENT_IDENTITY_CANDIDATES_V1"
def new_state():
    return {"schema":SCHEMA,"identities":{},"seen_hashes":{},"contradictions":[],
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"}
def load(path):
    if path is None:return new_state()
    state=json.loads(Path(path).read_text(encoding="utf-8"))
    seal=state.pop("digest",None)
    if seal!=digest(state) or state.get("schema")!=SCHEMA:raise ValueError("BAD_STATE_INTEGRITY")
    if state.get("native_memory_write") is not False or state.get("canonical_promotion") is not False:
        raise ValueError("FORBIDDEN_AUTHORITY")
    return state
def remember(state,image_hash,identity,image,teacher):
    if not isinstance(identity,str) or not identity.strip() or not teacher:
        return "HOLD_UNVERIFIED_TEACHER"
    owner=state["seen_hashes"].get(image_hash)
    if owner is not None and owner!=identity:
        state["contradictions"].append({"source_sha256":image_hash,
             "previous_identity":owner,"teacher_claim":identity,
             "status":"LOCAL_CONTRADICTION_UNRESOLVED"})
        return "HOLD_CONTRADICTION"
    if owner==identity:return "DUPLICATE_NOT_NEW_EVIDENCE"
    state["seen_hashes"][image_hash]=identity
    slot=state["identities"].setdefault(identity,{"observations":[],
              "teacher_origin":"DECLARED_UNVERIFIED","status":"TAUGHT_CANDIDATE"})
    slot["observations"].append({"sha256":image_hash,"signature":signature(image),
                                "teacher_ref":teacher})
    return "TEACHER_EXAMPLE_ADDED"
def run(exam,out,previous=None):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    state=load(previous)
    lessons=read_manifest(exam)
    # The exam is the supervision stream; the teacher label is never sent to
    # classification. It is revealed only after the prediction is sealed.
    results=[];prior=None;teaching_counts={}
    dest.mkdir(parents=True)
    with (dest/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for case in lessons:
            p=Path(case["file"]);raw=p.read_bytes()
            h=hashlib.sha256(raw).hexdigest()
            img=reference(p)
            decision=classify(state["identities"],img)
            sealed=digest({"source_sha256":h,"decision":decision})
            teacher=case.get("teacher_identity")
            outcome=remember(state,h,teacher,img,case.get("teacher_ref","teacher-unverified"))
            teaching_counts[outcome]=teaching_counts.get(outcome,0)+1
            event={"index":len(results)+1,"previous":prior,"source_sha256":h,
                   "pre_feedback_decision":decision,"pre_feedback_seal":sealed,
                   "teacher_identity_revealed_after_seal":teacher,
                   "teaching_outcome":outcome,
                   "native_memory_write":False,"canonical_promotion":False,
                   "decision_authority":"KX108_ONLY"}
            event["digest"]=digest(event);prior=event["digest"];results.append(event)
            f.write(json.dumps(event,sort_keys=True)+"\n")
    n,tip=verify_chain(dest/"receipts.jsonl")
    state["digest"]=digest(state)
    (dest/"identity_memory_candidate.json").write_text(json.dumps(state,indent=2)+"\n",encoding="utf-8")
    report={"schema":"BRODY_PERSISTENT_IDENTITY_TEACHER_LOOP_V1",
        "episodes":n,"known_identities":len(state["identities"]),
        "distinct_taught_examples":len(state["seen_hashes"]),
        "teaching_outcomes":teaching_counts,"contradictions":len(state["contradictions"]),
        "receipt_tip":tip,"memory_candidate_file":"identity_memory_candidate.json",
        "identity_decision_pre_feedback":True,"max_hypotheses":3,
        "cross_run_resume_supported":True,"checkpoint_during_run":False,
        "teacher_authenticity_verified":False,"real_semantic_identity_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "status":"PERSISTENT_LOCAL_TEACHER_IDENTITY_CANDIDATES"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--exam",required=True);p.add_argument("--out",required=True)
    p.add_argument("--previous")
    a=p.parse_args()
    print(json.dumps(run(a.exam,a.out,a.previous),indent=2))
if __name__=="__main__":main()
