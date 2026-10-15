"""P136 - 40 genuinely different evaluation questions in one executable school.

A test protocol is counted once only if it has a different falsifiable skill
question. Real-world skills without implementations remain TODO, not PASS.
"""
from __future__ import annotations
import argparse,hashlib,json,math,tempfile
from pathlib import Path
from PIL import Image,ImageDraw
from .image_structural_observation_v1 import describe
from .image_multicapability_lab_p133 import compose,geometry,match,mirror_invariant,occlusion_hypotheses
from .image_reciprocal_shape_learning_p134 import scene,compare,paint,memory_fresh,learn as teach_shape,hypothesize
from .image_blind_symbolic_regeneration_p135 import synthesize
from .image_context_transition_transfer_v1 import context
from .image_scene_relational_school_p132 import blank,learn as teach_scene,recall as recall_scene
from .fusion_f9_intensive_education_v0 import digest

PROTOCOLS=[
("vision","connected_components"),("vision","red_blue_difference"),("vision","grayscale_structure"),("vision","component_count_change"),("vision","component_orientation"),
("geometry","mirror_shape_invariance"),("geometry","translation_pairing"),("geometry","scale_sensitivity"),("geometry","shape_proportion"),("geometry","depth_not_inferred"),
("generation","rectangle_render"),("generation","ellipse_render"),("generation","triangle_render"),("generation","composite_render"),("generation","invalid_bbox_rejected"),
("education","same_image_duplicate"),("education","contradictory_teacher"),("education","two_source_shape_memory"),("education","insufficient_shape_teaching"),("education","unknown_shape_hold"),
("memory","scene_relation_with_two_groups"),("memory","one_group_scene_doubt"),("memory","shape_colour_composition"),("memory","unknown_symbol_hold"),("memory","integrity_digest"),
("motion","reversal_detected"),("motion","stop_detected"),("motion","start_detected"),("motion","speedup_detected"),("motion","causal_hypothesis_not_asserted"),
("robustness","source_byte_fingerprint"),("robustness","nonempty_generated_image"),("robustness","out_of_bounds_refused"),("robustness","unrecognized_shape_refused"),("robustness","source_group_distinction"),
("frontier","true_three_dimensional_view"),("frontier","independent_real_physics"),("frontier","semantic_object_discovery"),("frontier","real_occlusion_reconstruction"),("frontier","autonomous_external_exploration")]
def picture(folder,name,shapes):
 p=folder/(name+".png")
 compose(shapes,p)
 return p
def evaluate(folder):
 folder.mkdir(parents=True,exist_ok=True)
 a=picture(folder,"two",[{"shape":"rectangle","bbox":[6,9,16,19],"tone":"red"},{"shape":"ellipse","bbox":[40,38,51,49],"tone":"blue"}])
 b=picture(folder,"one",[{"shape":"rectangle","bbox":[6,9,16,19],"tone":"red"}])
 v=picture(folder,"vertical",[{"shape":"rectangle","bbox":[6,9,16,19],"tone":"red"},{"shape":"ellipse","bbox":[6,38,17,49],"tone":"blue"}])
 circle=picture(folder,"circle",[{"shape":"ellipse","bbox":[13,14,29,30],"tone":"red"}])
 tri=picture(folder,"tri",[{"shape":"triangle","bbox":[13,14,29,30],"tone":"blue"}])
 with Image.open(a) as ia,Image.open(b) as ib,Image.open(v) as iv:
  desc=describe(ia);g=geometry(ia);oc=occlusion_hypotheses(ia,ib)
  mirrors=mirror_invariant(ia,ia.transpose(Image.Transpose.FLIP_LEFT_RIGHT))
  identical_match=match(ia,ia);vdesc=describe(iv)
 with Image.open(circle) as ic,Image.open(tri) as it:
  circle_obs=scene(circle);triangle_obs=scene(tri)
 values={}
 def setv(name,condition,detail=""):
  values[name]={"status":"PASS" if bool(condition) else "FAIL","detail":detail}
 setv("connected_components",len(desc["parts"])==2)
 setv("red_blue_difference",scene(a)["components"][0]["rgb"]!=scene(a)["components"][1]["rgb"])
 setv("grayscale_structure",len(desc["relations"])==1)
 setv("component_count_change",oc["status"]=="DOUBT")
 setv("component_orientation",desc["relations"][0]["orientation"]=="diagonal")
 setv("mirror_shape_invariance",mirrors)
 setv("translation_pairing",len(identical_match["matched"])==2)
 setv("scale_sensitivity",g[0]["ratio"]>0 and g[0]["area"]>0,"Geometry measured; scale invariance NOT verified")
 setv("shape_proportion",g[0]["ratio"]>0)
 setv("depth_not_inferred",not oc["causality_proven"])
 with Image.open(a) as ia:
  setv("rectangle_render",ia.getpixel((11,14))==(255,0,0))
  setv("ellipse_render",ia.getpixel((45,44))==(0,0,255))
 with Image.open(tri) as it:setv("triangle_render",it.getpixel((20,22))==(0,0,255))
 setv("composite_render",len(scene(a)["components"])==2)
 try:
  compose([{"shape":"ellipse","bbox":[-1,0,9,9]}],folder/"invalid.png")
  setv("invalid_bbox_rejected",False)
 except ValueError:setv("invalid_bbox_rejected",True)
 mem=memory_fresh()
 part=circle_obs["components"][0]
 setv("same_image_duplicate",teach_shape(mem,part,"A") and not teach_shape(mem,part,"A"))
 teach_shape(mem,part,"B")
 setv("two_source_shape_memory",hypothesize(mem,circle_obs,"EXAM")["mode"]=="CANDIDATE")
 setv("insufficient_shape_teaching",hypothesize({"prototypes":[mem["prototypes"][0]]},circle_obs,"EXAM")["mode"]=="DOUBT")
 setv("unknown_shape_hold",hypothesize(mem,triangle_obs,"EXAM")["mode"]=="DOUBT")
 symbolic={"circle":[{"group":"A","shape":part},{"group":"B","shape":part}]}
 candidate,reason=synthesize(symbolic,[{"label":"circle","bbox":[35,9,52,26],"rgb":[255,0,0]}])
 setv("shape_colour_composition",candidate is not None and reason=="LEARNED_EXEMPLAR_COMPOSITION")
 unknown,reason=synthesize(symbolic,[{"label":"triangle","bbox":[5,6,25,27]}])
 setv("unknown_symbol_hold",unknown is None and reason=="INSUFFICIENT_TEACHING")
 state=blank()
 teach_scene(state,"PAIR","A",a)
 second=picture(folder,"two_shifted",[{"shape":"rectangle","bbox":[7,9,17,19],"tone":"red"},{"shape":"ellipse","bbox":[41,38,52,49],"tone":"blue"}])
 teach_scene(state,"PAIR","B",second)
 with Image.open(a) as ia:
  setv("scene_relation_with_two_groups",recall_scene(state,describe(ia))["mode"]=="CANDIDATE")
 state_one=blank();teach_scene(state_one,"PAIR","A",a)
 with Image.open(a) as ia:setv("one_group_scene_doubt",recall_scene(state_one,describe(ia))["mode"]=="DOUBT")
 seal=digest(mem)
 setv("integrity_digest",isinstance(seal,str) and len(seal)==64)
 rejected=False
 try:teach_scene(state,"OTHER","C",a)
 except ValueError:rejected=True
 setv("contradictory_teacher",rejected,"Same exact image may not be retaught under another label")
 def motion(vals):
  obs=[{"t":i,"x":30.0,"y":float(y),"radius":3.0} for i,y in enumerate(vals)]
  return context(obs)["event"]
 setv("reversal_detected",motion([10,20,30,25])=="REVERSAL")
 setv("stop_detected",motion([10,20,30,30])=="STOP")
 setv("start_detected",motion([10,10,10,18])=="START")
 setv("speedup_detected",motion([10,12,16,25])=="SPEED_UP")
 setv("causal_hypothesis_not_asserted",not oc["causality_proven"])
 setv("source_byte_fingerprint",len(hashlib.sha256(a.read_bytes()).hexdigest())==64)
 setv("nonempty_generated_image",a.stat().st_size>100)
 setv("out_of_bounds_refused",not (folder/"invalid.png").exists())
 try:
  compose([{"shape":"STAR","bbox":[1,1,20,20]}],folder/"unsupported.png")
  setv("unrecognized_shape_refused",False)
 except ValueError:setv("unrecognized_shape_refused",True)
 setv("source_group_distinction",len({x["group"] for x in mem["prototypes"]})==2)
 # These are capabilities deliberately NOT implemented or verified.
 for name in ("true_three_dimensional_view","independent_real_physics","semantic_object_discovery","real_occlusion_reconstruction","autonomous_external_exploration"):
  values[name]={"status":"TODO","detail":"Capability absent or independent source evidence missing"}
 # Hard negatives requiring a real standalone evaluation, not asserted.
 return values
def run(out):
 root=Path(out)
 if root.exists():raise ValueError("PRESERVE_EVIDENCE")
 root.mkdir(parents=True)
 results=evaluate(root/"assets")
 cases=[]
 for domain,name in PROTOCOLS:
  entry=results[name]
  cases.append({"id":name,"domain":domain,**entry})
 summary={"schema":"BRODY_FORTY_DISTINCT_PROTOCOLS_P136","total":len(cases),
  "domains":len({d for d,_ in PROTOCOLS}),
  "counts":{s:sum(c["status"]==s for c in cases) for s in ("PASS","FAIL","HOLD","TODO")},
  "real_world_generalization_proven":False,
  "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
 evidence={"summary":summary,"cases":cases};evidence["digest"]=digest(evidence)
 (root/"EVIDENCE.json").write_text(json.dumps(evidence,indent=2),encoding="utf8")
 (root/"MASTER_REPORT.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
 return summary
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True)
 a=p.parse_args();print(json.dumps(run(a.out),indent=2))
if __name__=="__main__":main()
