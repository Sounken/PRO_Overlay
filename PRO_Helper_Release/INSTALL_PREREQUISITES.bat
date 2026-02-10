@echo off
REM =========================================================
REM PRO Helper - Installer les Prérequis
REM =========================================================
REM Ce script installe les dépendances système requises
REM =========================================================

setlocal enabledelayedexpansion

REM Change to script directory
cd /d "%~dp0"

echo.
echo =========================================================
echo  PRO Helper - Installation des Prérequis
echo =========================================================
echo.

REM Vérifier si on a les droits admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERREUR: Ce script requiert les droits administrateur!
    echo.
    echo Solution:
    echo 1. Clic-droit sur ce fichier
    echo 2. Sélectionnez "Exécuter en tant qu'administrateur"
    echo.
    pause
    exit /b 1
)

echo Vérification des prérequis système...
echo.

REM =========================================================
REM Vérifier Visual C++ Redistributable 2019
REM =========================================================
echo [1/2] Vérification de Visual C++ Redistributable...

reg query "HKLM\Software\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" >nul 2>&1
if %errorLevel% equ 0 (
    echo   ✓ Visual C++ 2019 détecté
) else (
    echo   ✗ Visual C++ 2019 manquant - Téléchargement...

    REM Télécharger et installer Visual C++ 2019
    echo   Veuillez accepter l'installation quand demandé...

    REM Utiliser PowerShell pour télécharger
    powershell -NoProfile -ExecutionPolicy Bypass -Command "^
        $url = 'https://aka.ms/vs/16/release/VC_redist.x64.exe'; ^
        $out = '%TEMP%\vc_redist.x64.exe'; ^
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; ^
        (New-Object System.Net.WebClient).DownloadFile($url, $out); ^
        Write-Host 'Téléchargement terminé'; ^
    " 2>nul

    if exist "%TEMP%\vc_redist.x64.exe" (
        echo   Installation de Visual C++ Redistributable...
        "%TEMP%\vc_redist.x64.exe" /quiet /norestart

        REM Attendre l'installation
        timeout /t 5 /nobreak

        if %errorLevel% equ 0 (
            echo   ✓ Visual C++ 2019 installé avec succès
        ) else (
            echo   ! Erreur lors de l'installation
        )

        REM Nettoyer
        del "%TEMP%\vc_redist.x64.exe" 2>nul
    ) else (
        echo.
        echo   ATTENTION: Impossible de télécharger automatiquement.
        echo.
        echo   Solution manuelle:
        echo   1. Visitez https://support.microsoft.com/en-us/help/2977003
        echo   2. Téléchargez "Visual C++ Redistributable for Visual Studio 2019"
        echo   3. Exécutez le fichier téléchargé
        echo.
    )
)

REM =========================================================
REM Vérifier .NET Framework (optionnel mais recommandé)
REM =========================================================
echo.
echo [2/2] Vérification de .NET Framework...

reg query "HKLM\Software\Microsoft\NET Framework Setup\NDP\v4\Full" /v Release >nul 2>&1
if %errorLevel% equ 0 (
    echo   ✓ .NET Framework détecté
) else (
    echo   * .NET Framework non détecté (optionnel)
    echo   * L'application peut fonctionner sans
)

REM =========================================================
REM Résumé
REM =========================================================
echo.
echo =========================================================
echo  Installation Terminée
echo =========================================================
echo.
echo Vous pouvez maintenant lancer le programme:
echo   1. Double-cliquez sur RUN.bat
echo   OU
echo   2. Exécutez PROHelper.exe directement
echo.
echo =========================================================
echo.

pause
