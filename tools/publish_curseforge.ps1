[CmdletBinding()]
param(
    [string]$Version,
    [ValidateSet('alpha', 'beta', 'release')] [string]$ReleaseType,
    [string]$ChangelogFile,
    [ValidateSet('all', 'client', 'server')] [string]$Mode = 'all',
    [string]$ParentFileId,
    [string]$StateFile,
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
if ([string]::IsNullOrWhiteSpace($StateFile)) {
    $StateFile = Join-Path $repoRoot "dist/curseforge-$Version-state.json"
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
    if ($Mode -in @('all', 'client')) {
        Write-Host "DRY RUN: would upload $clientArchive"
        Write-Host ($mainMetadata | ConvertTo-Json -Depth 5)
        Write-Host "DRY RUN: would persist the returned client file ID to $StateFile"
    }
    if ($Mode -in @('all', 'server')) {
        Write-Host "DRY RUN: would attach $serverArchive as the server child file"
    }
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
    foreach ($archive in @($clientArchive, $serverArchive)) {
        if (-not (Test-Path -LiteralPath $archive -PathType Leaf)) {
            throw "Missing release archive: $archive"
        }
    }
    if (-not (Test-Path -LiteralPath $ChangelogFile -PathType Leaf)) {
        throw "Missing changelog: $ChangelogFile"
    }

    # This is the CurseForge author/upload API. Author tokens authenticate with
    # X-Api-Token; do not send them to the separate api.curseforge.com Core API.
    # /api/game/versions proves the token/API are reachable, but the response is
    # not used as an exhaustive allowlist for upload metadata names.
    $gameVersionsEndpoint = "$authorApiBase/game/versions"
    try {
        $gameVersions = @(Invoke-RestMethod -Uri $gameVersionsEndpoint -Headers $authorHeaders)
        if ($gameVersions.Count -eq 0) {
            throw 'CurseForge returned an empty game-version response.'
        }
        $requestedNames = @($mainMetadata.gameVersionNames) -join ', '
        Write-Host "PREFLIGHT: CurseForge author API authentication and reachability verified."
        Write-Host "PREFLIGHT: upload endpoint will validate game version names: $requestedNames"
    }
    catch {
        throw "PREFLIGHT: CurseForge author API reachability or authentication check failed: $($_.Exception.Message)"
    }
    Write-Host "PREFLIGHT: All checks passed."
    exit 0
}

if (-not $SkipBuild) { & (Join-Path $PSScriptRoot 'build_modpack.ps1') -Version $Version }
$requiredArchives = @()
if ($Mode -in @('all', 'client')) { $requiredArchives += $clientArchive }
if ($Mode -in @('all', 'server')) { $requiredArchives += $serverArchive }
foreach ($archive in $requiredArchives) {
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
        $pythonCommand = Get-Command python -CommandType Application -ErrorAction SilentlyContinue
        if ($null -eq $pythonCommand) {
            $pythonCommand = Get-Command python3 -CommandType Application -ErrorAction SilentlyContinue
        }
        if ($null -eq $pythonCommand) {
            throw 'Python is required for CurseForge uploads.'
        }

        $pythonPath = [string]$pythonCommand.Source
        $helperPath = Join-Path $PSScriptRoot 'curseforge_upload.py'
        $metadataJson = $Metadata | ConvertTo-Json -Compress -Depth 5
        $helperOutput = @(& $pythonPath $helperPath '--url' $uploadEndpoint '--metadata' $metadataJson '--file' $Archive)
        $helperExit = $LASTEXITCODE
        $helperJson = ($helperOutput -join "`n").Trim()
        if ([string]::IsNullOrWhiteSpace($helperJson)) {
            throw "CurseForge upload helper returned no output (exit $helperExit)."
        }
        if ($helperExit -ne 0) {
            throw "CurseForge upload helper failed: $helperJson"
        }

        $response = $helperJson | ConvertFrom-Json
        if (-not $response.ok -or -not $response.id) {
            throw "CurseForge upload helper returned an invalid success response: $helperJson"
        }
        return [string]$response.id
    }
    catch {
        $body = Get-UploadErrorBody $_

        # Recover idempotently on retries or on a lost HTTP response. Versioned
        # display names are unique within this release pipeline.
        $existing = Get-ExistingFileId $Metadata.displayName
        if ($existing) {
            Write-Host "Reusing existing CurseForge file $existing for $($Metadata.displayName)."
            return $existing
        }

        if ($body -match 'already|duplicate' -and $null -eq $coreHeaders) {
            Write-Warning 'CurseForge reported a duplicate. A saved publish-state file can recover the client ID for server retries; CURSEFORGE_CORE_API_KEY is still recommended for duplicate recovery across separate workflow runs.'
        }
        throw "CurseForge upload failed for ${Archive}: $body"
    }
}

function Save-ClientPublishState($ClientFileId) {
    $stateDirectory = Split-Path -Parent $StateFile
    if (-not [string]::IsNullOrWhiteSpace($stateDirectory)) {
        $null = New-Item -ItemType Directory -Path $stateDirectory -Force
    }
    $state = [ordered]@{
        version = $Version
        curseForgeProjectId = [long]$pack.curseForgeProjectId
        clientDisplayName = [string]$mainMetadata.displayName
        clientFileId = [long]$ClientFileId
        clientArchiveSha256 = (Get-FileHash -LiteralPath $clientArchive -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    $state | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $StateFile -Encoding utf8
    Write-Host "Saved CurseForge client publish state to $StateFile."
}

function Get-SavedClientFileId {
    if (-not (Test-Path -LiteralPath $StateFile -PathType Leaf)) { return $null }

    $state = Get-Content -LiteralPath $StateFile -Raw -Encoding utf8 | ConvertFrom-Json
    if ([string]$state.version -ne $Version) {
        throw "CurseForge state file version '$($state.version)' does not match requested version '$Version'."
    }
    if ([long]$state.curseForgeProjectId -ne [long]$pack.curseForgeProjectId) {
        throw "CurseForge state file project ID '$($state.curseForgeProjectId)' does not match '$($pack.curseForgeProjectId)'."
    }
    if (-not $state.clientFileId) {
        throw "CurseForge state file has no clientFileId: $StateFile"
    }
    if ($state.clientArchiveSha256 -and (Test-Path -LiteralPath $clientArchive -PathType Leaf)) {
        $currentHash = (Get-FileHash -LiteralPath $clientArchive -Algorithm SHA256).Hash.ToLowerInvariant()
        if ([string]$state.clientArchiveSha256 -ne $currentHash) {
            throw "CurseForge state file client archive hash does not match $clientArchive."
        }
    }
    return [string]$state.clientFileId
}

function Resolve-ClientFileId {
    if (-not [string]::IsNullOrWhiteSpace($ParentFileId)) {
        return $ParentFileId
    }

    $saved = Get-SavedClientFileId
    if ($saved) {
        Write-Host "Reusing saved CurseForge client file $saved from $StateFile."
        return $saved
    }

    $existing = Get-ExistingFileId $mainMetadata.displayName
    if ($existing) {
        Write-Host "Recovered existing CurseForge client file $existing through the Core API."
        return $existing
    }

    throw "Server publication needs a client file ID. Provide -ParentFileId, restore the saved state file '$StateFile', or configure CURSEFORGE_CORE_API_KEY for cross-run recovery."
}

$clientFileId = $null
if ($Mode -in @('all', 'client')) {
    $clientFileId = Publish-File $mainMetadata $clientArchive
    Save-ClientPublishState $clientFileId
    Write-Host "Client file $clientFileId is present on CurseForge."
}

if ($Mode -in @('all', 'server')) {
    if ([string]::IsNullOrWhiteSpace([string]$clientFileId)) {
        $clientFileId = Resolve-ClientFileId
    }
    $serverMetadata = [ordered]@{
        changelog = $changelog
        changelogType = 'markdown'
        displayName = "$($pack.name) $Version Server Pack"
        parentFileID = [long]$clientFileId
        releaseType = $ReleaseType
    }
    $serverFileId = Publish-File $serverMetadata $serverArchive
    Write-Host "Server child file $serverFileId is attached to CurseForge client file $clientFileId."
}
