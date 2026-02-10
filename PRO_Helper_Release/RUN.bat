@echo off
REM PRO Helper - Pokémon Revolution Online Helper
REM Lance l'application PROHelper avec vérifications de prérequis

setlocal enabledelayedexpansion

REM Change to script directory to ensure relative paths work
cd /d "%~dp0"

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

REM Lancer l'application depuis le répertoire courant
REM Utiliser /min pour éviter la console, /wait pour attendre le démarrage
set APP_PATH=%CD%\PROHelper.exe
echo Chemin: %APP_PATH%
echo.

REM Lancer l'exe et attendre qu'il démarre
start "" /B "%APP_PATH%"

REM Attendre plus longtemps pour que Electron démarre et se charge
echo Attente du démarrage de l'application...
timeout /t 5 /nobreak

echo.
echo =========================================================
echo  Informations:
echo =========================================================
echo.
echo Contrôles:
echo  - F9:   Basculer l'overlay en jeu
echo  - F12:  Ouvrir la console (debug)
echo  - ESC:  Quitter l'application
echo.
echo À la première utilisation:
echo  - Les modèles AI vont être téléchargés (~1-2 minutes)
echo  - L'application va créer la cache locale
echo.
echo Pour plus d'aide, lisez README.md
echo.
echo =========================================================
echo.
echo Si l'application ne démarre pas:
echo  1. Vérifiez l'espace disque (500 MB minimum requis)
echo  2. Lancez INSTALL_PREREQUISITES.bat
echo  3. Redémarrez votre ordinateur
echo.
echo =========================================================
