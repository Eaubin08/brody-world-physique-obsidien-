"""Brody image tool school: 10k lessons + 10k heterogeneous blind examinations.

Synthetic 64x64 drawing instruments only. No real camera physics, no sovereign
authority, no memory write, no proof of generic image understanding.
"""
from __future__ import annotations

import argparse, hashlib, json, random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

from .fusion_f9_intensive_education_v0 import (
    STYLES, SHAPES, TRAIN_TOOLS, EVAL_TOOLS,
    geometry, predict, run as run_school, digest, verify_chain,
)
from .instrument_school_v2 import TOOLS, render_instrument, _gray_pixel_loss

FAMILIES = (
    "fresh_geometry", "translation", "mirror", "rotation",
    "contrast", "blur", "sensor_noise", "part_occlusion",
    "wrong_intent", "unknown_intent",
)
SPLIT_SEED = 921764

def perturb(img: Image.Image, family: str, rng: random.Random) -> Image.Image:
    image=img.convert("L")
    if family=="translation":
        dx=rng.randint(-3,3);dy=rng.randint(-3,3)
        image=image.transform(image.size,Image.Transform.AFFINE,
                              (1,0,-dx,0,1,-dy),fillcolor=255)
    elif family=="mirror":
        image=ImageOps.mirror(image)
    elif family=="rotation":
        image=image.transpose(Image.Transpose.ROTATE_90)
    elif family=="contrast":
        image=ImageEnhance.Contrast(image).enhance(0.42)
    elif family=="blur":
        image=image.filter(ImageFilter.GaussianBlur(radius=1.2))
    elif family=="sensor_noise":
        pix=list(image.getdata())
        # Fixed noise field per case: same captured scene condition for all tools.
        for j in range(len(pix)):
            pix[j]=max(0,min(255,pix[j]+rng.randint(-16,16)))
        image.putdata(pix)
    elif family=="part_occlusion":
        from PIL import ImageDraw
        draw=ImageDraw.Draw(image)
        x=rng.randint(20,34);y=rng.randint(20,34)
        draw.rectangle((x,y,x+8,y+8),fill=255)
    return image

def common_transform(family,seed):
    # The same transformation/noise geometry MUST be applied to every candidate
    # and oracle target, to avoid cheating via tool-dependent disturbances.
    def apply(img):
        return perturb(img,family,random.Random(seed))
    return apply

def blind_challenge(policy, family, i, seed):
    rng=random.Random(seed+131071*i+FAMILIES.index(family)*7919)
    shape=SHAPES[(i//3)%len(SHAPES)]
    style=STYLES[i%len(STYLES)]
    observed_style="UNSEEN" if family=="unknown_intent" else style
    geometry_state=geometry(rng,shape)
    key=observed_style+"|"+shape
    chosen=predict(policy,key)
    transform=common_transform(family,rng.getrandbits(32))
    # Intentional distribution shift: label is misleading in wrong_intent.
    target_style=STYLES[(STYLES.index(style)+1)%len(STYLES)] if family=="wrong_intent" else style
    if chosen is not None:
        candidate=transform(render_instrument(geometry_state,chosen))
        candidate_hash=hashlib.sha256(candidate.tobytes()).hexdigest()
    else:
        candidate=None;candidate_hash=None
    # Teacher target generated only AFTER candidate has been computed and hashed.
    target=transform(render_instrument(geometry_state,EVAL_TOOLS[target_style]))
    losses={tool:_gray_pixel_loss(transform(render_instrument(geometry_state,tool)),target)
            for tool in TOOLS}
    best=min(losses.values())
    chosen_loss=_gray_pixel_loss(candidate,target) if candidate is not None else None
    return {
        "family":family,"test_index":i,"held":chosen is None,
        "tool":chosen,"candidate_sha256":candidate_hash,
        "loss":chosen_loss,"oracle_min_loss":best,
        "regret":None if chosen_loss is None else chosen_loss-best,
        "oracle_best_tool":min(TOOLS,key=lambda x:(losses[x],TOOLS.index(x))),
        "candidate_sealed_before_teacher":True,
        "teacher_test_only":True,
        "non_sovereign":True,
    }

def evaluate(policy,count,seed,output):
    if count<10 or count%len(FAMILIES):raise ValueError("exam count must be divisible by 10")
    tally={family:[] for family in FAMILIES}
    previous=None
    with output.open("x",encoding="utf-8") as f:
        for i in range(1,count+1):
            family=FAMILIES[(i-1)%len(FAMILIES)]
            case=blind_challenge(policy,family,i,seed)
            tally[family].append(case)
            row={"index":i,"previous":previous,**case,
                 "native_memory_write":False,"canonical_promotion":False,
                 "decision_authority":"KX108_ONLY"}
            row["digest"]=digest(row)
            f.write(json.dumps(row,sort_keys=True)+"\n")
            previous=row["digest"]
    n,tip=verify_chain(output)
    if n!=count:raise RuntimeError("exam receipts incomplete")
    by_family={}
    for family,records in tally.items():
        scored=[r for r in records if r["loss"] is not None]
        by_family[family]={
            "cases":len(records),"holds":sum(x["held"] for x in records),
            "evaluated":len(scored),
            "mean_loss":mean(x["loss"] for x in scored) if scored else None,
            "mean_regret":mean(x["regret"] for x in scored) if scored else None,
            "oracle_tool_match":sum(x["tool"]==x["oracle_best_tool"] for x in scored),
        }
    return {"cases":n,"receipt_tip":tip,"families":by_family,
            "target_generator_shared_with_training":True,
            "synthetic_perturbations_only":True}

def run(out,train=10000,exams=10000,seed=20261009,checkpoint=1000):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EXISTING_EVIDENCE")
    if train<1000 or train>100000 or exams<100 or exams>100000:
        raise ValueError("unsupported campaign size")
    root.mkdir(parents=True)
    training=run_school(root/"training",episodes=train,seed=seed,checkpoint=checkpoint)
    # Frozen state produced by the learner, not reconstructed from the TEST oracle.
    last=root/"training"/("snapshot-%06d.json"%train)
    snap=json.loads(last.read_text(encoding="utf-8"))
    if snap["hash"]!=digest(snap["candidate_stats"]):
        raise RuntimeError("FROZEN_SKILL_TAMPERED")
    policy=snap["candidate_stats"]
    examination=evaluate(policy,exams,seed+SPLIT_SEED,root/"blind_exam_receipts.jsonl")
    report={
      "schema":"BRODY_IMAGE_TOOL_SCHOOL_10K_TRAIN_10K_MULTIDIRECTION_V0",
      "training":{"episodes":training["completed_episodes"],
                  "changes":training["policy_changes_on_train"],
                  "training_tip":training["receipt_tip"],
                  "checkpoints":training["checkpoints"],
                  "final_policy":training["final_policy"]},
      "exam":examination,
      "benchmark_limitations":[
        "64x64 synthetic imagery",
        "teacher and pupil share the same renderer",
        "tool selection only; not generic perception or physics",
        "wrong_intent is intentionally misleading, not independently detectable",
        "noise and occlusion are reproducible artificial perturbations",
        "no external dataset, independent real sensor or model-weight training",
      ],
      "memory_candidate_only":True,
      "native_memory_write":False,"kernel_mutation":False,
      "source_attestation_verified":False,
      "decision_authority":"KX108_ONLY",
      "status":"SYNTHETIC_TOOL_SCHOOL_MEASURED_NOT_REAL_WORLD_PROOF",
    }
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    ap.add_argument("--train",type=int,default=10000)
    ap.add_argument("--exams",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=20261009)
    ap.add_argument("--checkpoint",type=int,default=1000)
    a=ap.parse_args()
    report=run(a.out,a.train,a.exams,a.seed,a.checkpoint)
    print(json.dumps({"schema":report["schema"],"train":report["training"]["episodes"],
      "exams":report["exam"]["cases"],"families":report["exam"]["families"],
      "status":report["status"]},indent=2))
if __name__=="__main__":main()
