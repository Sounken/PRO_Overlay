@echo off
REM Script de lancement rapide pour le développement

echo ========================================
echo PRO Helper - Development Launcher
echo ========================================
echo.

:menu
echo Que voulez-vous lancer ?
echo.
echo [1] Backend seul (Python FastAPI)
echo [2] Frontend seul (React dev server)
echo [3] Application complete (Electron)
echo [4] Installer les dependances
echo [5] Quitter
echo.

set /p choice="Votre choix (1-5): "

if "%choice%"=="1" goto backend
if "%choice%"=="2" goto frontend
if "%choice%"=="3" goto electron
if "%choice%"=="4" goto install
if "%choice%"=="5" goto end
goto menu

:backend
echo.
echo [*] Lancement du backend...
cd backend
python main.py
pause
goto menu

:frontend
echo.
echo [*] Lancement du frontend...
cd frontend
npm run dev
pause
goto menu

:electron
echo.
echo [*] Lancement de l'application Electron...
cd frontend
npm run electron:dev
pause
goto menu

:install
echo.
echo [*] Installation des dependances...
echo.
echo [Backend] Installation des packages Python...
cd backend
pip install -r requirements.txt
cd ..
echo.
echo [Frontend] Installation des packages Node...
cd frontend
npm install
cd ..
echo.
echo [+] Installation terminee !
pause
goto menu

:end
echo.
echo Au revoir !
exit
