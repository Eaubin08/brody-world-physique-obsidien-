"""P133: heterogeneous visual skills, explicit geometry/occlusion/composition.

Deterministic 2D observations, no pretrained semantic classifier and no 3D claim.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from PIL import Image,ImageDraw
from .image_structural_observation_v1 import describe
from .fusion_f9_intensive_education_v0 import digest

def parts(image):
    d=describe(image)
    return d["parts"]
def geometry(image):
    pp=parts(image)
    result=[]
    for p in pp:
        x0,y0,x1,y1=p["bbox"];w=x1-x0+1;h=y1-y0+1
        result.append({"bbox":p["bbox"],"width":w,"height":h,
            "ratio":round(w/h,4),"area":p["size"],
            "shape":"elongated_h" if w>1.6*h else "elongated_v" if h>1.6*w else "compact"})
    return result
def distance(a,b):
    if not a or not b:return float("inf")
    return abs(math.log(max(a["ratio"],1e-6)/max(b["ratio"],1e-6)))+abs(math.log(a["area"]/b["area"]))
def match(before,after,max_cost=0.65):
    aa=geometry(before);bb=geometry(after)
    pairs=[];available=set(range(len(bb)))
    for i,item in enumerate(aa):
        scored=sorted((distance(item,bb[j]),j) for j in available)
        if scored and scored[0][0]<=max_cost:
            cost,j=scored[0];pairs.append({"old":i,"new":j,"cost":round(cost,4)})
            available.remove(j)
    return {"matched":pairs,"unmatched_old":len(aa)-len(pairs),
        "unmatched_new":len(available),"identity_confirmed":False,
        "method":"relative silhouette only"}
def mirror_invariant(a,b):
    left=geometry(a);right=geometry(b)
    return sorted((p["width"],p["height"],p["area"]) for p in left)==sorted((p["width"],p["height"],p["area"]) for p in right)
def occlusion_hypotheses(before,after):
    a=geometry(before);b=geometry(after)
    if len(a)>len(b):
        return {"status":"DOUBT","hypotheses":["OCCLUSION","MERGE","REMOVAL"],
            "observable_change":"COMPONENT_COUNT_DECREASED","causality_proven":False}
    if len(a)<len(b):
        return {"status":"DOUBT","hypotheses":["REAPPEARANCE","SPLIT","ADDITION"],
            "observable_change":"COMPONENT_COUNT_INCREASED","causality_proven":False}
    return {"status":"OBSERVATION","hypotheses":["UNCHANGED_COUNT","HIDDEN_TRANSFORMATION"],
            "observable_change":"SAME_COMPONENT_COUNT","causality_proven":False}
def compose(spec,out):
    if not isinstance(spec,list) or not 1<=len(spec)<=8:raise ValueError("INVALID_SCENE_PROGRAM")
    im=Image.new("RGB",(64,64),"white");draw=ImageDraw.Draw(im)
    for obj in spec:
        bbox=obj.get("bbox");tone=obj.get("tone","black")
        if not isinstance(bbox,list) or len(bbox)!=4 or any(type(v)!=int for v in bbox):
            raise ValueError("INVALID_BBOX")
        x0,y0,x1,y1=bbox
        if not (0<=x0<=x1<64 and 0<=y0<=y1<64):raise ValueError("OUT_OF_BOUNDS")
        if tone not in ("black","red","blue","green"):raise ValueError("INVALID_COLOUR")
        shape=obj.get("shape")
        if shape=="rectangle":draw.rectangle(bbox,fill=tone)
        elif shape=="ellipse":draw.ellipse(bbox,fill=tone)
        elif shape=="triangle":
            draw.polygon([(x0,(y0+y1)//2),(x1,y0),(x1,y1)],fill=tone)
        else:raise ValueError("UNKNOWN_SHAPE")
    im.save(out)
    return {"image":str(out),"objects":len(spec),"generation":"symbolic 2D composition"}
def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True)
    cases=[]
    def c(key,family,ok,detail):
        cases.append({"id":key,"family":family,"status":"PASS" if ok else "FAIL","detail":detail})
    scene1=[{"shape":"ellipse","bbox":[8,12,20,24],"tone":"red"},
            {"shape":"rectangle","bbox":[38,12,50,24],"tone":"blue"}]
    compose(scene1,root/"base.png")
    with Image.open(root/"base.png") as im:
        c("COLOUR-MULTIOBJECT","perception",len(geometry(im))==2,{"visible_components":len(geometry(im))})
        c("PROGRAM-RENDER","generation",im.getpixel((14,18))==(255,0,0) and im.getpixel((44,18))==(0,0,255),{"rendered":"base.png"})
    compose([{"shape":"ellipse","bbox":[8,12,20,24],"tone":"red"}],root/"missing.png")
    with Image.open(root/"base.png") as a,Image.open(root/"missing.png") as b:
        oc=occlusion_hypotheses(a,b)
        c("OCCLUSION-DOUBT","inference",oc["status"]=="DOUBT" and len(oc["hypotheses"])==3,oc)
    with Image.open(root/"base.png") as a:
        mirrored=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        c("MIRROR-STRUCTURE","multiview",mirror_invariant(a,mirrored),{"semantic_identity_proven":False})
        c("TRACK-TWO","scene_tracking",len(match(a,mirrored)["matched"])==2,match(a,mirrored))
    compose([{"shape":"triangle","bbox":[8,7,32,30],"tone":"green"}],root/"triangle.png")
    with Image.open(root/"triangle.png") as im:
        c("TRIANGLE-PAINT","generation",im.getpixel((20,18))==(0,128,0),{"rendered":"triangle.png"})
    bad=False
    try:compose([{"shape":"rectangle","bbox":[-1,0,10,10]}],root/"invalid.png")
    except ValueError:bad=True
    c("GEOMETRY-FAIL-CLOSED","safety",bad and not (root/"invalid.png").exists(),{"rejected":bad})
    # Intentional negative capability: missing observation cannot warrant a causal statement.
    c("CAUSAL-RESTRAINT","reasoning",not oc["causality_proven"],{"hypotheses":oc["hypotheses"]})
    report={"schema":"BRODY_MULTICAPABILITY_P133","cases":len(cases),
      "families":len({v["family"] for v in cases}),
      "pass":sum(v["status"]=="PASS" for v in cases),
      "fail":sum(v["status"]=="FAIL" for v in cases),
      "novel_real_world_learning_proven":False,"physical_360_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    evidence={"report":report,"cases":cases};evidence["digest"]=digest(evidence)
    (root/"EVIDENCE.json").write_text(json.dumps(evidence,indent=2),encoding="utf8")
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args();print(json.dumps(run(args.out),indent=2))
if __name__=="__main__":main()
