# BRODY P0-P5 / executable from the repository root.
param(
  [string]$Output = "build/p0-p5-integrated-v1",
  [string]$ExternalImages = ""
)
$ErrorActionPreference = "Stop"
if (Test-Path $Output) { throw "PRESERVE_PRIOR_EVIDENCE: $Output already exists" }
Write-Host "=== P0: ALL REPOSITORY UNIT TESTS ==="
py -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "P0_FULL_REGRESSION_FAILED" }
Write-Host "=== P1-P5 INTEGRATED TESTS ==="
py -m unittest discover -s tests -p "test_p0_p5_integrated_evidence_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "P0_P5_TEST_FAILED" }
Write-Host "=== P1-P5 CAMPAIGN ==="
if ([string]::IsNullOrWhiteSpace($ExternalImages)) {
  py -m brody_world_physique.p0_p5_integrated_evidence_v1 --out $Output
} else {
  py -m brody_world_physique.p0_p5_integrated_evidence_v1 --out $Output --external-images $ExternalImages
}
if ($LASTEXITCODE -ne 0) { throw "P1_P5_CAMPAIGN_FAILED" }
Write-Host "=== MASTER REPORT ==="
Get-Content (Join-Path $Output "MASTER_REPORT.json")
