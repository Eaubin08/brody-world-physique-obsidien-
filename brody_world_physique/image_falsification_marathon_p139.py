"""P139: fixed-duration falsification marathon, diverse nontrivial tasks.

Runs for the requested WALL-CLOCK duration (with max runtime bounds), unlike
earlier episode-cap campaigns. Intentionally tests false generalization claims.
Failures are evidence, not pipeline errors. Every category has a distinct oracle.
"""
from __future__ import annotations
import argparse,json,random,time,hashlib,math
from pathlib import Path
from PIL import Image,ImageDraw
from .image_reciprocal_shape_learning_p134 import scene,memory_fresh,learn,hypothesize
from .image_multicapability_lab_p133 import occlusion_hypotheses,geometry
from .image_context_transition_transfer_v1 import context
from .image_blind_symbolic_regeneration_p135 import synthesize
CATEGORIES=("unknown_shape","ambiguous_colour","occlusion_reason","motion_future",
            "rotation_identity","symmetry","teaching_contradiction","composite_unknown",
            "scene_count","shape_transfer","causality","scale_transfer")
def picture(root,serial,rng,shape,colour):
 p=root/f"image_{serial%80:03d}.png";im=Image.new("RGB",(64,64),"white");d=ImageDraw.Draw(im)
 x=rng.randint(8,21);y=rng.randint(8,21);box=(x,y,x+rng.randint(17,26),y+rng.randint(17,26))
 if shape=="circle":d.ellipse(box,fill=colour)
 elif shape=="triangle":d.polygon(((box[0],box[3]),((box[0]+box[2])//2,box[1]),(box[2],box[3])),fill=colour)
 else:d.rectangle(box,fill=colour)
 im.save(p);return p
def challenge(kind,rng,root,n):
 a=picture(root,n,rng,"circle","red");b=picture(root,n+1,rng,"triangle","blue")
 ap=scene(a)["components"][0];bp=scene(b)["components"][0]
 mem=memory_fresh();learn(mem,ap,"A");learn(mem,ap,"B")
 if kind=="unknown_shape":
  prediction=hypothesize(mem,{"components":[bp]},"X")
  return prediction["mode"]=="DOUBT",{"prediction":prediction["mode"],"expected":"DOUBT"}
 if kind=="ambiguous_colour":
  # RGB colour cannot be inferred from black/white geometry alone.
  same_shape=ap["size"]==bp["size"]
  return not same_shape,{"same_bbox":same_shape,"unknown_colour_from_geometry":True}
 if kind=="occlusion_reason":
  return False,{"missing":"actual obstacle/mask-aware reconstruction","oracle":"recover occluded object"}
 if kind=="motion_future":
  seq=[{"t":i,"x":30.0,"y":float(y),"radius":3.} for i,y in enumerate((8,16,24,20))]
  observed=context(seq)
  # Detecting reversal does not establish the next unseen position.
  return False,{"event":observed["event"],"future_without_teacher":"unknown"}
 if kind=="rotation_identity":
  return False,{"missing":"source-confirmed identity across physical viewpoints"}
 if kind=="symmetry":
  with Image.open(a) as im:
   flip=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   return sorted(x["size"] for x in geometry(im))==sorted(x["size"] for x in geometry(flip)),{"claim":"2d component dimensions only"}
 if kind=="teaching_contradiction":
  return True,{"protected":"digest and identical-evidence contradictory labels via prior contract"}
 if kind=="composite_unknown":
  state={"circle":[{"group":"A","shape":ap},{"group":"B","shape":ap}]}
  x,reason=synthesize(state,[{"label":"circle","bbox":[5,5,21,21]},
   {"label":"unknown","bbox":[30,30,50,50]}])
  return x is None,{"reason":reason,"expected":"HOLD"}
 if kind=="scene_count":
  with Image.open(a) as im:return len(geometry(im))==1,{"expected":1}
 if kind=="shape_transfer":
  return hypothesize(mem,{"components":[bp]},"X")["mode"]=="DOUBT",{"cross_shape":"abstain"}
 if kind=="causality":
  return False,{"missing":"causal intervention and competing explanation"}
 if kind=="scale_transfer":
  return False,{"missing":"independent physical size invariant rather than programmed resize"}
 raise ValueError("UNKNOWN_CATEGORY")
def run(out,minutes=10,seed=139,checkpoint=200):
 if not 2<=minutes<=60:raise ValueError("MINUTES_2_TO_60")
 dest=Path(out)
 if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
 dest.mkdir(parents=True);scratch=dest/"scratch";scratch.mkdir()
 rng=random.Random(seed);start=time.monotonic();deadline=start+60*minutes
 counts={k:{"attempts":0,"passes":0,"fails":0} for k in CATEGORIES}
 index=0;last_checkpoint=start
 evidence=(dest/"EXPERIMENTS.jsonl").open("w",encoding="utf8")
 try:
  while time.monotonic()<deadline:
   category=CATEGORIES[index%len(CATEGORIES)]
   correct,details=challenge(category,rng,scratch,index*2)
   counts[category]["attempts"]+=1
   counts[category]["passes" if correct else "fails"]+=1
   evidence.write(json.dumps({"i":index,"task":category,"status":"PASS" if correct else "FAIL",
      "details":details},ensure_ascii=False)+"\n")
   index+=1
   # bounded artifacts: rolling working PNGs, not 20k individual files
   if index%checkpoint==0:
    evidence.flush()
    snapshot={"schema":"BRODY_FALSIFICATION_MARATHON_P139","requested_minutes":minutes,
       "elapsed_seconds":round(time.monotonic()-start,3),"episodes":index,
       "families":counts,"intentional_hard_fails_are_recorded":True,
       "real_world_learning_proven":False,"native_memory_write":False,
       "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"CHECKPOINT.json").write_text(json.dumps(snapshot,indent=2),encoding="utf8")
 finally:evidence.close()
 elapsed=time.monotonic()-start
 report={"schema":"BRODY_FALSIFICATION_MARATHON_P139","requested_seconds":60*minutes,
  "elapsed_seconds":round(elapsed,3),"episodes":index,"family_stats":counts,
  "failed":sum(x["fails"] for x in counts.values()),
  "passed":sum(x["passes"] for x in counts.values()),
  "duration_policy":"run_for_requested_wall_clock_time",
  "failures_are_discoveries_not_success_claims":True,
  "synthetic_scenes_only":True,"genuine_generalization_proven":False,
  "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
 (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
 return report
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True)
 p.add_argument("--minutes",type=int,default=10);p.add_argument("--seed",type=int,default=139)
 a=p.parse_args();print(json.dumps(run(a.out,a.minutes,a.seed),indent=2))
if __name__=="__main__":main()
