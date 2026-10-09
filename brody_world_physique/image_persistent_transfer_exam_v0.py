"""Persistent candidate learning from supervised episodes, tested blind on fresh geometry.

An instrument-routing benchmark with experimental family metadata exposed to
the learner; NOT autonomous semantic perception, external-world generalization,
or sovereign/native memory learning.
"""
from __future__ import annotations
import argparse,json,random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from .fusion_f9_intensive_education_v0 import STYLES,SHAPES,EVAL_TOOLS,geometry,predict,digest,verify_chain
from .instrument_school_v2 import TOOLS,render_instrument,_gray_pixel_loss
from .image_tool_school_20k_campaign_v0 import FAMILIES,common_transform

def context(family,style,shape):
    return family+"|"+style+"|"+shape

def select(experience,key,fallback):
    table=experience.get(key)
    if table:
        return min(TOOLS,key=lambda t:(table[t]["sum"]/table[t]["n"],TOOLS.index(t)))
    return fallback

def make_scene(i,seed):
    family=FAMILIES[(i-1)%10]
    rng=random.Random(seed+131071*i+FAMILIES.index(family)*7919)
    shape=SHAPES[(i//3)%4];style=STYLES[i%3]
    advertised="UNSEEN" if family=="unknown_intent" else style
    gestures=geometry(rng,shape)
    transform=common_transform(family,rng.getrandbits(32))
    return family,style,shape,advertised,gestures,transform

def one(i,seed,base,experience,training):
    family,style,shape,advertised,gestures,transform=make_scene(i,seed)
    fallback=predict(base,advertised+"|"+shape)
    key=context(family,advertised,shape)
    choice=select(experience,key,fallback) if fallback is not None else None
    initial=transform(render_instrument(gestures,choice)) if choice else None
    baseline=transform(render_instrument(gestures,fallback)) if fallback else None
    sealed=digest({"i":i,"family":family,"tool":choice,"fallback":fallback,
                   "image":initial.tobytes().hex() if initial else None})
    # Teacher revealed only after both choices and images have been committed.
    target_style=STYLES[(STYLES.index(style)+1)%3] if family=="wrong_intent" else style
    target=transform(render_instrument(gestures,EVAL_TOOLS[target_style]))
    loss=_gray_pixel_loss(initial,target) if initial else None
    baseline_loss=_gray_pixel_loss(baseline,target) if baseline else None
    if training and choice is not None:
        # All tools explored exclusively in TRAIN: evaluation never updates.
        losses={t:_gray_pixel_loss(transform(render_instrument(gestures,t)),target) for t in TOOLS}
        record=experience.setdefault(key,{t:{"sum":0.0,"n":0} for t in TOOLS})
        for t in TOOLS:
            record[t]["sum"]+=losses[t];record[t]["n"]+=1
    return {"family":family,"index":i,"tool":choice,"baseline_tool":fallback,
      "loss":loss,"baseline_loss":baseline_loss,"frozen_before_target_sha256":sealed,
      "feedback_used_for_learning":training and choice is not None,
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}

def score(rows):
    result={}
    for family in FAMILIES:
        entries=[r for r in rows if r["family"]==family]
        scored=[r for r in entries if r["loss"] is not None]
        result[family]={"cases":len(entries),"held":len(entries)-len(scored),
          "before_mean_loss":mean(r["baseline_loss"] for r in scored) if scored else None,
          "after_mean_loss":mean(r["loss"] for r in scored) if scored else None,
          "improved":sum(r["loss"]<r["baseline_loss"]-1e-10 for r in scored),
          "worsened":sum(r["loss"]>r["baseline_loss"]+1e-10 for r in scored)}
    return result

def run(out,snapshot,train=10000,exam=10000,seed=160120):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EXISTING_EVIDENCE")
    if min(train,exam)<100 or train%10 or exam%10:raise ValueError("REQUIRE_BALANCED_EPISODES")
    freeze=json.loads(Path(snapshot).read_text(encoding="utf-8"))
    base=freeze["candidate_stats"]
    if freeze["hash"]!=digest(base):raise ValueError("SNAPSHOT_TAMPERED")
    experiences={};root.mkdir(parents=True)
    # Independent deterministic seeds; each split has distinct geometries.
    train_rows=[one(i,seed,base,experiences,True) for i in range(1,train+1)]
    frozen=json.loads(json.dumps(experiences,sort_keys=True))
    (root/"candidate_skills.json").write_text(json.dumps({
      "skills":frozen,"digest":digest(frozen),"native_memory_write":False},indent=2)+"\n")
    prior=None;rows=[]
    with (root/"blind_receipts.jsonl").open("x",encoding="utf-8") as f:
        for i in range(1,exam+1):
            event=one(i,seed+7700007,base,frozen,False)
            rows.append(event)
            record={"index":i,"previous":prior,**event}
            record["digest"]=digest(record)
            f.write(json.dumps(record,sort_keys=True)+"\n")
            prior=record["digest"]
    n,tip=verify_chain(root/"blind_receipts.jsonl")
    if n!=exam or digest(frozen)!=digest(experiences):raise RuntimeError("BLIND_LEAKAGE_OR_INTEGRITY")
    metrics=score(rows)
    report={"schema":"BRODY_IMAGE_PERSISTENT_TOOL_TRANSFER_EXAM_V0",
      "train_episodes":train,"blind_exam_episodes":n,"blind_receipt_tip":tip,
      "skill_contexts":len(frozen),"families":metrics,
      "score_before_after_comparable":True,
      "blind_exam_feedback_used_for_training":False,
      "family_label_available_to_learner":True,
      "test_and_train_share_simulated_renderer":True,
      "different_seed_heldout_geometry":True,
      "unknown_intent_can_still_hold":True,
      "no_cross_domain_generalization_proven":True,
      "native_memory_write":False,"kernel_mutation":False,
      "decision_authority":"KX108_ONLY",
      "status":"SYNTHETIC_CROSS_EPISODE_TRANSFER_MEASURED_NOT_REAL_IMAGE_LEARNING"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);p.add_argument("--snapshot",required=True)
    p.add_argument("--train",type=int,default=10000);p.add_argument("--exam",type=int,default=10000)
    a=p.parse_args()
    r=run(a.out,a.snapshot,a.train,a.exam)
    print(json.dumps({"status":r["status"],"train":r["train_episodes"],
                       "exam":r["blind_exam_episodes"],"families":r["families"]},indent=2))
if __name__=="__main__":main()
