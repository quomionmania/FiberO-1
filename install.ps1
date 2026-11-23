# FiberO-1 Open Source Installer (Windows PowerShell)
# Installs OpenCode agent files and optional PC-control dependencies.

[CmdletBinding()]
param(
  [switch]$SkipOpenCode,
  [switch]$SkipReferenceCopies,
  [switch]$InstallPcControlDeps
)

$ErrorActionPreference = 'Stop'

function Write-Step($msg) { Write-Host "[FiberO-1] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$opencodeAgents = Join-Path $env:USERPROFILE '.config\opencode\agents'
$docsRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'FiberO-1-open-source'

Write-Step "Root: $root"

if (-not $SkipOpenCode) {
  Write-Step "Installing OpenCode agents..."
  New-Item -ItemType Directory -Force -Path $opencodeAgents | Out-Null

  $agentFiles = @()
  $agentFiles += Get-ChildItem -Path (Join-Path $root 'FiberO-1\opencode\agents') -Filter *.md -ErrorAction SilentlyContinue
  $agentFiles += Get-ChildItem -Path (Join-Path $root 'Fiberglass-5.0\opencode\agents') -Filter *.md -ErrorAction SilentlyContinue

  foreach ($f in $agentFiles) {
    Copy-Item -Path $f.FullName -Destination (Join-Path $opencodeAgents $f.Name) -Force
    Write-Ok "Installed agent: $($f.Name)"
  }

  if ($agentFiles.Count -eq 0) { Write-Warn "No OpenCode agent files found." }
}

if (-not $SkipReferenceCopies) {
  Write-Step "Copying Claude/ChatGPT reference prompts to Documents..."
  New-Item -ItemType Directory -Force -Path $docsRoot | Out-Null
  Copy-Item -Path (Join-Path $root 'FiberO-1') -Destination (Join-Path $docsRoot 'FiberO-1') -Recurse -Force
  Copy-Item -Path (Join-Path $root 'Fiberglass-5.0') -Destination (Join-Path $docsRoot 'Fiberglass-5.0') -Recurse -Force
  Write-Ok "Reference copy created: $docsRoot"
}

if ($InstallPcControlDeps) {
  Write-Step "Installing PC-control Python dependencies..."
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
  if (-not $py) {
    Write-Warn "Python not found. Install Python 3.10+ and rerun with -InstallPcControlDeps."
  } else {
    & $py.Source -m pip install --upgrade pip
    & $py.Source -m pip install pynput pillow
    Write-Ok "PC-control dependencies installed (pynput, pillow)."
  }
}

Write-Host ""
Write-Ok "Install complete."
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. OpenCode: restart/reload OpenCode to pick up new agents." -ForegroundColor Gray
Write-Host "  2. Claude/ChatGPT: use files in $docsRoot as system/custom prompts." -ForegroundColor Gray
Write-Host "  3. PC control prototype: python .\FiberO-1\pc-control\fiber_o1_pc_control.py" -ForegroundColor Gray
