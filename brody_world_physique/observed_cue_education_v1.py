"""F1F observed-cue learning: use a visible marker, not future answers.

Small synthetic laboratory, not a real collision physics model. Reuses the
existing forecast, scene drawing, visual analysis and hashed candidate memory.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw
from .f1b_physical_memory_bridge_v1 import episode
from .image_experience_guided_motion_v2 import forecast
from .image_observed_motion_school_v1 import analyze
from .image_multihypothesis_motion_memory_v1 import read
from .experiential_skill_learning_v1 import save, seal, sha

# A blue marker is visible at t=3, before the t=4 target. It stands for an
# observed environmental cue in a controlled world, not a physics law.
BLUE=(0,80,220)
def observe_marker(path):
    im=Image.open(path).convert("RGB")
    return any(im.getpixel((x,54))==BLUE for x in range(8,56,4))
def build(root,name,positions,marker,x):
    manifest,truth=episode(root,name,positions,x=x)
    spec=read(manifest)
    if marker:
        last=Path(spec["observations"][-1]["file"])
        with Image.open(last) as image:
            im=image.copy().convert("RGB")
        ImageDraw.Draw(im).line((6,54,57,54),fill=BLUE,width=1)
        im.save(last)
    return manifest,truth
def start(root,name,ys,marker,x):
    manifest,truth=build(root,name,ys,marker,x)
    frame=Path(read(manifest)["observations"][-1]["file"])
    cue=observe_marker(frame)
    folder=root/("forecast_"+name)
    forecast(manifest,folder)
    frozen=read(folder/"sealed_forecast.json")
    pred=frozen["hypotheses"]["ACCELERATION"]
    return folder,manifest,truth,cue,pred

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    # Identical observed trajectories for paired worlds; only the visible cue
    # and withheld continuation differ. Train separate correction distributions.
    train=(("train_free_1",(10,14,20,28,39),False,22),
           ("train_cue_1",(10,14,20,28,24),True,26),
           ("train_free_2",(12,16,22,30,41),False,30),
           ("train_cue_2",(12,16,22,30,26),True,34))
    test=(("new_free",(16,20,26,34,45),False,40),
          ("new_cue",(16,20,26,34,30),True,44),
          ("cue_false_alarm",(18,22,28,36,47),True,47),
          ("invisible_reversal",(18,22,28,36,32),False,50))
    learned={False:[],True:[]};train_hashes=set();lessons=[]
    for name,ys,marker,x in train:
        folder,manifest,truth,cue,pred=start(root,name,ys,marker,x)
        if cue!=marker:raise ValueError("CUE_OBSERVATION_FAILED")
        before=sha(folder/"sealed_forecast.json")
        measured=analyze(truth)
        residual=measured["y"]-pred["y"]
        if before!=sha(folder/"sealed_forecast.json"):raise ValueError("FORECAST_MUTATION")
        learned[cue].append(residual)
        train_hashes.update(sha(row["file"]) for row in read(manifest)["observations"])
        train_hashes.add(sha(truth))
        lessons.append({"case":name,"observed_marker":cue,"residual_y_px":residual})
    memory=seal({"schema":"BRODY_OBSERVABLE_CUE_SKILL_V1",
        "training":lessons,"mean_residual_by_marker":{
            "visible":sum(learned[True])/len(learned[True]),
            "absent":sum(learned[False])/len(learned[False])},
        "precondition":"cue measured from an observed frame before forecast",
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"})
    save(root/"candidate_cue_skill.json",memory)
    exams=[]
    for name,ys,marker,x in test:
        folder,manifest,truth,cue,pred=start(root,name,ys,marker,x)
        if sha(truth) in train_hashes or any(sha(row["file"]) in train_hashes for row in read(manifest)["observations"]):
            raise ValueError("TRAIN_TEST_LEAK")
        dy=memory["mean_residual_by_marker"]["visible" if cue else "absent"]
        candidate={**pred,"y":pred["y"]+dy}
        frozen=sha(folder/"sealed_forecast.json")
        save(folder/"candidate_pre_feedback.json",seal({
            "candidate":candidate,"cue_from_past_frame":cue,"memory_digest":memory["digest"],
            "frozen_forecast_sha256":frozen,"native_memory_write":False,
            "canonical_promotion":False,"decision_authority":"KX108_ONLY"}))
        actual=analyze(truth)
        base_err=round(math.hypot(actual["x"]-pred["x"],actual["y"]-pred["y"]),5)
        adapted_err=round(math.hypot(actual["x"]-candidate["x"],actual["y"]-candidate["y"]),5)
        if frozen!=sha(folder/"sealed_forecast.json"):raise ValueError("FORECAST_MUTATION")
        exams.append({"case":name,"visible_cue":cue,"base_error_px":base_err,
            "with_cue_skill_error_px":adapted_err,"utility_px":round(base_err-adapted_err,5),
            "candidate_committed_before_truth":True})
    report={"schema":"BRODY_F1F_OBSERVABLE_CUE_EDUCATION_V1",
        "lessons":lessons,"exam":exams,"improved":sum(e["utility_px"]>0 for e in exams),
        "degraded":sum(e["utility_px"]<0 for e in exams),
        "unchanged":sum(e["utility_px"]==0 for e in exams),
        "marker_observed_before_future":True,
        "indistinguishable_without_cue":True,
        "cue_is_controlled_synthetic_proxy":True,
        "learned_conditional_residual_not_causal_law":True,
        "p149_p150_p152_verified_reuse":False,
        "real_world_learning_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"F1F_BOUNDED_OBSERVED_CUE_LEARNING"}
    save(root/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args()
    r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"improved":r["improved"],
                      "degraded":r["degraded"],"unchanged":r["unchanged"]},indent=2))
if __name__=="__main__":main()
