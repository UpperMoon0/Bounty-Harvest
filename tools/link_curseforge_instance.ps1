[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$RepositoryRoot,
    [Parameter(Mandatory)] [string]$InstanceRoot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = [System.IO.Path]::GetFullPath($RepositoryRoot)
$instanceRoot = [System.IO.Path]::GetFullPath($InstanceRoot)
$instancesRoot = [System.IO.Path]::GetFullPath(
    (Join-Path ([Environment]::GetFolderPath('UserProfile')) 'curseforge\minecraft\Instances')
)
if (-not $instanceRoot.StartsWith($instancesRoot + [System.IO.Path]::DirectorySeparatorChar,
        [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Instance must be below $instancesRoot"
}

$repoMetadata = Join-Path $repoRoot 'minecraftinstance.json'
$instanceMetadata = Join-Path $instanceRoot 'minecraftinstance.json'
if (-not (Test-Path -LiteralPath $repoMetadata -PathType Leaf)) { throw "Missing $repoMetadata" }
if (-not (Test-Path -LiteralPath $instanceMetadata -PathType Leaf)) { throw "Missing $instanceMetadata" }

$item = Get-Item -LiteralPath $instanceMetadata -Force
if ($item.LinkType -eq 'SymbolicLink') {
    if ([System.IO.Path]::GetFullPath([string]$item.Target) -eq $repoMetadata) {
        Write-Host "Already linked: $instanceMetadata -> $repoMetadata"
        exit 0
    }
    throw "Refusing to replace an unexpected symbolic link: $instanceMetadata"
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = Join-Path $instanceRoot "minecraftinstance.pre-link-$stamp.json"
Move-Item -LiteralPath $instanceMetadata -Destination $backup
try {
    $null = New-Item -ItemType SymbolicLink -Path $instanceMetadata -Target $repoMetadata
}
catch {
    Move-Item -LiteralPath $backup -Destination $instanceMetadata
    throw
}

Write-Host "Linked $instanceMetadata -> $repoMetadata"
Write-Host "Original launcher metadata preserved at $backup"
