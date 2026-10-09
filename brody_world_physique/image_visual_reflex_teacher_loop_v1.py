"""Visual lesson loop: local taught reflexes, bounded doubt, durable checkpoints.

Reference is visible for lesson feedback, never for reflex selection.
Candidate knowledge stays outside Obsidia Native Memory and KX108.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random
from pathlib import Path
from PIL import Image
from .image_external_source_school_v0 import load_sources,reference
from .image_continuous_learning_cycle_v0 import reconstruct
from .image_stabilized_knowledge_school_v1 import fresh,load,observe,apply,PROCEDURES
from .instrument_school_v2 import _gray_pixel_loss
from .fusion_f9_intensive_education_v0 import digest,verify_chain

def context_of(image):
    """Visible-only rough feature bucket, explicitly NOT object recognition."""
    im=image.convert("L")
    lo,hi=im.getextrema()
    if hi-lo<20:return "flat"
    if sum(1 for v in im.getdata() if v<100)>2500:return "dark-dense"
    return "drawing"

def atomic_json(path,body):
    tmp=path.with_name(path.name+".tmp")
    with tmp.open("w",encoding="utf-8") as stream:
        json.dump(body,stream,sort_keys=True)
        stream.write("\n");stream.flush();os.fsync(stream.fileno())
    os.replace(tmp,path)

def run(images,out,previous=None,limit=100,interrupt_after=None):
    paths=load_sources(images)[:limit]
    if not paths:raise ValueError("NO_IMAGES")
    dest=Path(out);dest.mkdir(parents=True,exist_ok=True)
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    config={"manifest":manifest,"previous":str(previous) if previous else None}
    config_digest=digest(config)
    progress_path=dest/"checkpoint.json"
    receipts=dest/"receipts.jsonl"
    if progress_path.exists():
        checkpoint=json.loads(progress_path.read_text(encoding="utf-8"))
        sig=checkpoint.pop("digest",None)
        if sig!=digest(checkpoint) or checkpoint["config_digest"]!=config_digest:
            raise ValueError("INVALID_CHECKPOINT")
        state=checkpoint["state"]
        start=checkpoint["completed"]
        if start>len(paths):raise ValueError("INVALID_CHECKPOINT_INDEX")
        if not receipts.exists():raise ValueError("MISSING_RECEIPTS")
        count,tip=verify_chain(receipts)
        if count!=start or tip!=checkpoint["receipt_tip"]:
            raise ValueError("CHECKPOINT_RECEIPTS_MISMATCH")
        for i in range(start):
            if not any(p.name==list(manifest)[i] for p in paths):
                raise ValueError("SOURCE_DRIFT")
        previous_hash=tip
    else:
        if receipts.exists() or (dest/"MASTER_REPORT.json").exists():
            raise ValueError("PRESERVE_EXISTING_EVIDENCE")
        state=load(previous) if previous else fresh()
        start=0;previous_hash=None
    for i in range(start,len(paths)):
        p=paths[i];target=reference(p)
        context=context_of(target)
        method=apply(state,context)
        chosen=method["procedure"] if method["mode"]=="REFLEX" else (
            method["hypotheses"][0] if method["hypotheses"] else "raw")
        image,n_strokes=reconstruct(target,chosen)
        initial_sha=hashlib.sha256(image.tobytes()).hexdigest()
        # Feedback AFTER the initial procedure/candidate has been chosen and sealed.
        loss=_gray_pixel_loss(image,target)
        candidates=[chosen]
        if method["mode"]=="DOUBT":
            candidates+= [s for s in PROCEDURES if s!=chosen][:2]
        losses={s:_gray_pixel_loss(reconstruct(target,s)[0],target) for s in candidates}
        correction=min(candidates,key=lambda s:(losses[s],candidates.index(s)))
        # Teacher here is a supervised pixel comparator; not an authenticated human.
        # Distinct examples support procedural consolidation only.
        status=observe(state,context,correction,"pixel-feedback-simulated",manifest[p.name],
                       correction=(correction!=chosen))
        event={"index":i+1,"previous":previous_hash,"source":p.name,
               "source_sha256":manifest[p.name],"context":context,"mode":method["mode"],
               "procedure_before_feedback":chosen,"candidate_sha256":initial_sha,
               "pixel_loss":loss,"teacher_corrected_to":correction,
               "post_lesson_status":status,"native_memory_write":False,
               "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
        event["digest"]=digest(event)
        # Write and sync receipt first, then checkpoint. If interrupted between,
        # fail closed; never falsely claim a full recovery.
        with receipts.open("a",encoding="utf-8") as stream:
            stream.write(json.dumps(event,sort_keys=True)+"\n")
            stream.flush();os.fsync(stream.fileno())
        previous_hash=event["digest"]
        checkpoint={"schema":"BRODY_VISUAL_REFLEX_CHECKPOINT_V1",
                    "config_digest":config_digest,"completed":i+1,
                    "receipt_tip":previous_hash,"state":state}
        atomic_json(progress_path,{**checkpoint,"digest":digest(checkpoint)})
        if interrupt_after is not None and i+1>=interrupt_after:
            return {"status":"PAUSED_CHECKPOINTED","completed":i+1,"total":len(paths)}
    n,tip=verify_chain(receipts)
    if n!=len(paths):raise ValueError("NOT_ALL_IMAGES_COMPLETED")
    candidate={"state":state,"source_manifest":manifest,
               "native_memory_write":False,"canonical_promotion":False}
    atomic_json(dest/"knowledge_candidates_snapshot.json",
                {**candidate,"digest":digest(candidate)})
    report={"schema":"BRODY_VISUAL_REFLEX_TEACHER_LOOP_V1",
            "lessons":n,"contexts":len(state["concepts"]),
            "stable":sum(x["status"]=="STABLE" for x in state["concepts"].values()),
            "doubt":sum(x["status"]=="DOUBT" for x in state["concepts"].values()),
            "receipt_tip":tip,"checkpoint_each_lesson":True,
            "pixel_teacher_only":True,"actual_objects_recognized":False,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY",
            "status":"VISUAL_TAUGHT_CANDIDATE_REFLEXES_ONLY"}
    atomic_json(dest/"MASTER_REPORT.json",report)
    return report

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--images",required=True);ap.add_argument("--out",required=True)
    ap.add_argument("--previous");ap.add_argument("--limit",type=int,default=100)
    a=ap.parse_args()
    print(json.dumps(run(a.images,a.out,a.previous,a.limit),indent=2))
if __name__=="__main__":main()
