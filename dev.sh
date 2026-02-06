#!/bin/bash

# Script de lancement rapide pour le développement

echo "========================================"
echo "PRO Helper - Development Launcher"
echo "========================================"
echo ""

show_menu() {
    echo "Que voulez-vous lancer ?"
    echo ""
    echo "[1] Backend seul (Python FastAPI)"
    echo "[2] Frontend seul (React dev server)"
    echo "[3] Application complète (Electron)"
    echo "[4] Installer les dépendances"
    echo "[5] Quitter"
    echo ""
}

backend() {
    echo ""
    echo "[*] Lancement du backend..."
    cd backend
    python3 main.py
}

frontend() {
    echo ""
    echo "[*] Lancement du frontend..."
    cd frontend
    npm run dev
}

electron() {
    echo ""
    echo "[*] Lancement de l'application Electron..."
    cd frontend
    npm run electron:dev
}

install() {
    echo ""
    echo "[*] Installation des dépendances..."
    echo ""
    echo "[Backend] Installation des packages Python..."
    cd backend
    pip3 install -r requirements.txt
    cd ..
    echo ""
    echo "[Frontend] Installation des packages Node..."
    cd frontend
    npm install
    cd ..
    echo ""
    echo "[+] Installation terminée !"
}

while true; do
    show_menu
    read -p "Votre choix (1-5): " choice

    case $choice in
        1) backend ;;
        2) frontend ;;
        3) electron ;;
        4) install ;;
        5) echo ""; echo "Au revoir !"; exit 0 ;;
        *) echo "Choix invalide" ;;
    esac

    echo ""
    read -p "Appuyez sur Entrée pour continuer..."
    clear
done
