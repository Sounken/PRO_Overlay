# Pokemon Revolution Online - Helper

Application d'assistance pour Pokemon Revolution Online avec overlay en temps réel et dashboard de gestion.

## 🎯 Fonctionnalités

### Overlay (Prioritaire)
- ✅ Détection OCR du nom du Pokémon adverse
- ✅ Affichage instantané des faiblesses/résistances
- ✅ EVs obtenus si le Pokémon est vaincu
- ✅ Toggle avec hotkey (F9)
- 🔄 Recommandation d'attaque selon ton équipe (À venir)
- 🔄 Suggestion de switch (À venir)

### Dashboard
- ✅ Pokédex : Recherche par nom anglais ou numéro
- ✅ Fiche détaillée avec sprite haute qualité
- ✅ Fond coloré selon la couleur dominante du Pokémon
- ✅ Nom en français si disponible
- ✅ Types avec icônes Gen 9 (Scarlet/Violet)
- ✅ Statistiques avec barres de progression
- ✅ Tableau des 18 types avec multiplicateurs
- ✅ Effort Values (EVs) obtenus
- 🔄 Gestion d'équipe (À venir)
- 🔄 Calculateurs (Dégâts, EVs/IVs, Hidden Power) (À venir)

## 🏗️ Architecture

```
Backend Python (FastAPI) + Frontend Electron (React + TypeScript)
```

- **Backend** : FastAPI avec OCR (Tesseract), PokeAPI client, cache JSON
- **Frontend** : Electron + React + Tailwind CSS + Framer Motion
- **Livrable** : Un seul fichier `PROHelper.exe` (~200MB)

## 📦 Installation

### Prérequis

#### Backend
- Python 3.10+
- Tesseract OCR

Installation Tesseract (Windows) :
```bash
# Télécharger depuis : https://github.com/UB-Mannheim/tesseract/wiki
# Ou via chocolatey :
choco install tesseract
```

#### Frontend
- Node.js 18+
- npm ou yarn

### Installation des dépendances

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

## 🚀 Développement

### Lancer le backend
```bash
cd backend
python main.py
# Serveur sur http://localhost:8000
```

### Lancer le frontend (mode dev)
```bash
cd frontend
npm run dev
# Interface sur http://localhost:3000
```

### Lancer Electron en dev
```bash
cd frontend
npm run electron:dev
```

## 📦 Build & Packaging

### 1. Compiler le backend en .exe
```bash
cd backend
pyinstaller build.spec
# Génère : dist/backend.exe
```

### 2. Compiler le frontend + packager
```bash
cd frontend
npm run package
# Génère : release/PROHelper-Setup.exe
```

### 3. Distribution
Le fichier final sera disponible dans `frontend/release/` :
- `PROHelper-Setup.exe` : Installateur (~200MB)
- `PROHelper.exe` : Version portable

## 🎮 Utilisation

1. Lancer `PROHelper.exe`
2. Le backend démarre automatiquement
3. Dashboard s'ouvre automatiquement
4. Jouer à Pokemon Revolution Online
5. Appuyer sur **F9** pour toggle l'overlay
6. L'overlay détecte automatiquement le Pokémon adverse

## ⚙️ Configuration

Le fichier `config.json` permet de configurer :
- Port du backend
- Seuil de confiance OCR
- Hotkey de l'overlay
- Durée du cache

## 🔧 Développement

### Structure du projet

```
pokemon-pro-helper/
├── backend/                 # Python FastAPI
│   ├── main.py
│   ├── routes/             # Endpoints API
│   ├── services/           # OCR, PokeAPI, etc.
│   ├── models/             # Pydantic schemas
│   └── data/cache/         # Cache JSON
│
├── frontend/               # Electron + React
│   ├── electron/           # Main process
│   ├── src/                # React app
│   │   ├── components/
│   │   ├── services/
│   │   └── hooks/
│   └── public/
│
└── config.json
```

### API Endpoints

#### Pokémon
```
GET /pokemon/{identifier}
```

#### OCR
```
POST /ocr/detect
Body: { region?: { x, y, width, height } }
```

#### Cache
```
GET /cache/stats
DELETE /cache/clear?pokemon={name}
```

#### Health
```
GET /health
```

## 📝 TODO

- [ ] Compléter la liste des noms de Pokémon Gen 1-9 dans `ocr_engine.py`
- [ ] Implémenter les recommandations d'attaque
- [ ] Implémenter les suggestions de switch
- [ ] Gestion d'équipe
- [ ] Calculateurs (Dégâts, EVs/IVs, Hidden Power)
- [ ] Paramètres utilisateur
- [ ] WebSocket pour détection OCR en temps réel
- [ ] Tests unitaires
- [ ] CI/CD

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une PR.

## 📄 Licence

MIT

## 🙏 Remerciements

- [PokeAPI](https://pokeapi.co/) pour les données Pokémon
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Communauté Pokemon Revolution Online
