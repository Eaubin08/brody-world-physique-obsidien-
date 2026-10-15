# 48 — P2.6 large-scale adversarial pixel stress test

## Motivation from author
P2.5 with five designed scenes is too forgiving. Test a substantially wider set of configurations to locate failures, not just green metrics. The central hypothesis is that apparent "noise" can be a precision-relevant contextual observation provided it is situated in its correct spatial/temporal/reference hierarchy.

## Implementation
`brody_world_physique/p26_adversarial_pixels_v0.py`: default **480 synthetic image pairs** (960 source frames generated in memory), deterministic per-case seeds. Four groups of perturbations: camera/object translations, deliberately corrupted background landmarks (0–4), lighting shifts, landmark jitters, ball occlusion, and independent nuisance pixels. The 25%-DEV / 75%-TEST split is a report split only: there is **no learned model**, no parameter tuning and no external generator; results are NOT a scientific holdout demonstration.

The detector is an engineered OpenCV color extractor. The baseline observes only object motion in the image. The contextual comparator estimates landmark displacement via median+consensus and subtracts it. It is expected to fail under some perturbations: **failures must be counted**, not edited away. Comparisons are both all-baseline-eligible and on the identical cases accepted by the contextual arm; coverage/HOLD are separate.

Files:
- `evaluation.json` full per-case results and grouped TEST comparisons
- `predictions_pre_scoring.jsonl` candidate predictions written before scoring truth (the scene generator itself knows truth; do not claim independent sealed external precommit)
- `images/sample_pairs.png` a grid of 12 paired visual frames (actual generated pixels, not fabricated results)

`--verify` rerenders all images, recomputes outcomes and compares report, predictions and sample PNG exactly. Prevents unnoticed alteration of output, **not** proof that the developer could never inspect synthetic truth.

### PC / publication

```powershell
$ErrorActionPreference="Stop"
Set-Location "C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) {throw "Git failed"}
py -m unittest discover -s tests -p "test_*.py"
if ($LASTEXITCODE -ne 0) {throw "Tests failed"}
$out="build/p26-hard-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p26_adversarial_pixels_v0 --out $out --count 480
if ($LASTEXITCODE -ne 0) {throw "Benchmark failed"}
py -m brody_world_physique.p26_adversarial_pixels_v0 --out $out --verify
if ($LASTEXITCODE -ne 0) {throw "Replay failed"}
Invoke-Item "$out/images"
notepad "$out/evaluation.json"
.\scripts\publish_local_evidence.ps1 -RunPath $out
if ($LASTEXITCODE -ne 0) {throw "Publication failed"}
```

Future tests (NOT implemented here): camera rotations, true 3D perspective, variable scale, occluding background, changing identities, video temporal offset; independent unseen generator and learnable vision system. Maintain `KX108_ONLY`, never mutate native memory or main branch.

**Status: prepared experimental harness; no PC execution or outcome claimed prior to evidence.**
