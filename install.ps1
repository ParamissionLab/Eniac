# Install the skill from a Windows terminal, without needing to know which Python is on
# PATH. Everything real happens in scripts/install.py; this only finds an interpreter and
# forwards the arguments, so there is one implementation of the install and one place to
# fix it.
#
#   .\install.ps1                     # every runtime detected on this machine
#   .\install.ps1 --list
#   .\install.ps1 --runtime claude --backup
#   .\install.ps1 --project ..\my-app
#   .\install.ps1 --dry-run
#
# With no clone, skip this file entirely and pipe the installer itself:
#   irm https://raw.githubusercontent.com/ParamissionLab/Eniac/main/scripts/install.py | python -
#
# PowerShell treats a leading `-` as its own parameter, so pass the script's flags with
# the two dashes shown above.

$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'scripts\install.py'

# Probe rather than trust Get-Command: the `python` / `python3` on PATH is often the
# Microsoft Store stub, which exists, prints an advert, and exits non-zero. A candidate
# counts only if it can report a version.
$python = $null
foreach ($candidate in @('python', 'python3', 'py')) {
    if (-not (Get-Command $candidate -ErrorAction SilentlyContinue)) { continue }
    & $candidate -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' 2>$null
    if ($LASTEXITCODE -eq 0) { $python = $candidate; break }
}
if (-not $python) {
    Write-Error "No Python found on PATH. Install Python 3.8+ (nothing else is needed - the skill is Markdown), or copy skills\Eniac into your runtime's skills directory by hand; INSTALL.md has the paths."
    exit 1
}

& $python $script @args
exit $LASTEXITCODE
