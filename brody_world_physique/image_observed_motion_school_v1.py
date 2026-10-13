"""Brody observed-motion school: measure, extrapolate, draw, correct.

Only 2D tracked blobs from frames. Time gaps are explicit and no physics law
is hard-coded or claimed. Local candidate memory; no canonical promotion.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
from .fusion_f9_intensive_education_v0 import digest,verify_chain

def analyze(path):
    im=ImageOps.exif_transpose(Image.open(path)).convert("RGB").resize((64,64))
    pixels=list(im.getdata())
    fg=[(i%64,i//64) for i,p in enumerate(pixels) if min(p)<170 and max(p)-min(p)<90]
    if len(fg)<4 or len(fg)>3000:raise ValueError("NO_SINGLE_SEGMENTABLE_OBJECT")
    x=sum(p[0] for p in fg)/len(fg);y=sum(p[1] for p in fg)/len(fg)
    radius=math.sqrt(len(fg)/math.pi)
    return {"x":round(x,4),"y":round(y,4),"radius":round(radius,4),
            "source_sha256":hashlib.sha256(Path(path).read_bytes()).hexdigest()}
def fit(observations):
    if len(observations)<3:raise ValueError("THREE_FRAMES_REQUIRED")
    times=[r["t"] for r in observations]
    if any(b<=a for a,b in zip(times,times[1:])):raise ValueError("NONMONOTONIC_TIME")
    # Constant-acceleration quadratic through three most recent positions,
    # estimated from observations, not fixed gravity acceleration.
    a,b,c=observations[-3:]
    def axis(k):
        s1=(b[k]-a[k])/(b["t"]-a["t"])
        s2=(c[k]-b[k])/(c["t"]-b["t"])
        acc=2*(s2-s1)/(c["t"]-a["t"])
        return s2,acc
    vx,ax=axis("x");vy,ay=axis("y")
    return {"last_t":c["t"],"x":c["x"],"y":c["y"],
            "radius":c["radius"],"vx_interval":vx,"vy_interval":vy,
            "ax":ax,"ay":ay,"previous_dt":c["t"]-b["t"]}
def anticipate(model,t):
    dt=t-model["last_t"]
    if dt<=0:raise ValueError("FUTURE_TIME_REQUIRED")
    # Interval slope corresponds to velocity at the previous interval midpoint.
    vx=model["vx_interval"]+model["ax"]*model["previous_dt"]/2
    vy=model["vy_interval"]+model["ay"]*model["previous_dt"]/2
    return {"t":t,"x":model["x"]+vx*dt+model["ax"]*dt*dt/2,
            "y":model["y"]+vy*dt+model["ay"]*dt*dt/2,
            "radius":model["radius"]}
def render(pred,path):
    im=Image.new("RGB",(64,64),"white")
    d=ImageDraw.Draw(im)
    x,y,r=pred["x"],pred["y"],pred["radius"]
    d.ellipse((round(x-r),round(y-r),round(x+r),round(y+r)),fill=(50,50,50))
    im.save(path)
def load_manifest(path):
    payload=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    rows=payload["observations"]
    if not isinstance(rows,list) or len(rows)<3:raise ValueError("THREE_FRAMES_REQUIRED")
    if any("teacher_identity" in row for row in rows):raise ValueError("NO_LABELS_DURING_OBSERVATION")
    return payload
def run(manifest,out,feedback=None):
    target=Path(out)
    if target.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    spec=load_manifest(manifest)
    observations=[]
    for item in spec["observations"]:
        o=analyze(item["file"]);o["t"]=float(item["t"]);observations.append(o)
    model=fit(observations)
    next_time=float(spec["predict_t"])
    prediction=anticipate(model,next_time)
    target.mkdir(parents=True)
    render(prediction,target/"predicted_next.png")
    body={"schema":"BRODY_OBSERVED_2D_MOTION_SCHOOL_V1",
          "observations":observations,"fitted_model":model,
          "prediction":prediction,"next_image_generated_from_model":True,
          "model_is_fitted_not_gravity_hardcoded":True,"native_memory_write":False,
          "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    body["digest"]=digest(body)
    (target/"candidate_motion_memory.json").write_text(json.dumps(body,indent=2)+"\n")
    report={"schema":"BRODY_MOTION_PREDICTION_REPORT_V1",
        "frames":len(observations),"predicted_t":next_time,
        "predicted_x":prediction["x"],"predicted_y":prediction["y"],
        "generated_image":"predicted_next.png",
        "correction_applied":False,"native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY",
        "status":"MEASURED_2D_TRAJECTORY_CANDIDATE"}
    if feedback:
        truth=analyze(feedback)
        if truth["source_sha256"] in {o["source_sha256"] for o in observations}:
            raise ValueError("FEEDBACK_IMAGE_LEAK")
        ex=prediction["x"]-truth["x"];ey=prediction["y"]-truth["y"]
        report["feedback"]={"actual":truth,"error_px":round(math.hypot(ex,ey),4),
           "corrected_trajectory_estimate":"PENDING_NEW_FIT"}
        report["correction_applied"]=False
    (target/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    p.add_argument("--feedback")
    a=p.parse_args();print(json.dumps(run(a.manifest,a.out,a.feedback),indent=2))
if __name__=="__main__":main()
