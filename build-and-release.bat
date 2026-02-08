@echo off
REM Complete build and release script (without electron-builder issues)

echo.
echo ========================================
echo   PRO Helper - Build and Release
echo ========================================
echo.

REM Step 1: Build backend and frontend
echo [Step 1/4] Building backend...
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
pip install -r requirements.txt >nul 2>nul

echo Running PyInstaller...
pyinstaller build.spec
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend build failed
    cd ..
    pause
    exit /b 1
)

cd ..

REM Step 2: Build frontend
echo.
echo [Step 2/4] Building frontend...
cd frontend

echo Installing Node dependencies...
call npm install >nul 2>nul

echo Compiling TypeScript...
call npm run build:electron
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: TypeScript compilation failed
    cd ..
    pause
    exit /b 1
)

echo Building React app...
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: React build failed
    cd ..
    pause
    exit /b 1
)

REM Step 3: Update asar manually
echo.
echo [Step 3/4] Packaging application...

echo Extracting app.asar...
asar extract release\win-unpacked\resources\app.asar release\app-extracted >nul 2>nul

echo Updating compiled files...
copy /Y dist-electron\main.js release\app-extracted\dist-electron\main.js >nul
copy /Y dist-electron\preload.js release\app-extracted\dist-electron\preload.js >nul
rmdir /s /q release\app-extracted\dist
xcopy /E /I /Y dist release\app-extracted\dist >nul

echo Repacking app.asar...
del release\win-unpacked\resources\app.asar
asar pack release\app-extracted release\win-unpacked\resources\app.asar

cd ..

REM Step 4: Create portable release
echo.
echo [Step 4/4] Creating portable release package...

if exist "release-package" rmdir /s /q "release-package"
mkdir "release-package"

echo Copying application files...
xcopy /E /I /Y "frontend\release\win-unpacked" "release-package\PROHelper" >nul
copy "README.md" "release-package\" >nul
copy "QUICK_START.md" "release-package\" >nul
copy "INSTALL.md" "release-package\" >nul

REM Create launcher
(
    @echo @echo off
    @echo cd /d "%%~dp0PROHelper"
    @echo start PROHelper.exe
) > "release-package\RUN.bat"

echo.
echo ========================================
echo   ✓ Release Build Complete!
echo ========================================
echo.
echo Files created:
echo   - release-package\              (Ready to ZIP for release)
echo   - PROHelper\                    (Latest compiled version)
echo.
echo Next steps:
echo   1. Test: release-package\RUN.bat
echo   2. Zip: release-package as PROHelper-1.0.0-portable.zip
echo   3. Upload ZIP to GitHub Releases
echo.

pause
