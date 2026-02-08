@echo off
REM PRO Helper - Smart Launcher with Automatic Process Cleanup
REM This wrapper ensures all processes are killed when app closes

setlocal enabledelayedexpansion

echo PRO Helper Launcher
echo ====================
echo.

REM Kill any existing processes first
echo Cleaning up old processes...
taskkill /F /IM backend.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM python3.exe /T 2>nul
taskkill /F /IM electron.exe /T 2>nul
timeout /t 1 /nobreak >nul

REM Launch the application
echo Launching PRO Helper...
cd /d "%~dp0PROHelper"
set APP_PATH=%cd%\PROHelper.exe
if not exist "%APP_PATH%" (
    echo ERROR: PROHelper.exe not found!
    echo Expected: %APP_PATH%
    pause
    exit /b 1
)

REM Start app and get its PID
start "" "%APP_PATH%"
timeout /t 3 /nobreak >nul

REM Wait for PROHelper to close by polling
:WAIT_FOR_APP
tasklist /FI "IMAGENAME eq PROHelper.exe" 2>nul | find /I /N "PROHelper.exe" >nul
if "%ERRORLEVEL%"=="0" (
    timeout /t 1 /nobreak >nul
    goto WAIT_FOR_APP
)

REM App has closed - kill remaining processes
echo.
echo Cleaning up processes...
taskkill /F /IM backend.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM python3.exe /T 2>nul
taskkill /F /IM electron.exe /T 2>nul

echo Done!
exit /b 0
