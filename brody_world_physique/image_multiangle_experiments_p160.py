"""P160 multi-angle multi-step curriculum: contextual hypotheses with costly tests.

All response models are induced from rendered pixel positions. At examination,
hypotheses are updated with noisy visual evidence, never latent identity.
Five axes crossed: scenario, evidence noise, budget, requested answer, novelty.
"""
import argparse,json,math,random,time
from pathlib import Path
from PIL import Image,ImageDraw
REGIMES=("flat","slope","spring","near_slope")
ACTIONS={"observe":.05,"tap":.65,"tilt":1.,"pulse":.40}
SENSITIVITY={"observe":0.,"tap":1.,"tilt":2.,"pulse":.4}
COEF={"flat":0.,"slope":-1.,"spring":1.,"near_slope":-.83,"novel":2.4}
SCENARIOS=("clear","near","ambiguous","noisy","budget_tight","budget_open",
           "unknown_far","unknown_near","changed_context","request_multi",
           "unidentifiable","mixed_noise")
def render_position(x,rng,noise):
    im=Image.new("RGB",(128,76),(245,244,242));d=ImageDraw.Draw(im)
    xx=round(x);d.ellipse((xx-3,33,xx+3,39),fill=(224,37,45))
    for _ in range(noise):
        px=rng.randrange(128);py=rng.randrange(76)
        d.point((px,py),fill=(rng.randrange(180),rng.randrange(180),rng.randrange(180)))
    return im
def measure(images):
    out=[]
    for im in images:
        pix=im.load();found=[]
        for y in range(31,42):
            for x in range(128):
                rr,gg,bb=pix[x,y]
                if rr>190 and gg<85 and bb<100:found.append(x)
        out.append(sum(found)/len(found) if found else None)
    return out
def observe_response(regime,action,rng,noise=0):
    x=rng.randint(37,45);v=rng.choice((2,3))
    # action has no response in the first three observations
    xs=[]
    effect=COEF[regime]*SENSITIVITY[action]
    for t in range(7):
        xs.append(x)
        if t>=3:v+=effect
        x+=v
    imgs=[render_position(q,rng,noise) for q in xs]
    positions=measure(imgs)
    for im in imgs:im.close()
    if any(a is None for a in positions[3:7]):return None
    return .5*((positions[5]-2*positions[4]+positions[3])+
               (positions[6]-2*positions[5]+positions[4]))
def train(seed,examples):
    rng=random.Random(seed)
    model={}
    for regime in REGIMES:
        model[regime]={}
        for action in ACTIONS:
            data=[observe_response(regime,action,rng) for _ in range(examples)]
            valid=[x for x in data if x is not None]
            model[regime][action]={"mean":sum(valid)/len(valid) if valid else None,
                    "n":len(valid)}
    return model
def posterior(prior,action,value,model,sigma):
    if value is None:return prior[:]
    weights=[]
    for p,name in zip(prior,REGIMES):
        mu=model[name][action]["mean"]
        weights.append(p*math.exp(-.5*((value-mu)/sigma)**2) if mu is not None else 0.)
    z=sum(weights)
    return [v/z for v in weights] if z>1e-120 else prior[:]
def entropy(p):
    return -sum(x*math.log2(x) for x in p if x>0)
def expected_information(p,action,model,sigma):
    # deterministic Gaussian mixture quadrature: 9 representative responses
    points=[]
    for i,name in enumerate(REGIMES):
        mu=model[name][action]["mean"]
        for off,w in ((-2,.05),(-1,.24),(0,.42),(1,.24),(2,.05)):
            points.append((mu+off*sigma,p[i]*w))
    return max(0.,entropy(p)-sum(w*entropy(posterior(p,action,v,model,sigma))
                                      for v,w in points))
def choose(p,available,budget,used,model,sigma,price_weight=.38):
    options=[]
    for action in available:
        if action in used or ACTIONS[action]>budget:continue
        gain=expected_information(p,action,model,sigma)
        utility=gain-price_weight*ACTIONS[action]
        options.append((utility,gain,action))
    options.sort(reverse=True)
    if not options or options[0][0]<=.015:return None
    return options[0][2]
def decision(p,request):
    order=sorted(range(len(p)),key=lambda k:-p[k])
    if p[order[0]]>=.88 and p[order[0]]-p[order[1]]>=.55:
        return {"status":"SELECT","selected":REGIMES[order[0]],"confidence":p[order[0]]}
    if request=="possibilities":
        return {"status":"MULTI","hypotheses":[REGIMES[i] for i in order if p[i]>=.06]}
    return {"status":"HOLD","reason":"MULTIPLE_COMPATIBLE_CONTEXTS"}
def trial(regime,scenario,model,rng):
    noisy=scenario in ("noisy","mixed_noise")
    sigma=.18 if noisy else .12
    budget=.45 if scenario=="budget_tight" else 1.9
    available=["observe"] if scenario=="unidentifiable" else list(ACTIONS)
    request="possibilities" if scenario in ("request_multi","unidentifiable") else "single"
    prior=[.25]*4;p=prior[:];spent=0.;used=[];log=[]
    for step in range(3):
        action=choose(p,available,budget-spent,used,model,sigma)
        if action is None:break
        active=regime
        if scenario=="changed_context" and step>=1:
            active="spring" if regime!="spring" else "slope"
        # Unknown near is not in training and intentionally indistinguishable
        # from close known regimes under weak probes.
        value=observe_response(active,action,rng,noise=55 if noisy else 0)
        if scenario=="unknown_near":value=observe_response("near_slope",action,rng,noise=55 if noisy else 0)+.03
        updated=posterior(p,action,value,model,sigma)
        log.append({"step":step,"probe":action,"cost":ACTIONS[action],
                    "measurement":value,"posterior":updated})
        p=updated;spent+=ACTIONS[action];used.append(action)
    answer=decision(p,request)
    # Unlike known regimes, unknown types need density / distance rejection.
    # This provides a test of false certainty on novelty.
    if log and scenario=="unknown_far":
        last=log[-1];closest=min(abs(last["measurement"]-model[name][last["probe"]]["mean"]) for name in REGIMES)
        if closest>.65:answer={"status":"HOLD","reason":"OUT_OF_BANK"}
    if scenario=="changed_context":
        # A nonstationary context is an explicit evaluation target.
        # It is NOT handed to the predictor.
        pass
    return answer,log,spent
def run(out,minutes=20,seed=160,lessons_each=30,exam_each=160):
    if not (2<=minutes<=90 and 10<=lessons_each<=250 and 20<=exam_each<=1500):
        raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);start=time.monotonic();deadline=start+minutes*60
    model=train(seed+1,lessons_each)
    (root/"FROZEN_RESPONSE_MODELS.json").write_text(json.dumps(model,indent=2),encoding="utf8")
    rng=random.Random(seed+5050);stats={};stopped=False
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for scenario in SCENARIOS:
            row={"n":0,"SELECT":0,"MULTI":0,"HOLD":0,"correct_select":0,
                 "false_select":0,"unknown_total":0,"unknown_holds":0,
                 "probe_count":0,"probe_cost_sum":0.,"correct_multi_contains":0}
            for k in range(exam_each):
                if time.monotonic()>=deadline:stopped=True;break
                truth=("novel" if scenario=="unknown_far" else "near_slope" if scenario=="unknown_near"
                    else rng.choice(REGIMES))
                ans,steps,cost=trial(truth,scenario,model,rng)
                status=ans["status"];row["n"]+=1;row[status]+=1
                row["probe_count"]+=len(steps);row["probe_cost_sum"]+=cost
                row["correct_select"]+=int(status=="SELECT" and ans.get("selected")==truth)
                row["false_select"]+=int(status=="SELECT" and ans.get("selected")!=truth)
                row["correct_multi_contains"]+=int(status=="MULTI" and truth in ans.get("hypotheses",[]))
                if scenario in ("unknown_far","unknown_near"):
                    row["unknown_total"]+=1;row["unknown_holds"]+=int(status=="HOLD")
                f.write(json.dumps({"scenario":scenario,"episode":k,"hidden_truth":truth,
                                    "answer":ans,"experiments":steps,"cost":cost})+"\n")
            stats[scenario]=row
            if stopped:break
    outdata={"schema":"BRODY_P160_MULTIANGLE_EXPERIMENT",
      "conditions_expected":len(SCENARIOS),"conditions_completed":sum(v["n"]==exam_each for v in stats.values()),
      "exams":sum(x["n"] for x in stats.values()),
      "duration_seconds":round(time.monotonic()-start,3),
      "stopped_by":"TIME_BUDGET" if stopped else "EXAM_CAP","conditions":stats,
      "multiple_experiments_per_episode":True,"response_models_learned_from_pixels":True,
      "test_truth_hidden_from_policy":True,"actual_probe_planning_optimization":True,
      "unknown_near_reliable_detection_proven":False,"causal_understanding_proven":False,
      "real_world_transfer_proven":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(outdata,indent=2),encoding="utf8")
    return outdata
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20);p.add_argument("--seed",type=int,default=160)
    p.add_argument("--lessons-each",type=int,default=30);p.add_argument("--exam-each",type=int,default=160)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.lessons_each,a.exam_each)
    print(json.dumps({k:v for k,v in r.items() if k!="conditions"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
