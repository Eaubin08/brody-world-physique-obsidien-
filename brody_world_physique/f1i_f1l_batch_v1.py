"""F1I–F1L combined educational integration campaign.

F1I: image-visible camera/occlusion indicators from historical P150/P152.
F1J: perception -> coarse synthesis -> perception, with invariant error.
F1K: versioned experimental skill history and retention across interference.
F1L: optional independent image directory; no claim of real-world competence.

All grading is experimental, no canonical memory or decision authority.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random
from pathlib import Path
from PIL import Image, ImageDraw
from . import image_tracking_beam_p150 as p150
from . import image_identity_beam_p152 as p152
from . import image_multiangle_temporal_p149 as p149
from .image_identity_appearance_p151 import episode as p151_episode
from .image_real_transfer_exam_v2 import features, images, fingerprint
from .image_reciprocal_generation_school_v1 import decode
from .experiential_skill_learning_v1 import save, seal
from .fusion_f9_intensive_education_v0 import digest

def f1i(root):
    rng=random.Random(819)
    records=[]
    for scene in ("separate","camera_pan","occlude_both","overlap"):
        frames,truth,camera=p150.build(rng,scene)
        try:
            # Image detector alone supplies landmarks; never use truth/camera in inference.
            observations=[p150.observe(im) for im in frames[:8]]
            track=p150.infer(frames[:8])
            pre=seal({"case":scene,"history_sha":[hashlib.sha256(im.tobytes()).hexdigest() for im in frames[:8]],
                "detected_marks":[len(marks) for _,marks in observations],
                "observed_camera":track["camera_observed"],"prediction":track["prediction"],
                "reason":track["reason"],"native_memory_write":False,
                "canonical_promotion":False,"decision_authority":"KX108_ONLY"})
            save(root/("f1i_"+scene+".json"),pre)
            records.append({"case":scene,"camera_observed":track["camera_observed"],
                "detected_markers":pre["detected_marks"],"reason":track["reason"],
                "error_px":round(abs(track["prediction"]-truth[8][0]),5) if track["prediction"] is not None else None,
                "world_causal_contact_proven":False})
        finally:
            for im in frames:im.close()
    return {"cases":records,"true_contact_observability_implemented":False,
            "image_observability_from_historical_p150":True}

def f1j(root):
    items=[]
    # P149 historical renderer; no learned generator represented here.
    for idx,(a,b) in enumerate(((22,70),(30,64),(42,57))):
        source=p149.render(a,b,idx,"cross_distinct")
        path=root/("f1j_source_"+str(idx)+".png")
        source.save(path);source.close()
        before=features(path)
        recreated=root/("f1j_generated_"+str(idx)+".png")
        decode(before["colour_grid"],recreated)
        after=features(recreated)
        distance=sum(abs(a-b) for a,b in zip(before["colour_grid"],after["colour_grid"]))
        items.append({"source_sha256":fingerprint(path),
            "generated_sha256":fingerprint(recreated),
            "coarse_grid_L1":distance,
            "source_parts":before["parts"],"reconstructed_parts":after["parts"],
            "source_copied":False})
    return {"roundtrips":items,"reverse_observation_executed":True,
            "same_pixel_resolution":False,"semantic_generation":False,
            "geometric_reverse_360":False,"feedback_updates_visual_model":False}

def f1k(root):
    # A persisted, sealed ledger of method candidates and their dependencies.
    # Actual cross-skill reinforcement is not implied by this declarative ledger.
    versions=[]
    for stage,candidate,preconditions in (
        ("acquisition","P150_CAMERA_LANDMARK","at least one image-visible anchored landmark"),
        ("interference","P152_IDENTITY_BEAM","at least two target observations"),
        ("retention","P150_CAMERA_LANDMARK","at least one image-visible anchored landmark")):
        doc=seal({"schema":"BRODY_F1K_SKILL_LEDGER_V1","stage":stage,
            "candidate_skill":candidate,"precondition":preconditions,
            "depends_on":["pixel_observation","time_order"],
            "prior_digest":versions[-1]["digest"] if versions else None,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"})
        path=root/("f1k_"+stage+".json");save(path,doc)
        versions.append({"stage":stage,"candidate_skill":candidate,"digest":doc["digest"]})
    return {"versions":versions,"original_candidate_recurs_after_interference":True,
            "actual_accuracy_retention_proven":False,
            "no_second_canonical_memory":True}

def f1l(root,external_images):
    if external_images is None:
        return {"status":"HOLD_NO_INDEPENDENT_IMAGES","images_evaluated":0,
                "real_world_transfer_proven":False}
    source=Path(external_images)
    items=images(source)
    if not items:raise ValueError("EMPTY_EXTERNAL_IMAGE_SET")
    readouts=[]
    for path in items:
        feat=features(path)
        readouts.append({"source_sha256":fingerprint(path),
            "parts_candidate":feat["parts"],"dark_pixels":feat["dark_pixels"],
            "colour_grid_bins":len(feat["colour_grid"]),
            "teacher_label_used":False})
    return {"status":"UNLABELED_VISUAL_OBSERVATION_ONLY","images_evaluated":len(readouts),
        "observations":readouts,"real_world_transfer_proven":False,
        "image_provenance_independently_verified":False}

def run(out,external_images=None):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    dest.mkdir(parents=True)
    results={"F1I":f1i(dest),"F1J":f1j(dest),"F1K":f1k(dest),"F1L":f1l(dest,external_images)}
    summary={"schema":"BRODY_F1I_TO_F1L_BATCH_V1","stages":results,
        "stage_count":4,"historical_p150_reused":True,
        "historical_p149_reused":True,
        "historical_p152_imported":True,
        "full_integrated_education_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"BATCH_BOUNDARY_AND_EDUCATION_PRIMITIVES_ONLY"}
    save(dest/"MASTER_REPORT.json",summary)
    return summary
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--external-images")
    a=p.parse_args();r=run(a.out,a.external_images)
    print(json.dumps({"verdict":r["verdict"],"stages":list(r["stages"]),
        "external_status":r["stages"]["F1L"]["status"]},indent=2))
if __name__=="__main__":main()
