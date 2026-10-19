<#
.SYNOPSIS
Install ECS skills and repository adapters without overwriting conflicts.
.DESCRIPTION
Standalone installer for Windows PowerShell 5.1 and PowerShell 7.
Use -DryRun to preview changes. Python is not required.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('repo', 'user')]
    [string]$Scope,
    [string]$Repo,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$KitRoot = Split-Path -Parent $PSScriptRoot
$SkillSource = Join-Path $KitRoot '.agents/skills/engineering-clarity'
$AdapterFiles = @(
    'AGENTS.md', 'CLAUDE.md', 'GEMINI.md',
    '.github/copilot-instructions.md', '.github/PULL_REQUEST_TEMPLATE.md',
    '.github/ISSUE_TEMPLATE/user-story.md', '.azuredevops/pull_request_template.md'
)

function Get-FileDigest([string]$File) {
    $Hasher = [System.Security.Cryptography.SHA256]::Create()
    try { return [Convert]::ToBase64String($Hasher.ComputeHash([IO.File]::ReadAllBytes($File))) }
    finally { $Hasher.Dispose() }
}

function Test-SameFile([string]$Source, [string]$Destination) {
    if (-not (Test-Path -LiteralPath $Destination -PathType Leaf)) { return $false }
    return (Get-FileDigest $Source) -eq (Get-FileDigest $Destination)
}

function Get-SkillSnapshot([string]$Directory) {
    $Entries = @{}
    if (Test-Path -LiteralPath $Directory -PathType Container) {
        # Enumerate literal filesystem paths; brackets must not act as wildcards.
        $Directory = [IO.Path]::GetFullPath($Directory)
        foreach ($File in [IO.Directory]::GetFiles($Directory, '*', 'AllDirectories')) {
            $Relative = $File.Substring($Directory.Length).TrimStart([char[]]'\/')
            $Entries[$Relative] = (Get-FileDigest $File)
        }
    }
    return $Entries
}

function Copy-EcsSkill([string]$Destination) {
    if (Test-Path -LiteralPath $Destination) {
        $SourceEntries = Get-SkillSnapshot $SkillSource
        $DestinationEntries = Get-SkillSnapshot $Destination
        $Same = $SourceEntries.Count -eq $DestinationEntries.Count
        foreach ($Key in $SourceEntries.Keys) {
            if ($SourceEntries[$Key] -ne $DestinationEntries[$Key]) { $Same = $false }
        }
        if ($Same) { Write-Host "SAME: $Destination" }
        else { Write-Host "SKIP (existing skill differs; review and update manually): $Destination" }
        return
    }
    if ($DryRun) { Write-Host "WOULD INSTALL SKILL: $Destination"; return }
    New-Item -ItemType Directory -Path (Split-Path -Parent $Destination) -Force | Out-Null
    Copy-Item -LiteralPath $SkillSource -Destination $Destination -Recurse
    Write-Host "INSTALLED SKILL: $Destination"
}

function Copy-EcsFile([string]$Source, [string]$Destination) {
    if (Test-SameFile $Source $Destination) { Write-Host "SAME: $Destination"; return }
    if (Test-Path -LiteralPath $Destination) {
        Write-Host "SKIP (merge manually): $Destination"
        return
    }
    if ($DryRun) { Write-Host "WOULD INSTALL: $Destination"; return }
    New-Item -ItemType Directory -Path (Split-Path -Parent $Destination) -Force | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination
    Write-Host "INSTALLED: $Destination"
}

try {
    if ($Scope -eq 'repo') {
        if (-not $Repo) { throw '-Repo is required for -Scope repo' }
        if (-not (Test-Path -LiteralPath $Repo -PathType Container)) {
            throw "Repository directory does not exist: $Repo"
        }
        $Target = (Resolve-Path -LiteralPath $Repo).ProviderPath
    }
    else {
        if ($Repo) { throw '-Repo is only valid for -Scope repo' }
        $Target = if ($env:OS -eq 'Windows_NT') { $env:USERPROFILE } else { $env:HOME }
        if (-not $Target) { $Target = [Environment]::GetFolderPath('UserProfile') }
    }
    foreach ($Base in @('.agents/skills', '.claude/skills')) {
        Copy-EcsSkill (Join-Path $Target "$Base/engineering-clarity")
    }
    if ($Scope -eq 'repo') {
        foreach ($Relative in $AdapterFiles) {
            Copy-EcsFile (Join-Path $KitRoot $Relative) (Join-Path $Target $Relative)
        }
        Write-Host 'Review all SKIP entries; then commit approved changes for team and cloud-agent use.'
    }
    else {
        Write-Host 'Personal skills installed for supported local clients. Global always-on instruction files are not modified.'
    }
    Write-Host 'Done. Skill selection depends on the agent and task; review results.'
}
catch {
    Write-Error $_ -ErrorAction Continue
    exit 2
}
