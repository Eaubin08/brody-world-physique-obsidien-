"""U5/U7: real-file video provenance plus historical multiview identity exam.

No claim that 2D rotations are 360-degree camera views. Real videos are
hashed and frame timing can be checked, but no automated identity claim.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .world_camera_identity_p165d12 import run as run_multiview
from .video_observation_v0 import video_sha256,choose_frame_indices
from .image_unified_multiview_knowledge_v1 import build as teacher_views
from .experiential_skill_learning_v1 import save,seal

def video_evidence(source):
    if source is None:return {"status":"HOLD_NO_INDEPENDENT_VIDEO","video_frames_examined":0}
    path=Path(source)
    if not path.is_file() or path.stat().st_size==0:raise ValueError("INVALID_INDEPENDENT_VIDEO")
    # Byte-level provenance only. Do not decode or label on the user's behalf.
    return {"status":"FILE_HASHED_NOT_VISUALLY_EXAMINED","name":path.name,
        "sha256":video_sha256(path),"bytes":path.stat().st_size,
        "video_frames_examined":0,"sensor_authenticity_proven":False,
        "automatic_object_tracking_proven":False,
        "manual_four_frame_annotation_available":True}

def run(out,video=None,identity_manifest=None,seeds=3):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    videos=video_evidence(video)
    camera=run_multiview(root/"P165D12_WORLD_CAMERA_IDENTITY",seeds=seeds)
    if identity_manifest is None:
        taught={"status":"HOLD_NO_TEACHER_IDENTITY_MANIFEST",
                "semantic_identity_verified":False}
    else:
        taught=teacher_views(identity_manifest,root/"TEACHER_2D_VIEWS")
        taught={"status":taught["status"],"identities":taught["identities"],
                "observations":taught["observations"],"semantic_identity_verified":False}
    f=camera["families"]
    result={"schema":"BRODY_U5_U7_PROVENANCE_AND_2D_MULTIVIEW_V1",
        "U5":videos,"U7":{"status":"HISTORICAL_P165D12_TRACKING_EXAM",
           "episodes":camera["episodes"],"case_results":f,
           "teacher_view_graph":taught,
           "camera_parameters_provided_to_tracker":False,
           "identity_labels_provided_to_tracker":False,
           "full_reverse_360_proven":False,
           "real_3d_proven":False},
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"U5_U7_2D_SYNTHETIC_MULTIVIEW_EVIDENCE_BOUND"}
    save(root/"MASTER_REPORT.json",result)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);p.add_argument("--video")
    p.add_argument("--identity-manifest");p.add_argument("--seeds",type=int,default=3)
    a=p.parse_args()
    r=run(a.out,a.video,a.identity_manifest,a.seeds)
    print(json.dumps({"verdict":r["verdict"],"U5":r["U5"]["status"],
         "U7_episodes":r["U7"]["episodes"],"U7_manifest":r["U7"]["teacher_view_graph"]["status"]},indent=2))
if __name__=="__main__":main()
