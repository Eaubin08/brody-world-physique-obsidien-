"""P132 experimental multi-object scene learning and reciprocal composition.

Observable monochrome connected components only. Teacher labels are arbitrary
local symbols, not semantic recognition. Generation paints learned geometry.
"""
from __future__ import annotations
import argparse,json,hashlib,math
from pathlib import Path
from PIL import Image,ImageDraw
from .image_structural_observation_v1 import describe
from .fusion_f9_intensive_education_v0 import digest

SCHEMA="BRODY_SCENE_RELATION_MEMORY_P132"
def blank():
 return {"schema":SCHEMA,"lessons":[],"native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
def write(p,x):
 Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
def read(p):return json.loads(Path(p).read_text(encoding="utf8"))
def load(p=None):
 if not p:return blank()
 s=read(p);seal=s.pop("digest",None)
 if seal!=digest(s) or s.get("schema")!=SCHEMA or s.get("native_memory_write") is not False or s.get("canonical_promotion") is not False or s.get("decision_authority")!="KX108_ONLY":raise ValueError("CORRUPTED_SCENE_MEMORY")
 return s
def observe(path):
 with Image.open(path) as im:facts=describe(im)
 return facts
def signature(facts):
 # purely positional summary; order determined by descending area of connected components.
 return [{"size":p["size"],"bbox":p["bbox"],"center":p["center"]} for p in facts["parts"]]
def learn(memory,teacher,source_group,path):
 if not isinstance(teacher,str) or not teacher.strip() or not source_group:raise ValueError("TEACHER_AND_GROUP_REQUIRED")
 facts=observe(path)
 if len(facts["parts"])<2:raise ValueError("MULTIPART_SCENE_REQUIRED")
 source_sha=hashlib.sha256(Path(path).read_bytes()).hexdigest()
 earlier=[l for l in memory["lessons"] if l["source_sha256"]==source_sha]
 if earlier:
  if any(l["teacher"]!=teacher for l in earlier):raise ValueError("CONTRADICTORY_TEACHER")
  return {"status":"DUPLICATE","parts":len(facts["parts"])}
 lesson={"teacher":teacher,"source_group":source_group,"source_sha256":source_sha,
         "signature":signature(facts),"relations":facts["relations"],"context":facts["context"]}
 memory["lessons"].append(lesson)
 return {"status":"LEARNED_CANDIDATE","parts":len(facts["parts"]),"relations":len(facts["relations"])}
def compare(a,b):
 if len(a["parts"])!=len(b["parts"]):return False
 # coarse relation graph invariant under pixel translation (not rotation).
 return [r["orientation"] for r in a["relations"]]==[r["orientation"] for r in b["relations"]]
def recall(memory,facts):
 matches=[]
 for l in memory["lessons"]:
  old={"parts":l["signature"],"relations":l["relations"]}
  if compare(facts,old):matches.append(l)
 teachers={l["teacher"] for l in matches}
 if len(teachers)==1 and len({l["source_group"] for l in matches})>=2:
  return {"mode":"CANDIDATE","teacher":next(iter(teachers)),"evidence_groups":len({l["source_group"] for l in matches})}
 return {"mode":"DOUBT","teacher":None,"evidence_groups":len({l["source_group"] for l in matches})}
def reconstruct(lesson,dest):
 im=Image.new("RGB",(64,64),"white");draw=ImageDraw.Draw(im)
 for p in lesson["signature"]:draw.rectangle(p["bbox"],fill="black")
 im.save(dest)
 return {"file":str(dest),"approximation":"axis-aligned-bounding-boxes","pixel_fidelity_proven":False}
def experiment(scenes,out,previous=None):
 d=Path(out)
 if d.exists():raise ValueError("PRESERVE_EVIDENCE")
 rows=read(scenes)
 if not isinstance(rows,list) or not rows:raise ValueError("NO_SCENES")
 memory=load(previous)
 # sealed forecast before examiner feedback: no labels accepted for exam rows
 train=[r for r in rows if r.get("split")=="train"]
 exam=[r for r in rows if r.get("split")=="exam"]
 if not train or not exam:raise ValueError("TRAIN_EXAM_REQUIRED")
 if {r["source_group"] for r in train}&{r["source_group"] for r in exam}:raise ValueError("SOURCE_GROUP_LEAK")
 hashes={}
 for r in rows:
  h=hashlib.sha256(Path(r["file"]).read_bytes()).hexdigest()
  if h in hashes and hashes[h]!=r["split"]:raise ValueError("BYTE_LEAK")
  hashes[h]=r["split"]
 for r in train:learn(memory,r["teacher"],r["source_group"],r["file"])
 outcomes=[]
 for r in exam:
  facts=observe(r["file"]);prediction=recall(memory,facts)
  outcomes.append({"source_group":r["source_group"],"context":facts["context"],"predicted":prediction,
       "exam_teacher":r["teacher"],"correct":prediction["teacher"]==r["teacher"] if prediction["mode"]=="CANDIDATE" else None})
 d.mkdir(parents=True)
 snapshot=dict(memory);snapshot["digest"]=digest(snapshot);write(d/"candidate_scene_memory.json",snapshot)
 if memory["lessons"]:reconstruct(memory["lessons"][0],d/"reconstruction.png")
 report={"schema":"BRODY_MULTIOBJECT_RECIPROCAL_SCHOOL_P132",
  "train":len(train),"exam":len(exam),"candidate_predictions":sum(r["predicted"]["mode"]=="CANDIDATE" for r in outcomes),
  "correct_candidates":sum(r["correct"] is True for r in outcomes),
  "holds":sum(r["predicted"]["mode"]=="DOUBT" for r in outcomes),
  "observed_only":True,"semantic_object_recognition_proven":False,
  "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
 write(d/"SEALED_EXAM_RESULTS.json",outcomes);write(d/"MASTER_REPORT.json",report)
 return report
def main():
 p=argparse.ArgumentParser();p.add_argument("--scenes",required=True);p.add_argument("--out",required=True);p.add_argument("--previous")
 a=p.parse_args();print(json.dumps(experiment(a.scenes,a.out,a.previous),indent=2))
if __name__=="__main__":main()
