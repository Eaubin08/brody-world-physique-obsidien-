"""P165-D11 Gate C: independent counterfactual raster scenes, tracker unchanged.

New renderer independent of D2 draw(). Truth is scoring-only and never reaches
the tracker. Tests are diagnostic, NOT a demonstration of real-world physics.
"""
import argparse,json,math,random
from pathlib import Path
from PIL import Image,ImageDraw
from .reappearance_gate_p165d6 import infer,evaluate_tracks

KINDS=("abrupt_jump","rapid_accel","abrupt_brake","reverse",
       "camera_pan","target_swap","indistinguishable_crossing",
       "late_occlusion","long_occlusion","deceptive_distractor")
SEEDS=12
def render(kind,seed):
    if kind not in KINDS:raise ValueError("UNKNOWN_CASE")
    rng=random.Random(seed);ims=[];truth=[]
    x0=28+rng.randint(-4,4);vx=4+rng.randint(-1,2)
    for t in range(7):
        x=x0+vx*t
        if kind=="abrupt_jump" and t>=4:x+=rng.choice((-27,27))
        if kind=="rapid_accel":x+=int(1.3*t*t)
        if kind=="abrupt_brake" and t>=3:x=x0+vx*3
        if kind=="reverse" and t>=3:x=x0+vx*3-vx*(t-3)
        if kind=="camera_pan":x+=8*t
        if kind=="target_swap" and t>=4:x+=13
        if kind=="indistinguishable_crossing":x=x0+6*t
        if kind=="deceptive_distractor" and t>=4:x+=19
        truth.append(float(x))
        im=Image.new("RGB",(168,96),(220,225,220))
        d=ImageDraw.Draw(im)
        d.rectangle((0,70,167,95),fill=(175,184,180))
        d.ellipse((x-5,43,x+5,53),fill=(220,40,50))
        if kind in ("target_swap","indistinguishable_crossing","deceptive_distractor"):
            dx=108-6*t if kind=="indistinguishable_crossing" else x0+48-3*t
            d.ellipse((dx-5,43,dx+5,53),fill=(220,40,50))
        if kind=="long_occlusion" and 2<=t<=5:
            d.rectangle((x-9,36,x+9,60),fill=(120,120,120))
        if kind=="late_occlusion" and 4<=t<=5:
            d.rectangle((x-9,36,x+9,60),fill=(120,120,120))
        ims.append(im)
    return ims,truth

def run(out,beam=8,seeds=SEEDS):
    if not(2<=beam<=32 and 1<=seeds<=100):raise ValueError("INVALID_BOUNDS")
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    families={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for kind in KINDS:
            row={"episodes":0,"four_frame":0,"same_path_pre_post":0,
                 "pre_visible":0,"post_return":0,"HOLD":0,"MULTI":0,"CANDIDATE":0}
            for seed in range(seeds):
                frames,truth=render(kind,71001+seed*37)
                try:outcome=infer(frames,beam=beam)
                finally:
                    for im in frames:im.close()
                score=evaluate_tracks(outcome["raw"]["tracks"],truth)
                row["episodes"]+=1
                for field,target in (("four_frame","topk_four_frame_recall"),
                                      ("same_path_pre_post","same_path_pre_post_recall"),
                                      ("pre_visible","pre_visible_recall"),
                                      ("post_return","post_reappearance_recall")):
                    row[field]+=int(score[target])
                row[outcome["verdict"]["status"]]+=1
                f.write(json.dumps({"case_eval_only":kind,"seed":seed,
                    "scores_eval_only":score,"verdict":outcome["verdict"],
                    "tracks":outcome["raw"]["tracks"],"truth_eval_only":truth})+"\n")
            families[kind]=row
    report={"schema":"BRODY_P165D11_INDEPENDENT_GATE_C",
        "families":families,"episodes":len(KINDS)*seeds,
        "renderer_uses_d2_generator":False,
        "fixture_truth_in_inference":False,
        "tracker_unchanged":True,
        "real_image_or_sensor":False,
        "true_identity_proven":False,
        "pass_fail_interpretation":"DIAGNOSTIC_ONLY_NOT_AUTO_GREEN",
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    a=argparse.ArgumentParser();a.add_argument("--out",required=True)
    a.add_argument("--beam",type=int,default=8);a.add_argument("--seeds",type=int,default=12)
    x=a.parse_args();print(json.dumps(run(x.out,x.beam,x.seeds),indent=2))
if __name__=="__main__":main()
