# Publish ONLY the reviewed code files to a new public GitHub repository.
# Requirements: Git, Python 3, GitHub CLI (gh), authenticated using `gh auth login`.
param(
    [string]$RepositoryName = 'industrial-anomaly-detection-benchmark'
)
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))

foreach ($tool in @('git','gh','python')) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "Missing tool: $tool. Install it from the official source."
    }
}
if (Test-Path '.git') {
    throw 'For safety, publish from a freshly extracted, untracked directory only. An existing Git history could expose private information.'
}

python .\scripts\audit_repository.py
if ($LASTEXITCODE -ne 0) { throw 'Privacy preflight failed.' }
gh auth status
if ($LASTEXITCODE -ne 0) { throw 'Log into the intended GitHub account using gh auth login.' }
$who = gh api user --jq '.login'
if ($LASTEXITCODE -ne 0 -or -not $who) { throw 'Could not read authenticated GitHub user.' }
$accountId = gh api user --jq '.id'
if ($LASTEXITCODE -ne 0 -or -not $accountId) { throw 'Could not read authenticated GitHub user id.' }
$destination = "$who/$RepositoryName"

Write-Host ''
Write-Host 'PUBLICATION PRIVACY CHECK' -ForegroundColor Yellow
Write-Host "  Account and visible repository URL: https://github.com/$destination"
Write-Host '  GitHub username, repository ownership and account profile may reveal your identity.'
Write-Host '  Public code can be copied or forked even if the repository is later made private.'
Write-Host '  The dataset is excluded; only documentation and source code will be shared.'
Write-Host ''
$confirmation = Read-Host 'Type PUBLISH to create this PUBLIC repository (anything else cancels)'
if ($confirmation -cne 'PUBLISH') { throw 'Cancelled. No GitHub repository was created.' }

$files = @(
    '.gitignore', 'README.md', 'requirements.txt',
    'datasets/README.md', 'notebooks/anomaly_detection_benchmark.ipynb',
    'docs/technical-review.md', 'docs/observed-results.md',
    'scripts/audit_repository.py', 'scripts/check_dataset.py',
    'scripts/publish_github.ps1', 'tests/test_notebook_structure.py',
    'tests/test_dataset_layout.py'
)
git init -b main
if ($LASTEXITCODE -ne 0) { throw 'git init failed.' }
foreach ($file in $files) {
    git add -- $file
    if ($LASTEXITCODE -ne 0) { throw "Could not stage: $file" }
}
python .\scripts\audit_repository.py --staged
if ($LASTEXITCODE -ne 0) { throw 'Staged-file review failed. Nothing published.' }
$noReply = "$accountId+$who@users.noreply.github.com"
git -c user.name='Research Contributor' -c "user.email=$noReply" commit -m 'Publish anonymized industrial anomaly detection benchmark'
if ($LASTEXITCODE -ne 0) { throw 'git commit failed. Nothing published.' }

gh repo create $destination --public --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'GitHub command failed; check the output. Verify whether a repository was created.' }
Write-Host "Published successfully: https://github.com/$destination" -ForegroundColor Green
