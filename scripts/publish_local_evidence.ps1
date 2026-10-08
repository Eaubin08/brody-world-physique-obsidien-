<#
.SYNOPSIS
  Publish only chosen LOCAL Brody images and receipts to evidence branch.
  Never commit or push main. Reuse identity from last successful evidence commit.
.EXAMPLE
  .\scripts\publish_local_evidence.ps1 -RunPath "build\orientation-v4-2-..."
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$RunPath,
  [string]$Branch = "evidence/brody-local"
)
$ErrorActionPreference = "Stop"
$repo = (git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw "Run from a Brody Git checkout" }
$source = (Resolve-Path -LiteralPath $RunPath).Path
if (-not (Test-Path -LiteralPath (Join-Path $source "evaluation.json"))) {
  throw "Missing evaluation.json in source experiment"
}
if (-not (Test-Path -LiteralPath (Join-Path $source "images") -PathType Container)) {
  throw "Missing images folder in source experiment"
}
$pngs = @(Get-ChildItem -LiteralPath (Join-Path $source "images") -File -Filter "*.png")
if ($pngs.Count -eq 0) { throw "No image evidence to publish" }
$root = Split-Path -Parent $repo
$worktree = Join-Path $root "brody-image-evidence"
if (-not (Test-Path -LiteralPath $worktree)) {
  throw "Evidence worktree missing: $worktree. Create it explicitly first."
}
$active = (git -C $worktree branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $active -ne $Branch) {
  throw "Evidence checkout is not on branch $Branch"
}
git -C $worktree pull --ff-only origin $Branch
if ($LASTEXITCODE -ne 0) { throw "Cannot fast-forward evidence worktree" }
$name = Split-Path -Leaf $source
if ($name -notmatch "^[a-zA-Z0-9_.-]+$") { throw "Unsafe experiment directory name" }
$target = Join-Path $worktree "evidence\$name"
if (Test-Path -LiteralPath $target) { throw "Evidence already exists: $name" }
New-Item -ItemType Directory -Path (Join-Path $target "images") -Force | Out-Null
Get-ChildItem -LiteralPath $source -File |
  Where-Object { $_.Extension -in @(".json",".jsonl") } |
  Copy-Item -Destination $target
$pngs | Copy-Item -Destination (Join-Path $target "images")
$rel = "evidence/$name"
git -C $worktree add -- $rel
if ($LASTEXITCODE -ne 0) { throw "Failed to stage evidence" }
$staged = @(git -C $worktree diff --cached --name-only -- $rel)
if ($staged.Count -eq 0) { throw "Nothing staged for evidence" }
$outside = @(git -C $worktree diff --cached --name-only |
  Where-Object { -not $_.StartsWith("$rel/") })
if ($outside.Count -gt 0) {
  throw "Unrelated staged changes; refusing to commit"
}
$gitName = (git -C $worktree log -1 --format="%an").Trim()
$gitEmail = (git -C $worktree log -1 --format="%ae").Trim()
if (-not $gitName -or -not $gitEmail) {
  throw "Author identity unknown; configure worktree author locally"
}
git -C $worktree -c "user.name=$gitName" -c "user.email=$gitEmail" commit -m "Brody local evidence: $name"
if ($LASTEXITCODE -ne 0) { throw "Evidence commit failed; not pushing" }
git -C $worktree push origin $Branch
if ($LASTEXITCODE -ne 0) { throw "Evidence push failed" }
$files = @(git -C $worktree ls-tree -r --name-only HEAD -- $rel)
if ($files.Count -lt $staged.Count) { throw "Published tree missing staged set" }
$sha = (git -C $worktree rev-parse HEAD).Trim()
Write-Host "PUBLISHED_BRANCH=$Branch"
Write-Host "PUBLISHED_SHA=$sha"
Write-Host "PUBLISHED_COUNT=$($files.Count)"
$files | ForEach-Object { Write-Host $_ }
