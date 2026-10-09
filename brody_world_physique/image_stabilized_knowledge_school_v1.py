"""Bounded taught-knowledge / reflex engine, separate from score-based school.

A teacher corrects a named context; repeated compatible lessons stabilize a
locally reusable procedure. Contradictions reopen only that context. Novel
angles produce at most three hypotheses, never global strategy ranking.
The knowledge is LOCAL CANDIDATE only, not ground truth or Native Memory.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .fusion_f9_intensive_education_v0 import digest,verify_chain

PROCEDURES=("raw","invert","autocontrast","threshold","sharpen")
SCHEMA="BRODY_TAUGHT_KNOWLEDGE_CANDIDATES_V1"
def fresh():
    return {"schema":SCHEMA,"revision":0,"concepts":{},"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
def load(path):
    if path is None:return fresh()
    state=json.loads(Path(path).read_text(encoding="utf-8"))
    sig=state.pop("digest",None)
    if sig!=digest(state) or state.get("schema")!=SCHEMA:raise ValueError("TAMPERED_KNOWLEDGE")
    if state.get("native_memory_write") is not False or state.get("canonical_promotion") is not False:
        raise ValueError("FORBIDDEN_AUTHORITY")
    return state
def save(state,path):
    p=Path(path)
    if p.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps({**state,"digest":digest(state)},indent=2)+"\n",encoding="utf-8")
def observe(state,context,procedure,teacher_ref,example_ref,correction=False):
    if not context or not teacher_ref or not example_ref or procedure not in PROCEDURES:
        raise ValueError("LESSON_REQUIRES_PROVENANCE_AND_WHITELISTED_METHOD")
    record=state["concepts"].setdefault(context,{"status":"LEARNING","procedure":None,
          "lessons":[],"exceptions":[],"conditions":[context],"relations":[]})
    if any(e["example_ref"]==example_ref for e in record["lessons"]):
        raise ValueError("DUPLICATE_EXAMPLE_NOT_NEW_EVIDENCE")
    event={"teacher_ref":teacher_ref,"example_ref":example_ref,"procedure":procedure,
           "explicit_correction":bool(correction)}
    record["lessons"].append(event)
    previous=record["procedure"]
    if record["status"]=="STABLE" and previous!=procedure:
        record["status"]="DOUBT";record["exceptions"].append(event)
    elif correction:
        # Correction replaces the local provisional method, but does not
        # instantly certify a reflex based on one lesson.
        record["procedure"]=procedure;record["status"]="LEARNING"
    elif previous is None:
        record["procedure"]=procedure;record["status"]="LEARNING"
    compatible={e["example_ref"] for e in record["lessons"]
                if e["procedure"]==record["procedure"]}
    # Teacher corroboration on distinct examples, no reward threshold.
    if record["status"]=="LEARNING" and len(compatible)>=3 and (not record["exceptions"] or correction):
        record["status"]="STABLE"
    state["revision"]+=1
    return record["status"]
def apply(state,context,similar_contexts=()):
    entry=state["concepts"].get(context)
    if entry and entry["status"]=="STABLE":
        return {"mode":"REFLEX","procedure":entry["procedure"],"hypotheses":[],
                "context":context}
    # Only local, explicitly supplied related contexts considered.
    options=[]
    if entry and entry["procedure"]:options.append(entry["procedure"])
    for related in similar_contexts:
        r=state["concepts"].get(related)
        if r and r["status"]=="STABLE" and r["procedure"] not in options:
            options.append(r["procedure"])
        if len(options)==3:break
    return {"mode":"DOUBT","procedure":None,"hypotheses":options[:3],
            "context":context}
def run(lessons,out,previous=None):
    state=load(previous)
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    events=json.loads(Path(lessons).read_text(encoding="utf-8"))
    if not isinstance(events,list) or not events:raise ValueError("NO_LESSONS")
    dest.mkdir(parents=True)
    prior=None
    with (dest/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i,item in enumerate(events,1):
            required=("context","procedure","teacher_ref","example_ref")
            if any(k not in item for k in required):raise ValueError("MISSING_LESSON_FIELDS")
            status=observe(state,**{k:item[k] for k in required},
                           correction=item.get("correction",False))
            record={"index":i,"previous":prior,"context":item["context"],"status":status,
                    "revision":state["revision"],"native_memory_write":False,
                    "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
            record["digest"]=digest(record);prior=record["digest"]
            f.write(json.dumps(record,sort_keys=True)+"\n")
    count,tip=verify_chain(dest/"receipts.jsonl")
    save(state,dest/"knowledge_candidates.json")
    report={"schema":"BRODY_STABILIZED_KNOWLEDGE_SCHOOL_V1","lessons":count,
        "receipt_tip":tip,"stable":sum(c["status"]=="STABLE" for c in state["concepts"].values()),
        "learning":sum(c["status"]=="LEARNING" for c in state["concepts"].values()),
        "doubt":sum(c["status"]=="DOUBT" for c in state["concepts"].values()),
        "state":"knowledge_candidates.json","native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY",
        "status":"TAUGHT_PROCEDURAL_REFLEX_LOCAL_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--lessons",required=True);p.add_argument("--out",required=True)
    p.add_argument("--previous")
    a=p.parse_args();print(json.dumps(run(a.lessons,a.out,a.previous),indent=2))
if __name__=="__main__":main()
