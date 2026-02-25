param(
  [string]$Path = "postman/collections/PyPNM.postman_collection.json",
  [switch]$Check,
  [switch]$Fix,
  [switch]$Compact
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$PyTool = Join-Path $RepoRoot "tools\postman\format_collection.py"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
  $PythonExe = $VenvPython
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  $PythonExe = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $PythonExe = "python"
} else {
  Write-Error "Python interpreter not found (.venv\\Scripts\\python.exe, py, or python)."
  exit 1
}

$ArgsList = @($PyTool, "--path", $Path)
if ($Check) { $ArgsList += "--check" }
if ($Fix) { $ArgsList += "--fix" }
if ($Compact) { $ArgsList += "--compact" }

& $PythonExe @ArgsList
exit $LASTEXITCODE
