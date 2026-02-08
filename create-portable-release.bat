@echo off
REM Simple script to create a portable release from existing build

echo.
echo ========================================
echo   Creating Portable Release Package
echo ========================================
echo.

REM Check if build exists
if not exist "PROHelper\PROHelper.exe" (
    echo ERROR: Application not found!
    echo Please run build.bat first
    pause
    exit /b 1
)

REM Create release package
echo Creating release package...
if exist "release-package" rmdir /s /q "release-package"
mkdir "release-package"

REM Copy application
echo Copying application files...
xcopy /E /I /Y "PROHelper" "release-package\PROHelper" >nul 2>&1

REM Copy documentation
copy "README.md" "release-package\" >nul 2>&1
copy "QUICK_START.md" "release-package\" >nul 2>&1
copy "INSTALL.md" "release-package\" >nul 2>&1

REM Create launcher script
echo Creating launcher...
(
    @echo @echo off
    @echo REM PRO Helper Launcher
    @echo cd /d "%%~dp0PROHelper"
    @echo start PROHelper.exe
) > "release-package\RUN.bat"

REM Create version file
(
    @echo Version: 1.0.0
    @echo Date: %date%
    @echo Usage: Double-click RUN.bat to launch
) > "release-package\VERSION.txt"

echo.
echo ========================================
echo   ✓ Release Package Created!
echo ========================================
echo.
echo Location: release-package\
echo.
echo Files:
echo   - RUN.bat           ^(Launcher^)
echo   - PROHelper\        ^(Application^)
echo   - README.md         ^(Documentation^)
echo   - QUICK_START.md    ^(User Guide^)
echo   - INSTALL.md        ^(Installation Guide^)
echo.
echo Next steps:
echo   1. Test: release-package\RUN.bat
echo   2. Right-click release-package folder ^> Send to ^> Compressed folder
echo   3. Rename to: PROHelper-1.0.0-portable.zip
echo   4. Upload to GitHub Releases
echo.
echo Done!
pause
