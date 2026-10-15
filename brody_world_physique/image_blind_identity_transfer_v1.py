"""Teacher-supervised identity memory with sealed blind recognition attempts.

Learning corpus holds multiple independently supplied files per identity.
Exam candidate images are scored BEFORE the teacher reveals their labels.
A strict distance margin permits HOLD; max three local identity hypotheses.
This measures rudimentary raster descriptor matching, not semantic vision.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageOps
from .image_external_source_school_v0 import reference
from .image_structural_observation_v1 import describe
from .fusion_f9_intensive_education_v0 import digest,verify_chain

def signature(im):
    # Small spatial projection; more discriminative than coarse context bucket.
    grey=im.convert("L").resize((16,16))
    return [sum(1 for y in range(j*4,(j+1)*4) for x in range(i*4,(i+1)*4)
                if grey.getpixel((x,y))<128)
            for j in range(4) for i in range(4)]
def distance(a,b):
    return sum(abs(x-y) for x,y in zip(a,b))
def read_manifest(path):
    x=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(x,dict):x=[x]
    if not isinstance(x,list) or not x:raise ValueError("NO_IDENTITIES")
    return x
def build_memory(lessons):
    identities={};all_hashes={}
    for item in read_manifest(lessons):
        key=item["identity"]
        if not isinstance(key,str) or not key or key in identities:raise ValueError("BAD_IDENTITY")
        files=item["examples"]
        if not isinstance(files,list) or not files:raise ValueError("NO_EXAMPLES")
        fingerprints=set();observations=[]
        for file in files:
            p=Path(file);h=hashlib.sha256(p.read_bytes()).hexdigest()
            if h in all_hashes and all_hashes[h]!=key:raise ValueError("IDENTITY_CONTRADICTION_SAME_BYTES")
            all_hashes[h]=key
            if h in fingerprints:continue
            fingerprints.add(h)
            im=reference(p);facts=describe(im)
            observations.append({"sha256":h,"source":str(p),"signature":signature(im),
                "context":facts["context"],"part_count":len(facts["parts"])})
        identities[key]={"observations":observations,
                          "teacher_origin":"DECLARED_UNVERIFIED"}
    return identities,all_hashes

def classify(memory,im):
    query=signature(im)
    nearest=[]
    for key,value in memory.items():
        examples=value["observations"]
        if examples:nearest.append((min(distance(query,e["signature"]) for e in examples),key))
    nearest.sort()
    if not nearest:return {"mode":"HOLD","hypotheses":[],"prediction":None}
    candidates=[{"identity":key,"distance":dist} for dist,key in nearest[:3]]
    # Conservative: cannot certify identity from descriptor similarity alone.
    best=nearest[0][0]
    second=nearest[1][0] if len(nearest)>1 else None
    accepted=(best==0 and second is not None and second>0)
    return {"mode":"CANDIDATE" if accepted else "DOUBT",
            "hypotheses":candidates,"prediction":nearest[0][1] if accepted else None}

def run(lessons,exam,out):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    memory,training_hashes=build_memory(lessons)
    probes=json.loads(Path(exam).read_text(encoding="utf-8-sig"))
    if isinstance(probes,dict):probes=[probes]
    if not isinstance(probes,list) or not probes:raise ValueError("NO_EXAMS")
    dest.mkdir(parents=True)
    results=[];prev=None
    with (dest/"receipts.jsonl").open("x",encoding="utf-8") as stream:
        for item in probes:
            p=Path(item["file"]);h=hashlib.sha256(p.read_bytes()).hexdigest()
            if h in training_hashes:raise ValueError("EXAM_IMAGE_LEAKAGE")
            prediction=classify(memory,reference(p))
            # Prediction is sealed before accessing teacher_label, if provided.
            seal=digest({"source_sha256":h,"decision":prediction})
            teacher=item.get("teacher_identity")
            feedback={"teacher_identity":teacher,
                "agrees":prediction["prediction"]==teacher if teacher is not None else None}
            event={"index":len(results)+1,"previous":prev,"source_sha256":h,
                "pre_feedback":prediction,"pre_feedback_seal":seal,"feedback":feedback,
                "native_memory_write":False,"canonical_promotion":False,
                "decision_authority":"KX108_ONLY"}
            event["digest"]=digest(event);prev=event["digest"];results.append(event)
            stream.write(json.dumps(event,sort_keys=True)+"\n")
    n,tip=verify_chain(dest/"receipts.jsonl")
    candidate={"schema":"BRODY_TEACHER_IDENTITIES_CANDIDATE_V1",
        "identities":memory,"native_memory_write":False,"canonical_promotion":False}
    candidate["digest"]=digest(candidate)
    (dest/"identity_memory_candidate.json").write_text(json.dumps(candidate,indent=2)+"\n",encoding="utf-8")
    report={"schema":"BRODY_BLIND_IDENTITY_TRANSFER_V1","taught_identities":len(memory),
       "independent_train_files":sum(len(v["observations"]) for v in memory.values()),
       "exam_images":n,"holds_or_doubts":sum(r["pre_feedback"]["mode"]!="CANDIDATE" for r in results),
       "candidate_predictions":sum(r["pre_feedback"]["mode"]=="CANDIDATE" for r in results),
       "receipt_tip":tip,"identity_labels_hidden_during_prediction":True,
       "cross_session_auto_learning":False,"teacher_authenticated":False,
       "semantic_understanding_proven":False,"native_memory_write":False,
       "canonical_promotion":False,"decision_authority":"KX108_ONLY",
       "status":"BLIND_RASTER_IDENTITY_CANDIDATE_EXAM"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--lessons",required=True);p.add_argument("--exam",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.lessons,a.exam,a.out),indent=2))
if __name__=="__main__":main()
