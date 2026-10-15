"""F1H: real historical P149/P150/P152 read-only API reuse in one audit.

No synthetic replacement of these historical algorithms. Report grades only
the explicit experiment outputs; no learner weights or canonical memory change.
"""
from __future__ import annotations
import argparse, hashlib, json, random
from pathlib import Path
from . import image_multiangle_temporal_p149 as p149
from . import image_tracking_beam_p150 as p150
from . import image_identity_beam_p152 as p152
from .image_identity_appearance_p151 import episode as episode151
from .experiential_skill_learning_v1 import save, seal

def sha_image(image):
    return hashlib.sha256(image.tobytes()).hexdigest()

def run(out,seed=418):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    rng=random.Random(seed)
    cf=p149.paired_counterfactual()
    if not(cf["same_final_pixels"] and cf["different_histories"]):
        raise ValueError("COUNTERFACTUAL_CONTRACT_FAILED")
    rows=[]
    # P149 actual detector+estimator, with known lane limitation.
    for kind in ("cross_identical","same_frame_opposite_history","camera_offset","occlude_one"):
        frames,result=p149.experiment(rng,kind)
        try:
            rows.append({"module":"P149","case":kind,"reason":result["reason"],
                "prediction":result["prediction"],"error":result["mae"],
                "history_observations":len(result["history"]),
                "source_sha256":sha_image(frames[0])})
        finally:
            for im in frames:im.close()
    # P150: infer observes images and scene landmarks, never latent IDs or truth.
    for kind in ("separate","overlap","camera_pan","occlude_both"):
        frames,truth,cam=p150.build(rng,kind)
        try:
            result=p150.infer(frames[:8])
            prediction=result["prediction"]
            rows.append({"module":"P150","case":kind,"reason":result["reason"],
                "prediction":prediction,"error":abs(prediction-truth[8][0]) if prediction is not None else None,
                "camera_observed":result["camera_observed"],
                "source_sha256":sha_image(frames[0])})
        finally:
            for im in frames:im.close()
    # P152: persistent beam is run on the same frames as P151 (no ID oracle).
    from .image_identity_appearance_p151 import CASES
    for kind in list(CASES)[:4]:
        frames,truth=episode151(rng,kind)
        try:
            prediction,reason,diagnostics=p152.beam_predict(frames[:9])
            target=truth[9]["A"]
            import math
            rows.append({"module":"P152","case":kind,"reason":reason,
                "prediction":prediction,"error":round(math.dist(prediction,target),5) if prediction is not None else None,
                "diagnostics":diagnostics,"source_sha256":sha_image(frames[0])})
        finally:
            for im in frames:im.close()
    report={"schema":"BRODY_F1H_HISTORICAL_MODULE_REUSE_V1",
        "modules":{
            "P149":"brody_world_physique.image_multiangle_temporal_p149",
            "P150":"brody_world_physique.image_tracking_beam_p150",
            "P152":"brody_world_physique.image_identity_beam_p152"},
        "direct_imports_verified_at_runtime":True,
        "counterfactual":cf,
        "exams":rows,"cases":len(rows),
        "answers":sum(row["prediction"] is not None for row in rows),
        "holds":sum(row["prediction"] is None for row in rows),
        "physical_law_discovery_proven":False,
        "single_shared_skill_state":False,
        "world_model_sens_connected":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"F1H_REUSE_HISTORICAL_APIS_BOUNDARY_TEST"}
    save(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args()
    r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"cases":r["cases"],
        "answers":r["answers"],"holds":r["holds"]},indent=2))
if __name__=="__main__":main()
