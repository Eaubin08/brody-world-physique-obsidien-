# 100 - U1 U2: executed probe updates an experimental candidate memory

The probe is chosen with the existing P158 ambiguity policy. A P158 synthetic image trajectory is then actually sampled and processed through the existing P157 pixel observer. The observed acceleration is stored in a versioned experimental state.

P155 rejects a global update that would damage the clean context. The new candidate memory therefore stores separate clean and intervention-specific acceleration. Two later, independently generated sequences are predicted before the final observation is scored. Check measured prediction error before and after the local correction.

This is a genuine experimental state-to-prediction causal data path, unlike the previous E8 probe proposal. Still, the setting is predefined, synthetic, one-dimensional motion. Context selection for the exam is provided by its harness; no spontaneous object model, full multimodal shared state, physical action, or autonomous category discovery has been proven.

## PowerShell single pass
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_u1_u2_shared_candidate_learning_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.u1_u2_shared_candidate_learning_v1 --out "build/u1-u2-shared-candidate-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/u1-u2-shared-candidate-v1/MASTER_REPORT.json"
```
The output directory must not exist. Reports are experimental candidates; native_memory_write false, canonical_promotion false, KX108_ONLY.

## Next stages
U3: integrate pixel-derived context selection with generated visual future, removing examiner-provided context routing.
U4: genuine shared persistent scene/skill memory across E1-E5, strict replay/retention.
U5: independent videos with source provenance and zero heldout leakage.
U6: read-only audit and integration of actual upstream SENS/MMonde contracts; no duplicated authority.
U7: Reverse360 multi-view invariance and object permanence under occlusion.
