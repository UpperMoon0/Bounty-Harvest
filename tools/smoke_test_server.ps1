[CmdletBinding()]
param(
    [int]$TimeoutSeconds = 420,
    [string]$JavaPath = 'java'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$repoRoot = Split-Path -Parent $PSScriptRoot
$pack = Get-Content -Raw -LiteralPath (Join-Path $repoRoot 'pack/pack.json') | ConvertFrom-Json
$archive = Join-Path $repoRoot "dist/$($pack.artifactName)-$($pack.version)-server.zip"
if (-not (Test-Path -LiteralPath $archive -PathType Leaf)) { throw "Missing $archive" }

$smokeParent = Join-Path $repoRoot '.server-smoke'
$smokeRoot = Join-Path $smokeParent ([guid]::NewGuid().ToString('N'))
$null = New-Item -ItemType Directory -Path $smokeRoot -Force

function Invoke-JavaProcess {
    param([string[]]$Arguments, [int]$Timeout, [switch]$WatchForDone)

    $token = [guid]::NewGuid().ToString('N')
    $stdout = Join-Path $smokeRoot "$token.stdout.log"
    $stderr = Join-Path $smokeRoot "$token.stderr.log"
    $process = Start-Process -FilePath $JavaPath -ArgumentList $Arguments -WorkingDirectory $smokeRoot `
        -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    # Hold the native process handle so PowerShell retains ExitCode after Refresh()/HasExited polling.
    $null = $process.Handle

    $deadline = [DateTime]::UtcNow.AddSeconds($Timeout)
    while ([DateTime]::UtcNow -lt $deadline) {
        $process.Refresh()
        if ($process.HasExited) { break }
        $output = if (Test-Path $stdout) { [string](Get-Content -Raw -LiteralPath $stdout) } else { '' }
        if ($WatchForDone -and $output -match 'Done \([0-9.]+s\)!') {
            Stop-Process -Id $process.Id -Force
            $process.WaitForExit()
            return $output
        }
        Start-Sleep -Milliseconds 500
    }
    $output = if (Test-Path $stdout) { [string](Get-Content -Raw -LiteralPath $stdout) } else { '' }
    $errors = if (Test-Path $stderr) { [string](Get-Content -Raw -LiteralPath $stderr) } else { '' }
    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
        throw "Java timed out after $Timeout seconds.`n$output`n$errors"
    }
    $process.WaitForExit()
    $exitCode = $process.ExitCode
    if ($exitCode -ne 0) { throw "Java exited with code $exitCode.`n$output`n$errors" }
    if ($WatchForDone) { throw "Server exited before reaching Done.`n$output`n$errors" }
    return "$output`n$errors"
}

try {
    Expand-Archive -LiteralPath $archive -DestinationPath $smokeRoot
    $coordinate = "$($pack.minecraftVersion)-$($pack.forgeVersion)"
    $installer = "forge-$coordinate-installer.jar"
    Invoke-JavaProcess -Arguments @('-jar', $installer, '--installServer') -Timeout 180 | Out-Null
    [System.IO.File]::WriteAllText((Join-Path $smokeRoot 'eula.txt'), "eula=true`n")
    [System.IO.File]::WriteAllText((Join-Path $smokeRoot 'user_jvm_args.txt'), "-Xms1G`n-Xmx4G`n-XX:+UseG1GC`n")
    $argsFile = "@libraries/net/minecraftforge/forge/$coordinate/win_args.txt"
    Invoke-JavaProcess -Arguments @('@user_jvm_args.txt', $argsFile, 'nogui') -Timeout $TimeoutSeconds -WatchForDone | Out-Null
    Write-Host 'Dedicated server smoke test reached Done.'
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($smokeRoot)
    $parent = [System.IO.Path]::GetFullPath($smokeParent)
    if ($resolved.StartsWith($parent, [System.StringComparison]::OrdinalIgnoreCase) -and (Test-Path $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
