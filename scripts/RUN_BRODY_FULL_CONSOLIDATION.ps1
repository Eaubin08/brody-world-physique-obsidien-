param(
  [string]$Out = "build/BRODY_CONSOLIDATION_20261015",
  [string]$Video = "",
  [switch]$SkipFullRegression
)
$ErrorActionPreference = "Stop"
$branch = "exp/p2-multirepresentation-ablation-20261009"
if (Test-Path $Out) { throw "PRESERVE_EVIDENCE: $Out" }
New-Item -ItemType Directory -Path $Out -Force | Out-Null
$revision=(git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw "GIT_HEAD_FAILED" }
$branchActive=(git branch --show-current).Trim()
if ($branchActive -ne $branch) { throw "WRONG_BRANCH: $branchActive" }
$meta=@{ schema="BRODY_FULL_CONSOLIDATION_V1"; git_revision=$revision;
 full_regression_executed=(!$SkipFullRegression);
 tests=@{}; video_evidence="HOLD_NO_INDEPENDENT_VIDEO";
 decision_authority="KX108_ONLY"; native_memory_write=$false; canonical_promotion=$false }
$meta | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $Out "CAMPAIGN_STARTED.json")
function Invoke-Test([string]$Name,[string[]]$Args) {
  $log=Join-Path $Out ("TEST_"+$Name+".log")
  & py @Args 2>&1 | Out-File -FilePath $log -Encoding utf8
  $code=$LASTEXITCODE
  Get-Content $log | Select-Object -Last 12
  $meta.tests[$Name]=@{exit_code=$code; log=$log; passed=($code -eq 0)}
  if ($code -ne 0) {
    $meta | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $Out "CAMPAIGN_FAILURE.json")
    throw "TEST_FAILED: $Name — see $log"
  }
}
if (!$SkipFullRegression) {
  Invoke-Test "ALL" @("-m","unittest","discover","-s","tests","-v")
}
Invoke-Test "CONSOLIDATED" @("-m","unittest","discover","-s","tests","-p","test_consolidated_education_replay_v1.py","-v")
Invoke-Test "U5B_U8" @("-m","unittest","discover","-s","tests","-p","test_u5b_u8_integrated_big_batch_v1.py","-v")
& py -m brody_world_physique.consolidated_education_replay_v1 --out (Join-Path $Out "REPLAY")
if ($LASTEXITCODE -ne 0) { throw "REPLAY_CAMPAIGN_FAILED" }
& py -m brody_world_physique.u5b_u8_integrated_big_batch_v1 --out (Join-Path $Out "MULTIVIEW")
if ($LASTEXITCODE -ne 0) { throw "MULTIVIEW_CAMPAIGN_FAILED" }
if ($Video) {
  if (!(Test-Path $Video -PathType Leaf)) { throw "VIDEO_NOT_FOUND: $Video" }
  # ONLY an independent manual annotation can grade a real video's future.
  $meta.video_evidence="VIDEO_AVAILABLE_REQUIRES_MANUAL_ANNOTATION"
  Write-Host "Video detected. Manual 4-frame annotation is a separate user-confirmed UI workflow."
}
$meta.verdict="CONSOLIDATION_TESTS_PASSED_EXTERNAL_EVIDENCE_GATED"
$meta | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $Out "MASTER_REGRESSION_REPORT.json")
Get-Content (Join-Path $Out "MASTER_REGRESSION_REPORT.json")
Get-Content (Join-Path $Out "REPLAY/MASTER_REPORT.json")
Write-Host "DONE: $Out"
