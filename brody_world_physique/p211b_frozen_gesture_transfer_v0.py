"""P2.11b: persist validated TRAIN gestures, then render them without TEST pixels.

A preprogrammed motor transfer baseline, not general image synthesis. TRAIN
reference is visible when extracting gestures; TEST target only for scoring
after image output is sealed.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image
from .drawing_school_v0 import SIDE
from .drawing_school_v1 import suggest_gestures_from_reference,render
from .experience_memory_v1 import checked_gesture,gesture_snapshot,code_fingerprint
from .p210a_visual_loop_contract_v0 import digest,open_rgba,pixel_error
from .p210d_visual_error_memory_bridge_v0 import hexdigest

SCHEMA="BRODY_P211B_FROZEN_GESTURE_V0"

def learn(train_image,memory):
    path=Path(memory)
    if path.exists():raise ValueError("memory exists")
    source=open_rgba(train_image)
    if source.size!=(SIDE,SIDE):raise ValueError("drawing-school dimensions")
    gestures=suggest_gestures_from_reference(source)
    if not gestures:raise ValueError("no learnable gestures")
    snapshot=[gesture_snapshot(g) for g in gestures]
    checked=[checked_gesture(g) for g in snapshot]
    if len(checked)!=len(gestures):raise ValueError("gesture validation")
    data={"schema":SCHEMA,"train_sha256":digest(train_image),
          "gestures":snapshot,"motor_code":code_fingerprint("drawing-motor-render"),
          "learning_code":code_fingerprint("image-thinning"),
          "teacher_seen_in_train":True,"native_memory_write":False,
          "knowledge_promotion":False}
    data["receipt_digest"]=hexdigest(data)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return data

def read(memory):
    x=json.loads(Path(memory).read_text(encoding="utf-8"))
    if x.get("schema")!=SCHEMA or x.get("native_memory_write") is not False or x.get("knowledge_promotion") is not False:
        raise ValueError("memory contract")
    if x.get("receipt_digest")!=hexdigest({k:v for k,v in x.items() if k!="receipt_digest"}):
        raise ValueError("memory altered")
    for cap,key in (("drawing-motor-render","motor_code"),("image-thinning","learning_code")):
        if x[key]!=code_fingerprint(cap):raise ValueError("code version drift")
    if not 1<=len(x["gestures"])<=128:raise ValueError("gesture budget")
    return x,tuple(checked_gesture(g) for g in x["gestures"])

def generate(memory,out,reference=None):
    record,gestures=read(memory)
    out=Path(out)
    if out.exists() or out.with_suffix(".json").exists():raise ValueError("output exists")
    candidate=render(gestures)
    out.parent.mkdir(parents=True,exist_ok=True)
    candidate.save(out)
    sealed=digest(out)
    data={"schema":"BRODY_P211B_GENERATION_V0","memory_sha256":digest(memory),
          "candidate_sha256":sealed,"method":"FROZEN_TRAIN_GESTURES",
          "gestures_replayed":len(gestures),
          "sealed_before_test_reference":True,
          "learned_content_reused":True,
          "no_test_image_in_generation":True,
          "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    if reference:
        ref=open_rgba(reference)
        if ref.size!=(SIDE,SIDE):raise ValueError("test dimensions")
        data["reference_sha256"]=digest(reference)
        data["candidate_pixel_error"]=pixel_error(ref,candidate.convert("RGBA"))
        data["blank_pixel_error"]=pixel_error(ref,Image.new("RGBA",ref.size,"white"))
    out.with_suffix(".json").write_text(json.dumps(data,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return data

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--train");p.add_argument("--memory",required=True)
    p.add_argument("--out");p.add_argument("--reference")
    a=p.parse_args()
    if a.train and not a.out:r=learn(a.train,a.memory)
    elif a.out and not a.train:r=generate(a.memory,a.out,a.reference)
    else:p.error("provide --train OR --out")
    print(json.dumps({"schema":r["schema"],"status":"EXPERIMENTAL_GESTURE_MEMORY"}))
if __name__=="__main__":main()
