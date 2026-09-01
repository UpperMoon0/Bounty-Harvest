[CmdletBinding()]
param(
    [string]$Version,
    [ValidateSet('alpha', 'beta', 'release')] [string]$ReleaseType,
    [string]$ChangelogFile,
    [switch]$SkipBuild,
    [switch]$DryRun,
    [switch]$Preflight
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = Split-Path -Parent $PSScriptRoot
$pack = Get-Content -LiteralPath (Join-Path $repoRoot 'pack/pack.json') -Raw | ConvertFrom-Json
if ([string]::IsNullOrWhiteSpace($Version)) { $Version = [string]$pack.version }
if ([string]::IsNullOrWhiteSpace($ReleaseType)) { $ReleaseType = [string]$pack.releaseType }
if ([string]::IsNullOrWhiteSpace($ChangelogFile)) {
    $ChangelogFile = Join-Path $repoRoot "changelog/$Version.md"
}

$artifact = [string]$pack.artifactName
$clientArchive = Join-Path $repoRoot "dist/$artifact-$Version.zip"
$serverArchive = Join-Path $repoRoot "dist/$artifact-$Version-server.zip"
$changelog = [string](Get-Content -LiteralPath $ChangelogFile -Raw -Encoding utf8)
$endpoint = "https://minecraft.curseforge.com/api/projects/$($pack.curseForgeProjectId)/upload-file"
$mainMetadata = [ordered]@{
    changelog = $changelog
    changelogType = 'markdown'
    displayName = "$($pack.name) $Version"
    gameVersionNames = @(
        [string]$pack.minecraftVersion,
        'Forge',
        "Java $($pack.javaVersion)",
        'Client'
    )
    releaseType = $ReleaseType
}

if ($DryRun) {
    Write-Host "DRY RUN: would upload $clientArchive"
    Write-Host ($mainMetadata | ConvertTo-Json -Depth 5)
    Write-Host "DRY RUN: would attach $serverArchive as the server child file"
    exit 0
}

if ($Preflight) {
    Write-Host "PREFLIGHT: validating CurseForge upload prerequisites"
    if (-not (Test-Path -LiteralPath $clientArchive -PathType Leaf)) {
        throw "Missing client archive: $clientArchive"
    }
    if (-not (Test-Path -LiteralPath $serverArchive -PathType Leaf)) {
        throw "Missing server archive: $serverArchive"
    }
    if (-not (Test-Path -LiteralPath $ChangelogFile -PathType Leaf)) {
        throw "Missing changelog: $ChangelogFile"
    }
    $token = [Environment]::GetEnvironmentVariable('CURSEFORGE_API_TOKEN')
    if ([string]::IsNullOrWhiteSpace($token)) { throw 'CURSEFORGE_API_TOKEN is required for preflight.' }
    if (-not $pack.curseForgeProjectId -or $pack.curseForgeProjectId -eq 0) { throw 'CurseForge project ID is required.' }
    $headers = @{ 'X-Api-Token' = $token }
    $gameVersionsEndpoint = "https://api.curseforge.com/v1/mods/$($pack.curseForgeProjectId)/files/game-versions"
    try {
        $gameVersions = Invoke-RestMethod -Uri $gameVersionsEndpoint -Headers $headers
        $availableNames = @($gameVersions.data | ForEach-Object { [string]$_.name })
        $requiredNames = @(
            [string]$pack.minecraftVersion,
            'Forge',
            "Java $($pack.javaVersion)",
            'Client'
        )
        foreach ($required in $requiredNames) {
            if ($availableNames -notcontains $required) {
                throw "CurseForge does not recognize required game version '$required'. Available: $($availableNames -join ', ')"
            }
        }
        Write-Host "PREFLIGHT: All required game version names are recognized by CurseForge."
    }
    catch {
        throw "PREFLIGHT: CurseForge API reachability or game-version check failed: $($_.Exception.Message)"
    }
    Write-Host "PREFLIGHT: All checks passed."
    exit 0
}

if (-not $SkipBuild) { & (Join-Path $PSScriptRoot 'build_modpack.ps1') -Version $Version }
foreach ($archive in @($clientArchive, $serverArchive)) {
    if (-not (Test-Path -LiteralPath $archive -PathType Leaf)) {
        throw "Missing release archive: $archive"
    }
}

$token = [Environment]::GetEnvironmentVariable('CURSEFORGE_API_TOKEN')
if ([string]::IsNullOrWhiteSpace($token)) { throw 'CURSEFORGE_API_TOKEN is required.' }
$headers = @{ 'X-Api-Token' = $token }
$filesEndpoint = "https://api.curseforge.com/v1/mods/$($pack.curseForgeProjectId)/files"

function Get-UploadErrorBody($ErrorRecord) {
    if ($ErrorRecord.ErrorDetails -and $ErrorRecord.ErrorDetails.Message) {
        return [string]$ErrorRecord.ErrorDetails.Message
    }
    return [string]$ErrorRecord.Exception.Message
}

function Get-ExistingFileId($DisplayName) {
    $pageSize = 50
    for ($index = 0; $index -lt 2500; $index += $pageSize) {
        $page = Invoke-RestMethod -Uri "$filesEndpoint`?index=$index&pageSize=$pageSize" -Headers $headers
        if (-not $page -or -not $page.data) { break }
        foreach ($file in @($page.data)) {
            if ($file.displayName -eq $DisplayName -and $file.id) { return [string]$file.id }
        }
        if ($page.data.Count -lt $pageSize) { break }
    }
    return $null
}

function Publish-File($Metadata, $Archive) {
    try {
        $response = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $headers -Form @{
            metadata = ($Metadata | ConvertTo-Json -Compress -Depth 5)
            file = Get-Item -LiteralPath $Archive
        }
        if (-not $response.id) { throw "CurseForge returned no file ID for $Archive." }
        return [string]$response.id
    }
    catch {
        $body = Get-UploadErrorBody $_
        if ($body -match 'already|duplicate') {
            $existing = Get-ExistingFileId $Metadata.displayName
            if ($existing) {
                Write-Host "Reusing existing CurseForge file $existing for $($Metadata.displayName)."
                return $existing
            }
        }
        throw "CurseForge upload failed for ${Archive}: $body"
    }
}

$clientFileId = Publish-File $mainMetadata $clientArchive
$serverMetadata = [ordered]@{
    changelog = $changelog
    changelogType = 'markdown'
    displayName = "$($pack.name) $Version Server Pack"
    parentFileID = [long]$clientFileId
    releaseType = $ReleaseType
}
$serverFileId = Publish-File $serverMetadata $serverArchive
Write-Host "Client file $clientFileId and server child file $serverFileId are present on CurseForge."
