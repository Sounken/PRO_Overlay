# PRO Helper - Guide d'Installation

## Pour les Utilisateurs Finaux

### ✅ Installation Simple

1. **Téléchargez** `PROHelper Setup 1.0.0.exe` depuis les releases
2. **Double-cliquez** sur le fichier pour lancer l'installation
3. Suivez les instructions à l'écran
4. L'application sera installée dans `Program Files`
5. Lancez **PRO Helper** depuis le menu Démarrer

**Configuration requise**: Windows 7 ou plus récent, 200 MB d'espace disque

---

## Pour les Développeurs

### 📋 Prérequis

Assurez-vous d'avoir installé:

- **Node.js** 18 ou plus: https://nodejs.org/
- **Python** 3.10 ou plus: https://www.python.org/
- **Git** (optionnel): https://git-scm.com/

### 🔨 Construire l'Exécutable

**Méthode 1 : Script Automatique (Recommandé)**

```bash
# Double-cliquez sur build.bat
# Ou en ligne de commande:
build.bat
```

Le script va automatiquement:
1. Construire le backend Python en exe
2. Installer les dépendances du frontend
3. Compiler React et Electron
4. Créer l'installateur Windows

**Durée**: 5-10 minutes (selon votre connexion internet)

**Résultat**:
- `frontend/release/PROHelper Setup 1.0.0.exe` - Installateur
- `frontend/release/PROHelper 1.0.0.exe` - Version portable

---

**Méthode 2 : Construction Manuelle**

#### Étape 1: Backend

```bash
cd backend

# Créer l'environnement virtuel (Windows)
py -m venv venv
venv\Scripts\activate.bat

# Installer les dépendances
pip install -r requirements.txt

# Construire l'exécutable
pyinstaller build.spec
```

Le fichier `backend.exe` sera dans `backend/dist/`

#### Étape 2: Frontend

```bash
cd frontend

# Installer les dépendances Node
npm install

# Compiler TypeScript
npm run build:electron

# Construire l'app React
npm run build

# Créer l'installateur
npm run package
```

Les fichiers seront dans `frontend/release/`

---

## 🚀 Développement

### Lancer en Mode Développement

```bash
# Depuis le dossier frontend:
npm run electron:dev
```

Cela va:
1. Démarrer le serveur de développement React
2. Lancer Electron avec rechargement automatique
3. Ouvrir les DevTools

### Structure du Projet

```
PRO-Overlay/
├── backend/
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── requirements.txt        # Dépendances Python
│   ├── build.spec             # Configuration PyInstaller
│   ├── routes/                # Endpoints API
│   ├── services/              # Logique métier (OCR, PokeAPI)
│   ├── models/                # Schémas Pydantic
│   └── dist/                  # Fichiers compilés
│
├── frontend/
│   ├── electron/              # Processus principal Electron
│   │   ├── main.ts           # Création fenêtres, IPC
│   │   └── preload.ts        # Bridge IPC
│   ├── src/                   # Application React
│   │   ├── components/       # Composants
│   │   ├── services/         # Services API
│   │   └── styles/           # Tailwind CSS
│   ├── package.json           # Config Node + electron-builder
│   ├── tsconfig.json          # Config TypeScript
│   └── vite.config.ts         # Config Vite
│
├── config.json               # Configuration de l'app
├── build.bat                 # Script de build Windows
└── README.md                 # Documentation
```

---

## ⚙️ Configuration Post-Build

Après l'installation, configurez l'app:

1. **OCR Detection Zone** (Obligatoire)
   - Allez dans **Settings**
   - Cliquez sur **Set OCR Zone**
   - Dessinez une zone autour du nom du Pokémon adverse

2. **Équipe** (Recommandé)
   - Allez dans l'onglet **Team**
   - Ajoutez vos 6 Pokémon
   - Vous pouvez aussi utiliser **Detect Team via OCR**

3. **Auto Battle Mode** (Optionnel)
   - Dans **Settings**, activez/désactivez le mode automatique

---

## 🔧 Dépannage

### Build échoue: "Python not found"
```bash
# Vérifiez que Python est installé:
py --version

# Si ça ne marche pas, ajoutez Python au PATH Windows
```

### Build échoue: "Node not found"
```bash
# Vérifiez que Node.js est installé:
node --version

# Redémarrez votre terminal après installation
```

### PyInstaller erreur: "module not found"
```bash
# Mettez à jour pip et réinstallez les dépendances:
pip install --upgrade pip
pip install -r requirements.txt
```

### Electron Builder échoue
```bash
# Nettoyez les fichiers de cache:
cd frontend
rm -rf dist
rm -rf dist-electron
rm -rf release
npm cache clean --force
npm install
npm run package
```

---

## 📦 Distribution

Une fois compilé, vous pouvez distribuer:

1. **PROHelper Setup 1.0.0.exe** - Installateur (recommandé pour utilisateurs finaux)
2. **PROHelper 1.0.0.exe** - Version portable (aucune installation requise)

Les deux incluent le backend compilé (`backend.exe`) embarqué.

---

## 🔐 Notes de Sécurité

- Les exécutables construits avec PyInstaller et Electron sont des binaires signés
- Aucune dépendance externe n'est requise après installation
- Tesseract OCR est téléchargé automatiquement à la première utilisation
- Les données Pokemon sont cachées localement

---

## ❓ FAQ Développement

**Q: Comment activer Tesseract pour le dev?**
```bash
# Installez Tesseract depuis:
# https://github.com/UB-Mannheim/tesseract/wiki

# Ou via Chocolatey:
choco install tesseract
```

**Q: Comment tester le backend seul?**
```bash
cd backend
# Mode dev avec rechargement automatique:
pip install watchdog
python -m watchdog.auto_reload main.py

# Accédez à: http://localhost:8000/docs
```

**Q: Comment déboguer Electron?**
```bash
npm run electron:dev
# Les DevTools s'ouvrent automatiquement (F12)
```

---

**Version**: 1.0.0 | **Mise à jour**: Février 2025
