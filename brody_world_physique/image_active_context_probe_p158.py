"""P158 active context discovery, intervention and identifiability.

Two hypotheses have identical initial observations but differ after a probe.
No oracle context is given to the learner. Probe action and its observed
consequence are simulated; hidden truth is used only by examiner.
"""
import argparse,json,random,time
from pathlib import Path
from PIL import Image,ImageDraw
from .image_context_coexistence_p157 import observed,induce

W,H=120,76
CONDITIONS=("discriminating_probe","no_probe","uninformative_probe","noisy_probe","out_of_bank")
def render(x,rng,noise=False):
    im=Image.new("RGB",(W,H),(246,246,242));d=ImageDraw.Draw(im)
    cx=round(x);d.ellipse((cx-3,35,cx+3,41),fill=(224,37,47))
    if noise:
        for _ in range(15):d.point((rng.randrange(W),rng.randrange(H)),fill=(rng.randrange(180),rng.randrange(180),rng.randrange(180)))
    return im
def trajectory(regime,probe,rng,noise=False):
    # Same initial trajectory for every latent regime. After a discriminating
    # test, hidden regimes exhibit distinct acceleration responses.
    x=rng.randint(23,31);v=rng.choice((3,4))
    imgs=[]
    for t in range(7):
        imgs.append(render(x,rng,noise))
        if t<3 or probe=="uninformative":acc=0
        elif regime=="flat":acc=0
        elif regime=="slope":acc=-1
        else:acc=1
        v+=acc;x+=v
    return imgs
def learn(rng,n=30):
    bank={}
    for regime in ("flat","slope"):
        series=[]
        for _ in range(n):
            frames=trajectory(regime,"discriminating",rng)
            xs=observed(frames)
            series.extend(xs[i+2]-2*xs[i+1]+xs[i] for i in (3,4) if xs[i] is not None and xs[i+1] is not None and xs[i+2] is not None)
            for frame in frames:frame.close()
        bank[regime]=sum(series)/len(series) if series else None
    return bank
def decide(before,bank,request,probe_available=True,after=None,tol=.32,probe_informative=True):
    # Decision before probing: competing futures equally compatible.
    choices={k:v for k,v in bank.items() if v is not None}
    if len(choices)<2:return {"decision":"HOLD","reason":"INSUFFICIENT_MODELS"}
    if after is None:
        if request=="possibilities":return {"decision":"MULTI","hypotheses":list(choices),"reason":"OBSERVATIONALLY_EQUIVALENT"}
        if probe_available:return {"decision":"PROBE","action":"observe_after_discriminating_intervention","reason":"INFORMATION_GAIN"}
        return {"decision":"HOLD","reason":"UNIDENTIFIABLE_WITHOUT_PROBE","hypotheses":list(choices)}
    if not probe_informative:\n        return {"decision":"MULTI" if request=="possibilities" else "HOLD","reason":"PROBE_NON_DISCRIMINATING","hypotheses":list(choices)}\n    measured=observed(after)
    # The first four time slices cannot discriminate. Acceleration estimated
    # only from the intervention response after t=3.
    if len(measured)<7 or any(x is None for x in measured[3:7]):
        return {"decision":"HOLD","reason":"INSUFFICIENT_POST_PROBE_OBSERVATIONS"}
    dv=[measured[i+2]-2*measured[i+1]+measured[i] for i in (3,4)]
    estimate=sum(dv)/len(dv)
    matches=[(abs(estimate-a),name) for name,a in choices.items()]
    matches.sort()
    if matches[0][0]>tol:return {"decision":"HOLD","reason":"NOVEL_DYNAMICS","observed_acceleration":estimate}
    if len(matches)>1 and matches[1][0]-matches[0][0]<tol:
        return {"decision":"MULTI","reason":"POST_PROBE_AMBIGUOUS","hypotheses":[name for _,name in matches]}
    return {"decision":"SELECT","selected":matches[0][1],"observed_acceleration":estimate}
def run(out,minutes=12,seed=158,lessons_each=30,exam_each=140):
    if not(2<=minutes<=60 and 10<=lessons_each<=500 and 20<=exam_each<=2000):raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);st=time.monotonic();deadline=st+minutes*60
    tr=random.Random(seed+11);ex=random.Random(seed+9191)
    bank=learn(tr,lessons_each)
    (root/"FROZEN_HYPOTHESES.json").write_text(json.dumps(bank,indent=2),encoding="utf8")
    scores={};stop=False
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for condition in CONDITIONS:
            row={"n":0,"pre_probe_correct":0,"post_select":0,"post_correct":0,
                 "post_hold":0,"post_multi":0,"false_certainty":0}
            for i in range(exam_each):
                if time.monotonic()>=deadline:stop=True;break
                regime=ex.choice(("flat","slope","novel")) if condition=="out_of_bank" else ex.choice(("flat","slope"))
                imgs=trajectory(regime,"uninformative" if condition=="uninformative_probe" else "discriminating",ex,condition=="noisy_probe")
                first=imgs[:4]
                req="possibilities" if condition=="uninformative_probe" else "single"
                pre=decide(first,bank,req,probe_available=condition!="no_probe")
                expected=("MULTI" if condition=="uninformative_probe" else "HOLD" if condition=="no_probe" else "PROBE")
                row["pre_probe_correct"]+=int(pre["decision"]==expected)
                if condition in ("no_probe","uninformative_probe"):
                    post=pre if condition=="no_probe" else decide(first,bank,"single",after=imgs,probe_informative=False)
                else:post=decide(first,bank,"single",after=imgs)
                row["n"]+=1
                row["post_select"]+=int(post["decision"]=="SELECT")
                row["post_hold"]+=int(post["decision"]=="HOLD")
                row["post_multi"]+=int(post["decision"]=="MULTI")
                row["post_correct"]+=int(post["decision"]=="SELECT" and post.get("selected")==regime)
                row["false_certainty"]+=int(post["decision"]=="SELECT" and post.get("selected")!=regime)
                log.write(json.dumps({"condition":condition,"case":i,"hidden_truth":regime,"before":pre,"after":post})+"\n")
                for im in imgs:im.close()
            scores[condition]=row
            if stop:break
    report={"schema":"BRODY_P158_ACTIVE_CONTEXT_PROBE",
      "episodes":sum(s["n"] for s in scores.values()),
      "conditions_completed":sum(s["n"]==exam_each for s in scores.values()),
      "conditions_expected":len(CONDITIONS),"duration_seconds":round(time.monotonic()-st,3),
      "stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP",
      "hypotheses":bank,"per_condition":scores,
      "probe_actuation":"SIMULATED","hidden_regime_in_inference":False,
      "probe_design_learned_autonomously":False,"out_of_distribution_physics_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=12);p.add_argument("--seed",type=int,default=158)
    p.add_argument("--lessons-each",type=int,default=30);p.add_argument("--exam-each",type=int,default=140)
    a=p.parse_args();result=run(a.out,a.minutes,a.seed,a.lessons_each,a.exam_each)
    print(json.dumps({k:v for k,v in result.items() if k!="per_condition"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
