# Démarrage Rapide - PRO Helper

Guide pour tester rapidement l'application en mode développement.

## ⚡ Installation Express (Windows)

### 1. Prérequis

Installer les outils nécessaires :

```powershell
# Chocolatey (gestionnaire de paquets Windows)
# Exécuter PowerShell en admin et copier :
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Python
choco install python -y

# Node.js
choco install nodejs -y

# Tesseract OCR
choco install tesseract -y

# Redémarrer le terminal après installation
```

### 2. Installer les dépendances du projet

Ouvrir un terminal à la racine du projet et exécuter :

```bash
# Utiliser le script automatique
dev.bat
# Puis choisir l'option [4] Installer les dépendances
```

Ou manuellement :

```bash
# Backend
cd backend
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
npm install
cd ..
```

### 3. Tester l'application

#### Option A : Application Electron complète (Recommandé)

```bash
cd frontend
npm run electron:dev
```

Cela démarre automatiquement :
- Le backend FastAPI sur `http://localhost:8000`
- L'interface Electron avec Dashboard et Overlay

**Hotkey** : Appuyer sur `F9` pour afficher/masquer l'overlay

#### Option B : Tester séparément

**Terminal 1 - Backend :**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend :**
```bash
cd frontend
npm run dev
```

Puis ouvrir [http://localhost:3000](http://localhost:3000) dans un navigateur.

## 🧪 Test rapide des fonctionnalités

### 1. Tester le Pokédex

Dans le Dashboard :
1. Chercher "pikachu" dans la barre de recherche
2. Cliquer sur "Rechercher"
3. Vérifier que les informations s'affichent :
   - Sprite du Pokémon
   - Types (Electric)
   - Stats avec barres de progression
   - Tableau d'efficacité des types

### 2. Tester l'Overlay

1. Appuyer sur `F9` pour afficher l'overlay
2. L'overlay est transparent et reste au-dessus des autres fenêtres
3. Appuyer à nouveau sur `F9` pour masquer

**Note** : En mode dev, l'OCR ne détectera rien car il n'y a pas de jeu lancé. La détection automatique affichera "Aucun Pokémon détecté".

### 3. Tester l'API Backend

Ouvrir [http://localhost:8000/docs](http://localhost:8000/docs) pour voir la documentation Swagger interactive.

Endpoints à tester :
- `GET /pokemon/gengar` - Récupère les infos de Gengar
- `GET /health` - Vérifie que le backend fonctionne
- `GET /cache/stats` - Stats du cache

## 🔍 Vérifications

### Backend fonctionne ?
```bash
curl http://localhost:8000/health
# Devrait retourner : {"status":"ok"}
```

### Frontend fonctionne ?
```bash
curl http://localhost:3000
# Devrait retourner du HTML
```

### Tesseract installé ?
```bash
tesseract --version
# Devrait afficher la version
```

## 🐛 Problèmes courants

### Port déjà utilisé

**Backend (8000)** :
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Frontend (3000)** :
```bash
# Modifier le port dans frontend/vite.config.ts
server: {
  port: 3001,  // Nouveau port
}
```

### Module Python manquant

```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### npm install échoue

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Tesseract non trouvé

Ajouter manuellement au PATH :
```powershell
# Windows - Ajouter à la variable d'environnement PATH :
C:\Program Files\Tesseract-OCR
```

## 📚 Prochaines étapes

Une fois le test réussi :

1. Lire [README.md](README.md) pour comprendre l'architecture
2. Lire [CONTRIBUTING.md](CONTRIBUTING.md) pour contribuer
3. Lire [BUILD.md](BUILD.md) pour compiler en .exe

## 🎮 Test avec Pokemon Revolution Online

Pour tester l'OCR en conditions réelles :

1. Lancer Pokemon Revolution Online
2. Lancer PRO Helper
3. Entrer en combat
4. L'overlay devrait détecter automatiquement le Pokémon adverse
5. Les faiblesses/résistances s'affichent en temps réel

**Note** : La région de détection OCR est configurable dans `config.json`

## 💬 Support

- Issues GitHub : [Lien vers les issues]
- Discord : [Lien à venir]
- Documentation : [README.md](README.md)

Bon test ! 🎮✨
