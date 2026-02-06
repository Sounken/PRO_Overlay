# Guide de Build - PRO Helper

Ce guide explique comment compiler et packager l'application en un fichier exécutable unique.

## Prérequis

### Backend
- Python 3.10 ou supérieur
- Tesseract OCR installé

#### Installation Tesseract (Windows)
```powershell
# Option 1 : Chocolatey
choco install tesseract

# Option 2 : Téléchargement manuel
# https://github.com/UB-Mannheim/tesseract/wiki
```

Vérifier l'installation :
```bash
tesseract --version
```

### Frontend
- Node.js 18 ou supérieur
- npm ou yarn

Vérifier l'installation :
```bash
node --version
npm --version
```

## Installation des dépendances

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend
```bash
cd frontend
npm install
```

## Développement

### Démarrer le backend seul
```bash
cd backend
python main.py
```
Le backend sera accessible sur [http://localhost:8000](http://localhost:8000)

### Démarrer le frontend seul (mode web)
```bash
cd frontend
npm run dev
```
L'interface sera accessible sur [http://localhost:3000](http://localhost:3000)

### Démarrer l'application Electron complète (dev)
```bash
cd frontend
npm run electron:dev
```
Cela démarre automatiquement le backend ET le frontend dans Electron.

## Build Production

### Étape 1 : Compiler le backend

```bash
cd backend
pyinstaller build.spec
```

Cela génère `backend/dist/backend.exe` (~50-100 MB)

**Troubleshooting :**
- Si PyInstaller échoue, vérifiez que tous les modules sont installés
- Les warnings sont normaux, seules les erreurs sont bloquantes

### Étape 2 : Compiler et packager le frontend

```bash
cd frontend
npm run package
```

Cela :
1. Compile le code React en production
2. Package Electron avec le backend
3. Génère `frontend/release/PROHelper-Setup.exe` (~200 MB)

**Structure de sortie :**
```
frontend/release/
├── PROHelper-Setup.exe        # Installateur Windows
└── win-unpacked/              # Version portable
    └── PROHelper.exe
```

### Étape 3 : Tester l'executable

```bash
cd frontend/release/win-unpacked
./PROHelper.exe
```

L'application devrait :
1. Démarrer le backend automatiquement
2. Ouvrir le dashboard
3. Permettre de toggle l'overlay avec F9

## Distribution

### Installateur (recommandé)
Distribuer `PROHelper-Setup.exe` qui :
- Installe l'application dans Program Files
- Crée des raccourcis bureau/menu démarrer
- Permet la désinstallation propre

### Version portable
Distribuer le dossier `win-unpacked/` complet (ou zipper)
- Pas d'installation nécessaire
- Exécutable directement
- Utile pour clés USB ou tests rapides

## Troubleshooting

### Backend ne démarre pas

**Problème** : Erreur "Tesseract not found"
```
Solution : Ajouter Tesseract au PATH ou spécifier le chemin dans le code
```

**Problème** : Port 8000 déjà utilisé
```
Solution : Modifier le port dans config.json
```

### Frontend ne compile pas

**Problème** : Erreur TypeScript
```bash
# Vérifier les types
npm run type-check

# Si problème persiste
rm -rf node_modules package-lock.json
npm install
```

**Problème** : electron-builder échoue
```bash
# Installer les dépendances Windows build tools
npm install --global windows-build-tools
```

### Build PyInstaller échoue

**Problème** : Module manquant au runtime
```python
# Ajouter dans build.spec, section hiddenimports
hiddenimports=[
    'nom_du_module_manquant',
]
```

**Problème** : Fichier de données manquant
```python
# Ajouter dans build.spec, section datas
datas=[
    ('chemin/source', 'chemin/destination'),
]
```

## Optimisations

### Réduire la taille de l'executable

#### Backend
```bash
# Utiliser UPX pour compresser
pyinstaller build.spec --upx-dir=/path/to/upx
```

#### Frontend
```javascript
// Dans electron-builder config (package.json)
"compression": "maximum",
"nsis": {
  "oneClick": false,
  "allowToChangeInstallationDirectory": true,
  "compressionLevel": "ultra"
}
```

### Améliorer les performances

#### Backend
- Mettre le cache sur un SSD
- Augmenter la durée de cache (config.json)

#### Frontend
- Activer la minification (déjà activé en prod)
- Utiliser le mode production de React

## CI/CD (À venir)

Pour automatiser les builds :

```yaml
# .github/workflows/build.yml
name: Build
on: [push]
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Backend
        run: |
          cd backend
          pip install -r requirements.txt
          pyinstaller build.spec
      - name: Build Frontend
        run: |
          cd frontend
          npm install
          npm run package
      - name: Upload Artifacts
        uses: actions/upload-artifact@v2
        with:
          name: PROHelper
          path: frontend/release/*.exe
```

## Support

En cas de problème, ouvrir une issue sur GitHub avec :
- Version de Python
- Version de Node.js
- Logs d'erreur complets
- Étape où ça bloque
