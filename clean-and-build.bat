@echo off
REM Clean Python 3.14 references and rebuild

echo.
echo ========================================
echo   PRO Helper - Clean Build
echo ========================================
echo.

echo Cleaning old environment...
cd backend

REM Remove old venv
if exist venv (
    echo Removing old virtual environment...
    rmdir /s /q venv
    timeout /t 1 >nul
)

REM Remove build artifacts
if exist build (
    echo Removing old build files...
    rmdir /s /q build
    timeout /t 1 >nul
)

if exist dist (
    echo Removing old dist files...
    rmdir /s /q dist
    timeout /t 1 >nul
)

REM Remove __pycache__
if exist __pycache__ (
    echo Removing __pycache__...
    rmdir /s /q __pycache__
    timeout /t 1 >nul
)

echo.
echo Creating fresh virtual environment with Python 3.13...
py -3.13 -m venv venv

if not exist venv\Scripts\python.exe (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.13 is installed
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip >nul 2>nul
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Installing PyInstaller...
pip install pyinstaller

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo Building executable with PyInstaller...
if not exist dist mkdir dist
pyinstaller build.spec

if not exist dist\backend.exe (
    echo ERROR: Failed to build backend.exe
    pause
    exit /b 1
)

echo.
echo ✓ Backend built successfully!
echo.

cd ..

echo.
echo Building frontend...
cd frontend

echo Installing Node dependencies...
call npm install

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm install failed
    pause
    exit /b 1
)

echo Compiling TypeScript...
call npm run build:electron

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: TypeScript compilation failed
    pause
    exit /b 1
)

echo Building React app...
call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: React build failed
    pause
    exit /b 1
)

echo.
echo Creating installer (this may take several minutes)...
call npm run package

if exist "release\PROHelper Setup 1.0.0.exe" (
    echo.
    echo ========================================
    echo   ✓ BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Files created:
    echo ✓ PROHelper Setup 1.0.0.exe (Installer)
    echo ✓ PROHelper 1.0.0.exe (Portable)
    echo.
) else (
    echo.
    echo ERROR: Build failed!
    echo.
)

cd ..
pause