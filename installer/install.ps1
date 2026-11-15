# AetherTune Installer
$ErrorActionPreference = "Stop"
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs -WindowStyle Hidden
    exit
}
$installDir = Join-Path $env:ProgramFiles "AetherTune"
New-Item -ItemType Directory -Path $installDir -Force | Out-Null
Copy-Item (Join-Path $PSScriptRoot "AetherTune.exe") (Join-Path $installDir "AetherTune.exe") -Force

# Start Menu shortcut
$sm = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs"
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut((Join-Path $sm "AetherTune.lnk"))
$sc.TargetPath = Join-Path $installDir "AetherTune.exe"
$sc.WorkingDirectory = $installDir
$sc.IconLocation = (Join-Path $installDir "AetherTune.exe") + ",0"
$sc.Save()

# Desktop shortcut
$desk = [Environment]::GetFolderPath("Desktop")
$sc2 = $ws.CreateShortcut((Join-Path $desk "AetherTune.lnk"))
$sc2.TargetPath = Join-Path $installDir "AetherTune.exe"
$sc2.WorkingDirectory = $installDir
$sc2.Save()

# Uninstall registry entry
$reg = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\AetherTune"
New-Item -Path $reg -Force | Out-Null
Set-ItemProperty $reg "DisplayName" "AetherTune"
Set-ItemProperty $reg "UninstallString" "powershell -NoProfile -ExecutionPolicy Bypass -File `"$installDir\uninstall.ps1`""
Set-ItemProperty $reg "InstallLocation" $installDir
Set-ItemProperty $reg "Publisher" "AetherTune"
Set-ItemProperty $reg "DisplayVersion" "0.1.0"

# copy uninstaller
Copy-Item (Join-Path $PSScriptRoot "uninstall.ps1") (Join-Path $installDir "uninstall.ps1") -Force

Write-Host "AetherTune installed to $installDir"
Write-Host "Launching..."
Start-Process (Join-Path $installDir "AetherTune.exe")
