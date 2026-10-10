"""F11: learn visual-context cues, then route F10 OLD/NEW tools or HOLD.

Synthetic cues: dark pixels in left/right corner of 64x64 scene; no
regime label is passed to learner at evaluation. All policy updates TRAIN only.
"""
import argparse,hashlib,json,random
from pathlib import Path
from PIL import Image,ImageDraw
from .fusion_f9_intensive_education_v0 import digest,verify_chain,geometry
from .fusion_f10_contextual_1000_v0 import teacher_tool
from .instrument_school_v2 import render_instrument,_gray_pixel_loss

def scene(cue,shape,seed):
    rng=random.Random(seed)
    canvas=Image.new("L",(64,64),255)
    d=ImageDraw.Draw(canvas)
    if cue in ("LEFT","BOTH"):d.rectangle((1,1,8,8),fill=0)
    if cue in ("RIGHT","BOTH"):d.rectangle((55,1,62,8),fill=0)
    gestures=geometry(rng,shape)
    # Cue is the perception signal, not a secret metadata label.
    return canvas,gestures

def features(canvas):
    pixels=canvas.load()
    def count(box):
        return sum(pixels[x,y]<128 for y in range(box[1],box[3]+1)
                   for x in range(box[0],box[2]+1))
    a=count((1,1,8,8))>=40
    b=count((55,1,62,8))>=40
    return "BOTH" if a and b else "LEFT" if a else "RIGHT" if b else "NONE"

def decide(mem,observed):
    candidates=mem.get(observed,{})
    total=sum(candidates.values())
    if total<3:return {"status":"HOLD_NO_TRAIN","regime":None}
    if observed in ("BOTH","NONE") or not candidates:
        return {"status":"HOLD_AMBIGUOUS","regime":None}
    ranked=sorted(candidates.items(),key=lambda kv:(-kv[1],kv[0]))
    if len(ranked)>1 and ranked[0][1]/total<0.8:
        return {"status":"HOLD_CONFLICTING_FEEDBACK","regime":None}
    return {"status":"CONTEXT_PROPOSAL","regime":ranked[0][0]}

def run(out,episodes=1000,seed=20261009,checkpoint=100):
    if type(episodes)!=int or episodes<20 or type(checkpoint)!=int or checkpoint<1:
        raise ValueError("invalid size")
    root=Path(out)
    if root.exists():raise ValueError("output exists")
    root.mkdir(parents=True)
    rng=random.Random(seed)
    memory={};tip=None;history=[];corrected=0
    with (root/"receipts.jsonl").open("x",encoding="utf-8") as receipt:
        for n in range(1,episodes+1):
            regime="OLD" if n%2 else "NEW"
            cue="LEFT" if regime=="OLD" else "RIGHT"
            if n%17==0:cue="BOTH"
            image,_=scene(cue,"line",rng.randrange(10000000))
            observed=features(image)
            before=decide(memory,observed)
            if cue in ("LEFT","RIGHT"):
                count=memory.setdefault(observed,{"OLD":0,"NEW":0})
                count[regime]+=1
            after=decide(memory,observed)
            if before["regime"]!=after["regime"] and before["regime"] is not None:
                corrected+=1
            event={"index":n,"previous":tip,"kind":"TRAIN","features":observed,
                "feedback_regime":regime if cue in ("LEFT","RIGHT") else None,
                "policy_before":before,"policy_after":after,
                "native_memory_write":False,"canonical_promotion":False,
                "decision_authority":"KX108_ONLY"}
            event["digest"]=digest(event);tip=event["digest"]
            receipt.write(json.dumps(event,sort_keys=True)+"\n")
            if n%checkpoint==0 or n==episodes:
                saved=json.loads(json.dumps(memory))
                scores={"known_correct":0,"known_wrong":0,"holds_ambiguous":0,
                        "wrong_ambiguous":0,"evaluated":0}
                # TEST distributions and raw pixels are not passed to TRAIN.
                for j in range(80):
                    truth="OLD" if j%2==0 else "NEW"
                    label=("LEFT" if truth=="OLD" else "RIGHT") if j%4!=3 else "BOTH"
                    if j%10==9:label="NONE"
                    img,gestures=scene(label,"line" if j%3 else "angle",
                                      seed+900000+j)
                    observed_test=features(img)
                    prediction=decide(saved,observed_test)
                    chosen=prediction["regime"]
                    # Seal prediction before constructing teacher-style output.
                    sealed=digest({"observed":observed_test,"proposal":chosen,
                                   "candidate_tool":teacher_tool("LIGHT","line",chosen)
                                    if chosen in ("OLD","NEW") else None})
                    if label in ("BOTH","NONE"):
                        if chosen is None:scores["holds_ambiguous"]+=1
                        else:scores["wrong_ambiguous"]+=1
                    elif chosen==truth:scores["known_correct"]+=1
                    else:scores["known_wrong"]+=1
                    scores["evaluated"]+=1
                history.append({"episode":n,"scores":scores,"snapshot_digest":digest(saved)})
                (root/("snapshot-%06d.json"%n)).write_text(
                    json.dumps({"memory":saved,"digest":digest(saved),
                                "candidate_only":True},indent=2)+"\n")
    count,verified=verify_chain(root/"receipts.jsonl")
    if count!=episodes or verified!=tip:raise ValueError("ledger")
    report={"schema":"BRODY_F11_VISUAL_CONTEXT_1000_V0","episodes":count,
      "policy_changes":corrected,"checkpoints":history,
      "receipt_tip":tip,"inference_from_pixels":True,
      "visual_perception_limited_to_corner_markers":True,
      "general_image_understanding_proven":False,
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    (root/"report.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--episodes",type=int,default=1000)
    p.add_argument("--checkpoint",type=int,default=100)
    a=p.parse_args()
    r=run(a.out,a.episodes,20261009,a.checkpoint)
    print(json.dumps({"episodes":r["episodes"],
      "checkpoints":len(r["checkpoints"]),
      "last":r["checkpoints"][-1]["scores"]}))
if __name__=="__main__":main()
