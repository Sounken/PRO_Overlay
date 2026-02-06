# PRO_Overlay

Assistant overlay pour Pokemon Revolution Online avec détection OCR et recommandations en temps réel.

## Fonctionnalités

- 🎯 Overlay en jeu avec détection automatique du Pokémon adverse
- ⚔️ Tableau de matchup instantané (faiblesses/résistances)
- 💪 Affichage des EVs obtenus après victoire
- 🔄 Recommandations d'attaque et de switch
- 📊 Dashboard avec Pokédex complet

## Installation

### Prérequis
- Python 3.10+
- Tesseract OCR

### Installation Tesseract
**Windows** : Télécharger depuis https://github.com/UB-Mannheim/tesseract/wiki 

Ajouter au PATH : `C:\Program Files\Tesseract-OCR`

**Linux** : `sudo apt install tesseract-ocr`

### Installation des dépendances
```bash
pip install -r requirements.txt


F9 : Toggle overlay

F10 : Rafraîchir détection

Ctrl+Q : Quitter
