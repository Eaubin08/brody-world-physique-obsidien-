"""Paired visible vs hidden reference experiment; not semantic vision.

A visually observable reference allows pixel comparison with candidate renders.
When reference is hidden and instructions might be adversarial, HOLD instead of
guessing. Labels are examiner-only, not learner input. No training or memory write.
"""
from __future__ import annotations
import argparse,hashlib,json,random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from PIL import Image
from .fusion_f9_intensive_education_v0 import STYLES,SHAPES,EVAL_TOOLS,geometry,digest,verify_chain
from .instrument_school_v2 import TOOLS,render_instrument,_gray_pixel_loss

def choose_from_pixels(reference, candidate_images, threshold=0.000001):
    """Only receives a reference image and three tool renderings, never oracle labels."""
    if not isinstance(reference,Image.Image):
        return {"status":"HOLD_UNOBSERVABLE","tool":None,"error":None}
    errors={t:_gray_pixel_loss(img,reference) for t,img in candidate_images.items()}
    selected=min(TOOLS,key=lambda t:(errors[t],TOOLS.index(t)))
    if errors[selected]>threshold:
        return {"status":"HOLD_UNMATCHED_REFERENCE","tool":None,"error":errors[selected]}
    return {"status":"MATCHED_VISIBLE_REFERENCE","tool":selected,"error":errors[selected]}

def case(i,seed):
    rng=random.Random(seed+i*100003)
    style=rng.choice(STYLES);shape=rng.choice(SHAPES)
    truth_tool=EVAL_TOOLS[style]
    misleading=bool(rng.getrandbits(1))
    observable=i%2==0
    if misleading:
        truth_tool=TOOLS[(TOOLS.index(truth_tool)+1+rng.randrange(len(TOOLS)-1))%len(TOOLS)]
    gestures=geometry(rng,shape)
    candidates={t:render_instrument(gestures,t) for t in TOOLS}
    reference=render_instrument(gestures,truth_tool)
    # Visibility boundary: learner receives no examiner labels, modes, or true tool.
    presented=reference if observable else None
    result=choose_from_pixels(presented,candidates)
    expected="MATCHED_VISIBLE_REFERENCE" if observable else "HOLD_UNOBSERVABLE"
    if result["status"]!=expected:raise RuntimeError("EVALUATION_GATE_FAILED")
    success=(result["tool"]==truth_tool) if observable else result["tool"] is None
    return {"index":i,"observable_exam_only":observable,
      "misleading_exam_only":misleading,"declared_style":style,"shape":shape,
      "target_tool_exam_only":truth_tool,
      "reference_sha256":hashlib.sha256(reference.tobytes()).hexdigest(),
      "result":result,"expected_status":expected,"meets_expected_behavior":success,
      "reference_visible_to_learner":observable,
      "family_label_available_to_learner":False,"oracle_tool_available_to_learner":False,
      "source_kind":"SYNTHETIC_RENDERER",
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}

def run(out,cases=10000,seed=20261009):
    if cases<100 or cases%2:raise ValueError("EVEN_CASE_COUNT_AT_LEAST_100")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    root.mkdir(parents=True)
    buckets=defaultdict(list);previous=None
    with (root/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i in range(1,cases+1):
            result=case(i,seed)
            key=("visible" if result["observable_exam_only"] else "hidden")+"_"+("misleading" if result["misleading_exam_only"] else "truthful")
            buckets[key].append(result)
            row={"index":i,"previous":previous,**result}
            row["digest"]=digest(row)
            f.write(json.dumps(row,sort_keys=True)+"\n")
            previous=row["digest"]
    count,tip=verify_chain(root/"receipts.jsonl")
    metrics={}
    for k,group in sorted(buckets.items()):
        metrics[k]={"cases":len(group),
          "behavior_correct":sum(r["meets_expected_behavior"] for r in group),
          "matched":sum(r["result"]["status"]=="MATCHED_VISIBLE_REFERENCE" for r in group),
          "held":sum(r["result"]["status"].startswith("HOLD") for r in group)}
    report={"schema":"BRODY_IMAGE_VISIBLE_CONTRADICTION_VS_UNOBSERVABLE_10K_V0",
        "cases":count,"receipt_tip":tip,"metrics":metrics,
        "method":"PIXEL_NEAREST_TOOL_WITH_ABSTENTION",
        "uses_simulated_reference":True,"same_renderer_for_reference_and_candidates":True,
        "recognizes_physical_contradiction":False,
        "semantic_visual_understanding_proven":False,
        "detection_without_visible_reference_proven":False,
        "model_weights_trained":False,"native_memory_write":False,
        "kernel_mutation":False,"decision_authority":"KX108_ONLY",
        "status":"VISIBLE_REFERENCE_COMPARISON_SYNTHETIC_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--cases",type=int,default=10000)
    p.add_argument("--seed",type=int,default=20261009)
    a=p.parse_args()
    report=run(a.out,a.cases,a.seed)
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
