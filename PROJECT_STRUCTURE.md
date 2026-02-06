# Structure du Projet

Documentation de l'organisation des fichiers et dossiers.

## 📂 Vue d'ensemble

```
PRO_Overlay/
├── backend/                    # Backend Python (FastAPI)
├── frontend/                   # Frontend Electron + React
├── .vscode/                    # Configuration VSCode
├── config.json                 # Configuration application
├── README.md                   # Documentation principale
├── QUICKSTART.md              # Guide démarrage rapide
├── BUILD.md                   # Guide de compilation
├── CONTRIBUTING.md            # Guide de contribution
├── LICENSE                    # Licence MIT
├── dev.bat                    # Script dev Windows
└── dev.sh                     # Script dev Linux/Mac
```

## 🐍 Backend (Python FastAPI)

```
backend/
├── main.py                    # Point d'entrée FastAPI
├── requirements.txt           # Dépendances Python
├── build.spec                 # Configuration PyInstaller
│
├── models/                    # Modèles de données
│   ├── __init__.py
│   └── schemas.py             # Pydantic schemas
│
├── routes/                    # Endpoints API
│   ├── __init__.py
│   ├── pokemon.py             # GET /pokemon/{id}
│   ├── ocr.py                 # POST /ocr/detect
│   └── cache.py               # Cache management
│
├── services/                  # Logique métier
│   ├── __init__.py
│   ├── pokeapi_client.py      # Client PokeAPI + cache
│   ├── type_matchup.py        # Calcul efficacité types
│   ├── ocr_engine.py          # Tesseract OCR
│   └── screen_capture.py      # Capture écran (mss)
│
└── data/
    └── cache/                 # Cache JSON Pokemon
        └── .gitkeep
```

### Fichiers clés

- **main.py** : Serveur FastAPI, enregistre les routes
- **schemas.py** : Définit les types de données (Pokemon, OCR, etc.)
- **pokeapi_client.py** : Gère les appels PokeAPI avec cache local
- **type_matchup.py** : Calcule les multiplicateurs de types
- **ocr_engine.py** : Détecte les noms de Pokemon via OCR

## ⚛️ Frontend (Electron + React)

```
frontend/
├── package.json               # Dépendances Node.js
├── tsconfig.json              # Configuration TypeScript
├── vite.config.ts             # Configuration Vite
├── tailwind.config.js         # Configuration Tailwind CSS
├── postcss.config.js          # Configuration PostCSS
├── index.html                 # HTML de base
│
├── electron/                  # Processus principal Electron
│   ├── main.ts                # Lance backend + fenêtres
│   └── preload.ts             # Bridge IPC sécurisé
│
├── public/                    # Assets statiques
│   └── pokeball.svg           # Icône app
│
└── src/                       # Code React
    ├── main.tsx               # Point d'entrée React
    ├── App.tsx                # Composant racine
    │
    ├── components/            # Composants UI
    │   ├── Dashboard/         # Interface principale
    │   │   ├── Dashboard.tsx
    │   │   ├── Sidebar.tsx
    │   │   ├── Pokedex.tsx
    │   │   ├── PokemonCard.tsx
    │   │   └── TypeGrid.tsx
    │   │
    │   └── Overlay/           # Interface overlay
    │       ├── OverlayWindow.tsx
    │       └── PokemonInfo.tsx
    │
    ├── services/              # Communication API
    │   └── api.ts             # Client Axios
    │
    ├── hooks/                 # React hooks personnalisés
    │   └── (à venir)
    │
    └── styles/                # Styles globaux
        └── globals.css        # Tailwind + custom CSS
```

### Fichiers clés

- **electron/main.ts** : Lance le subprocess Python, crée les fenêtres
- **electron/preload.ts** : Expose l'API Electron au renderer
- **App.tsx** : Router Dashboard/Overlay selon le hash
- **api.ts** : Abstraction des appels backend
- **Dashboard/** : Interface de recherche et affichage Pokemon
- **Overlay/** : Fenêtre transparente en jeu

## 🔧 Configuration

### config.json
Configuration globale de l'application :
- Ports backend/frontend
- Paramètres OCR
- Hotkey overlay
- Durée cache

### .vscode/
Configuration VSCode pour faciliter le développement :
- **settings.json** : Formatage, linting
- **extensions.json** : Extensions recommandées
- **launch.json** : Configurations de debug

## 📦 Build Artifacts

```
backend/
└── dist/
    └── backend.exe            # Backend compilé (PyInstaller)

frontend/
└── release/
    ├── PROHelper-Setup.exe    # Installateur Windows
    └── win-unpacked/          # Version portable
        └── PROHelper.exe
```

## 🔄 Flux de données

### 1. Démarrage
```
PROHelper.exe (Electron)
    ↓
electron/main.ts démarre backend.exe
    ↓
Backend lance FastAPI sur :8000
    ↓
Electron crée Dashboard + Overlay
```

### 2. Recherche Pokemon (Dashboard)
```
User → Pokedex.tsx
    ↓
api.ts → GET /pokemon/{name}
    ↓
Backend → PokeAPI (ou cache)
    ↓
PokemonCard.tsx affiche résultat
```

### 3. Détection OCR (Overlay)
```
OverlayWindow.tsx (auto polling 2s)
    ↓
api.ts → POST /ocr/detect
    ↓
Backend → Capture écran → Tesseract
    ↓
Nom Pokemon détecté → GET /pokemon/{name}
    ↓
PokemonInfo.tsx affiche résultat
```

## 🎨 Stack Technique

### Backend
- **FastAPI** : Framework web moderne
- **Pydantic** : Validation de données
- **Tesseract** : OCR
- **mss** : Capture d'écran
- **requests** : Client HTTP
- **uvicorn** : Serveur ASGI

### Frontend
- **Electron** : Application native
- **React 18** : UI library
- **TypeScript** : Type safety
- **Vite** : Build tool rapide
- **Tailwind CSS** : Styling utilitaire
- **Framer Motion** : Animations
- **Axios** : Client HTTP

### Build
- **PyInstaller** : Compile Python → .exe
- **electron-builder** : Package Electron

## 📝 Conventions

### Nommage
- **Python** : snake_case
- **TypeScript** : camelCase
- **React Components** : PascalCase
- **Fichiers** : kebab-case ou PascalCase selon le type

### Organisation
- Un fichier = une responsabilité
- Services isolés et testables
- Composants réutilisables
- Types centralisés (schemas.py, api.ts)

### Documentation
- Docstrings Python (Google style)
- JSDoc TypeScript
- README par feature si nécessaire

## 🔍 Points d'entrée

### Développement
- **Backend** : `python backend/main.py`
- **Frontend** : `npm run dev` (dans frontend/)
- **Electron** : `npm run electron:dev` (dans frontend/)

### Build
- **Backend** : `pyinstaller backend/build.spec`
- **Frontend** : `npm run package` (dans frontend/)

### Tests (à venir)
- **Backend** : `pytest backend/tests/`
- **Frontend** : `npm test` (dans frontend/)
