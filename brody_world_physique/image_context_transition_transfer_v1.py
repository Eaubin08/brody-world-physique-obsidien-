"""Brody P129 — local event/context transfer from corrected trajectories.

A transition is an observed relation between successive displacements, not a
claim about gravity or collisions. Future hypotheses use teacher-confirmed
episodes from other source groups only, with bounded doubt.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from .image_multihypothesis_motion_memory_v1 import track,read,write
from .image_observed_motion_school_v1 import analyze,render
from .fusion_f9_intensive_education_v0 import digest

SCHEMA="BRODY_TRANSITION_CONTEXT_MEMORY_V1"
def fresh():
    return {"schema":SCHEMA,"episodes":[],"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
def load(path):
    if not path:return fresh()
    d=read(path);seal=d.pop("digest",None)
    if seal!=digest(d) or d.get("schema")!=SCHEMA or d.get("native_memory_write") is not False or d.get("canonical_promotion") is not False or d.get("decision_authority")!="KX108_ONLY":raise ValueError("BAD_MEMORY")
    return d
def vector(a,b):
    dt=b["t"]-a["t"]
    if dt<=0:raise ValueError("BAD_TIMESTAMPS")
    return ((b["x"]-a["x"])/dt,(b["y"]-a["y"])/dt)
def context(obs):
    if len(obs)<4:raise ValueError("FOUR_FRAMES_REQUIRED")
    v=[vector(a,b) for a,b in zip(obs,obs[1:])]
    a,b=v[-2:];sa=math.hypot(*a);sb=math.hypot(*b)
    dominant="vertical" if abs(b[1])>=abs(b[0]) else "horizontal"
    if sa>0.8 and sb>0.8 and sum(x*y for x,y in zip(a,b))< -0.2*sa*sb:event="REVERSAL"
    elif sb<0.7 and sa>=0.7:event="STOP"
    elif sa<0.7 and sb>=0.7:event="START"
    elif sb>sa+0.8:event="SPEED_UP"
    elif sb<sa-0.8:event="SLOW_DOWN"
    else:event="STEADY"
    return {"event":event,"axis":dominant,"speed":round(sb,4),
            "velocity":[round(b[0],5),round(b[1],5)],
            "prior_velocity":[round(a[0],5),round(a[1],5)],
            "radius":round(obs[-1]["radius"],4)}
def propose(obs,memory,t,group):
    ctx=context(obs);last=obs[-1];vx,vy=ctx["velocity"];dt=t-last["t"]
    if dt<=0:raise ValueError("FUTURE_TIME_REQUIRED")
    local={"x":last["x"]+vx*dt,"y":last["y"]+vy*dt,"t":t,"radius":last["radius"]}
    # Match transition first, then allow cross-axis transfer in local
    # coordinate frame (parallel/perpendicular components).
    matches=[e for e in memory["episodes"] if e["context"]["event"]==ctx["event"] and e["source_group"]!=group]
    unique={e["source_group"] for e in matches}
    if len(unique)<2:
        return {"mode":"DOUBT","proposal":local,"source":"LOCAL_VELOCITY_ONLY",
                "hypotheses":[{"kind":"LOCAL_VELOCITY"}],"matched_groups":len(unique),"context":ctx}
    # Normalise correction vectors relative to last measured motion axis.
    corrections=[]
    for e in matches:
        old=e["context"]["velocity"];mag=math.hypot(*old)
        if mag<0.7:continue
        u=(old[0]/mag,old[1]/mag);v=(-u[1],u[0])
        ex,ey=e["residual_velocity"]
        corrections.append((ex*u[0]+ey*u[1],ex*v[0]+ey*v[1]))
    speed=math.hypot(vx,vy)
    if speed<0.7 or len(corrections)<2:
        return {"mode":"DOUBT","proposal":local,"source":"INSUFFICIENT_DIRECTION",
                "hypotheses":[{"kind":"LOCAL_VELOCITY"}],"matched_groups":len(unique),"context":ctx}
    parallel=sorted(x for x,y in corrections);perp=sorted(y for x,y in corrections)
    def median(x):return (x[(len(x)-1)//2]+x[len(x)//2])/2
    dp,dq=median(parallel),median(perp)
    u=(vx/speed,vy/speed);v=(-u[1],u[0])
    guided={"x":local["x"]+(dp*u[0]+dq*v[0])*dt,
            "y":local["y"]+(dp*u[1]+dq*v[1])*dt,"t":t,"radius":last["radius"]}
    return {"mode":"CANDIDATE","proposal":guided,"source":"TRANSFERRED_TRANSITION",
            "hypotheses":[{"kind":"TRANSFERRED_TRANSITION"},{"kind":"LOCAL_VELOCITY"}],
            "matched_groups":len(unique),"context":ctx}
def forecast(manifest,out,previous=None):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    spec=read(manifest);group=spec.get("source_group")
    if not isinstance(group,str) or not group:raise ValueError("SOURCE_GROUP_REQUIRED")
    obs=track(spec);t=float(spec["predict_t"])
    memory=load(previous);prediction=propose(obs,memory,t,group)
    body={"schema":"BRODY_TRANSITION_CONTEXT_FORECAST_V1","source_group":group,
      "observations":obs,"predict_t":t,"choice":prediction,
      "prior_memory_digest":digest(memory),"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    body["digest"]=digest(body)
    dest.mkdir(parents=True);write(dest/"sealed_forecast.json",body)
    render(prediction["proposal"],dest/"predicted.png")
    report={"source_group":group,"event":prediction["context"]["event"],
      "mode":prediction["mode"],"source":prediction["source"],
      "matched_groups":prediction["matched_groups"],"generated":"predicted.png",
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    write(dest/"MASTER_REPORT.json",report);return report
def correct(sealed_file,actual_file,out,previous=None):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    seal=read(sealed_file);expected=seal.pop("digest",None)
    if expected!=digest(seal) or seal.get("schema")!="BRODY_TRANSITION_CONTEXT_FORECAST_V1":raise ValueError("BAD_FORECAST")
    state=load(previous);actual=analyze(actual_file)
    if actual["source_sha256"] in {o["source_sha256"] for o in seal["observations"]}:raise ValueError("FEEDBACK_LEAK")
    choice=seal["choice"];base=seal["observations"][-1];dt=seal["predict_t"]-base["t"]
    observed_velocity=((actual["x"]-base["x"])/dt,(actual["y"]-base["y"])/dt)
    pre=choice["context"]["velocity"]
    episode={"forecast_digest":expected,"source_group":seal["source_group"],
       "context":choice["context"],"feedback_sha256":actual["source_sha256"],
       "residual_velocity":[observed_velocity[0]-pre[0],observed_velocity[1]-pre[1]],
       "prediction_error_px":round(math.hypot(choice["proposal"]["x"]-actual["x"],choice["proposal"]["y"]-actual["y"]),5)}
    earlier=next((e for e in state["episodes"] if e["forecast_digest"]==expected),None)
    if earlier is not None and earlier!=episode:raise ValueError("CONTRADICTORY_CORRECTION")
    if earlier is None:state["episodes"].append(episode)
    state["digest"]=digest(state);dest.mkdir(parents=True)
    write(dest/"candidate_transition_memory.json",state)
    result={"episodes":len(state["episodes"]),"event":choice["context"]["event"],
       "error_px":episode["prediction_error_px"],"native_memory_write":False,
       "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    write(dest/"MASTER_REPORT.json",result);return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--mode",choices=("forecast","correct"),required=True)
    p.add_argument("--manifest");p.add_argument("--forecast");p.add_argument("--observed")
    p.add_argument("--previous");p.add_argument("--out",required=True)
    a=p.parse_args()
    print(json.dumps(forecast(a.manifest,a.out,a.previous) if a.mode=="forecast" else correct(a.forecast,a.observed,a.out,a.previous),indent=2))
if __name__=="__main__":main()
