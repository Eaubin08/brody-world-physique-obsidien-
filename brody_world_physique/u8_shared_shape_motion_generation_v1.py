"""U8 integrated experimental memory: shape + contextual acceleration + generated raster.

A single evidence-backed candidate stores the taught shape mask and measured
motion response; neither exam target nor hidden regime label enters prediction.
Synthetic controlled laboratory, not semantic identity or Reverse360.
"""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
from PIL import Image,ImageDraw
from .image_reciprocal_shape_learning_p134 import scene,paint,compare
from .image_active_context_probe_p158 import trajectory
from .image_context_coexistence_p157 import observed
from .experiential_skill_learning_v1 import seal,save

def teaching_shape(path):
    im=Image.new("RGB",(64,64),"white")
    ImageDraw.Draw(im).ellipse((19,27,25,33),fill=(224,37,47))
    im.save(path)

def motion_features(xs):
    if len(xs)<4 or any(x is None for x in xs[-4:]):return None
    return sum(xs[i+2]-2*xs[i+1]+xs[i] for i in (-4,-3))/2

def predict(xs,acc):
    return xs[-1]+xs[-1]-xs[-2]+acc

def draw_candidate(part,x,out):
    w,h=part["size"];xc=round(x*64/120)
    top=part["bbox"][1]
    left=xc-w//2
    if left<0 or left+w>64:raise ValueError("BOUNDS")
    obj={**part,"bbox":[left,top,left+w-1,top+h-1]}
    paint([obj],out)

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    source=root/"shape_lesson.png";teaching_shape(source)
    part=scene(source)["components"][0]
    lesson=trajectory("slope","discriminating",random.Random(100))
    try:xs=observed(lesson)
    finally:
        for im in lesson:im.close()
    acc=motion_features(xs[:6])
    if acc is None:raise ValueError("NO_LEARNED_MOTION")
    memory={"schema":"BRODY_U8_SHARED_SHAPE_MOTION_CANDIDATE","shape":part,
        "motion":{"clean":0.,"intervention":acc},"source":"PIXEL_SHAPE_AND_PIXEL_MOTION",
        "readonly":True,"native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"}
    save(root/"SHARED_MEMORY.json",seal(memory))
    records=[]
    for name,regime,seed in (("learned","slope",404),("retained","flat",505),("unknown","spring",606)):
        frames=trajectory(regime,"discriminating",random.Random(seed))
        try:
            positions=observed(frames);history=positions[:6];measured=motion_features(history)
            if measured is not None and abs(measured-acc)<.25:context="intervention"
            elif measured is not None and abs(measured)<.25:context="clean"
            else:context=None
            next_x=predict(history,memory["motion"][context]) if context else None
            pre=seal({"case":name,"history":history,"inferred_context":context,
                "prediction_x":next_x,"memory_digest":seal(memory)["digest"],
                "native_memory_write":False,"canonical_promotion":False,
                "decision_authority":"KX108_ONLY"})
            save(root/(name+"_PRECOMMIT.json"),pre)
            output=root/(name+"_future.png")
            if next_x is not None:
                draw_candidate(memory["shape"],next_x,output)
            # Reveal after irrevocable precommit. The target is reconstructed
            # from a generic object prototype and measured heldout location;
            # not a second label handed to the predictor.
            actual=positions[6]
            truth=root/(name+"_truth.png")
            draw_candidate(memory["shape"],actual,truth)
            err=compare(output,truth)["mae_rgb"] if next_x is not None else None
            records.append({"case":name,"context":context,"predicted_x":next_x,
                "actual_x_eval_only":actual,"visual_mae":err,
                "candidate_created":next_x is not None})
        finally:
            for im in frames:im.close()
    report={"schema":"BRODY_U8_SHARED_CANDIDATE_VISUAL_PHYSICS_V1",
        "cases":records,"one_state_holds_visual_and_physical_skills":True,
        "future_renderer_reads_stored_shape_and_motion":True,
        "teacher_shape_is_synthetic":True,"exam_truth_absent_until_precommit":True,
        "same_object_identity_across_camera_views_proven":False,
        "new_semantic_object_discovery_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"U8_SHARED_SHAPE_MOTION_RENDERING_SYNTHETIC"}
    save(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"cases":r["cases"]},indent=2))
if __name__=="__main__":main()
