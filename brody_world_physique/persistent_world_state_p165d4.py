"""P165-D4 persistent world state lab: observation vs prediction, goal dependent views.

Synthetic calibrated scalar positions, NOT an integrated perception/world model.
"""
import argparse,json,math
from pathlib import Path

GOALS=("AVOID_COLLISION","REIDENTIFY","RENDER","EXPLAIN")
def initial(entity="ball"):
    return {"entity":entity,"time":0.0,"position":None,"velocity":None,
            "position_uncertainty":None,"mode":"UNINITIALIZED",
            "observations":[],"hypotheses":[],"contradictions":[]}
def update(state,record):
    """Immutable world update. Input is an *observation record*, no oracle."""
    s=json.loads(json.dumps(state))
    source=record.get("source")
    if source not in ("OBSERVED","SIMULATED_SENSOR"):
        return {**s,"mode":"HOLD_SOURCE","contradictions":s["contradictions"]+["NON_SENSOR_EVIDENCE"]}
    if not isinstance(record.get("time"),(int,float)) or not math.isfinite(record["time"]):
        raise ValueError("INVALID_TIME")
    t=float(record["time"])
    if t<s["time"]:return {**s,"mode":"HOLD_TIME","contradictions":s["contradictions"]+["BACKWARDS_TIME"]}
    if record.get("frame")!="world_1d":return {**s,"mode":"HOLD_FRAME","contradictions":s["contradictions"]+["UNALIGNED_FRAME"]}
    if record.get("quality",1.)<.5:return {**s,"mode":"HOLD_QUALITY"}
    x=record.get("position")
    if x is None:return propagate(s,t)
    if not isinstance(x,(int,float)) or not math.isfinite(x):raise ValueError("INVALID_POSITION")
    x=float(x);old=s["position"];prev=s["time"]
    if old is not None and t>prev:
        vx=(x-old)/(t-prev)
        if s["velocity"] is not None and abs(x-(old+s["velocity"]*(t-prev)))>max(3.,3.*(s["position_uncertainty"] or 0.)):
            s["contradictions"].append("POSITION_PREDICTION_MISMATCH")
        s["velocity"]=vx
    s["position"]=x;s["time"]=t;s["position_uncertainty"]=.5
    s["mode"]="OBSERVED";s["observations"].append({"time":t,"position":x,"source":source})
    return s
def propagate(state,to_time,process_noise=1.):
    s=json.loads(json.dumps(state));t=float(to_time)
    if not math.isfinite(t) or t<s["time"]:raise ValueError("INVALID_FORWARD_TIME")
    dt=t-s["time"];s["time"]=t
    if s["position"] is None or s["velocity"] is None:
        s["mode"]="HOLD_NO_DYNAMIC_MODEL";return s
    s["position"]=s["position"]+s["velocity"]*dt
    s["position_uncertainty"]=(s["position_uncertainty"] or 0.)+process_noise*dt+0.1*dt*dt
    s["mode"]="PREDICTED"
    s["hypotheses"].append({"time":t,"position":s["position"],
                             "uncertainty":s["position_uncertainty"],
                             "type":"CONSTANT_VELOCITY_ASSUMPTION"})
    return s
def view(state,goal):
    if goal not in GOALS:raise ValueError("UNKNOWN_GOAL")
    fields={"AVOID_COLLISION":("position","velocity","position_uncertainty","mode"),
            "REIDENTIFY":("entity","observations","hypotheses","contradictions","mode"),
            "RENDER":("position","position_uncertainty","mode","hypotheses"),
            "EXPLAIN":("observations","hypotheses","contradictions","mode")}[goal]
    return {"goal":goal,"state":{f:state[f] for f in fields},
            "identity_proven":False,"physical_truth_proven":False}
def scenario(kind):
    s=initial()
    s=update(s,{"time":0,"position":10,"frame":"world_1d","source":"SIMULATED_SENSOR"})
    s=update(s,{"time":1,"position":14,"frame":"world_1d","source":"SIMULATED_SENSOR"})
    if kind=="occlusion":
        s=propagate(s,3)
    elif kind=="consistent_reappearance":
        s=propagate(s,3);s=update(s,{"time":4,"position":26,"frame":"world_1d","source":"SIMULATED_SENSOR"})
    elif kind=="unexpected_reappearance":
        s=propagate(s,3);s=update(s,{"time":4,"position":49,"frame":"world_1d","source":"SIMULATED_SENSOR"})
    elif kind=="generated_not_evidence":
        s=update(s,{"time":2,"position":100,"frame":"world_1d","source":"GENERATED"})
    elif kind=="wrong_reference_frame":
        s=update(s,{"time":2,"position":19,"frame":"camera","source":"SIMULATED_SENSOR"})
    elif kind=="no_new_measurement":
        s=propagate(s,12)
    else:raise ValueError("UNKNOWN_CASE")
    return s
CASES=("occlusion","consistent_reappearance","unexpected_reappearance",
       "generated_not_evidence","wrong_reference_frame","no_new_measurement")
def run(out):
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    result={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for case in CASES:
            s=scenario(case);result[case]={"mode":s["mode"],"uncertainty":s["position_uncertainty"],
                                "contradictions":s["contradictions"]}
            f.write(json.dumps({"case":case,"state":s,"views":{g:view(s,g) for g in GOALS}})+"\n")
    report={"schema":"BRODY_P165D4_PERSISTENT_WORLD_STATE_LAB",
       "cases":result,"cases_completed":len(result),"goal_views":list(GOALS),
       "world_geometry":"SYNTHETIC_1D_KINEMATICS",
       "real_multisensor_fusion_connected":False,
       "pixels_to_world_graph_connected":False,"metric_3d_connected":False,
       "autonomous_learning_connected":False,"true_identity_proven":False,
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.out),indent=2))
if __name__=="__main__":main()
