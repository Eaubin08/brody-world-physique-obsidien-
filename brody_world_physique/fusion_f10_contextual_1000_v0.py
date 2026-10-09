"""F10: 1000-episode contextual retention / reversal experiment, candidate only.

Reuses F9 geometry, hashed journal verification, and historic V2 instrument
renderers. TRAIN observations only update contextual empirical policy.
"""
import argparse,hashlib,json,random
from pathlib import Path
from statistics import mean
from .fusion_f9_intensive_education_v0 import (STYLES,SHAPES,TOOLS,geometry,
    render_instrument,_gray_pixel_loss,digest,verify_chain,update,predict,snapshot)

REGIMES=("OLD","NEW","MIXED")
def teacher_tool(style,shape,regime):
    if regime not in REGIMES:raise ValueError("untrusted context")
    if regime=="MIXED":return None
    if style=="LIGHT" and shape=="line":
        return "PENCIL" if regime=="OLD" else "PEN"
    return {"LIGHT":"PENCIL","UNIFORM":"PEN","EXPRESSIVE":"NIB"}[style]

def decide(memory,style,shape,regime):
    if regime not in REGIMES or style not in STYLES or shape not in SHAPES:
        return {"status":"HOLD_UNSUPPORTED_CONTEXT","tool":None}
    if regime=="MIXED" and style=="LIGHT" and shape=="line":
        return {"status":"HOLD_AMBIGUOUS_CONFLICT","tool":None}
    chosen=predict(memory,regime+"|"+style+"|"+shape) if regime!="MIXED" else None
    if regime=="MIXED":
        # Agreement required between the independent historic contextual tracks.
        a=predict(memory,"OLD|"+style+"|"+shape)
        b=predict(memory,"NEW|"+style+"|"+shape)
        if a is None or b is None or a!=b:
            return {"status":"HOLD_INSUFFICIENT_OR_CONFLICT","tool":None}
        chosen=a
    return {"status":"PROPOSAL" if chosen else "HOLD_NO_TRAIN","tool":chosen}

def examine(memory,seed,checkpoint):
    rng=random.Random(seed+450000)
    rows=[]
    for regime in REGIMES:
        for style in STYLES:
            for shape in SHAPES:
                for repetition in range(4):
                    gestures=geometry(rng,shape)
                    decision=decide(memory,style,shape,regime)
                    tool=decision["tool"]
                    sealed=(hashlib.sha256(render_instrument(gestures,tool).tobytes()).hexdigest()
                            if tool else None)
                    oracle=teacher_tool(style,shape,regime)
                    if oracle is None:
                        rows.append({"regime":regime,"style":style,"shape":shape,
                                     "status":decision["status"],"held":tool is None,
                                     "ambiguity":True,"candidate_sha256":sealed})
                        continue
                    # Teacher reference is only materialized after candidate digest.
                    reference=render_instrument(gestures,oracle)
                    loss=(_gray_pixel_loss(render_instrument(gestures,tool),reference)
                          if tool else None)
                    rows.append({"regime":regime,"style":style,"shape":shape,
                                 "status":decision["status"],"held":tool is None,
                                 "error":loss,"candidate_sha256":sealed,
                                 "oracle_after_candidate":True})
    by={}
    for regime in REGIMES:
        subset=[x for x in rows if x["regime"]==regime]
        observed=[x["error"] for x in subset if x.get("error") is not None]
        by[regime]={"mean_error":mean(observed) if observed else None,
                    "evaluated":len(observed),"holds":sum(x["held"] for x in subset)}
    return {"episode":checkpoint,"regimes":by,"rows":rows,
            "test_feedback_to_train":False,"no_teacher_before_candidate":True}

def run(out,episodes=1000,seed=20261009,checkpoint=100):
    if type(episodes)!=int or episodes<24 or type(checkpoint)!=int or checkpoint<1:
        raise ValueError("invalid campaign size")
    root=Path(out)
    if root.exists():raise ValueError("output already exists")
    root.mkdir(parents=True)
    rng=random.Random(seed)
    memory={};tip=None;checkpoints=[];changes=0
    with (root/"receipts.jsonl").open("x",encoding="utf-8") as stream:
        for episode in range(1,episodes+1):
            # Both contexts continue appearing throughout the course:
            # avoids conflating changed policy with erased old knowledge.
            regime="OLD" if episode%2 else "NEW"
            style=STYLES[((episode-1)//2)%3]
            shape=SHAPES[((episode-1)//6)%4]
            key=regime+"|"+style+"|"+shape
            gestures=geometry(rng,shape)
            before=predict(memory,key)
            expected=teacher_tool(style,shape,regime)
            target=render_instrument(gestures,expected)
            losses={t:_gray_pixel_loss(render_instrument(gestures,t),target) for t in TOOLS}
            update(memory,key,losses)
            after=predict(memory,key)
            if before is not None and before!=after:changes+=1
            receipt={"index":episode,"previous":tip,"kind":"TRAIN",
                 "context":key,"tool_losses":losses,"policy_before":before,
                 "policy_after":after,"native_memory_write":False,
                 "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
            receipt["digest"]=digest(receipt);tip=receipt["digest"]
            stream.write(json.dumps(receipt,sort_keys=True)+"\n")
            if episode%checkpoint==0 or episode==episodes:
                frozen=snapshot(memory)
                exam=examine(frozen,seed,episode)
                checkpoints.append(exam)
                (root/("snapshot-%06d.json"%episode)).write_text(
                    json.dumps({"episode":episode,"policy":frozen,
                                "digest":digest(frozen),"candidate_only":True},indent=2)+"\n")
    count,verified_tip=verify_chain(root/"receipts.jsonl")
    if count!=episodes or verified_tip!=tip:raise ValueError("invalid journal")
    first=checkpoints[0]["regimes"];last=checkpoints[-1]["regimes"]
    report={"schema":"BRODY_F10_CONTEXTUAL_INTENSIVE_V0",
            "episodes":count,"receipt_tip":verified_tip,
            "candidate_policy_changes":changes,"trained_contexts":len(memory),
            "exam_count":sum(sum(v["evaluated"] for v in c["regimes"].values()) for c in checkpoints),
            "checkpoints":[{"episode":c["episode"],"regimes":c["regimes"]} for c in checkpoints],
            "final_regimes":last,"first_regimes":first,
            "ambiguous_contexts_held":all(
                x["held"] for c in checkpoints for x in c["rows"]
                if x["regime"]=="MIXED" and x["style"]=="LIGHT" and x["shape"]=="line"),
            "no_test_feedback_learning":True,"evaluation_synthetic_shared_renderer":True,
            "general_world_comprehension_proven":False,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"}
    (root/"report.json").write_text(json.dumps(report,indent=2)+"\n")
    (root/"heldout.json").write_text(json.dumps(checkpoints,indent=2)+"\n")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--episodes",type=int,default=1000)
    p.add_argument("--checkpoint",type=int,default=100)
    p.add_argument("--seed",type=int,default=20261009)
    a=p.parse_args();r=run(a.out,a.episodes,a.seed,a.checkpoint)
    print(json.dumps({"episodes":r["episodes"],"checkpoints":len(r["checkpoints"]),
                      "ambiguous_contexts_held":r["ambiguous_contexts_held"]}))
if __name__=="__main__":main()
