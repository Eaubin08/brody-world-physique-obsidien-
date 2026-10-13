"""Brody V2: independent exam labels, RGB/shape descriptors and transfer audit.

Exam images and sealed predictions are processed WITHOUT teacher labels.
Feedback is a separate step requiring an explicit separate file.
No semantic claim, external networking, sovereign memory mutation, or new authority.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageOps
from .image_external_source_school_v0 import reference
from .image_structural_observation_v1 import describe
from .fusion_f9_intensive_education_v0 import digest, verify_chain

EXT={".png",".jpg",".jpeg",".bmp",".webp"}
def fingerprint(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def features(p):
    im=Image.open(p).convert("RGB")
    im=ImageOps.exif_transpose(im).resize((64,64))
    # An interpretable coarse colour/geometry descriptor, not a semantic embedding.
    colours=[]
    for y in range(4):
        for x in range(4):
            tile=im.crop((x*16,y*16,(x+1)*16,(y+1)*16))
            px=list(tile.getdata())
            colours.extend([round(sum(q[c] for q in px)/len(px)/32) for c in range(3)])
    shape=describe(im)
    return {"colour_grid":colours,"context":shape["context"],
            "parts":len(shape["parts"]),"dark_pixels":shape["properties"]["dark_pixels"]}
def distance(a,b):
    return sum(abs(x-y) for x,y in zip(a["colour_grid"],b["colour_grid"])) + abs(a["parts"]-b["parts"])*3
def json_read(p):return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def write_new(path,value):
    with Path(path).open("x",encoding="utf-8") as f:json.dump(value,f,indent=2,sort_keys=True);f.write("\n")
def images(folder):
    p=Path(folder)
    if not p.is_dir():raise ValueError("INVALID_IMAGES_DIR")
    return sorted(x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in EXT)
def train(lesson_json,out):
    entries=json_read(lesson_json)
    if isinstance(entries,dict):entries=[entries]
    if not isinstance(entries,list) or not entries:raise ValueError("NO_LESSONS")
    memory={"schema":"BRODY_RGB_GEOMETRY_TEACHER_MEMORY_V2","identities":{},
            "seen_hashes":{},"native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"}
    for entry in entries:
        identity=entry["identity"]
        if not isinstance(identity,str) or not identity.strip():raise ValueError("INVALID_IDENTITY")
        for name in entry["examples"]:
            h=fingerprint(name)
            prior=memory["seen_hashes"].get(h)
            if prior is not None and prior!=identity:raise ValueError("CONTRADICTORY_LABEL")
            if prior==identity:continue
            memory["seen_hashes"][h]=identity
            memory["identities"].setdefault(identity,[]).append({"sha256":h,"features":features(name)})
    if Path(out).exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    memory["digest"]=digest(memory)
    write_new(out,memory)
    return {"taught_identities":len(memory["identities"]),"unique_examples":len(memory["seen_hashes"])}
def load_memory(path):
    m=json_read(path);seal=m.pop("digest",None)
    if seal!=digest(m) or m.get("schema")!="BRODY_RGB_GEOMETRY_TEACHER_MEMORY_V2" or m.get("native_memory_write") is not False or m.get("canonical_promotion") is not False or m.get("decision_authority")!="KX108_ONLY":
        raise ValueError("MEMORY_INTEGRITY")
    return m
def predict(memory,feat):
    ranks=sorted((min(distance(feat,x["features"]) for x in rows),key)
                 for key,rows in memory["identities"].items() if rows)
    options=[{"identity":key,"distance":dist} for dist,key in ranks[:3]]
    if len(ranks)<2 or not ranks[0][0]<ranks[1][0] or ranks[0][0]>24:
        return {"mode":"DOUBT","prediction":None,"hypotheses":options}
    return {"mode":"CANDIDATE","prediction":ranks[0][1],"hypotheses":options}
def examine(memory_file,folder,out):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    memory=load_memory(memory_file)
    candidates=images(folder)
    if not candidates:raise ValueError("NO_EXAM_IMAGES")
    samples=[]
    for p in candidates:
        h=fingerprint(p)
        if h in memory["seen_hashes"]:raise ValueError("EXACT_TRAIN_TEST_LEAK")
        samples.append((p,h,features(p)))
    dest.mkdir(parents=True)
    tip=None;rows=[]
    with (dest/"sealed_predictions.jsonl").open("x",encoding="utf-8") as f:
        for index,(p,h,feat) in enumerate(samples,1):
            result=predict(memory,feat)
            row={"index":index,"previous":tip,"file":p.relative_to(folder).as_posix(),
                 "source_sha256":h,"decision":result,
                 "decision_before_teacher_feedback":True,
                 "native_memory_write":False,"canonical_promotion":False,
                 "decision_authority":"KX108_ONLY"}
            row["digest"]=digest(row);tip=row["digest"];rows.append(row)
            f.write(json.dumps(row,sort_keys=True)+"\n")
    # Reuse chain validator via standard receipt filename.
    n,tip=verify_chain(dest/"sealed_predictions.jsonl")
    write_new(dest/"MASTER_REPORT.json",{"schema":"BRODY_RGB_GEOMETRY_BLIND_EXAM_V2",
              "exam_cases":n,"candidate_proposals":sum(x["decision"]["prediction"] is not None for x in rows),
              "doubts":sum(x["decision"]["prediction"] is None for x in rows),
              "receipt_tip":tip,"teacher_labels_available_during_exam":False,
              "semantic_recognition_proven":False,"native_memory_write":False,
              "canonical_promotion":False,"decision_authority":"KX108_ONLY"})
    return json_read(dest/"MASTER_REPORT.json")
def grade(predictions,teacher_labels,out):
    # Separate post-exam invocation: labels cannot influence previous decisions.
    if Path(out).exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    labels=json_read(teacher_labels)
    if not isinstance(labels,dict):raise ValueError("BAD_TEACHER_LABELS")
    n,tip=verify_chain(Path(predictions)/"sealed_predictions.jsonl")
    rows=[json.loads(line) for line in (Path(predictions)/"sealed_predictions.jsonl").read_text().splitlines()]
    counts={"correct":0,"wrong":0,"doubt":0,"unlabeled":0}
    details=[]
    for row in rows:
        expected=labels.get(row["file"])
        guess=row["decision"]["prediction"]
        if expected is None:status="unlabeled"
        elif guess is None:status="doubt"
        elif guess==expected:status="correct"
        else:status="wrong"
        counts[status]+=1
        details.append({"file":row["file"],"expected":expected,"predicted":guess,"status":status})
    write_new(out,{"schema":"BRODY_POST_EXAM_TEACHER_AUDIT_V2","graded_cases":n,
        "receipt_tip":tip,"outcomes":counts,"details":details,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"})
    return counts
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("train","exam","grade"),required=True)
    p.add_argument("--lessons");p.add_argument("--memory");p.add_argument("--images")
    p.add_argument("--predictions");p.add_argument("--labels");p.add_argument("--out",required=True)
    a=p.parse_args()
    if a.mode=="train":result=train(a.lessons,a.out)
    elif a.mode=="exam":result=examine(a.memory,a.images,a.out)
    else:result=grade(a.predictions,a.labels,a.out)
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
