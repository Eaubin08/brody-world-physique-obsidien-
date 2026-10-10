"""Ablation of hidden family labels from Brody's instrument-routing learner.

The learner sees only declared goal and geometry category. The evaluator owns
the hidden perturbation and target. Shuffled balanced family assignment and
random independent style/shape prevent family inference from row index/modulo.
This measures whether corrected behavior transfers WITHOUT family metadata.
"""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
from statistics import mean
from .fusion_f9_intensive_education_v0 import STYLES,SHAPES,EVAL_TOOLS,geometry,predict,digest,verify_chain
from .instrument_school_v2 import TOOLS,render_instrument,_gray_pixel_loss
from .image_tool_school_20k_campaign_v0 import FAMILIES,common_transform

def choose(stats,key,fallback):
    record=stats.get(key)
    if not record or any(record[t]["n"]==0 for t in TOOLS):return fallback
    return min(TOOLS,key=lambda t:(record[t]["sum"]/record[t]["n"],TOOLS.index(t)))

def schedule(count,seed):
    if count%len(FAMILIES):raise ValueError("UNBALANCED_EXAM")
    rng=random.Random(seed)
    families=list(FAMILIES)*(count//len(FAMILIES))
    rng.shuffle(families)
    return [(family,rng.choice(STYLES),rng.choice(SHAPES),rng.getrandbits(63))
            for family in families]

def evaluate_case(fixture,policy,learned,training):
    # Fixture is PRIVATE to the evaluator. Neither 'family' nor 'true_style',
    # nor transformation parameters enter context_key or choose().
    family,style,shape,seed=fixture
    advertised="UNSEEN" if family=="unknown_intent" else style
    key=advertised+"|"+shape
    fallback=predict(policy,key)
    selected=choose(learned,key,fallback) if fallback is not None else None
    rng=random.Random(seed)
    gestures=geometry(rng,shape)
    transform=common_transform(family,rng.getrandbits(32))
    before_image=transform(render_instrument(gestures,fallback)) if fallback else None
    proposed=transform(render_instrument(gestures,selected)) if selected else None
    commitment=digest({"tool":selected,"baseline":fallback,
                       "render_hash":digest(list(proposed.tobytes())) if proposed else None})
    # No teacher or reference is evaluated until after both choices are sealed.
    real_style=STYLES[(STYLES.index(style)+1)%3] if family=="wrong_intent" else style
    reference=transform(render_instrument(gestures,EVAL_TOOLS[real_style]))
    first_loss=_gray_pixel_loss(before_image,reference) if before_image else None
    loss=_gray_pixel_loss(proposed,reference) if proposed else None
    if training and selected is not None:
        losses={t:_gray_pixel_loss(transform(render_instrument(gestures,t)),reference)
                for t in TOOLS}
        record=learned.setdefault(key,{t:{"sum":0.0,"n":0} for t in TOOLS})
        for t in TOOLS:
            record[t]["sum"]+=losses[t];record[t]["n"]+=1
    return {"family_evaluator_only":family,"key_visible_to_learner":key,
      "chosen_tool":selected,"baseline_tool":fallback,"baseline_loss":first_loss,
      "learned_loss":loss,"choice_commitment":commitment,
      "target_opened_after_prediction":True,"exam_feedback_used":training,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}

def run(out,snapshot,train=10000,exam=10000,seed=123461):
    out=Path(out)
    if out.exists():raise ValueError("PRESERVE_EXISTING_EVIDENCE")
    if min(train,exam)<100 or train%10 or exam%10:raise ValueError("REQUIRE_BALANCED_CASES")
    source=json.loads(Path(snapshot).read_text(encoding="utf-8"))
    base=source["candidate_stats"]
    if digest(base)!=source["hash"]:raise ValueError("SNAPSHOT_TAMPER")
    learner={}
    for fixture in schedule(train,seed):
        evaluate_case(fixture,base,learner,True)
    frozen=json.loads(json.dumps(learner,sort_keys=True))
    freeze_digest=digest(frozen)
    rows=[];prior=None
    out.mkdir(parents=True)
    (out/"candidate_skills.json").write_text(json.dumps(
        {"skills":frozen,"digest":freeze_digest,"native_memory_write":False},indent=2)+"\n",
        encoding="utf-8")
    with (out/"blind_receipts.jsonl").open("x",encoding="utf-8") as f:
        for i,fixture in enumerate(schedule(exam,seed+7700007),1):
            result=evaluate_case(fixture,base,frozen,False)
            rows.append(result)
            entry={"index":i,"previous":prior,**result}
            entry["digest"]=digest(entry);prior=entry["digest"]
            f.write(json.dumps(entry,sort_keys=True)+"\n")
    count,tip=verify_chain(out/"blind_receipts.jsonl")
    if count!=exam or digest(frozen)!=freeze_digest:raise RuntimeError("EXAM_MUTATED_SKILLS")
    scores={}
    for family in FAMILIES:
        group=[r for r in rows if r["family_evaluator_only"]==family]
        evaluated=[r for r in group if r["learned_loss"] is not None]
        scores[family]={"cases":len(group),"holds":len(group)-len(evaluated),
          "baseline_mean_loss":mean(r["baseline_loss"] for r in evaluated) if evaluated else None,
          "learned_mean_loss":mean(r["learned_loss"] for r in evaluated) if evaluated else None,
          "improved":sum(r["learned_loss"]<r["baseline_loss"]-1e-10 for r in evaluated),
          "worsened":sum(r["learned_loss"]>r["baseline_loss"]+1e-10 for r in evaluated)}
    result={"schema":"BRODY_IMAGE_FAMILY_BLIND_ABLATION_V0",
       "train":train,"exam":count,"receipt_tip":tip,"learner_contexts":len(frozen),
       "family_label_exposed_to_learner":False,
       "family_and_style_shape_independent_in_schedule":True,
       "same_evaluation_scenes_for_baseline_and_ablation":True,
       "candidate_skills_digest":freeze_digest,"scores":scores,
       "exam_feedback_used_for_training":False,
       "shared_renderer":True,"real_image_perception_proven":False,
       "can_detect_wrong_intent_from_observable_data":False,
       "native_memory_write":False,"kernel_mutation":False,
       "decision_authority":"KX108_ONLY",
       "status":"FAMILY_ABLATION_MEASURED_SYNTHETIC_ONLY"}
    (out/"MASTER_REPORT.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);p.add_argument("--snapshot",required=True)
    p.add_argument("--train",type=int,default=10000);p.add_argument("--exam",type=int,default=10000)
    a=p.parse_args()
    r=run(a.out,a.snapshot,a.train,a.exam)
    print(json.dumps({"status":r["status"],"train":r["train"],"exam":r["exam"],
                      "scores":r["scores"]},indent=2))
if __name__=="__main__":main()
