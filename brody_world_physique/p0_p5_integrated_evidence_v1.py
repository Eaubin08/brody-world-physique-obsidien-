"""Brody P0-P5 integrated evidence campaign. Experimental, non-canonical.

Uses P134 structural masks, P155 retention decision, P150 visual uncertainty
and P158 active-probe policy. All feedback is time-separated from predictions.
"""
from __future__ import annotations
import argparse, json, math, hashlib, random
from pathlib import Path
from PIL import Image,ImageDraw
from .image_reciprocal_shape_learning_p134 import scene,paint,compare,learn,memory_fresh
from .image_reciprocal_generation_school_v1 import decode
from .image_real_transfer_exam_v2 import features,images,fingerprint
from .image_tracking_beam_p150 import build,infer,observe
from .image_education_retention_gate_p155 import choose
from .image_active_context_probe_p158 import decide
from .experiential_skill_learning_v1 import save,seal,sha
from .fusion_f9_intensive_education_v0 import digest

def make_scene(path,cx,shape="square"):
    im=Image.new("RGB",(64,64),"white");d=ImageDraw.Draw(im)
    d.rectangle((cx,10,cx+8,18),fill=(25,45,75))
    if shape=="square":d.rectangle((cx+15,34,cx+25,44),fill=(140,45,35))
    elif shape=="circle":d.ellipse((cx+15,34,cx+25,44),fill=(140,45,35))
    else:raise ValueError("BAD_SHAPE")
    im.save(path)

def structural_reciprocity(root):
    tr=root/"training.png";exam=root/"unseen.png"
    make_scene(tr,5);make_scene(exam,15)
    learned=scene(tr)
    target=scene(exam)
    # P1: structural mask generation with observed bounding boxes; compare to
    # historical RGB coarse generator. Exam geometry is a perceptual input,
    # never a future answer about dynamics.
    colour=features(exam)["colour_grid"]
    coarse=root/"coarse.png";decode(colour,coarse)
    structural=root/"structure_before_feedback.png"
    proposal=[]
    for source,observed in zip(learned["components"],target["components"]):
        candidate={**source,"bbox":observed["bbox"],"size":observed["size"]}
        proposal.append(candidate)
    paint(proposal,structural)
    before=compare(structural,exam)
    pre=seal({"source_sha":sha(tr),"exam_input_sha":sha(exam),
        "coarse_sha":sha(coarse),"structural_prediction_sha":sha(structural),
        "training_prototypes":len(learned["components"]),
        "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"})
    save(root/"P1_PRE_FEEDBACK.json",pre)
    # P2: only after a committed reconstruction, use exam observation to
    # correct the *candidate* structural prototype. This is self-reconstruction,
    # not heldout prediction of a future physical event.
    corrected=root/"structure_after_feedback.png"
    paint(target["components"],corrected)
    after=compare(corrected,exam)
    if pre["structural_prediction_sha"]!=sha(structural):raise ValueError("PREDICTION_TAMPER")
    return {"P1":{"coarse_parts":len(scene(coarse)["components"]),
        "structural_parts":len(scene(structural)["components"]),
        "source_parts":target["count"],"structural_mae_before":before["mae_rgb"],
        "coarse_grid_not_structure":True,
        "real_object_identity_proven":False},
        "P2":{"before_feedback_mae":before["mae_rgb"],
        "after_feedback_mae":after["mae_rgb"],
        "candidate_updated_after_commit":True,
        "feedback_uses_exam_image":True,"retraining_generalization_proven":False}}

def retention(root):
    # P155 real pre-existing decision gate: validation improvement must not
    # compromise separate clean retention.
    feedback=[(10.,12.),(20.,22.),(30.,32.)]
    clean=[(10.,10.),(20.,20.),(30.,30.)]
    proposed=2.
    accepted,reason=choose(proposed,feedback,clean,tolerance=.03)
    if accepted:raise ValueError("CLEAN_RETENTION_GATE_BYPASSED")
    baseline_check,baseline_reason=choose(0.,feedback,clean,tolerance=.03)
    # Persist a hashed chain of actual candidate decisions, not only names.
    ledger=[]
    for name,action in (("acquire","propose_plus_two"),("interfere","validate_clean_world"),("retain","reject_regressive_candidate")):
        doc=seal({"phase":name,"action":action,"previous_digest":ledger[-1]["digest"] if ledger else None,
            "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"})
        save(root/("P3_"+name+".json"),doc);ledger.append(doc)
    return {"historical_p155_choose_reused":True,"candidate_rejected":not accepted,
        "retention_reason":reason,"no_gain_rejected":not baseline_check,
        "no_gain_reason":baseline_reason,"ledger_entries":len(ledger),
        "actual_multitask_memory_training_proven":False}

def uncertainty(root):
    rng=random.Random(404)
    rows=[]
    for typ in ("separate","camera_pan","occlude_both","overlap"):
        frames,truth,camera=build(rng,typ)
        try:
            # Predefined sensor availability rule, independent of hidden future.
            history=frames[:8]
            observed_counts=[len(observe(im)[0]) for im in history]
            raw=infer(history)
            recent_visibility=min(observed_counts[-3:])>=2
            status="HOLD_VISIBILITY" if not recent_visibility else ("HOLD_MODEL" if raw["prediction"] is None else "CANDIDATE")
            commit=seal({"scene":typ,"visibility_counts":observed_counts,
                "status":status,"prediction":raw["prediction"],"reason":raw["reason"],
                "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"})
            save(root/("P4_"+typ+".json"),commit)
            err=abs(raw["prediction"]-truth[8][0]) if raw["prediction"] is not None else None
            rows.append({"scene":typ,"status":status,"raw_error":err,
                "camera_observed":raw["camera_observed"]})
        finally:
            for f in frames:f.close()
    return {"cases":rows,"coverage":sum(x["status"]=="CANDIDATE" for x in rows)/len(rows),
        "sensor_gate_uses_only_past_frames":True,
        "calibrated_risk_proven":False}

def world_and_external(root,external_images):
    # P158 confirms that a model can PROBE while two futures are observationally
    # indistinguishable; it does not prove a SENS/MMonde integration.
    bank={"flat":0.,"slope":-1.}
    pre=decide([],bank,"single",probe_available=True)
    no_probe=decide([],bank,"single",probe_available=False)
    if pre["decision"]!="PROBE" or no_probe["decision"]!="HOLD":
        raise ValueError("PROBE_CONTRACT_BROKEN")
    ext=[]
    if external_images is not None:
        for p in images(external_images):
            ext.append({"sha256":fingerprint(p),"feature_parts":features(p)["parts"]})
    return {"historical_p158_probe_reused":True,"pre_probe":pre,
        "without_probe":no_probe,"external_images_seen":len(ext),
        "external_receipts":ext,
        "external_exam_status":"UNLABELED_ONLY" if ext else "HOLD_NO_INDEPENDENT_IMAGES",
        "sens_mmonde_connected":False,"reverse_360_complete":False,
        "real_world_transfer_proven":False}

def run(out,external_images=None):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    p1p2=structural_reciprocity(root)
    report={"schema":"BRODY_P0_P5_INTEGRATED_EVIDENCE_V1",
        "P0":{"status":"SMOKE_GATES_IN_BATCH","full_regression_executed":False,
              "runner":"py -m unittest discover -s tests -v"},
        **p1p2,"P3":retention(root),"P4":uncertainty(root),
        "P5":world_and_external(root,external_images),
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "full_educational_continuity_proven":False,
        "verdict":"P0_P5_BOUNDED_INTEGRATION_NOT_CANONICAL"}
    save(root/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--external-images")
    a=p.parse_args();r=run(a.out,a.external_images)
    print(json.dumps({"verdict":r["verdict"],"P1":r["P1"],"P2":r["P2"],
        "P3":r["P3"],"P4_coverage":r["P4"]["coverage"],
        "P5_status":r["P5"]["external_exam_status"]},indent=2))
if __name__=="__main__":main()
