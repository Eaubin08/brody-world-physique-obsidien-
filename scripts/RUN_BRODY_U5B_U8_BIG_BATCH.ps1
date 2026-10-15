param(
  [string]$Out = "build/u5b-u8-big-batch-v1",
  [string]$Video = "",
  [int]$Seeds = 3
)
$ErrorActionPreference = "Stop"
if (Test-Path $Out) { throw "PRESERVE_PRIOR_EVIDENCE: $Out" }
py -m unittest discover -s tests -p "test_u8_shared_shape_motion_generation_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "U8_TEST_FAILED" }
py -m unittest discover -s tests -p "test_u5b_u8_integrated_big_batch_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "BIG_BATCH_TEST_FAILED" }
if ($Video) {
  py -m brody_world_physique.u5b_u8_integrated_big_batch_v1 --out $Out --video $Video --seeds $Seeds
} else {
  py -m brody_world_physique.u5b_u8_integrated_big_batch_v1 --out $Out --seeds $Seeds
}
if ($LASTEXITCODE -ne 0) { throw "BIG_BATCH_CAMPAIGN_FAILED" }
Get-Content (Join-Path $Out "MASTER_REPORT.json")
