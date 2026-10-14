"""P165-D12: world/camera/identity/projection separated in synthetic evaluation.

The renderer is a measurement generator. Latent world variables and identities
must never be given to the D6 inference path. All 3D and sensor claims forbidden.
"""
import argparse,json,math,random
from pathlib import Path
from PIL import Image,ImageDraw
from .reappearance_gate_p165d6 import infer,evaluate_tracks

CASES=("OBJECT_MOVES","CAMERA_MOVES","COMPENSATED_MOTION",
       "OCCLUSION","IDENTITY_SWAP","CROSSING")
def world(case,seed):
    if case not in CASES:raise ValueError("UNKNOWN_CASE")
    rng=random.Random(seed)
    x=34+rng.randint(-2,2); other=114+rng.randint(-2,2)
    steps=[]
    for t in range(7):
        camera=(5*t if case=="CAMERA_MOVES" else (4*t if case=="COMPENSATED_MOTION" else 0))
        obj=(x+(5*t if case in ("OBJECT_MOVES","COMPENSATED_MOTION") else 0))
        identity="A"
        if case=="IDENTITY_SWAP" and t>=4:
            obj=other-5*t
            identity="B"
        if case=="CROSSING":
            obj=x+9*t
            other_world=other-9*t
        else:other_world=other
        hidden=(case=="OCCLUSION" and 3<=t<=4)
        steps.append({"t":t,"world_x_a":obj if identity=="A" else x,
                      "world_x_b":other_world,"camera_x":camera,
                      "rendered_main_identity":identity,"main_x":obj,
                      "main_visible":not hidden})
    return steps
def raster(scene,case):
    frames=[];projected=[]
    for state in scene:
        cam=state["camera_x"]
        x=state["main_x"]-cam
        projected.append(float(x))
        im=Image.new("RGB",(168,96),(233,228,216))
        draw=ImageDraw.Draw(im)
        # Independent static world landmarks allow camera motion to be observable.
        for landmark in (12,80,149):
            lx=landmark-cam
            draw.rectangle((lx-2,10,lx+2,17),fill=(70,80,90))
        if case in ("IDENTITY_SWAP","CROSSING"):
            ox=state["world_x_b"]-cam
            draw.ellipse((ox-5,43,ox+5,53),fill=(220,40,50))
        if state["main_visible"]:
            draw.ellipse((x-5,43,x+5,53),fill=(220,40,50))
        else:
            draw.rectangle((x-8,36,x+8,60),fill=(120,120,120))
        frames.append(im)
    return frames,projected
def episode(case,seed):
    scene=world(case,seed)
    frames,pixels=raster(scene,case)
    return frames,{"case_eval_only":case,"world_eval_only":scene,
                   "projection_eval_only":pixels,
                   "primary_is_single_persistent_identity":case!="IDENTITY_SWAP"}
def run(out,seeds=12,beam=8):
    if not(1<=seeds<=100 and 2<=beam<=32):raise ValueError("INVALID_BOUNDS")
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    families={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for case in CASES:
            row={"n":0,"pre":0,"post":0,"same_path":0,"identity_proven":0,
                 "CANDIDATE":0,"MULTI":0,"HOLD":0}
            for k in range(seeds):
                frames,oracle=episode(case,80017+k*101)
                try:r=infer(frames,beam=beam)
                finally:
                    for im in frames:im.close()
                m=evaluate_tracks(r["raw"]["tracks"],oracle["projection_eval_only"])
                row["n"]+=1
                row["pre"]+=int(m["pre_visible_recall"])
                row["post"]+=int(m["post_reappearance_recall"])
                row["same_path"]+=int(m["same_path_pre_post_recall"])
                row["identity_proven"]+=int(r["unique_identity_proven"])
                row[r["verdict"]["status"]]+=1
                f.write(json.dumps({"case_eval_only":case,"seed":k,
                      "oracle_eval_only":oracle,"scores_eval_only":m,
                      "verdict":r["verdict"],"tracks":r["raw"]["tracks"]})+"\n")
            families[case]=row
    report={"schema":"BRODY_P165D12_WORLD_CAMERA_IDENTITY_SEPARATION",
      "families":families,"episodes":len(CASES)*seeds,
      "true_world_coordinates_used_only_for_evaluation":True,
      "camera_landmarks_are_visible_pixels":True,
      "camera_parameters_to_infer":False,
      "identity_to_infer":False,
      "identity_swap_claim_of_continuity_is_invalid":True,
      "genuine_3d_or_physical_world_proven":False,
      "tracker_unchanged":True,
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True)
    ap.add_argument("--seeds",type=int,default=12);ap.add_argument("--beam",type=int,default=8)
    a=ap.parse_args();print(json.dumps(run(a.out,a.seeds,a.beam),indent=2))
if __name__=="__main__":main()
