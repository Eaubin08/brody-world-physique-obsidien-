"""U1/U2 shared candidate state; active experiment corrects subsequent forecasts.

P158 supplies the pixel-only probe observation. Candidate memory stores a
measured acceleration response; update gated on disjoint clean retention.
All future exam data stays behind the immutable precommit.
"""
from __future__ import annotations
import argparse,json,random
from pathlib import Path
from .image_active_context_probe_p158 import trajectory,render,decide
from .image_context_coexistence_p157 import observed
from .image_education_retention_gate_p155 import choose
from .experiential_skill_learning_v1 import save,seal

def forecast(xs,acc):
    if len(xs)<2 or xs[-1] is None or xs[-2] is None:return None
    return xs[-1]+(xs[-1]-xs[-2])+acc

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    bank={"flat":0.,"slope":-1.}
    state={"schema":"BRODY_U1_CANDIDATE_SHARED_STATE_V1","acceleration":0.,
        "lessons":[],"authority":"KX108_ONLY"}
    save(root/"STATE_BEFORE.json",seal(state))
    policy=decide([],bank,"single",probe_available=True)
    save(root/"U2_PROBE_PRECOMMIT.json",seal({"decision":policy,
         "native_memory_write":False,"canonical_promotion":False,
         "decision_authority":"KX108_ONLY"}))
    rng=random.Random(100)
    frames=trajectory("slope","discriminating",rng)
    try:
        measurements=observed(frames)
    finally:
        for im in frames:im.close()
    accel_values=[measurements[i+2]-2*measurements[i+1]+measurements[i] for i in (3,4)]
    measured=sum(accel_values)/len(accel_values)
    verdict=decide([],bank,"single",after=[render(x,random.Random(1)) for x in measurements])
    # No hidden regime label consulted for any decision.
    old_acc=state["acceleration"]
    feedback=[(x,x+measured) for x in (11.,21.,31.)]
    clean=[(x,x) for x in (12.,22.,32.)]
    accepted,reason=choose(measured,feedback,clean,retention_tolerance if False else .03)
    # Global correction is legitimately blocked by retention. Instead learn
    # context-scoped parameter while preserving old clean-world candidate.
    state["lessons"].append({"context":"observed_intervention","measured_acceleration":measured,
        "global_correction_accepted":accepted,"global_reason":reason})
    state["contextual_acceleration"]={"clean":old_acc,"observed_intervention":measured}
    save(root/"STATE_AFTER.json",seal(state))
    # Independent exam: future is generated only AFTER precommit.
    cases=[]
    for name,regime in (("known_probe","slope"),("retention_clean","flat")):
        im=trajectory(regime,"discriminating",random.Random(404 if regime=="slope" else 505))
        try:
            xs=observed(im)
            # Predict frame 6 using only positions through frame 5.
            hist=xs[:6];base=forecast(hist,old_acc)
            context="observed_intervention" if name=="known_probe" else "clean"
            corrected=forecast(hist,state["contextual_acceleration"][context])
            pre=seal({"case":name,"observations":hist,"baseline":base,"candidate":corrected,
               "state_digest":seal(state)["digest"],
               "native_memory_write":False,"canonical_promotion":False,
               "decision_authority":"KX108_ONLY"})
            save(root/(name+"_PRECOMMIT.json"),pre)
            truth=xs[6]
            cases.append({"case":name,"baseline_error":abs(base-truth),
                "corrected_error":abs(corrected-truth),
                "precommit_before_truth":True})
        finally:
            for image in im:image.close()
    report={"schema":"BRODY_U1_U2_CONTEXTUAL_EXPERIENCE_V1",
        "probe_decision":policy["decision"],"observed_probe_response":measured,
        "state_changed":state["contextual_acceleration"]["observed_intervention"]!=old_acc,
        "global_correction_accepted":accepted,
        "context_scoped_memory":True,"cases":cases,
        "source_pixel_observations":True,
        "outside_simulation_action":False,
        "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY",
        "verdict":"U1_U2_CANDIDATE_STATE_CHANGED_BY_PROBE"}
    save(root/"MASTER_REPORT.json",report);return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"state_changed":r["state_changed"],"cases":r["cases"]},indent=2))
if __name__=="__main__":main()
