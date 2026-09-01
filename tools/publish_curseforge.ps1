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
$authorApiBase = 'https://minecraft.curseforge.com/api'
$uploadEndpoint = "$authorApiBase/projects/$($pack.curseForgeProjectId)/upload-file"
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

$token = [Environment]::GetEnvironmentVariable('CURSEFORGE_API_TOKEN')
if ([string]::IsNullOrWhiteSpace($token)) {
    if ($Preflight) { throw 'CURSEFORGE_API_TOKEN is required for preflight.' }
    throw 'CURSEFORGE_API_TOKEN is required.'
}
if (-not $pack.curseForgeProjectId -or $pack.curseForgeProjectId -eq 0) {
    throw 'CurseForge project ID is required.'
}
$authorHeaders = @{ 'X-Api-Token' = $token }

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

    # This is the CurseForge author/upload API. Author tokens authenticate with
    # X-Api-Token; do not send them to the separate api.curseforge.com Core API.
    $gameVersionsEndpoint = "$authorApiBase/game/versions"
    try {
        $gameVersions = @(Invoke-RestMethod -Uri $gameVersionsEndpoint -Headers $authorHeaders)
        $availableNames = @($gameVersions | ForEach-Object { [string]$_.name })
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
        throw "PREFLIGHT: CurseForge author API reachability or game-version check failed: $($_.Exception.Message)"
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

# Duplicate recovery uses the separate CurseForge Core API only when its own
# x-api-key credential is configured. Normal uploads require only the author token.
$coreApiKey = [Environment]::GetEnvironmentVariable('CURSEFORGE_CORE_API_KEY')
$coreHeaders = $null
if (-not [string]::IsNullOrWhiteSpace($coreApiKey)) {
    $coreHeaders = @{ 'x-api-key' = $coreApiKey }
}
$filesEndpoint = "https://api.curseforge.com/v1/mods/$($pack.curseForgeProjectId)/files"

function Get-UploadErrorBody($ErrorRecord) {
    if ($ErrorRecord.ErrorDetails -and $ErrorRecord.ErrorDetails.Message) {
        return [string]$ErrorRecord.ErrorDetails.Message
    }
    return [string]$ErrorRecord.Exception.Message
}

function Get-ExistingFileId($DisplayName) {
    if ($null -eq $coreHeaders) { return $null }

    $pageSize = 50
    try {
        for ($index = 0; $index -lt 2500; $index += $pageSize) {
            $page = Invoke-RestMethod -Uri "$filesEndpoint`?index=$index&pageSize=$pageSize" -Headers $coreHeaders
            if (-not $page -or -not $page.data) { break }
            foreach ($file in @($page.data)) {
                if ($file.displayName -eq $DisplayName -and $file.id) { return [string]$file.id }
            }
            if ($page.data.Count -lt $pageSize) { break }
        }
    }
    catch {
        throw "CurseForge duplicate lookup failed with CURSEFORGE_CORE_API_KEY: $($_.Exception.Message)"
    }
    return $null
}

function Publish-File($Metadata, $Archive) {
    try {
        $response = Invoke-RestMethod -Uri $uploadEndpoint -Method Post -Headers $authorHeaders -Form @{
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
            if ($null -eq $coreHeaders) {
                Write-Warning 'CurseForge reported a duplicate. Configure CURSEFORGE_CORE_API_KEY to enable idempotent duplicate lookup.'
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
