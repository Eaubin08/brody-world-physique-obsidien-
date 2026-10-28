"""P159 choose an experiment by expected information gain before seeing outcome.

Three learned regimes with different responses to interventions. Probe outcomes
are learnt from pixel trajectories (training), then frozen. Test selection uses
only their empirical response distribution and prices; hidden truth is never
passed to policy. Out-of-bank testing is disaggregated.
"""
import argparse,json,math,random,time
from pathlib import Path
from PIL import Image,ImageDraw
REGIMES=("flat","slope","spring")
PROBES={"observe":{"cost":0.1,"factors":(0,0,0)},
        "tap":{"cost":0.7,"factors":(0,-1,1)},
        "tilt":{"cost":1.0,"factors":(0,-2,2)},
        "weak_tap":{"cost":0.25,"factors":(0,-.15,.15)}}
CONDITIONS=("tap_available","tilt_only","weak_only","no_informative","cost_sensitive","novel_only","known_vs_novel")
W,H=116,68
def trajectory(rng,regime,probe):
    x=rng.randint(22,34);v=rng.choice((3,4))
    coef={"flat":0,"slope":-1,"spring":1,"novel":3}[regime]
    factor={"observe":0,"tap":1,"tilt":2,"weak_tap":.15}[probe]
    xs=[]
    for t in range(8):
        xs.append(x)
        if t>=3:v+=coef*factor
        x+=v
    return xs
def image_at(x):
    im=Image.new("RGB",(W,H),(245,244,242));d=ImageDraw.Draw(im)
    xx=round(x);d.ellipse((xx-3,30,xx+3,36),fill=(222,40,50))
    return im
def measure(images):
    xs=[]
    for im in images:
        pix=im.load();hits=[]
        for y in range(29,38):
            for x in range(W):
                r,g,b=pix[x,y]
                if r>190 and g<90 and b<100:hits.append(x)
        xs.append(sum(hits)/len(hits) if hits else None)
    return xs
def response(xs):
    if any(x is None for x in xs[3:7]):return None
    return ((xs[5]-2*xs[4]+xs[3])+(xs[6]-2*xs[5]+xs[4]))/2
def entropy(weights):
    return -sum(p*math.log2(p) for p in weights if p>0)
def probabilities(bank,probe,prior):
    # Learn-from-pixels responses with discrete tolerance bins; action outcomes
    # induce a partition of hypotheses. Entropy reduction measured ex ante.
    values=[bank[name][probe] for name in REGIMES]
    groups={}
    for i,value in enumerate(values):
        bucket=round(value/.35) if value is not None else "missing"
        groups.setdefault(bucket,[]).append(i)
    after=sum(sum(prior[i] for i in indices)*entropy([prior[i]/sum(prior[k] for k in indices) for i in indices])
              for indices in groups.values())
    return entropy(prior)-after
def choose_probe(bank,available,prior=(1/3,1/3,1/3),price_weight=.25):
    options=[]
    for action in available:
        info=probabilities(bank,action,prior)
        utility=info-price_weight*PROBES[action]["cost"]
        options.append({"action":action,"information":round(info,6),
                        "cost":PROBES[action]["cost"],"utility":round(utility,6)})
    options.sort(key=lambda z:(-z["utility"],z["cost"],z["action"]))
    if not options or options[0]["information"]<.1 or options[0]["utility"]<=0:
        return {"decision":"HOLD","reason":"NO_WORTHWHILE_DISCRIMINATING_PROBE","options":options}
    return {"decision":"PROBE","action":options[0]["action"],"options":options}
def classify(bank,action,observed,tolerance=.38):
    if observed is None:return {"decision":"HOLD","reason":"NO_OBSERVATION"}
    matches=sorted((abs(observed-bank[name][action]),name) for name in REGIMES)
    best=matches[0][0]
    if best>tolerance:return {"decision":"HOLD","reason":"NOVEL_RESPONSE","distance":best}
    plausible=[name for distance,name in matches if distance<=best+.08]
    if len(plausible)>1:return {"decision":"MULTI","reason":"EQUIVALENT_RESPONSES","hypotheses":plausible}
    return {"decision":"SELECT","selected":matches[0][1],"distance":best}
def learn(rng,lessons_each):
    bank={name:{} for name in REGIMES}
    for name in REGIMES:
        for action in PROBES:
            measurements=[]
            for _ in range(lessons_each):
                images=[image_at(x) for x in trajectory(rng,name,action)]
                measurements.append(response(measure(images)))
                for im in images:im.close()
            good=[v for v in measurements if v is not None]
            bank[name][action]=sum(good)/len(good) if good else None
    return bank
def run(out,minutes=12,seed=159,lessons_each=25,exam_each=140):
    if not (2<=minutes<=60 and 10<=lessons_each<=300 and 20<=exam_each<=2000):raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);started=time.monotonic();rng=random.Random(seed+1);exam_rng=random.Random(seed+2000)
    bank=learn(rng,lessons_each)
    (root/"FROZEN_PROBE_RESPONSES.json").write_text(json.dumps(bank,indent=2),encoding="utf8")
    available_map={"tap_available":["observe","weak_tap","tap","tilt"],
       "tilt_only":["observe","tilt"],"weak_only":["observe","weak_tap"],
       "no_informative":["observe"],"cost_sensitive":["observe","tap","tilt"],
       "novel_only":["tap","tilt"],"known_vs_novel":["tap","tilt"]}
    stats={};expired=False;deadline=started+minutes*60
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for condition in CONDITIONS:
            st={"n":0,"PROBE":0,"HOLD_BEFORE":0,"SELECT":0,"MULTI":0,"HOLD_AFTER":0,
                "correct_known":0,"known_total":0,"novel_total":0,"novel_hold":0,"false_known_on_novel":0,
                "selected_cost":0.,"chosen_actions":{}}
            for j in range(exam_each):
                if time.monotonic()>=deadline:expired=True;break
                truth="novel" if condition=="novel_only" else (
                    exam_rng.choice(REGIMES+("novel",)) if condition=="known_vs_novel" else exam_rng.choice(REGIMES))
                opts=available_map[condition]
                pre=choose_probe(bank,opts,price_weight=.7 if condition=="cost_sensitive" else .25)
                st["n"]+=1
                if pre["decision"]=="HOLD":
                    st["HOLD_BEFORE"]+=1;post={"decision":"HOLD","reason":"NO_PROBE"}
                else:
                    st["PROBE"]+=1
                    a=pre["action"];st["selected_cost"]+=PROBES[a]["cost"]
                    st["chosen_actions"][a]=st["chosen_actions"].get(a,0)+1
                    imgs=[image_at(x) for x in trajectory(exam_rng,truth,a)]
                    observed=response(measure(imgs))
                    post=classify(bank,a,observed)
                    for im in imgs:im.close()
                if truth=="novel":
                    st["novel_total"]+=1
                    st["novel_hold"]+=int(post["decision"]=="HOLD")
                    st["false_known_on_novel"]+=int(post["decision"]=="SELECT")
                else:
                    st["known_total"]+=1
                    st["correct_known"]+=int(post["decision"]=="SELECT" and post.get("selected")==truth)
                st[post["decision"] if post["decision"] in ("SELECT","MULTI") else "HOLD_AFTER"]+=1
                log.write(json.dumps({"condition":condition,"index":j,"hidden_truth":truth,"before":pre,"after":post})+"\n")
            stats[condition]=st
            if expired:break
    report={"schema":"BRODY_P159_EXPECTED_INFORMATION_GAIN","conditions_expected":len(CONDITIONS),
      "conditions_completed":sum(v["n"]==exam_each for v in stats.values()),
      "episodes":sum(v["n"] for v in stats.values()),
      "duration_seconds":round(time.monotonic()-started,3),
      "stopped_by":"TIME_BUDGET" if expired else "EXAM_CAP",
      "frozen_empirical_models":bank,"conditions":stats,
      "candidate_probes_programmed":True,"probe_selection_uses_exam_truth":False,
      "real_world_probe_actuation":False,"unknown_regime_detection_guaranteed":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=12);p.add_argument("--seed",type=int,default=159)
    p.add_argument("--lessons-each",type=int,default=25);p.add_argument("--exam-each",type=int,default=140)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.lessons_each,a.exam_each)
    print(json.dumps({k:v for k,v in r.items() if k not in ("conditions","frozen_empirical_models")},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
