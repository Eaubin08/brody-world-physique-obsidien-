"""P165-B sensor evidence fusion: modal signatures with strict source and time gates.
Synthetic laboratory evidence only. NOT real radar, thermal, LiDAR or physics.
"""
import argparse,json,math,random,time
from pathlib import Path

MODES=("RGB","SPECTRAL","THERMAL","RADAR","LIDAR","ACOUSTIC","FLOW","GEOMETRY")
def obs(mode,values,source="SIMULATED",time_id=0,frame="scene",quality=1.):
    if mode not in MODES:raise ValueError("UNKNOWN_MODE")
    if source not in ("OBSERVED","SIMULATED","GENERATED","INFERRED"):raise ValueError("UNKNOWN_SOURCE")
    return dict(mode=mode,values=tuple(float(x) for x in values),
                source=source,time_id=time_id,frame=frame,quality=float(quality))
def distance(a,b):
    if len(a)!=len(b):return math.inf
    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
def compare(a,b):
    if a["mode"]!=b["mode"]:return {"status":"INCOMPARABLE_MODE"}
    if a["frame"]!=b["frame"] or a["time_id"]!=b["time_id"]:
        return {"status":"HOLD","reason":"UNALIGNED_FRAME_OR_TIME"}
    if a["source"] in ("GENERATED","INFERRED") or b["source"] in ("GENERATED","INFERRED"):
        return {"status":"HOLD","reason":"NONINDEPENDENT_EVIDENCE"}
    if not a["values"] or not b["values"] or min(a["quality"],b["quality"])<.5:
        return {"status":"HOLD","reason":"LOW_QUALITY"}
    return {"status":"COMPARED","distance":distance(a["values"],b["values"])}
def identity(left,right):
    # A modality votes only if actual independent comparable evidence exists.
    votes=[];conflicts=[];unusable=[]
    for mode in MODES:
        ls=[x for x in left if x["mode"]==mode]
        rs=[x for x in right if x["mode"]==mode]
        if not ls or not rs:continue
        p=compare(ls[0],rs[0])
        if p["status"]!="COMPARED":unusable.append((mode,p));continue
        # Normalized fixture signatures are designed within [0,1].
        if p["distance"]<=.12:votes.append(mode)
        elif p["distance"]>=.5:conflicts.append(mode)
        else:unusable.append((mode,p))
    if conflicts and votes:status="MULTI"
    elif conflicts:status="CONTRADICTED"
    elif len(votes)>=2:status="SUPPORTED_CANDIDATE"
    else:status="HOLD"
    return {"status":status,"votes":votes,"conflicts":conflicts,"unusable":unusable,
            "identity_proven":False}

def scene(case):
    # Simulator yields modality fingerprints. A reader must not mistake these
    # arrays for sensors physically measured by the device.
    A=[obs("RGB",[.9,.1,.1]),obs("GEOMETRY",[.45,.45]),
       obs("THERMAL",[.8,.8]),obs("RADAR",[.2,.7]),obs("SPECTRAL",[.3,.6]),
       obs("LIDAR",[.5,.6]),obs("ACOUSTIC",[.3,.8]),obs("FLOW",[.2,.1])]
    B=[obs(x["mode"],x["values"]) for x in A]
    if case=="color_changed":
        B[0]=obs("RGB",[.1,.2,.95])
    elif case=="thermal_contradiction":
        B[2]=obs("THERMAL",[.1,.1])
    elif case=="radar_hidden":
        B[0]=obs("RGB",[],quality=0)
    elif case=="multi_conflict":
        B[0]=obs("RGB",[.1,.9,.9]);B[2]=obs("THERMAL",[.1,.1])
    elif case=="generated_forgery":
        B=[obs(x["mode"],x["values"],source="GENERATED") for x in B]
    elif case=="time_mismatch":
        B=[obs(x["mode"],x["values"],time_id=6) for x in B]
    elif case=="same_signature_distinct_entities":
        pass
    elif case=="camera_frame_mismatch":
        B=[obs(x["mode"],x["values"],frame="camera") for x in B]
    elif case=="no_sensor_available":
        B=[]
    else:raise ValueError("UNKNOWN_CASE")
    return A,B
CASES=("color_changed","thermal_contradiction","radar_hidden","multi_conflict",
       "generated_forgery","time_mismatch","same_signature_distinct_entities",
       "camera_frame_mismatch","no_sensor_available")
def run(path):
    p=Path(path)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True);results={};unsafe=0
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for c in CASES:
            a,b=scene(c);result=identity(a,b)
            # A distinctive fingerprint is NOT proof of identity: two
            # physically different objects may share identical signatures.
            false_proof=bool(result["identity_proven"])
            unsafe+=int(false_proof)
            results[c]={"decision":result["status"],"votes":len(result["votes"]),
                        "conflicts":len(result["conflicts"]),"false_identity_proof":false_proof}
            log.write(json.dumps({"case":c,"a":a,"b":b,"result":result})+"\n")
    report={"schema":"BRODY_P165B_MODAL_SIGNATURE_CONTRACT_LAB",
       "cases":results,"cases_completed":len(results),
       "false_identity_proofs":unsafe,"modalities":list(MODES),
       "evidence_is_synthetic_fixture":True,"real_sensor_connected":False,
       "image_to_modalities_model_trained":False,
       "world_scene_graph_connected":False,
       "legacy_77_and_p165a_150_not_replayed":True,
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    a=argparse.ArgumentParser();a.add_argument("--out",required=True)
    x=a.parse_args();print(json.dumps(run(x.out),indent=2))
if __name__=="__main__":main()
