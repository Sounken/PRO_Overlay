# PRO Helper - Pokémon Revolution Online Helper
**Version 1.0.2** (Build 2026-02-10)

## 🎮 Qu'est-ce que c'est ?

PRO Helper est une application Windows qui vous aide à jouer **Pokémon Revolution Online** en detectant automatiquement les noms des Pokémon et en vous donnant des conseils de type.

## ✨ Fonctionnalités

✅ **Détection OCR** - Reconnaît automatiquement les noms des Pokémon sur l'écran
✅ **Gestion d'équipe** - Créez et gérez votre équipe de 6 Pokémon
✅ **Recommandations** - Recevez des conseils sur quel Pokémon utiliser
✅ **Analyse de type** - Comprendre l'efficacité des types
✅ **Mode Auto** - Basculez l'overlay automatiquement
✅ **100% Autonome** - Aucune installation externe requise

## 📋 Prérequis

- **Windows 10 ou plus récent**
- **500 MB d'espace disque** (pour les modèles AI)
- **Résolution d'écran 1920x1080 ou plus** (recommandé)
- **Pas d'autre logiciel requis** ✓ Tout est bundlé!

## 🚀 Installation & Lancement

### Étape 1 - Lancer l'application

Double-cliquez sur **`RUN.bat`** ou exécutez **`PROHelper.exe`** directement.

### Étape 2 - Première utilisation

La première fois:
- Les modèles AI vont être téléchargés (~1-2 minutes)
- L'overlay va s'initialiser
- Vous pouvez voir le dashboard de configuration

### Étape 3 - Utiliser en jeu

1. Lancez **Pokémon Revolution Online** (PRO)
2. Appuyez sur **F9** pour activer/désactiver l'overlay
3. L'overlay affichera le Pokémon détecté + conseils

## ⌨️ Contrôles

| Touche | Action |
|--------|--------|
| **F9** | Basculer l'overlay |
| **F12** | Ouvrir la console (debug) |
| **ESC** | Quitter l'application |

## 📖 Utilisation

### Dashboard
- **Pokedex** - Voir tous les Pokémon avec leurs types
- **Équipe** - Gérer votre équipe de combat
- **Settings** - Configurer les zones OCR

### Overlay
L'overlay affiche:
- **Pokémon adverse** - Détecté via OCR
- **Conseil de changement** - Quel Pokémon utiliser
- **Efficacité de type** - Avantages/désavantages

### Sélection de Zone OCR
1. Cliquez sur "Sélectionner zone"
2. Dessinez un rectangle sur le nom du Pokémon en jeu
3. L'app apprendra à reconnaître cette zone

## 🐛 Dépannage

### L'overlay n'apparaît pas
- Vérifiez que vous êtes dans une fenêtre PRO active
- Appuyez sur F9 pour basculer
- Vérifiez que la zone OCR est correctement configurée

### L'OCR ne détecte rien
- La zone OCR peut être mal positionnée
- Utilisez "Sélectionner zone" pour réajuster
- Assurez-vous que le nom du Pokémon est visible

### L'application plante
- Essayez de relancer RUN.bat
- Vérifiez que vous avez 500 MB libres
- Consultez la console (F12) pour les erreurs

## 📞 Support

Pour les bugs ou questions:
- Vérifiez que vous avez la dernière version (1.0.2)
- Consultez les logs dans la console (F12)
- Reportez les problèmes avec des screenshots

## 🔧 Améliorations Récentes (v1.0.2)

✓ Changement de Tesseract à EasyOCR (meilleure IA)
✓ Preprocessing d'image pour meilleure détection
✓ Interface utilisateur améliorée
✓ Correction de bugs de compatibilité

## 📝 Notes Techniques

- **Frontend** - Electron + React (interface moderne)
- **Backend** - FastAPI + EasyOCR (AI engine)
- **Taille** - ~270 MB (tout incluant les modèles AI)
- **Modèles** - EasyOCR PyTorch (téléchargés au premier lancement)

## ✅ Vérification de l'Installation

Si tout est correct, vous devriez voir:
- ✓ PROHelper.exe (application principale)
- ✓ backend/backend.exe (moteur OCR)
- ✓ config.json (configuration)
- ✓ RUN.bat (script de lancement)

---

**Prêt à jouer ? Lancez RUN.bat ! 🎮**
