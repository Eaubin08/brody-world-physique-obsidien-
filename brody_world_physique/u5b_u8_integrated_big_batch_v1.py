"""Large batch U5B/U6/U7B/U8: one executable laboratory and evidence chain.

Distinct remote repos are not silently cloned. Local video remains untouched.
2D affine views are NOT reverse 360 or independent physical cameras.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
from .u8_shared_shape_motion_generation_v1 import run as u8
from .world_camera_identity_p165d12 import run as world_camera
from .image_multiview_identity_school_v0 import run as view_school
from .video_observation_v0 import video_sha256
from . import contracts_v0
from .experiential_skill_learning_v1 import save,seal

def prepare_multiview(root):
    # Generate a deliberately asymmetric object to expose 2D transform drift.
    im=Image.new("RGB",(64,64),"white")
    d=ImageDraw.Draw(im)
    d.rectangle((14,30,42,43),fill=(20,55,80))
    d.polygon([(14,30),(24,12),(33,30)],fill=(20,55,80))
    source=root/"asymmetric_object.png";im.save(source);im.close()
    manifest=root/"teacher_identity_manifest.json"
    save(manifest,[{"identity":"teacher-object-A","examples":[str(source)]}])
    return manifest

def run(out,video=None,seeds=3):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    # Eager pipeline relies on each module's own immutable outputs.
    learning=u8(root/"U8_SHARED_MEMORY")
    teacher_manifest=prepare_multiview(root)
    views=view_school(teacher_manifest,root/"U7B_2D_VIEWS")
    camera=world_camera(root/"U7B_CAMERA_OCCLUSION",seeds=seeds)
    if video is None:
        media={"status":"HOLD_NO_INDEPENDENT_VIDEO",
               "video_frames_examined":0}
    else:
        p=Path(video)
        if not p.is_file() or not p.stat().st_size:raise ValueError("BAD_EXTERNAL_VIDEO")
        media={"status":"FILE_HASHED_ANNOTATION_REQUIRED",
            "sha256":video_sha256(p),"filename":p.name,"bytes":p.stat().st_size,
            "video_frames_examined":0,
            "next_step":"video_observation_v0.annotate_video",
            "actual_video_prediction_proven":False}
    upstream=("WorldTransformationV0","WorldStateDeltaV0","WorldExperienceCandidateV0")
    local={k:hasattr(contracts_v0,k) for k in upstream}
    boundary={"status":"LOCAL_CONTRACTS_ONLY_NO_UPSTREAM_SOURCE_AUDIT",
        "local_contracts":local,"upstream_sens_verified":False,
        "upstream_mmonde_verified":False,
        "upstream_git_shas_collected":False,"decision_authority":"KX108_ONLY"}
    report={"schema":"BRODY_INTEGRATED_U5B_U6_U7B_U8_BUNDLE_V1",
        "U5B":media,"U6":boundary,
        "U7B":{"status":"SYNTHETIC_2D_TEACHER_VIEWS_AND_CAMERA_TRACKING",
            "heldout_views":views["heldout_views"],
            "heldout_context_matches":views["heldout_context_matches"],
            "heldout_context_misses":views["heldout_context_misses"],
            "camera_episodes":camera["episodes"],
            "families":camera["families"],
            "unseen_physical_camera_view_proven":False,
            "reverse_360_proven":False,
            "semantic_identity_proven":False},
        "U8":{"status":"SHARED_SHAPE_MOTION_GENERATOR",
            "cases":learning["cases"],
            "single_candidate_state":learning["one_state_holds_visual_and_physical_skills"],
            "full_cross_modal_education_proven":False},
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"U5B_U8_INTEGRATED_SYNTHETIC_PASS_OR_GATED"}
    save(root/"MASTER_REPORT.json",report)
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);p.add_argument("--video")
    p.add_argument("--seeds",type=int,default=3)
    a=p.parse_args();r=run(a.out,a.video,a.seeds)
    print(json.dumps({"verdict":r["verdict"],"U5B":r["U5B"]["status"],
        "U6":r["U6"]["status"],"U7B":r["U7B"]["status"],
        "U8":r["U8"]["cases"]},indent=2))
if __name__=="__main__":main()
