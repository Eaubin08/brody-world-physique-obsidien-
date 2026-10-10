"""Unified drawing -> visual re-perception -> discrepancy -> correction -> reconstruction.

A supervised synthetic laboratory. The initial prediction is sealed before the
teacher is revealed. Correction sees the target and is NOT blind evaluation.
"""
from __future__ import annotations
import argparse,hashlib,json,random
from pathlib import Path
from collections import defaultdict
from statistics import mean
from PIL import Image,ImageChops
from .fusion_f9_intensive_education_v0 import STYLES,SHAPES,EVAL_TOOLS,geometry,predict,digest,verify_chain
from .instrument_school_v2 import TOOLS,render_instrument,_gray_pixel_loss
from .image_tool_school_20k_campaign_v0 import FAMILIES,common_transform

def visual_fingerprint(image):
    a=image.convert("L")
    vals=a.tobytes()
    dark=sum(v<128 for v in vals)
    bbox=ImageChops.difference(a,Image.new("L",a.size,255)).getbbox()
    return {"ink_pixels":dark,"bbox":bbox,"sha256":hashlib.sha256(vals).hexdigest()}

def episode(policy,i,seed):
    family=FAMILIES[(i-1)%len(FAMILIES)]
    rng=random.Random(seed+i*131071+FAMILIES.index(family)*7919)
    style=STYLES[i%3];shape=SHAPES[(i//3)%4]
    advertised="UNSEEN" if family=="unknown_intent" else style
    key=advertised+"|"+shape
    gestures=geometry(rng,shape)
    transformation=common_transform(family,rng.getrandbits(32))
    chosen=predict(policy,key)
    initial=transformation(render_instrument(gestures,chosen)) if chosen else None
    first=visual_fingerprint(initial) if initial else None
    # Stage A is frozen. Stage B teacher is opened only after the first output.
    true_style=STYLES[(STYLES.index(style)+1)%3] if family=="wrong_intent" else style
    target=transformation(render_instrument(gestures,EVAL_TOOLS[true_style]))
    observed=visual_fingerprint(target)
    before=_gray_pixel_loss(initial,target) if initial else None
    contradictory=(chosen is not None and before>1e-10)
    # Explicit feedback is now available. This is supervised trial-and-error
    # with the SAME renderer/target, not heldout generalization.
    attempts=[]
    if initial is not None:
        for tool in TOOLS:
            candidate=transformation(render_instrument(gestures,tool))
            attempts.append((tool,_gray_pixel_loss(candidate,target),candidate))
        tool,after,reconstructed=min(attempts,key=lambda t:(t[1],TOOLS.index(t[0])))
    else:tool=None;after=None;reconstructed=None
    corrected=visual_fingerprint(reconstructed) if reconstructed else None
    return {
      "family":family,"style_visible":advertised,"shape":shape,"before_tool":chosen,
      "after_tool":tool,"before_loss":before,"after_loss":after,
      "visual_discrepancy_detected":contradictory,
      "correction_attempted":bool(attempts),
      "improved":before is not None and after < before-1e-10,
      "initial_fingerprint":first,"observed_fingerprint":observed,
      "reconstruction_fingerprint":corrected,
      "reconstruction_roundtrip_loss":after,
      "unknown_context_held":chosen is None,
      "initial_sealed_before_feedback":True,
      "correction_feedback_is_supervised":True,
      "candidate_only":True,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}

def run(out,snapshot,cases=10000,seed=250112):
    out=Path(out)
    if out.exists():raise ValueError("PRESERVE_EXISTING_EVIDENCE")
    if cases<10 or cases%10:raise ValueError("cases must be multiple of ten")
    s=json.loads(Path(snapshot).read_text(encoding="utf-8"))
    if digest(s["candidate_stats"])!=s["hash"]:raise ValueError("SNAPSHOT_TAMPER")
    policy=s["candidate_stats"]
    out.mkdir(parents=True)
    agg=defaultdict(list);prior=None
    with (out/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i in range(1,cases+1):
            event=episode(policy,i,seed)
            agg[event["family"]].append(event)
            record={"index":i,"previous":prior,**event}
            record["digest"]=digest(record)
            f.write(json.dumps(record,sort_keys=True)+"\n")
            prior=record["digest"]
    count,tip=verify_chain(out/"receipts.jsonl")
    if count!=cases:raise ValueError("INCOMPLETE_EXAM")
    families={}
    for family,items in agg.items():
        seen=[x for x in items if x["before_loss"] is not None]
        families[family]={"cases":len(items),
          "holds":sum(x["unknown_context_held"] for x in items),
          "discrepancy_detected":sum(x["visual_discrepancy_detected"] for x in items),
          "corrections_improved":sum(x["improved"] for x in items),
          "mean_before_loss":mean(x["before_loss"] for x in seen) if seen else None,
          "mean_after_loss":mean(x["after_loss"] for x in seen) if seen else None}
    report={"schema":"BRODY_IMAGE_INTEGRATED_VISUAL_FEEDBACK_V0",
       "cases":count,"receipt_tip":tip,"families":families,
       "perception":"pixel_fingerprint_and_visual_difference_not_semantic_vision",
       "reconstruction":"bounded_three_instrument_search_not_free_generation",
       "transformations":"controlled_synthetic_image_operations",
       "learning":"frozen_policy_plus_supervised_episode_corrections_no_cross_episode_update",
       "blind_exam_proven":False,"physical_world_proven":False,
       "native_memory_write":False,"kernel_mutation":False,
       "decision_authority":"KX108_ONLY","status":"INTEGRATED_SYNTHETIC_FEEDBACK_LAB_NOT_WORLD_MODEL"}
    (out/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--snapshot",required=True)
    p.add_argument("--cases",type=int,default=10000)
    p.add_argument("--seed",type=int,default=250112)
    a=p.parse_args()
    report=run(a.out,a.snapshot,a.cases,a.seed)
    print(json.dumps({"cases":report["cases"],"families":report["families"],
      "status":report["status"]},indent=2))
if __name__=="__main__":main()
