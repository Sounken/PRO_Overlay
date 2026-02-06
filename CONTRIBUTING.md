# Guide de Contribution

Merci de vouloir contribuer à PRO Helper ! Ce document explique comment participer au projet.

## 🚀 Démarrage rapide

1. Forker le repo
2. Cloner votre fork
```bash
git clone https://github.com/VOTRE_USERNAME/PRO_Overlay.git
cd PRO_Overlay
```

3. Installer les dépendances
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

4. Créer une branche
```bash
git checkout -b feature/ma-fonctionnalite
```

## 📝 Standards de code

### Backend (Python)

- Style : PEP 8
- Docstrings : Google style
- Type hints obligatoires

```python
def get_pokemon(identifier: str) -> Optional[Dict[str, Any]]:
    """
    Récupère les données d'un Pokémon.

    Args:
        identifier: Nom ou ID du Pokémon

    Returns:
        Données du Pokémon ou None si erreur
    """
    pass
```

### Frontend (TypeScript/React)

- Style : Standard TypeScript
- Composants : Functional components + hooks
- Props : Interfaces TypeScript

```typescript
interface PokemonCardProps {
  pokemon: Pokemon
}

function PokemonCard({ pokemon }: PokemonCardProps) {
  // Component logic
}
```

## 🎯 Zones de contribution

### Prioritaire
- [ ] Compléter la liste des Pokémon Gen 1-9 (`backend/services/ocr_engine.py`)
- [ ] Améliorer la précision OCR
- [ ] Implémenter les recommandations d'attaque
- [ ] Gestion d'équipe

### Améliorations
- [ ] Calculateur de dégâts
- [ ] Calculateur d'EVs/IVs
- [ ] Support multilingue complet
- [ ] Mode sombre/clair
- [ ] Thèmes personnalisables

### Corrections
- [ ] Bugs OCR
- [ ] Performance overlay
- [ ] Gestion mémoire cache

## 🧪 Tests

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

Tous les PRs doivent inclure des tests.

## 📋 Checklist PR

Avant de soumettre une PR :

- [ ] Le code compile sans erreur
- [ ] Les tests passent
- [ ] Le code suit les standards
- [ ] La documentation est à jour
- [ ] Les commits sont clairs
- [ ] Pas de `console.log()` ou `print()` de debug

## 🐛 Rapporter un bug

Utiliser le template d'issue avec :

- Version de l'application
- OS et version
- Description du problème
- Étapes pour reproduire
- Comportement attendu vs obtenu
- Screenshots si applicable

## 💡 Proposer une fonctionnalité

Ouvrir une issue "Feature Request" avec :

- Description de la fonctionnalité
- Cas d'utilisation
- Mockups/wireframes si possible
- Complexité estimée

## 🔧 Architecture

### Backend
- FastAPI pour l'API REST
- Tesseract pour l'OCR
- mss pour les captures d'écran
- Cache JSON local

### Frontend
- Electron pour l'application native
- React + TypeScript pour l'UI
- Tailwind CSS pour le styling
- Framer Motion pour les animations

## 📚 Ressources

- [PokeAPI Documentation](https://pokeapi.co/docs/v2)
- [Tesseract Documentation](https://tesseract-ocr.github.io/)
- [Electron Documentation](https://www.electronjs.org/docs/latest)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Code de conduite

- Respecter les autres contributeurs
- Constructif dans les reviews
- Pas de discrimination
- Professionnalisme

## 📞 Contact

- Issues GitHub pour les bugs
- Discussions GitHub pour les questions
- Discord : [lien à venir]

Merci de contribuer ! 🎮✨
