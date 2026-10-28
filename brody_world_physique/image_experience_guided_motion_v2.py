"""Experience-guided motion prediction V2.

Predict using a pre-feedback sealed memory of earlier corrected sequences.
A matching motion *context* can inform the model selection; unrelated memories
do not vote. Teacher feedback is separate, and original forecast is immutable.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
from .image_multihypothesis_motion_memory_v1 import track,position,KINDS,read,write
from .image_observed_motion_school_v1 import analyze,render
from .fusion_f9_intensive_education_v0 import digest

SCHEMA="BRODY_CONTEXTUAL_PHYSICS_MEMORY_V2"
def fresh():
    return {"schema":SCHEMA,"experiences":[],"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
def load(path):
    if path is None:return fresh()
    state=read(path);seal=state.pop("digest",None)
    if seal!=digest(state) or state.get("schema")!=SCHEMA or state.get("native_memory_write") is not False or state.get("canonical_promotion") is not False or state.get("decision_authority")!="KX108_ONLY":
        raise ValueError("CORRUPTED_PHYSICS_MEMORY")
    return state
def context(obs):
    # Motion signs are local descriptions, not universal physical laws.
    displacements=[]
    for a,b in zip(obs,obs[1:]):
        dt=b["t"]-a["t"]
        displacements.append(((b["x"]-a["x"])/dt,(b["y"]-a["y"])/dt))
    last=displacements[-1];prev=displacements[-2]
    axis="vertical" if abs(last[1])>=abs(last[0]) else "horizontal"
    speed=math.hypot(*last)
    sign_last=last[1] if axis=="vertical" else last[0]
    sign_prev=prev[1] if axis=="vertical" else prev[0]
    if sign_last*sign_prev<0:regime="reversal"
    elif speed<0.5:regime="stationary"
    elif abs(sign_last)>abs(sign_prev)+0.7:regime="speeding_up"
    elif abs(sign_last)+0.7<abs(sign_prev):regime="slowing_down"
    else:regime="steady"
    return axis+"|"+regime
def backtest(obs):
    # All models are evaluated on the same earlier known final frame.
    earlier=obs[:-1];actual=obs[-1]
    errors={}
    for kind in KINDS:
        pred=position(earlier,kind,actual["t"])
        errors[kind]=round(math.hypot(actual["x"]-pred["x"],actual["y"]-pred["y"]),6)
    return errors
def decision(obs,memory):
    c=context(obs);baseline=backtest(obs)
    eligible=[x for x in memory["experiences"] if x["context"]==c]
    # Fewer than 2 corrected independent trajectories: rely on local evidence.
    totals={}
    if len({x["forecast_digest"] for x in eligible})>=2:
        for k in KINDS:totals[k]=sum(x["errors_px"][k] for x in eligible)/len(eligible)
        origin="EXPERIENCE_MATCHED"
    else:
        totals=baseline.copy();origin="LOCAL_BACKTEST"
    ranked=sorted((val,key) for key,val in totals.items())
    best=ranked[0][0];ties=[k for v,k in ranked if abs(v-best)<1e-6]
    chosen=ties[0] if len(ties)==1 else None
    return {"context":c,"evidence_source":origin,"eligible_episodes":len(eligible),
            "backtest_errors_px":baseline,"selection_errors_px":totals,
            "selected":chosen,"mode":"CANDIDATE" if chosen else "DOUBT",
            "hypotheses":[{"model":k,"error_px":v} for v,k in ranked[:3]]}
def forecast(manifest,out,previous=None):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    spec=read(manifest);obs=track(spec);future=float(spec["predict_t"])
    if future<=obs[-1]["t"]:raise ValueError("FUTURE_TIME_REQUIRED")
    memory=load(previous)
    choice=decision(obs,memory)
    outputs={kind:position(obs,kind,future) for kind in KINDS}
    body={"schema":"BRODY_CONTEXTUAL_PHYSICS_FORECAST_V2",
          "observations":obs,"predict_t":future,"choice":choice,
          "hypotheses":outputs,"prior_memory_digest":digest(memory),
          "native_memory_write":False,"canonical_promotion":False,
          "decision_authority":"KX108_ONLY"}
    body["digest"]=digest(body)
    dest.mkdir(parents=True)
    write(dest/"sealed_forecast.json",body)
    for model,pred in outputs.items():render(pred,dest/(model.lower()+".png"))
    report={"schema":"BRODY_CONTEXTUAL_PHYSICS_FORECAST_REPORT_V2",
        "context":choice["context"],"mode":choice["mode"],
        "selected":choice["selected"],"evidence_source":choice["evidence_source"],
        "eligible_episodes":choice["eligible_episodes"],"forecast_sealed":True,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    write(dest/"MASTER_REPORT.json",report);return report
def correct(forecast_file,observed_image,out,previous=None):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    original=read(forecast_file);seal=original.pop("digest",None)
    if seal!=digest(original) or original.get("schema")!="BRODY_CONTEXTUAL_PHYSICS_FORECAST_V2" or original.get("native_memory_write") is not False or original.get("canonical_promotion") is not False or original.get("decision_authority")!="KX108_ONLY":
        raise ValueError("TAMPERED_FORECAST")
    actual=analyze(observed_image)
    if actual["source_sha256"] in {o["source_sha256"] for o in original["observations"]}:
        raise ValueError("FEEDBACK_LEAK")
    state=load(previous)
    errors={k:round(math.hypot(p["x"]-actual["x"],p["y"]-actual["y"]),5)
            for k,p in original["hypotheses"].items()}
    episode={"forecast_digest":seal,"context":original["choice"]["context"],
             "feedback_sha256":actual["source_sha256"],"errors_px":errors,
             "original_selection":original["choice"]["selected"]}
    existing=next((e for e in state["experiences"] if e["forecast_digest"]==seal),None)
    if existing and existing!=episode:raise ValueError("CONTRADICTORY_FEEDBACK")
    if not existing:state["experiences"].append(episode)
    state["digest"]=digest(state)
    dest.mkdir(parents=True)
    write(dest/"candidate_physics_memory.json",state)
    result={"schema":"BRODY_CONTEXTUAL_PHYSICS_CORRECTION_V2",
            "context":episode["context"],"errors_px":errors,
            "experiences":len(state["experiences"]),
            "original_forecast_immutable":True,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"}
    write(dest/"MASTER_REPORT.json",result);return result
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("forecast","correct"),required=True)
    p.add_argument("--manifest");p.add_argument("--forecast");p.add_argument("--observed")
    p.add_argument("--previous");p.add_argument("--out",required=True)
    a=p.parse_args()
    result=forecast(a.manifest,a.out,a.previous) if a.mode=="forecast" else correct(a.forecast,a.observed,a.out,a.previous)
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
