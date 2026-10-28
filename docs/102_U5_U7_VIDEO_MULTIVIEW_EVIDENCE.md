# 102 - U5/U7 video provenance + two-dimensional identity and camera invariants

Existing modules reused: P165D12 world-camera-identity separation with 6 case families, video_observation_v0 source hashing and optional user-driven four-frame annotation, image_unified_multiview_knowledge_v1 optional teacher-manifest view graph.

Without a local user-supplied video U5 returns HOLD_NO_INDEPENDENT_VIDEO. If video is supplied, it is byte-hashed, not decoded, examined, or sensor-authenticated: FILE_HASHED_NOT_VISUALLY_EXAMINED. Do not infer success on real-video transfer from this report.

U7 executes the unmodified P165-D12 image-sequence tracker and collects six case families: object motion, camera motion, compensated motion, occlusion, identity swap, crossing. True world coordinates and hidden object identity are only used for grading. Existing teacher-labeled graph, if selected, describes 2D transformed images; it does not prove novel semantic identity, camera 360 or 3D reconstruction.

## One Windows PowerShell pass
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_u5_u7_video_multiview_evidence_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.u5_u7_video_multiview_evidence_v1 --out "build/u5-u7-multiview-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/u5-u7-multiview-v1/MASTER_REPORT.json"
```

Optional: `--video "path/to/local.mp4"` and `--identity-manifest "path/to/teacher.json"`, always with a NEW --out path. No auto-actions in external services.

## Remaining roadmap
U5B: visual evaluation of local video via manually annotated frames using existing video_observation_v0; only then can image-plane prediction be graded.
U6: real cross-repository SENS/MMonde contracts and read-only boundary audit.
U7B: independent multi-camera views, unobserved viewpoint exam, identity after occlusion; Reverse360 claim remains HOLD.
U8: same persistent candidate memory for structural shape, temporal forecast, image-generation correction and replay.
Gates: KX108_ONLY, native_memory_write false, canonical_promotion false.
