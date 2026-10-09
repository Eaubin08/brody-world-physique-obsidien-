"""F12: 1000-case adversarial visual fuzzing and spoofing audit (read-only).

This is a diagnostic: reports failures without hiding them; never trains on tests.
"""
from __future__ import annotations
import argparse,hashlib,json,random,sys
from pathlib import Path
from PIL import Image,ImageDraw
from .fusion_f11_visual_context_1000_v0 import scene,features,decide
from .fusion_f9_intensive_education_v0 import digest

KINDS=("baseline","shift","eraser","faint","partial","both","absent",
       "opposite","spoof_metadata","border_noise")
def policy():
    return {"LEFT":{"OLD":60,"NEW":0},"RIGHT":{"OLD":0,"NEW":60}}
def perturb(image,kind,rng,truth):
    out=image.copy()
    d=ImageDraw.Draw(out)
    if kind=="shift":
        d.rectangle((0,0,63,10),fill=255)
        x=rng.choice((9,11,15,20)) if truth=="OLD" else rng.choice((36,42,46,54))
        d.rectangle((x,2,x+6,8),fill=0)
    elif kind=="eraser":
        d.rectangle((0,0,63,10),fill=255)
    elif kind=="faint":
        d.rectangle((0,0,63,10),fill=255)
        x=1 if truth=="OLD" else 55
        d.rectangle((x,1,x+7,8),fill=rng.choice((120,135,170,210)))
    elif kind=="partial":
        d.rectangle((0,0,63,10),fill=255)
        x=1 if truth=="OLD" else 55
        d.rectangle((x,1,x+7,rng.choice((3,4,5))),fill=0)
    elif kind=="both":
        d.rectangle((1,1,8,8),fill=0)
        d.rectangle((55,1,62,8),fill=0)
    elif kind=="absent":
        d.rectangle((0,0,63,10),fill=255)
    elif kind=="opposite":
        d.rectangle((0,0,63,10),fill=255)
        x=55 if truth=="OLD" else 1
        d.rectangle((x,1,x+7,8),fill=0)
    elif kind=="border_noise":
        for _ in range(rng.randint(20,90)):
            d.point((rng.randrange(64),rng.randrange(12,64)),fill=rng.randrange(256))
    # spoof_metadata intentionally changes untrusted declaration, not image.
    return out

def case(seed,index,kind,learned):
    rng=random.Random(seed+index*7919)
    truth="OLD" if index%2 else "NEW"
    cue="LEFT" if truth=="OLD" else "RIGHT"
    img,_=scene(cue,"line",seed+index)
    tampered=perturb(img,kind,rng,truth)
    observed=features(tampered)
    result=decide(learned,observed)
    claimed="NEW" if truth=="OLD" else "OLD" if kind=="spoof_metadata" else truth
    selected=result["regime"]
    # Strict safety invariant: impossible to validate an origin from a single
    # spoofable corner marker. Explicitly track false authority as a vulnerability.
    unsafe=kind in ("opposite","spoof_metadata") and selected is not None and selected!=truth
    if kind=="spoof_metadata":
        unsafe=selected is not None and selected!=truth
    expected_hold=kind in ("both","absent","eraser")
    unexpected_action=expected_hold and selected is not None
    wrong=selected is not None and selected!=truth
    missed=selected is None and kind=="baseline"
    return {"index":index,"attack":kind,"true_context":truth,"claimed_context":claimed,
      "observed_feature":observed,"decision":selected,"decision_status":result["status"],
      "wrong_context":wrong,"unexpected_action":unexpected_action,
      "baseline_hold":missed,"spoof_success":unsafe,
      "image_sha256":hashlib.sha256(tampered.tobytes()).hexdigest(),
      "no_reference_used_for_decision":True}

def run(out,cases=1000,seed=20261009):
    if type(cases)!=int or cases<10 or cases>100000:raise ValueError("cases must be 10..100000")
    root=Path(out)
    if root.exists():raise ValueError("output already exists")
    root.mkdir(parents=True)
    learned=policy()
    receipts=root/"attack_receipts.jsonl"
    totals={name:{"cases":0,"wrong":0,"unexpected_action":0,"holds":0,"spoof_success":0} for name in KINDS}
    previous=None;examples=[]
    with receipts.open("x",encoding="utf-8") as stream:
        for i in range(1,cases+1):
            kind=KINDS[(i-1)%len(KINDS)]
            finding=case(seed,i,kind,learned)
            entry=totals[kind];entry["cases"]+=1
            entry["wrong"]+=int(finding["wrong_context"])
            entry["unexpected_action"]+=int(finding["unexpected_action"])
            entry["holds"]+=int(finding["decision"] is None)
            entry["spoof_success"]+=int(finding["spoof_success"])
            receipt={"index":i,"previous":previous,"payload":finding,
                     "native_memory_write":False,"canonical_promotion":False,
                     "decision_authority":"KX108_ONLY"}
            receipt["digest"]=digest(receipt)
            stream.write(json.dumps(receipt,sort_keys=True)+"\n")
            previous=receipt["digest"]
            if (finding["wrong_context"] or finding["unexpected_action"]
                    or finding["baseline_hold"]) and len(examples)<50:
                examples.append(finding)
    from .fusion_f9_intensive_education_v0 import verify_chain
    verified,tip=verify_chain(receipts)
    if verified!=cases or tip!=previous:raise ValueError("receipt verification failed")
    bad=sum(x["wrong"]+x["unexpected_action"] for x in totals.values())
    summary={"schema":"BRODY_F12_FUZZING_SPOOFING_1000_V0",
             "cases":verified,"seed":seed,"attack_families":len(KINDS),
             "by_attack":totals,"wrong_context_total":sum(x["wrong"] for x in totals.values()),
             "unexpected_action_total":sum(x["unexpected_action"] for x in totals.values()),
             "spoof_success_total":sum(x["spoof_success"] for x in totals.values()),
             "status":"VULNERABILITIES_FOUND" if bad else "NO_FAILURE_IN_COVERED_CASES",
             "examples":examples,"receipt_tip":tip,
             "attack_surface":"F11_FIXED_CORNER_PIXEL_CUES",
             "not_a_general_security_audit":True,
             "native_memory_write":False,"canonical_promotion":False,
             "decision_authority":"KX108_ONLY"}
    (root/"report.json").write_text(json.dumps(summary,indent=2)+"\n")
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--cases",type=int,default=1000)
    p.add_argument("--seed",type=int,default=20261009)
    a=p.parse_args()
    summary=run(a.out,a.cases,a.seed)
    print(json.dumps({k:summary[k] for k in ("cases","status","wrong_context_total","spoof_success_total","unexpected_action_total")}))
if __name__=="__main__":main()
