"""Brody candidate motion-model comparison, blind forecasts, and memory review.

Models are predefined hypothesis families, never inferred physical laws.
Forecasts are sealed before feedback. Feedback can be graded in a later run.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
from .image_observed_motion_school_v1 import analyze,render
from .fusion_f9_intensive_education_v0 import digest,verify_chain

KINDS=("STILL","VELOCITY","ACCELERATION")
def read(path):return json.loads(Path(path).read_text(encoding="utf-8-sig"))
def write(path,body):
    with Path(path).open("x",encoding="utf-8") as f:json.dump(body,f,indent=2,sort_keys=True);f.write("\n")
def track(spec):
    obs=[]
    for row in spec["observations"]:
        point=analyze(row["file"]);point["t"]=float(row["t"]);obs.append(point)
    if len(obs)<4 or any(a["t"]>=b["t"] for a,b in zip(obs,obs[1:])):raise ValueError("FOUR_ORDERED_FRAMES_REQUIRED")
    return obs
def position(obs,kind,t):
    a,b,c=obs[-3:];dt=t-c["t"]
    if dt<0:raise ValueError("BACKWARD_PREDICTION")
    result={"t":t,"radius":c["radius"]}
    for axis in ("x","y"):
        s1=(b[axis]-a[axis])/(b["t"]-a["t"])
        s2=(c[axis]-b[axis])/(c["t"]-b["t"])
        acceleration=2*(s2-s1)/(c["t"]-a["t"])
        if kind=="STILL":value=c[axis]
        elif kind=="VELOCITY":value=c[axis]+s2*dt
        elif kind=="ACCELERATION":
            value=c[axis]+(s2+acceleration*(c["t"]-b["t"])/2)*dt+acceleration*dt*dt/2
        else:raise ValueError("UNKNOWN_HYPOTHESIS")
        result[axis]=value
    return result
def compare(obs):
    # Backtest on last known frame: train on all preceding observations.
    train=obs[:-1];last=obs[-1]
    scores={}
    for name in KINDS:
        forecast=position(train,name,last["t"])
        scores[name]=round(math.hypot(forecast["x"]-last["x"],forecast["y"]-last["y"]),5)
    best=min(scores.values())
    winners=[name for name in KINDS if abs(scores[name]-best)<1e-6]
    # A single validation frame cannot securely distinguish tied explanations.
    return {"scores_px":scores,"best_hypotheses":winners,
            "mode":"DOUBT" if len(winners)>1 else "CANDIDATE",
            "selected":winners[0] if len(winners)==1 else None}
def forecast(manifest,out):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    spec=read(manifest);obs=track(spec);t=float(spec["predict_t"])
    if t<=obs[-1]["t"]:raise ValueError("FUTURE_TIME_REQUIRED")
    decision=compare(obs)
    possibilities={name:position(obs,name,t) for name in KINDS}
    evidence={"schema":"BRODY_MULTIHYPOTHESIS_MOTION_V1","observations":obs,
        "selection":decision,"forecasts":possibilities,"predict_t":t,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    evidence["digest"]=digest(evidence)
    dest.mkdir(parents=True)
    write(dest/"sealed_forecast.json",evidence)
    for name,pred in possibilities.items():render(pred,dest/(name.lower()+".png"))
    report={"schema":"BRODY_MOTION_MULTI_HYPOTHESIS_REPORT_V1",
        "model_hypotheses":list(KINDS),"selection":decision,
        "frames":len(obs),"predictions_sealed_before_feedback":True,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    write(dest/"MASTER_REPORT.json",report)
    return report
def feedback(forecast_file,observed_image,out,prior_memory=None):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    sealed=read(forecast_file);seal=sealed.pop("digest",None)
    if seal!=digest(sealed) or sealed.get("schema")!="BRODY_MULTIHYPOTHESIS_MOTION_V1":raise ValueError("BAD_FORECAST_SEAL")
    real=analyze(observed_image)
    if real["source_sha256"] in {r["source_sha256"] for r in sealed["observations"]}:raise ValueError("FEEDBACK_LEAK")
    memory={"schema":"BRODY_LOCAL_PHYSICAL_EXPERIENCE_V1","episodes":[],
            "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    if prior_memory:
        old=read(prior_memory);hash_value=old.pop("digest",None)
        if hash_value!=digest(old) or old.get("schema")!=memory["schema"] or old.get("native_memory_write") is not False or old.get("canonical_promotion") is not False or old.get("decision_authority")!="KX108_ONLY":
            raise ValueError("BAD_PREVIOUS_MEMORY")
        memory=old
    errors={name:round(math.hypot(p["x"]-real["x"],p["y"]-real["y"]),4)
            for name,p in sealed["forecasts"].items()}
    episode={"forecast_digest":seal,"feedback_sha256":real["source_sha256"],
             "predicted_time":sealed["predict_t"],"errors_px":errors,
             "prior_selection":sealed["selection"],
             "status":"OBSERVED_CORRECTION_NOT_PHYSICAL_LAW"}
    if not any(e["forecast_digest"]==seal for e in memory["episodes"]):
        memory["episodes"].append(episode)
    memory["digest"]=digest(memory)
    dest.mkdir(parents=True)
    write(dest/"candidate_experience_memory.json",memory)
    result={"schema":"BRODY_PHYSICAL_FEEDBACK_REPORT_V1","errors_px":errors,
        "saved_episodes":len(memory["episodes"]),"memory_cross_session":True,
        "forecast_unchanged":True,"native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    write(dest/"MASTER_REPORT.json",result)
    return result
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("forecast","feedback"),required=True)
    p.add_argument("--manifest");p.add_argument("--forecast");p.add_argument("--observed")
    p.add_argument("--previous");p.add_argument("--out",required=True)
    a=p.parse_args()
    result=forecast(a.manifest,a.out) if a.mode=="forecast" else feedback(a.forecast,a.observed,a.out,a.previous)
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
