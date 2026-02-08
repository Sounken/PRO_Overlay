@echo off
REM PRO Helper - Build Script
REM Builds the complete application including backend and frontend

echo.
echo ========================================
echo   PRO Helper - Application Builder
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where py >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Detected:
echo - Node.js:
node --version
echo - Python:
py --version
echo.

REM Build Backend
echo.
echo [1/3] Building Backend...
cd backend

REM Check if pyinstaller is available
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller >nul 2>nul
)

if not exist venv (
    echo Creating virtual environment...
    py -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install Python dependencies
    echo Make sure requirements.txt exists and is correct
    cd ..
    pause
    exit /b 1
)

echo Building executable...
if not exist dist (
    mkdir dist
)

echo Running PyInstaller...
pyinstaller build.spec
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PyInstaller build failed
    echo Check the output above for details
    cd ..
    pause
    exit /b 1
)

if not exist dist\backend.exe (
    echo ERROR: backend.exe was not created
    echo Possible causes:
    echo - build.spec file is missing or incorrect
    echo - PyInstaller failed silently
    echo - Missing dependencies
    cd ..
    pause
    exit /b 1
)

echo ✓ Backend built successfully: dist\backend.exe
cd ..

REM Build Frontend
echo.
echo [2/3] Building Frontend...
cd frontend

echo Installing Node dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm install failed
    echo Try: npm cache clean --force
    cd ..
    pause
    exit /b 1
)

echo Compiling TypeScript...
call npm run build:electron
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: TypeScript compilation failed
    echo Check above for error details
    cd ..
    pause
    exit /b 1
)

echo Building React app...
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: React build failed
    echo Check above for error details
    cd ..
    pause
    exit /b 1
)

REM Package with Electron Builder
echo.
echo [3/3] Packaging Application...
echo This may take 5-10 minutes...
echo.

call npm run package
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Electron Builder packaging failed
    echo Check above for error details
    cd ..
    pause
    exit /b 1
)

REM Check if build was successful
if exist "release\PROHelper Setup 1.0.0.exe" (
    echo.
    echo ========================================
    echo   ✓ BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Files created:
    echo ✓ frontend\release\PROHelper Setup 1.0.0.exe  (Installer)
    echo ✓ frontend\release\PROHelper 1.0.0.exe        (Portable)
    echo.
    echo Next steps:
    echo 1. Test the installer: PROHelper Setup 1.0.0.exe
    echo 2. Or test portable: PROHelper 1.0.0.exe
    echo.
    echo Happy testing!
    echo.
) else (
    echo.
    echo ERROR: Build completed but files not found!
    echo Check if release\ folder has any files.
    echo.
)

cd ..
pause
