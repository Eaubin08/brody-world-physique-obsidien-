# RECONCILE V1 REGISTER — brody-world-physique-obsidien-

Branch: `reconcile/brody-world-physique-obsidien-v1`
Date: 2026-10-13
Status: **ORGANIZATION_RECONCILED — RUNTIME_NOT_CERTIFIED**

Organizational closure tag: `org-reconciled/brody-world-physique-obsidien-v1-20261013`, placed on the commit that contains this register. This tag certifies the Git organization only (provenance, integration, exclusions). **It is not a runtime freeze.** CI is green on this branch, but CI runs synthetic and bounded checks only; no physical validation was performed.

No source branch was modified. Nothing was deleted. Nothing was merged into `main`. No PR was opened, closed, retargeted or merged.

## 1. Base

| Item | Value |
|---|---|
| Base branch | `main` |
| Base SHA | `687949e66e7bc144bbd16c899fad61b7d3e4df4d` |
| Why this base | common ancestor of every lineage; the only branch that was green in CI before the reconciliation |

## 2. Integrated

| # | Source | Source SHA | Method | Resulting commit | Content |
|---|---|---|---|---|---|
| 1 | `exp/p2-multirepresentation-ablation-20261009` | `4a9d7f5c670ee1812a22c4451d77c07d05489edf` | merge commit (no squash, no rebase) | `8faf23f7aaccdf90b0523d82660829a5103e94be` | 256 commits (2026-10-08 → 2026-10-10), strictly ahead of the base (0 behind), no merge commit inside |

The 256 original commits are all reachable from this branch with their original SHA.
Tree check: the tree of `8faf23f7` is `5aa54f54124c2049bd45be5b10ac3099ba5ac0b2`, identical to the tree of the source head `4a9d7f5c`. Relative to `main`: 207 files added (303 files vs 96), mainly `brody_world_physique/` (20 → 90 files), `tests/` (21 → 88) and `docs/` (45 → 115).

Themes of the integrated lineage, from commit scopes: P2 multirepresentation ablations (`p2`, `p2.5`, `p2.8`, `p2.9j`, `p2.11c`, `p2.11d`), image school, fusion campaigns (`fusion-f2`, `fusion-f3b`, F8–F17), multiview.

Open draft PR #4 (`exp/p2-multirepresentation-ablation-20261009` → `main`) is left exactly as it was.

## 3. Reconciliation-only commits (exist in no source branch)

| SHA | Purpose |
|---|---|
| `ddba0a39a81e4453217efd63718c088fd83f41d5` | `.github/workflows/learning-loop-contracts.yml`: push trigger extended to `reconcile/**`; both jobs install `opencv-python-headless>=4.8,<5` before test discovery. Python 3.14 kept |
| (this commit) | adds this register |

## 4. Kept separate on purpose — evidence channel

| Branch | Head SHA | Role |
|---|---|---|
| `evidence/brody-local` | `309e123b97c667873abb73f25379e57d0b064cff` | Dedicated publication channel for local evidence. **Not merged**, by decision |

- Fed by `scripts/publish_local_evidence.ps1` (present in `main` and in this branch), whose rule is "Never commit or push main".
- Fork point: `1b21ead5` (ancestor of `main`). 8 commits, each adding files under `evidence/` only (verified commit by commit: 0 file outside `evidence/`).
- 69 evidence files, 1 726 142 bytes: 52 PNG, 12 JSON, 5 JSONL. None of these paths exists in `main`, in `exp/p2-…` or in this branch.

| Commit | Evidence set | Files |
|---|---|---|
| `cb302402dfdcc8adafe0544ca5b1622125d64872` | `relations-v4-1-20261009-003945` | 18 |
| `fcc80cf14ce9bf81077e9b5029f2488c9b205ad5` | `orientation-v4-2-20261009-012020` | 25 |
| `fdcd71860d8d7a6b4869bf291963fdd8da7eb39d` | `p2-evidence` | 5 |
| `3d956e7729a683fd7756a0357455eb424594a1ef` | `p2-streaming-20261009-021333` | 3 |
| `1d56cfb374577fc25173e915831c5e51a4518696` | `p24-fluctuations-20261009-023702` | 1 |
| `203fbee9249cb463fdd4562ffd206207dc807a60` | `p25-pixels-20261009-024419` | 11 |
| `e7af131256a3803c00bf1d759f4993f9474fe53d` | `p26-hard-20261009-033624` | 3 |
| `309e123b97c667873abb73f25379e57d0b064cff` | `p27-hierarchy-20261009-040107` | 3 |

This is a living branch: evidence published after `309e123b` is not covered by this register.

## 5. Already contained in the base (nothing to integrate)

| Branch | SHA | Evidence |
|---|---|---|
| `f0/cross-audit-contract-freeze-v0` | `ef69c248884f16ee67a13a37a26c070503a4fc61` | ancestor of `main` (PR #1 merged) |
| `f0/learning-loop-contracts-v0` | `4404324b88aafc7d67cad7fd080b60e3aee80618` | ancestor of `main` (PR #2 closed unmerged, but its head is reachable from `main`) |
| `f0/document-source-reconciliation-20261008` | `95c77d85a91d344aa5f5d8373fb362483daa2fbf` | ancestor of `main` (PR #3 merged) |

## 6. Tests

CI run `38350475720` on `ddba0a39a81e4453217efd63718c088fd83f41d5` (workflow `brody-image-f0-checks`, push): **success**.

| Job | Result |
|---|---|
| `windows-path-and-instrument-compatibility` (Windows, Python 3.14) | success — 417 tests OK, then instrument school, hidden-reference drawing, world-candidate bridge, V4.1 relations, V4.2 orientation |
| `contracts-and-docs (3.11)` (Ubuntu) | success — 417 tests OK, then the synthetic demonstrations and video experiments |
| `contracts-and-docs (3.12)` (Ubuntu) | success — 417 tests OK |

For comparison, as observed before the reconciliation:

- `main` @ `687949e6`: all three jobs green.
- `exp/p2-…` @ `4a9d7f5c`: never green (0 success out of 40 runs). Known cause on the head: `ModuleNotFoundError: No module named 'cv2'`. The P2 tests import OpenCV, while the workflow installed it only after the unit-test step and only for Python 3.11; the Windows 3.14 job never installed it. This is an environment gap in the workflow, resolved here by `ddba0a39`. The source branch itself still carries the original workflow.

OpenCV installs and imports on Windows with Python 3.14 (verified by this run).

## 7. Open items

| Item | Status |
|---|---|
| Physical validation (real cameras, instruments, physical world loops) | **PENDING** — CI uses synthetic and bounded inputs only |
| Local evidence vs code | evidence sets `p24`–`p27` on `evidence/brody-local` match P2 stages by name; no automated link between an evidence set and a code SHA was verified |
| CI on `exp/p2-…` | still red on the source branch (workflow unchanged there, by design) |
| OPEN_TECHNICAL_ITEMS | none found by CI on this branch |

## 8. Guarantees

- `main` is still at `687949e66e7bc144bbd16c899fad61b7d3e4df4d`.
- The 6 pre-existing branches are at the same SHA as before the operation. The repository had no tag before.
- PRs #1, #2, #3 (closed) and #4 (open, draft, → `main`) are unchanged.
- No force-push, rebase or squash.
