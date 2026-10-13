"""P135: blind scene regeneration from symbolic prompts, learned examples only.

Exam target image is opened only AFTER candidate generation is saved. The
prompt contains labels, relative bounding boxes and palette request, not
pixels/masks from the target. No real-world generalization is implied.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image
from .image_reciprocal_shape_learning_p134 import scene,paint,compare
from .fusion_f9_intensive_education_v0 import digest
def put(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
def sig(part):
 w,h=part["size"];return (round(w/h,2),round(part["area"]/(w*h),2))
def learn(rows):
 memory={}
 for r in rows:
  if r["split"]!="train":continue
  observed=scene(r["file"])
  if len(observed["components"])!=1:raise ValueError("TRAIN_ONE_COMPONENT_REQUIRED")
  p=observed["components"][0]
  memory.setdefault(r["label"],[]).append({"group":r["group"],"shape":p})
 return memory
def synthesize(memory,prompt):
 result=[]
 for item in prompt:
  label=item["label"];bbox=item["bbox"]
  if not isinstance(bbox,list) or len(bbox)!=4 or not all(type(v)==int for v in bbox):return None,"INVALID_BBOX"
  x0,y0,x1,y1=bbox
  if not (0<=x0<x1<64 and 0<=y0<y1<64):return None,"INVALID_BOUNDS"
  exemplars=memory.get(label,[])
  if len({e["group"] for e in exemplars})<2:return None,"INSUFFICIENT_TEACHING"
  shapes={sig(e["shape"]) for e in exemplars}
  if len(shapes)>2:return None,"AMBIGUOUS_LABEL"
  proto=exemplars[0]["shape"];ow,oh=proto["size"];nw=x1-x0+1;nh=y1-y0+1
  mask=sorted(set((min(nw-1,round(x*(nw-1)/max(ow-1,1))),
                   min(nh-1,round(y*(nh-1)/max(oh-1,1)))) for x,y in proto["mask"]))
  rgb=item.get("rgb",proto["rgb"])
  if not isinstance(rgb,(list,tuple)) or len(rgb)!=3 or not all(type(x)==int and 0<=x<=255 for x in rgb):
   return None,"INVALID_COLOUR"
  result.append({"bbox":bbox,"size":[nw,nh],"rgb":rgb,"mask":[list(p) for p in mask]})
 return result,"LEARNED_EXEMPLAR_COMPOSITION"
def run(manifest,out):
 dest=Path(out)
 if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
 rows=json.loads(Path(manifest).read_text(encoding="utf8-sig"))
 if not isinstance(rows,list) or not rows:raise ValueError("EMPTY_MANIFEST")
 train=[r for r in rows if r.get("split")=="train"]
 exam=[r for r in rows if r.get("split")=="exam"]
 if not train or not exam:raise ValueError("BOTH_SPLITS_REQUIRED")
 if {r["group"] for r in train}&{r["group"] for r in exam}:raise ValueError("SOURCE_GROUP_LEAK")
 # Do not open any exam image until all predictions are saved.
 observed_train={r["group"]:hashlib.sha256(Path(r["file"]).read_bytes()).hexdigest() for r in train}
 if len(observed_train)!=len(train):raise ValueError("DUPLICATE_TRAIN_GROUP")
 memory=learn(train)
 dest.mkdir(parents=True)
 predictions=[]
 for i,row in enumerate(exam):
  parts,status=synthesize(memory,row["prompt"])
  out_image=dest/f"predicted_{i:03d}.png"
  if parts is not None:paint(parts,out_image)
  predictions.append({"group":row["group"],"mode":"CANDIDATE" if parts is not None else "DOUBT",
     "reason":status,"output":str(out_image) if parts is not None else None,
     "prompt_sha256":digest(row["prompt"])})
 put(dest/"SEALED_BEFORE_EXAM.json",{"predictions":predictions,
   "exam_pixels_read_before_prediction":False,"native_memory_write":False,"canonical_promotion":False})
 results=[]
 for row,pred in zip(exam,predictions):
  truth=Path(row["file"])
  actual_sha=hashlib.sha256(truth.read_bytes()).hexdigest()
  if actual_sha in observed_train.values():raise ValueError("EXAM_IMAGE_LEAK")
  quality=compare(pred["output"],truth) if pred["mode"]=="CANDIDATE" else None
  results.append({**pred,"target_sha256":actual_sha,"quality":quality})
 report={"schema":"BRODY_BLIND_PROMPT_RECIPROCAL_P135","train":len(train),"exam":len(exam),
   "candidates":sum(x["mode"]=="CANDIDATE" for x in results),
   "holds":sum(x["mode"]=="DOUBT" for x in results),
   "avg_mae_candidates":round(sum(x["quality"]["mae_rgb"] for x in results if x["quality"])/max(1,sum(x["quality"] is not None for x in results)),5),
   "exam_target_not_used_in_generation":True,
   "prompt_supplies_bbox_and_colour":True,
   "independent_provenance_verified":False,"real_world_generalization_proven":False,
   "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
 put(dest/"CANDIDATE_MEMORY.json",{"labels":memory,"digest":digest(memory)})
 put(dest/"EXAM_RESULTS.json",results);put(dest/"MASTER_REPORT.json",report)
 return report
def main():
 p=argparse.ArgumentParser();p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
 a=p.parse_args();print(json.dumps(run(a.manifest,a.out),indent=2))
if __name__=="__main__":main()
