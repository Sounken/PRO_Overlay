@echo off
REM PRO Helper - Launcher with Process Cleanup

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

REM Launch the application from PROHelper folder
echo Launching PRO Helper...
if not exist "PROHelper\PROHelper.exe" (
    echo ERROR: PROHelper\PROHelper.exe not found!
    echo Current directory: %cd%
    pause
    exit /b 1
)

cd /d "PROHelper"
start "" "PROHelper.exe"
cd /d ..

REM Wait for app to close
timeout /t 2 /nobreak >nul

REM Monitor and wait for PROHelper to close
:WAIT_FOR_APP
tasklist /FI "IMAGENAME eq PROHelper.exe" 2>nul | find /I /N "PROHelper.exe" >nul
if "%ERRORLEVEL%"=="0" (
    timeout /t 1 /nobreak >nul
    goto WAIT_FOR_APP
)

REM Kill remaining processes
echo.
echo Cleaning up processes...
taskkill /F /IM backend.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM python3.exe /T 2>nul
taskkill /F /IM electron.exe /T 2>nul

echo Done!
