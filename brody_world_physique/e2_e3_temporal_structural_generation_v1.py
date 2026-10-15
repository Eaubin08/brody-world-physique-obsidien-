"""E2+E3: historical time inference -> generated future mask -> held-out image.

P149 observations and estimator only see first 6 frames. P134 mask comes from
the first training frame, not from target image. All targets are post-commit.
Synthetic, single colored object, known pixel plane; not 3D/reverse360.
"""
from __future__ import annotations
import argparse, hashlib, json, random
from pathlib import Path
from PIL import Image,ImageDraw
from .image_multiangle_temporal_p149 import observed,estimator,paired_counterfactual
from .image_reciprocal_shape_learning_p134 import scene,paint,compare
from .experiential_skill_learning_v1 import save,seal,sha

def render(x):
    im=Image.new("RGB",(96,64),"white")
    ImageDraw.Draw(im).ellipse((round(x)-3,23,round(x)+3,29),fill=(210,40,50))
    return im
def view64(im):
    return im.resize((64,64),Image.Resampling.NEAREST)
def predict_mask(template,x):
    obj=template["components"][0]
    # 96-wide camera pixel -> 64-wide projection; x provided ONLY by P149 forecast.
    w,h=obj["size"];left=round(x*64/96)-w//2;top=obj["bbox"][1]
    if left<0 or left+w>64:raise ValueError("OUT_OF_IMAGE")
    return [{**obj,"bbox":[left,top,left+w-1,top+h-1]}]
def experiment(root,name,positions):
    root.mkdir(parents=True,exist_ok=True)
    frames=[render(x) for x in positions]
    try:
        # Source memory trained only on first frame; no target input.
        memory_source=root/"training_first.png";view64(frames[0]).save(memory_source)
        template=scene(memory_source)
        history=[observed(im) for im in frames[:6]]
        x_pred,reason=estimator(history)
        last=history[-1]["26"]
        sealed=seal({"case":name,"history_pixel_sha256":[hashlib.sha256(im.tobytes()).hexdigest() for im in frames[:6]],
            "source_mask_sha":sha(memory_source),"P149_reason":reason,
            "x_prediction":x_pred,"x_last":last,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"})
        save(root/"PRECOMMIT.json",sealed)
        generated=None;baseline=None
        if x_pred is not None:
            generated=root/"generated_future.png"
            paint(predict_mask(template,x_pred),generated)
            baseline=root/"static_baseline.png"
            paint(predict_mask(template,last),baseline)
        # Target is materialized and opened only AFTER candidate is sealed.
        target=root/"heldout_future.png";view64(frames[6]).save(target)
        if generated:
            score=compare(generated,target);baseline_score=compare(baseline,target)
            source=scene(generated)
            return {"case":name,"status":"CANDIDATE","reason":reason,
                "candidate_mae":score["mae_rgb"],"static_mae":baseline_score["mae_rgb"],
                "reconstructed_parts":source["count"],"target_parts":scene(target)["count"],
                "generated_sha":sha(generated),"target_sha":sha(target)}
        return {"case":name,"status":"HOLD","reason":reason,
                "candidate_mae":None,"static_mae":None}
    finally:
        for im in frames:im.close()
def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    # Cases explicitly include a future reversal not identifiable from preceding
    # constant-velocity frames: this must remain a visible negative result.
    cases={
        "regular_A":(12,16,20,24,28,32,36),
        "regular_B":(20,23,26,29,32,35,38),
        "hidden_reversal":(12,16,20,24,28,32,28)}
    results=[experiment(root/name,name,values) for name,values in cases.items()]
    cf=paired_counterfactual()
    report={"schema":"BRODY_E2_E3_TEMPORAL_STRUCTURAL_GENERATION_V1",
        "exam":results,"counterfactual":cf,
        "P149_observation_and_estimator_reused":True,
        "P134_mask_and_renderer_reused":True,
        "target_geometry_passed_to_generator":False,
        "target_pixels_passed_to_generator":False,
        "generator_has_first_frame_object_mask":True,
        "heldout_future_scored_after_precommit":True,
        "camera_and_identity_beam_fused":False,
        "physical_understanding_proven":False,
        "reverse_360_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"E2_E3_SYNTHETIC_TEMPORAL_MASK_GENERATION"}
    save(root/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"exam":r["exam"]},indent=2))
if __name__=="__main__":main()
