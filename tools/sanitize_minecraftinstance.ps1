[CmdletBinding()]
param(
    [string]$Path
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if ([string]::IsNullOrWhiteSpace($Path)) {
    $Path = Join-Path (Split-Path -Parent $PSScriptRoot) 'minecraftinstance.json'
}
$source = Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json

$addons = @($source.installedAddons | ForEach-Object {
    $addon = $_
    [ordered]@{
        addonID = [long]$addon.addonID
        name = [string]$addon.name
        primaryAuthor = [string]$addon.primaryAuthor
        webSiteURL = [string]$addon.webSiteURL
        isEnabled = if ($null -eq $addon.isEnabled) { $true } else { [bool]$addon.isEnabled }
        installedFile = [ordered]@{
            id = [long]$addon.installedFile.id
            fileName = [string]$addon.installedFile.fileName
            downloadUrl = [string]$addon.installedFile.downloadUrl
            hashes = @($addon.installedFile.hashes | ForEach-Object {
                [ordered]@{ type = [int]$_.type; value = [string]$_.value }
            })
        }
    }
})

$sanitized = [ordered]@{
    name = [string]$source.name
    gameVersion = [string]$source.gameVersion
    baseModLoader = [ordered]@{
        name = [string]$source.baseModLoader.name
        forgeVersion = [string]$source.baseModLoader.forgeVersion
        type = [int]$source.baseModLoader.type
    }
    installedAddons = $addons
}

$json = $sanitized | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText(
    [System.IO.Path]::GetFullPath($Path), $json + "`n", [System.Text.UTF8Encoding]::new($false)
)
Write-Host "Sanitized $($addons.Count) CurseForge projects in $Path"
