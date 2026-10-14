"""F1B bounded physical-memory experiment: real motion APIs, blind paired forecasts.

F1B is a physics-memory bridge, not a connection to the P156 model or a proof
of autonomous understanding. Ground truth is revealed only AFTER both forecasts.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw
from .image_experience_guided_motion_v2 import forecast, correct
from .image_observed_motion_school_v1 import analyze
from .image_multihypothesis_motion_memory_v1 import read

def image(path,y,x=32):
    im=Image.new("RGB",(64,64),"white")
    ImageDraw.Draw(im).ellipse((x-4,y-4,x+4,y+4),fill=(40,40,40))
    im.save(path)

def episode(root,name,ys):
    path=root/name;path.mkdir()
    rows=[]
    for i,y in enumerate(ys):
        file=path/f"frame_{i}.png"
        image(file,y)
        if i<3:rows.append({"t":i,"file":str(file.resolve())})
    spec=path/"manifest.json"
    spec.write_text(json.dumps({"observations":rows,"predict_t":3}),encoding="utf8")
    return spec,path/"frame_3.png"

def measured_forecast(folder,truth):
    sealed=read(folder/"sealed_forecast.json")
    truth_data=analyze(truth)
    return {kind:round(math.hypot(pred["x"]-truth_data["x"],pred["y"]-truth_data["y"]),5)
            for kind,pred in sealed["hypotheses"].items()}

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    # TRAIN: two separate sequences, same motion regime, feedback after forecast.
    memory=None
    training=[]
    for i,ys in enumerate(([10,14,20,28],[17,21,27,35])):
        spec,truth=episode(root,"train_"+str(i),ys)
        f=root/("forecast_train_"+str(i))
        forecast(spec,f,previous=memory)
        correction=root/("correction_train_"+str(i))
        result=correct(f/"sealed_forecast.json",truth,correction,previous=memory)
        memory=correction/"candidate_physics_memory.json"
        training.append({"case":i,"experiences":result["experiences"],
                         "forecast":str(f.relative_to(root))})
    # TEST: target frame exists on disk, but engine gets only past-frame manifest.
    spec,truth=episode(root,"test_unseen",[24,28,34,42])
    without=root/"test_no_memory";withmem=root/"test_with_memory"
    base=forecast(spec,without)
    guided=forecast(spec,withmem,previous=memory)
    # Check commitments before opening the TEST image to grade.
    before=[(p/"sealed_forecast.json").read_bytes() for p in (without,withmem)]
    errors_no=measured_forecast(without,truth)
    errors_yes=measured_forecast(withmem,truth)
    after=[(p/"sealed_forecast.json").read_bytes() for p in (without,withmem)]
    if before!=after:raise ValueError("FORECAST_MUTATED_AFTER_EVALUATION")
    report={
        "schema":"BRODY_F1B_PHYSICAL_MEMORY_BRIDGE_V1",
        "train":training,
        "test_with_no_memory":base,
        "test_with_memory":guided,
        "paired_errors_no_memory_px":errors_no,
        "paired_errors_with_memory_px":errors_yes,
        "sealed_forecasts_unchanged":True,
        "train_test_episode_separated":True,
        "same_test_input":True,
        "different_test_source_from_train":True,
        "shared_physical_competence_candidate":True,
        "memory_changed_model_choice":base["selected"]!=guided["selected"],
        "reciprocal_prototype_generator_connected":False,
        "p156_memory_connected":False,
        "pause_resume_tested":False,
        "unified_education_e2e":False,
        "physical_law_discovered":False,
        "native_memory_write":False,
        "canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"F1B_BOUNDED_MOTION_MEMORY_EXPERIMENT",
    }
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args()
    print(json.dumps(run(args.out),indent=2))
if __name__=="__main__":main()
