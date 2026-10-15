param(
  [string]$Out = "build/BRODY_FINALE_G1",
  [string]$ExternalVideo = ""
)
$ErrorActionPreference = "Stop"
if (Test-Path $Out) { throw "PRESERVE_PRIOR_EVIDENCE: $Out" }
$branch=(git branch --show-current).Trim()
if ($branch -ne "exp/p2-multirepresentation-ablation-20261009") { throw "WRONG_BRANCH" }
$head=(git rev-parse HEAD).Trim()
New-Item -Path $Out -ItemType Directory | Out-Null
$testlog=Join-Path $Out "SESSION_TESTS.log"
$oldPref=$ErrorActionPreference
try {
  $ErrorActionPreference="Continue"
  & py -m unittest discover -s tests -p "test_session_restart_replay_v1.py" -v 2>&1 | Out-File -FilePath $testlog -Encoding utf8
  $testcode=$LASTEXITCODE
} finally {
  $ErrorActionPreference=$oldPref
}
Get-Content $testlog | Select-Object -Last 12
if ($testcode -ne 0) { throw "SESSION_TESTS_FAILED: $testlog" }
$full=Join-Path $Out "FULL_REGRESSION"
& powershell -NoProfile -ExecutionPolicy Bypass -File scripts/RUN_BRODY_FULL_CONSOLIDATION.ps1 -Out $full
if ($LASTEXITCODE -ne 0) { throw "FULL_REGRESSION_FAILED" }
$memory=Join-Path $full "REPLAY/CANDIDATE_MEMORY.json"
$restart=Join-Path $Out "RESTARTED_SESSION"
& py -m brody_world_physique.session_restart_replay_v1 --memory $memory --out $restart
if ($LASTEXITCODE -ne 0) { throw "SESSION_REPLAY_FAILED" }
$fullmeta=Get-Content (Join-Path $full "MASTER_REGRESSION_REPORT.json") -Raw | ConvertFrom-Json
$replayed=Get-Content (Join-Path $restart "MASTER_REPORT.json") -Raw | ConvertFrom-Json
if (!$fullmeta.tests.ALL.passed -or !$fullmeta.tests.CONSOLIDATED.passed -or !$fullmeta.tests.U5B_U8.passed) { throw "REGRESSION_NOT_GREEN" }
if (!$replayed.memory_bytes_unchanged) { throw "MEMORY_INTEGRITY_FAILED" }
$gate="HOLD_NO_INDEPENDENT_VIDEO"
if ($ExternalVideo) {
  if (!(Test-Path -LiteralPath $ExternalVideo -PathType Leaf)) { throw "EXTERNAL_VIDEO_NOT_FOUND" }
  $gate="VIDEO_AVAILABLE_MANUAL_ANNOTATION_REQUIRED"
}
$final=@{
 schema="BRODY_G1_FINAL_FREEZE_CANDIDATE_V1";git_head=$head
 full_regression_pass=$true;restart_replay_pass=$true
 video_gate=$gate
 real_multicamera_reverse360_proven=$false
 sens_mmonde_runtime_verified=$false
 canonical_promotion=$false;native_memory_write=$false
 decision_authority="KX108_ONLY"
 verdict="LOCAL_SYNTHETIC_GREEN_EXTERNAL_GATES_OPEN"
}
$final | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $Out "MASTER_FREEZE_VERDICT.json")
Get-Content (Join-Path $Out "MASTER_FREEZE_VERDICT.json")
Write-Host "FINAL_REPORT=$Out/MASTER_FREEZE_VERDICT.json"
