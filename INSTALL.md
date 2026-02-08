# 📦 Installation et Utilisation - PRO Helper

## Pour les Utilisateurs

### Option 1: Version Portable (Recommandé) ⭐

**Télécharger:**
1. Allez sur la page [Releases](https://github.com/[votre-username]/PRO_Overlay/releases)
2. Téléchargez `PROHelper-1.0.0-portable.zip`
3. Décompressez le fichier

**Lancer l'application:**
- Double-cliquez sur `RUN.bat` dans le dossier décompressé
- Ou lancez directement `PROHelper/PROHelper.exe`

**Avantages:**
- ✅ Aucune installation requise
- ✅ Peut tourner depuis une clé USB
- ✅ Aucune modification du système

### Option 2: Installateur (Optionnel)

1. Téléchargez `PROHelper-1.0.0-Setup.exe` depuis les Releases
2. Exécutez l'installateur
3. L'application s'installera dans `C:\Program Files\PROHelper`
4. Raccourcis créés automatiquement dans le menu Démarrer

**Avantages:**
- ✅ Installation classique
- ✅ Raccourcis dans le menu Démarrer
- ✅ Désinstallation propre

---

## Pour les Développeurs

### Compiler depuis le code source

**Prérequis:**
- Python 3.13+
- Node.js 18+
- Git

**Installation:**
```bash
git clone https://github.com/[votre-username]/PRO_Overlay.git
cd PRO_Overlay
build.bat
```

**Lancer en développement:**
```bash
cd frontend
npm run electron:dev
```

---

## Dépannage

### "ffmpeg.dll introuvable"
- ✅ Utilisez le `RUN.bat` au lieu de cliquer directement sur l'exe
- ✅ Assurez-vous que tous les fichiers sont dans le même dossier

### "Rien ne s'affiche"
- Appuyez sur **F12** pour ouvrir les outils de développement
- Vérifiez la console pour les erreurs

### Backend ne démarre pas
- Vérifiez que port 8000 est disponible
- Essayez de redémarrer l'application

---

## Support

Pour les problèmes:
1. Vérifiez le [README principal](README.md)
2. Consultez [QUICK_START.md](QUICK_START.md)
3. Ouvrez une issue sur GitHub

---

**Version:** 1.0.0
**Date:** Février 2026
