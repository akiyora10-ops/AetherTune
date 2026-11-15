$ErrorActionPreference = "SilentlyContinue"
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}
$installDir = Join-Path $env:ProgramFiles "AetherTune"
Remove-Item -Path (Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\AetherTune.lnk") -Force
Remove-Item -Path (Join-Path ([Environment]::GetFolderPath("Desktop")) "AetherTune.lnk") -Force
Remove-Item -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\AetherTune" -Recurse -Force
Remove-Item -Path $installDir -Recurse -Force
Write-Host "AetherTune uninstalled."
