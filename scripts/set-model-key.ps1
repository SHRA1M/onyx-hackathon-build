# Writes the Claude API key from the clipboard into .env (gitignored). Never prints the key.
# Run from Claude Code:  ! powershell -ExecutionPolicy Bypass -File D:\Projects\engineering\onyx-hackathon-build\scripts\set-model-key.ps1
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $repo ".env"

$key = (Get-Clipboard -Raw)
if ($null -eq $key) { $key = "" }
$key = $key.Trim()
if (-not $key.StartsWith("sk-ant-")) {
    Write-Output "STOPPED: the clipboard does not hold a Claude API key (it should start with sk-ant-). Copy the key and run again. .env not changed."
    exit 1
}

if (Test-Path $envPath) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    Copy-Item $envPath "$envPath.bak-$stamp"
    Write-Output "Backed up the old .env to .env.bak-$stamp"
}

$lines = @(
    "ONYX_MODEL_BASE_URL=https://api.anthropic.com/v1/",
    "ONYX_MODEL=claude-opus-5-5",
    "ONYX_MODEL_API_KEY=$key"
)
[System.IO.File]::WriteAllLines($envPath, $lines, (New-Object System.Text.UTF8Encoding($false)))
Set-Clipboard -Value " "

$check = Get-Content $envPath
$ok = ($check.Count -eq 3) -and ($check[2].Length -gt 30)
$ignored = (& git -C $repo check-ignore .env) -ne $null
Write-Output ("DONE: .env written, 3 lines, key length " + ($key.Length) + " characters. Clipboard cleared.")
Write-Output ("Check: three values filled = " + $ok + "; .env ignored by git = " + $ignored)
