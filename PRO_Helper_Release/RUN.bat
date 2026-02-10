@echo off
REM PRO Helper - Pokémon Revolution Online Helper
REM Lance l'application PROHelper

echo.
echo =====================================
echo  PRO Helper - Pokémon Helper Tool
echo =====================================
echo.
echo Lancement de l'application...
echo.

REM Vérifier que les fichiers essentiels existent
if not exist "PROHelper.exe" (
    echo ERREUR: PROHelper.exe non trouvé!
    echo Assurez-vous que vous êtes dans le dossier correct.
    pause
    exit /b 1
)

if not exist "backend\backend.exe" (
    echo ERREUR: backend/backend.exe non trouvé!
    echo Assurez-vous que vous êtes dans le dossier correct.
    pause
    exit /b 1
)

REM Lancer l'application
start "" "PROHelper.exe"

REM Attendre un peu pour que l'app démarre
timeout /t 2 /nobreak

REM Afficher les infos
echo.
echo ✓ Application lancée avec succès!
echo.
echo Commandes:
echo  - F9: Basculer l'overlay en jeu
echo  - ESC: Quitter l'application
echo  - F12: Ouvrir les outils de développement
echo.
echo Pour plus d'aide, consultez la documentation.
echo.
