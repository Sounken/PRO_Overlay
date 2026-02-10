@echo off
REM PRO Helper - Pokémon Revolution Online Helper
REM Lance l'application PROHelper avec vérifications de prérequis

setlocal enabledelayedexpansion

echo.
echo =========================================================
echo  PRO Helper - Pokémon Helper Tool
echo =========================================================
echo.

REM Vérifier que les fichiers essentiels existent
echo Vérification des fichiers...
echo.

if not exist "PROHelper.exe" (
    echo [ERREUR] PROHelper.exe non trouvé!
    echo.
    echo Assurez-vous que:
    echo  1. Vous êtes dans le bon dossier
    echo  2. Les fichiers n'ont pas été supprimés
    echo  3. L'extraction est complète
    echo.
    pause
    exit /b 1
)
echo ✓ PROHelper.exe trouvé (169 MB)

if not exist "backend\backend.exe" (
    echo [ERREUR] backend/backend.exe non trouvé!
    echo.
    echo Assurez-vous que:
    echo  1. Le dossier backend/ existe
    echo  2. Le fichier backend.exe est présent (246 MB)
    echo.
    pause
    exit /b 1
)
echo ✓ backend/backend.exe trouvé (246 MB)

if not exist "ffmpeg.dll" (
    echo [ERREUR] ffmpeg.dll manquant!
    echo.
    echo La mise à jour n'est pas complète.
    echo Veuillez télécharger le package complet.
    echo.
    pause
    exit /b 1
)
echo ✓ ffmpeg.dll trouvé (2.8 MB)

if not exist "config.json" (
    echo [ERREUR] config.json non trouvé!
    echo.
    pause
    exit /b 1
)
echo ✓ config.json trouvé
echo.

REM Vérifier Visual C++ Redistributable
echo Vérification des prérequis système...
echo.

reg query "HKLM\Software\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" >nul 2>&1
if %errorLevel% neq 0 (
    echo [ATTENTION] Visual C++ Redistributable manquant!
    echo.
    echo L'application a besoin de Visual C++ 2019 pour fonctionner.
    echo.
    echo Solutions:
    echo  1. Lancer INSTALL_PREREQUISITES.bat (recommandé)
    echo  2. Installer manuellement depuis:
    echo     https://support.microsoft.com/en-us/help/2977003
    echo.
    pause
    exit /b 1
)
echo ✓ Visual C++ Redistributable présent
echo.

REM Tous les checks sont passés
echo =========================================================
echo  Lancement de l'application...
echo =========================================================
echo.

REM Lancer l'application
start "" "PROHelper.exe"

REM Attendre un peu pour que l'app démarre
timeout /t 3 /nobreak

echo.
echo ✓ Application lancée avec succès!
echo.
echo Contrôles:
echo  - F9:   Basculer l'overlay en jeu
echo  - F12:  Ouvrir la console (debug)
echo  - ESC:  Quitter l'application
echo.
echo À la première utilisation:
echo  - Les modèles AI vont être téléchargés (~1-2 minutes)
echo  - Une zone de détection OCR sera configurée
echo.
echo Pour plus d'aide, lisez README.md
echo.
echo =========================================================
