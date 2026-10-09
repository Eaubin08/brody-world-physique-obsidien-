"""F9 intensive education, reproducible 1000 TRAIN episodes, no canonical writes.

An intentionally bounded synthetic instrument-policy learner. Images are 64x64
and train/test geometry and style contexts are separated. No claim of real vision.
"""
from __future__ import annotations
import argparse,hashlib,json,random,sys
from pathlib import Path
from statistics import mean
from PIL import Image
from .drawing_school_v1 import GestureV1
from .instrument_school_v2 import TOOLS,render_instrument,_gray_pixel_loss

STYLES=("LIGHT","UNIFORM","EXPRESSIVE")
TRAIN_TOOLS={"LIGHT":"PENCIL","UNIFORM":"PEN","EXPRESSIVE":"NIB"}
# Evaluation-only fixture is kept outside learner observations and decisions.
EVAL_TOOLS={"LIGHT":"PENCIL","UNIFORM":"PEN","EXPRESSIVE":"NIB"}
SHAPES=("line","angle","zigzag","box")
def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def geometry(rng,shape):
    x=rng.randint(7,15);y=rng.randint(7,16)
    dx=rng.randint(24,39);dy=rng.randint(24,38)
    if shape=="line":pts=((x,y),(x+dx,y+dy))
    elif shape=="angle":pts=((x,y+dy),(x+dx//2,y),(x+dx,y+dy))
    elif shape=="zigzag":pts=((x,y),(x+dx//3,y+dy),(x+2*dx//3,y),(x+dx,y+dy))
    else:pts=((x,y),(x+dx,y),(x+dx,y+dy),(x,y+dy),(x,y))
    return (GestureV1(tuple(pts),"STRAIGHT_STROKE"),)
def error(gestures,tool,target):
    return _gray_pixel_loss(render_instrument(gestures,tool),target)
def predict(stats,key):
    record=stats.get(key)
    if not record or not all(record[t]["n"] for t in TOOLS):return None
    return min(TOOLS,key=lambda t:(record[t]["sum"]/record[t]["n"],TOOLS.index(t)))
def update(stats,key,losses):
    record=stats.setdefault(key,{t:{"sum":0.0,"n":0} for t in TOOLS})
    for tool in TOOLS:
        record[tool]["sum"]+=losses[tool];record[tool]["n"]+=1
def snapshot(stats):
    return json.loads(json.dumps(stats,sort_keys=True))
def blind_exam(stats,seed,stage,seen,episodes):
    # External TEST contexts never enter the training pool.
    rng=random.Random(seed+100000+stage*104729)
    scored=[];holds=0
    for k in range(48):
        style=STYLES[k%3]
        shape=SHAPES[(k//3)%4]
        key=style+"|"+shape
        gestures=geometry(rng,shape)
        choice=predict(stats,key)
        # Freeze decision and generated candidate before constructing teacher.
        if choice is None:
            holds+=1
            scored.append({"key":key,"choice":None,"status":"HOLD"})
            continue
        candidate=render_instrument(gestures,choice)
        candidate_bytes_sha256=hashlib.sha256(candidate.tobytes()).hexdigest()
        # Teacher is created exclusively AFTER output is sealed.
        target=render_instrument(gestures,EVAL_TOOLS[style])
        loss=_gray_pixel_loss(candidate,target)
        scored.append({"key":key,"choice":choice,"candidate_sha256":candidate_bytes_sha256,
                       "error":loss,"status":"TEST_ONLY"})
    actual=[r["error"] for r in scored if "error" in r]
    return {"at_train_episode":episodes,"exam_seed":seed+100000+stage*104729,
            "mean_error":mean(actual) if actual else None,"evaluated":len(actual),
            "held":holds,"outcomes":scored,"feedback_used_for_training":False,
            "test_target_access_before_candidate_seal":False}
def verify_chain(path):
    previous=None;expected=1
    with Path(path).open(encoding="utf-8") as handle:
        for line in handle:
            x=json.loads(line)
            body={k:v for k,v in x.items() if k!="digest"}
            if x.get("index")!=expected or x.get("previous")!=previous or digest(body)!=x.get("digest"):
                raise ValueError("ledger tamper detected")
            if x.get("native_memory_write") is not False or x.get("canonical_promotion") is not False:
                raise ValueError("unauthorized memory write")
            previous=x["digest"];expected+=1
    return expected-1,previous
def run(out,episodes=1000,seed=20261009,checkpoint=100):
    if type(episodes)!=int or episodes<1 or episodes>100000:raise ValueError("episodes must be 1..100000")
    if type(checkpoint)!=int or checkpoint<1:raise ValueError("invalid checkpoint")
    root=Path(out)
    if root.exists():raise ValueError("output exists: keep evidence")
    root.mkdir(parents=True)
    rng=random.Random(seed)
    stats={};history=[];prior=None;corrections=0;regime_change_episodes=0
    tests=[]
    ledger=root/"receipts.jsonl"
    with ledger.open("x",encoding="utf-8") as stream:
        for i in range(1,episodes+1):
            style=STYLES[(i-1)%3];shape=SHAPES[((i-1)//3)%4]
            key=style+"|"+shape
            gestures=geometry(rng,shape)
            old=predict(stats,key)
            # Change teacher preference on one previously learned context.
            conflicting=(key=="LIGHT|line" and i>episodes//2)
            expected_tool="PEN" if conflicting else TRAIN_TOOLS[style]
            if conflicting:regime_change_episodes+=1
            reference=render_instrument(gestures,expected_tool)
            losses={t:error(gestures,t,reference) for t in TOOLS}
            update(stats,key,losses)
            new=predict(stats,key)
            if old is not None and old!=new:corrections+=1
            event={"index":i,"previous":prior,"kind":"TRAIN","episode":i,
                   "skill_context":key,"prior_choice":old,"new_choice":new,
                   "train_tool_losses":losses,"target_tool_train_only":expected_tool,
                   "contradictory_train":conflicting,"corrected":old is not None and old!=new,
                   "native_memory_write":False,"canonical_promotion":False,
                   "decision_authority":"KX108_ONLY"}
            event["digest"]=digest(event)
            stream.write(json.dumps(event,sort_keys=True)+"\n")
            prior=event["digest"]
            if i%checkpoint==0 or i==episodes:
                frozen=snapshot(stats)
                # Repeat exactly the same heldout distribution across checkpoints,
                # useful for forgetting/accuracy trend; never updates TRAIN.
                report=blind_exam(frozen,seed,0,None,i)
                report["snapshot_digest"]=digest(frozen)
                tests.append(report)
                (root/("snapshot-%06d.json"%i)).write_text(
                    json.dumps({"episode":i,"candidate_stats":frozen,"hash":digest(frozen),
                                "native_memory_write":False},indent=2)+"\n")
    count,tip=verify_chain(ledger)
    if count!=episodes:raise ValueError("incomplete episode ledger")
    first=tests[0];last=tests[-1]
    # Compute potential forgetting by comparing test results for each context
    # across checkpoints; new classes taught later are not treated as forgetting.
    forgetting=[]
    earliest={}
    for checkpoint_result in tests:
        for outcome in checkpoint_result["outcomes"]:
            if outcome["status"]!="TEST_ONLY":continue
            key=outcome["key"]
            baseline=earliest.setdefault(key,outcome["error"])
            forgetting.append({"at":checkpoint_result["at_train_episode"],
                               "context":key,"delta_from_first_test":outcome["error"]-baseline})
    summary={"schema":"BRODY_F9_INTENSIVE_1000_V0","requested_episodes":episodes,
             "completed_episodes":count,"seed":seed,"training_contexts":len(stats),
             "policy_changes_on_train":corrections,
             "contradictory_train_episodes":regime_change_episodes,
             "checkpoints":[{"at":x["at_train_episode"],"mean_error":x["mean_error"],
                             "held":x["held"],"evaluated":x["evaluated"],
                             "snapshot_digest":x["snapshot_digest"]} for x in tests],
             "blind_test_count":sum(x["evaluated"] for x in tests),
             "max_forgetting_delta":max((x["delta_from_first_test"] for x in forgetting),default=None),
             "final_policy":{k:predict(stats,k) for k in sorted(stats)},
             "receipt_tip":tip,"receipt_count":count,
             "no_test_to_train_feedback":True,
             "eval_generator_shared_with_train":True,
             "general_vision_proven":False,"native_memory_write":False,
             "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    (root/"heldout_checkpoints.json").write_text(json.dumps(tests,indent=2)+"\n")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--episodes",type=int,default=1000)
    p.add_argument("--seed",type=int,default=20261009)
    p.add_argument("--checkpoint",type=int,default=100)
    args=p.parse_args()
    result=run(args.out,args.episodes,args.seed,args.checkpoint)
    print(json.dumps({"completed_episodes":result["completed_episodes"],
      "checkpoints":len(result["checkpoints"]),"receipts":result["receipt_count"]}))
if __name__=="__main__":main()
