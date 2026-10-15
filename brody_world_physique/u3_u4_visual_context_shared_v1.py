"""U3/U4: pixels select context; shared candidate controls trajectory and raster.

An intervention effect is learned once through observed frames, then stored as
one context-scoped candidate. The very same value drives both predicted X
and rendered image. No exam condition label reaches the model.
"""
from __future__ import annotations
import argparse,json,random
from pathlib import Path
from PIL import Image,ImageDraw
from .image_active_context_probe_p158 import trajectory
from .image_context_coexistence_p157 import observed
from .image_education_retention_gate_p155 import choose
from .experiential_skill_learning_v1 import save,seal

def forecast(xs,acc):
    return xs[-1]+(xs[-1]-xs[-2])+acc

def visual(xs):
    # Context is estimated from the last 4 observed pixel centroids.
    if any(v is None for v in xs[-4:]):return None
    a=[xs[i+2]-2*xs[i+1]+xs[i] for i in (-4,-3)]
    return sum(a)/len(a)

def raster(x):
    im=Image.new("RGB",(120,76),(246,246,242))
    ImageDraw.Draw(im).ellipse((round(x)-3,35,round(x)+3,41),fill=(224,37,47))
    return im

def exam(root,state,name,kind,seed):
    ims=trajectory(kind,"discriminating",random.Random(seed))
    try:
        xs=observed(ims)
        hist=xs[:6]
        a=visual(hist)
        context=("intervention" if a is not None and abs(a-state["intervention_acceleration"])<.26
                 else ("clean" if a is not None and abs(a)<.26 else None))
        # Context inferred from pixels, never from 'kind'.
        corrected=forecast(hist,state["intervention_acceleration"] if context=="intervention" else 0.) if context else None
        baseline=forecast(hist,0.)
        pre=seal({"case":name,"observed_history":hist,"selected_context":context,
             "baseline_x":baseline,"candidate_x":corrected,
             "memory_digest":seal(state)["digest"],"native_memory_write":False,
             "canonical_promotion":False,"decision_authority":"KX108_ONLY"})
        save(root/(name+"_PRECOMMIT.json"),pre)
        # Targets only accessible to scorer after precommit.
        truth=xs[6]
        if corrected is not None:
            out=root/(name+"_predicted.png");raster(corrected).save(out)
            err=abs(corrected-truth)
        else:err=None
        return {"name":name,"inferred_context":context,
             "baseline_error":abs(baseline-truth),"candidate_error":err,
             "target_x":truth,"candidate_image_generated":corrected is not None}
    finally:
        for im in ims:im.close()

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    imgs=trajectory("slope","discriminating",random.Random(100))
    try:
        xs=observed(imgs)
    finally:
        for im in imgs:im.close()
    accel=visual(xs[:6])
    if accel is None:raise ValueError("PROBE_UNOBSERVABLE")
    state={"schema":"BRODY_U3_U4_SHARED_CANDIDATE_V1",
           "clean_acceleration":0.,"intervention_acceleration":accel,
           "source":"PIXEL_PROBE_P158","authority":"KX108_ONLY"}
    save(root/"MEMORY_CANDIDATE.json",seal(state))
    # P155 guard: reject global correction that hurts clean retention.
    decision=choose(accel,[(i,i+accel) for i in (10.,20.,30.)],
                    [(i,i) for i in (11.,21.,31.)],.03)
    rows=[exam(root,state,"slope_new","slope",404),
          exam(root,state,"clean_new","flat",505),
          exam(root,state,"unknown_new","spring",606)]
    report={"schema":"BRODY_U3_U4_PIXELS_TO_SHARED_RENDERER_V1",
       "probe_acceleration":accel,"global_correction_accepted":decision[0],
       "global_rejection_reason":decision[1],"exams":rows,
       "pixel_context_routing":True,"same_candidate_for_forecast_and_raster":True,
       "no_exam_label_used_by_model":True,
       "semantic_object_identity_proven":False,"multi_view_proven":False,
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY",
       "verdict":"U3_U4_CONTEXTUAL_SINGLE_PARAMETER_VISUAL_LOOP"}
    save(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"exams":r["exams"]},indent=2))
if __name__=="__main__":main()
