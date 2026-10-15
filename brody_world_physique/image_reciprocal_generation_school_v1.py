"""Perception-to-generation reciprocity: reconstruct RGB block model, compare and teach.

Learns only a coarse visual prototype from explicit labelled images. The source
image is not copied into the generated output; only a 4x4 colour representation
is decoded. Separate exam grades held-out examples without altering memory.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image
from .image_real_transfer_exam_v2 import features,images,fingerprint,json_read,write_new
from .fusion_f9_intensive_education_v0 import digest,verify_chain

SCHEMA="BRODY_RECIPROCAL_RGB_PROTOTYPES_V1"
def encode_training(lesson_file,out):
    entries=json_read(lesson_file)
    if isinstance(entries,dict):entries=[entries]
    if not isinstance(entries,list) or not entries:raise ValueError("NO_COURSES")
    if Path(out).exists():raise ValueError("PRESERVE_PREVIOUS")
    memory={"schema":SCHEMA,"identities":{},"seen_hashes":{},
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    for entry in entries:
        name=entry["identity"]
        if not isinstance(name,str) or not name.strip():raise ValueError("BAD_IDENTITY")
        for path in entry["examples"]:
            h=fingerprint(path)
            owner=memory["seen_hashes"].get(h)
            if owner is not None and owner!=name:raise ValueError("CONTRADICTORY_TEACHING")
            if owner==name:continue
            memory["seen_hashes"][h]=name
            f=features(path)
            memory["identities"].setdefault(name,{"observations":[]})["observations"].append(
                {"sha256":h,"colour_grid":f["colour_grid"],"context":f["context"]})
    for item in memory["identities"].values():
        samples=item["observations"]
        item["prototype"]=[round(sum(s["colour_grid"][j] for s in samples)/len(samples))
                            for j in range(48)]
        item["unique_sources"]=len(samples)
        item["status"]="TAUGHT_CANDIDATE"
    memory["digest"]=digest(memory)
    write_new(out,memory)
    return {"identities":len(memory["identities"]),"distinct_examples":len(memory["seen_hashes"])}

def decode(grid,path):
    if len(grid)!=48:raise ValueError("BAD_GRID")
    im=Image.new("RGB",(64,64))
    for y in range(4):
        for x in range(4):
            i=(y*4+x)*3
            colour=tuple(max(0,min(255,int(grid[i+c])*32)) for c in range(3))
            for yy in range(y*16,(y+1)*16):
                for xx in range(x*16,(x+1)*16):
                    im.putpixel((xx,yy),colour)
    im.save(path)

def validate(path):
    m=json_read(path)
    seal=m.pop("digest",None)
    if seal!=digest(m) or m.get("schema")!=SCHEMA or m.get("native_memory_write") is not False or m.get("canonical_promotion") is not False or m.get("decision_authority")!="KX108_ONLY":
        raise ValueError("BAD_CANDIDATE_MEMORY")
    return m
def reconstruct(memory_path,out):
    if Path(out).exists():raise ValueError("PRESERVE_PREVIOUS")
    mem=validate(memory_path);root=Path(out);root.mkdir(parents=True)
    mapping={}
    for i,(identity,item) in enumerate(sorted(mem["identities"].items()),1):
        filename=f"prototype_{i:03d}.png"
        decode(item["prototype"],root/filename)
        mapping[filename]={"teacher_identity":identity,"sources":item["unique_sources"]}
    write_new(root/"INDEX.json",{"generated":mapping,"source_pixels_copied":False,
               "generation_method":"RGB_4x4_TILE_PROTOTYPE"})
    return {"reconstructions":len(mapping),"generator":"RGB_4x4_TILE_PROTOTYPE"}

def assess(memory_path,exam_dir,out):
    if Path(out).exists():raise ValueError("PRESERVE_PREVIOUS")
    mem=validate(memory_path)
    candidates=images(exam_dir)
    if not candidates:raise ValueError("NO_EXAM_IMAGES")
    for p in candidates:
        if fingerprint(p) in mem["seen_hashes"]:raise ValueError("EXAM_LEAK")
    root=Path(out);root.mkdir()
    tip=None;rows=[]
    with (root/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i,p in enumerate(candidates,1):
            observation=features(p)
            ranks=sorted((sum(abs(a-b) for a,b in zip(observation["colour_grid"],entry["prototype"])),name)
                         for name,entry in mem["identities"].items())
            proposals=[{"identity":name,"distance":dist} for dist,name in ranks[:3]]
            # No guarantee of semantic identity; keep exam candidacy separate.
            decision={"hypotheses":proposals,"mode":"DOUBT" if len(ranks)<2 or ranks[0][0]==ranks[1][0] else "CANDIDATE",
                      "prediction":ranks[0][1] if len(ranks)>1 and ranks[0][0]<ranks[1][0] else None}
            if decision["prediction"] is not None:
                # Generated from remembered prototype, not the exam pixels.
                idx=list(sorted(mem["identities"])).index(decision["prediction"])+1
                decode(mem["identities"][decision["prediction"]]["prototype"],root/f"exam_{i:03d}_generation.png")
            record={"index":i,"previous":tip,"file":p.relative_to(exam_dir).as_posix(),
                    "source_sha256":fingerprint(p),"pre_feedback_decision":decision,
                    "reconstruction_distance":ranks[0][0],
                    "teacher_label_during_exam":False,"native_memory_write":False,
                    "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
            record["digest"]=digest(record);tip=record["digest"];rows.append(record)
            f.write(json.dumps(record,sort_keys=True)+"\n")
    n,tip=verify_chain(root/"receipts.jsonl")
    report={"schema":"BRODY_RECIPROCAL_GENERATION_EXAM_V1","cases":n,
            "candidate_predictions":sum(x["pre_feedback_decision"]["prediction"] is not None for x in rows),
            "doubts":sum(x["pre_feedback_decision"]["prediction"] is None for x in rows),
            "receipt_tip":tip,"generations_from_stored_prototypes":True,
            "semantic_generation_proven":False,"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    write_new(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("train","generate","exam"),required=True)
    p.add_argument("--lessons");p.add_argument("--memory");p.add_argument("--images");p.add_argument("--out",required=True)
    a=p.parse_args()
    if a.mode=="train":result=encode_training(a.lessons,a.out)
    elif a.mode=="generate":result=reconstruct(a.memory,a.out)
    else:result=assess(a.memory,a.images,a.out)
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
