"""P157 contextual rule selection without overwriting competing knowledge.

A latent scenario has one of two motion regimes. Context cue is visually
present, hidden, or contradicted; the learner stores separate observed rules.
Evaluation tests SELECT, MULTI, HOLD, and memory retention. No oracle regime
passed into prediction. The exam uses unseen rendered trajectories.
"""
from __future__ import annotations
import argparse,json,random,time,math
from pathlib import Path
from PIL import Image,ImageDraw

W,H=120,76
CONTEXTS=("flat","slope")
CONDITIONS=("clear_flat","clear_slope","cue_missing","cue_conflict","noisy_cue","unknown_context")
REQUESTS=("single","possibilities","explain")
def render(x,cue,noise,rng):
    im=Image.new("RGB",(W,H),(246,246,242));d=ImageDraw.Draw(im)
    d.ellipse((round(x)-3,35,round(x)+3,41),fill=(224,37,47))
    if cue=="flat":d.rectangle((8,58,35,61),fill=(30,130,205))
    if cue=="slope":d.polygon([(8,63),(35,51),(35,55),(8,67)],fill=(30,130,205))
    if cue=="unknown":d.rectangle((8,58,35,61),fill=(110,110,110))
    if noise:
        for _ in range(22):
            d.point((rng.randrange(W),rng.randrange(H)),fill=(rng.randrange(200),rng.randrange(200),rng.randrange(200)))
    return im
def make(rng,regime,condition):
    initial=rng.randint(25,38);v=rng.choice((3,4,5))
    accel=0 if regime=="flat" else -1
    positions=[]
    for t in range(8):positions.append(initial+v*t+accel*t*(t-1)/2)
    cue=regime
    if condition=="cue_missing":cue=None
    if condition=="cue_conflict":cue="slope" if regime=="flat" else "flat"
    if condition=="unknown_context":cue="unknown"
    images=[render(positions[t],cue,condition=="noisy_cue",rng) for t in range(5)]
    return images,positions
def observed(images):
    measurements=[]
    for im in images:
        px=im.load();found=[]
        for y in range(31,44):
            for x in range(W):
                r,g,b=px[x,y]
                if r>190 and g<85 and b<95:found.append(x)
        measurements.append(sum(found)/len(found) if found else None)
    return measurements
def read_cue(im):
    p=im.load()
    flat=0;slope=0;unknown=0
    for x in range(8,36):
        for y in range(48,69):
            r,g,b=p[x,y]
            if b>150 and r<85 and g>90:
                if y in (58,59,60,61):flat+=1
                if abs(y-(63-(x-8)*12/27))<=3:slope+=1
            if 80<r<150 and abs(r-g)<10 and abs(g-b)<10:unknown+=1
    if unknown>40:return None,"UNKNOWN_MARK"
    if flat<6 and slope<6:return None,"MISSING"
    if slope>flat*1.35:return "slope","OBSERVED"
    if flat>slope*1.35:return "flat","OBSERVED"
    return None,"AMBIGUOUS"
def induce(training):
    bank={}
    for name,samples in training.items():
        accelerations=[]
        for images in samples:
            xs=observed(images)
            if any(v is None for v in xs):continue
            accelerations.extend(xs[i+2]-2*xs[i+1]+xs[i] for i in range(len(xs)-2))
        bank[name]={"acceleration":sum(accelerations)/len(accelerations) if accelerations else None,
                    "observations":len(accelerations)}
    return bank
def predict(images,bank,request,spread_threshold=1.,contradiction_threshold=.8):
    xs=observed(images)
    if xs[-1] is None or xs[-2] is None:return {"status":"HOLD","reason":"NO_MOTION_OBSERVATION","predictions":[]}
    cue,cue_status=read_cue(images[-1])
    x=xs[-1];speed=xs[-1]-xs[-2]
    candidates={k:x+speed+v["acceleration"] for k,v in bank.items() if v["acceleration"] is not None}
    if not candidates:return {"status":"HOLD","reason":"NO_LEARNED_RULE","predictions":[]}
    observed_acc=xs[-1]-2*xs[-2]+xs[-3] if xs[-3] is not None else None
    spread=max(candidates.values())-min(candidates.values())
    # A conflicting cue is not silently overwritten: return alternatives
    # with evidence provenance so the uncertainty stays explicit.
    conflict=(cue in candidates and observed_acc is not None and
              abs(observed_acc-bank[cue]["acceleration"])>contradiction_threshold)
    if request=="possibilities":
        return {"status":"MULTI","reason":"REQUEST_ALTERNATIVES","predictions":candidates,
                "cue":cue,"cue_status":cue_status}
    if cue is None:
        if request=="single":return {"status":"HOLD","reason":"MISSING_CONTEXT","predictions":candidates}
        return {"status":"MULTI","reason":"CONTEXT_NOT_RESOLVED","predictions":candidates}
    if conflict:
        if request=="single":return {"status":"HOLD","reason":"CONTRADICTORY_EVIDENCE","predictions":candidates}
        return {"status":"MULTI","reason":"CONTRADICTORY_EVIDENCE","predictions":candidates}
    if cue not in candidates:return {"status":"HOLD","reason":"NOVEL_CONTEXT","predictions":candidates}
    return {"status":"SELECT","reason":"CONTEXT_MATCH","selected":cue,
            "predictions":{cue:candidates[cue]},"cue_status":cue_status}
def run(out,minutes=15,seed=157,lessons_each=40,exam_each=100):
    if not (2<=minutes<=90 and 10<=lessons_each<=500 and 20<=exam_each<=2000):
        raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    start=time.monotonic();train_rng=random.Random(seed+11);exam_rng=random.Random(seed+991)
    samples={}
    for regime in CONTEXTS:
        samples[regime]=[]
        for _ in range(lessons_each):
            imgs,_=make(train_rng,regime,"clear_"+regime)
            samples[regime].append(imgs)
    bank=induce(samples)
    for group in samples.values():
        for seq in group:
            for img in seq:img.close()
    (dest/"FROZEN_CONTEXT_RULES.json").write_text(json.dumps(bank,indent=2),encoding="utf8")
    report={};stopped=False;deadline=start+60*minutes
    with (dest/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for condition in CONDITIONS:
            for request in REQUESTS:
                key=condition+"/"+request
                row={"n":0,"SELECT":0,"MULTI":0,"HOLD":0,"selection_correct":0,
                     "selected_mae_sum":0.,"selected_answered":0,"multi_contains_true_regime":0}
                for i in range(exam_each):
                    if time.monotonic()>=deadline:stopped=True;break
                    true=exam_rng.choice(CONTEXTS)
                    imgs,positions=make(exam_rng,true,condition)
                    ans=predict(imgs,bank,request)
                    row["n"]+=1;row[ans["status"]]+=1
                    if ans["status"]=="SELECT":
                        row["selection_correct"]+=int(ans["selected"]==true)
                        row["selected_mae_sum"]+=abs(ans["predictions"][ans["selected"]]-positions[5])
                        row["selected_answered"]+=1
                    if ans["status"]=="MULTI":row["multi_contains_true_regime"]+=int(true in ans["predictions"])
                    f.write(json.dumps({"condition":condition,"request":request,"truth":true,
                        "actual_x":positions[5],"answer":ans})+"\n")
                    for img in imgs:img.close()
                row["selection_accuracy"]=row["selection_correct"]/row["selected_answered"] if row["selected_answered"] else None
                row["selected_mae"]=row["selected_mae_sum"]/row["selected_answered"] if row["selected_answered"] else None
                report[key]=row
                if stopped:break
            if stopped:break
    output={"schema":"BRODY_P157_CONTEXTUAL_COEXISTENCE",
      "duration_seconds":round(time.monotonic()-start,3),"conditions_expected":len(CONDITIONS)*len(REQUESTS),
      "conditions_completed":sum(x["n"]==exam_each for x in report.values()),
      "exams":sum(x["n"] for x in report.values()),"status":"TIME_BUDGET" if stopped else "EXAM_CAP",
      "frozen_context_rules":bank,"by_condition":report,
      "context_provided_to_inference_as_pixels_only":True,"requests_provided_as_instructions":True,
      "full_context_understanding_proven":False,"physical_law_discovery_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(output,indent=2),encoding="utf8")
    return output
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=157)
    p.add_argument("--lessons-each",type=int,default=40);p.add_argument("--exam-each",type=int,default=100)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.lessons_each,a.exam_each)
    print(json.dumps({k:v for k,v in r.items() if k!="by_condition"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
