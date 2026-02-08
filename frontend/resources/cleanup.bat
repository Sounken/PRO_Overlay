@echo off
REM Kill all backend processes when app closes
REM This is called by Electron main.ts on shutdown

taskkill /F /IM backend.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM python3.exe /T 2>nul

exit /b 0
