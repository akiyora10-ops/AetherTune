@echo off
powershell -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "%~dp0install.ps1"
if %errorlevel% neq 0 (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
)
pause