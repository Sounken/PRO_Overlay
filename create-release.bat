@echo off
REM Script pour créer une release portable

echo.
echo ========================================
echo   Creating PRO Helper Release Package
echo ========================================
echo.

REM Vérifier que la build existe
if not exist "frontend\release\win-unpacked\PROHelper.exe" (
    echo ERROR: Build not found. Run build.bat first.
    pause
    exit /b 1
)

REM Créer le dossier de release
if exist "release-package" rmdir /s /q "release-package"
mkdir "release-package"

REM Copier l'application
xcopy /E /I /Y "frontend\release\win-unpacked" "release-package\PROHelper"

REM Créer les fichiers README
echo Creating documentation files...
copy "README.md" "release-package\README.md"
copy "QUICK_START.md" "release-package\QUICK_START.md"

REM Créer le launcher
echo Creating launcher...
(
    @echo @echo off
    @echo cd /d "%%~dp0PROHelper"
    @echo start PROHelper.exe
) > "release-package\RUN.bat"

echo.
echo ========================================
echo   Release Package Created!
echo ========================================
echo.
echo Location: release-package\
echo.
echo Next steps:
echo 1. Test by running: release-package\RUN.bat
echo 2. Zip the folder: PROHelper-1.0.0-win.zip
echo 3. Upload to GitHub Releases
echo.

pause
