# PRO Helper - Pokemon Revolution Online Assistant

A desktop application for Pokemon Revolution Online that provides real-time Pokemon data, team management, and intelligent battle recommendations using OCR detection.

## ✨ Features

### Overlay (Real-time Battle Support)
- ✅ Auto-detect enemy Pokemon with OCR
- ✅ Display weaknesses & resistances instantly
- ✅ Show earned Effort Values (EVs)
- ✅ Toggle with F9 hotkey
- ✅ Smart Pokemon switch recommendations based on type matchups
- ✅ Automatic overlay activation in battle mode

### Dashboard
- ✅ **Pokedex**: Search by name or ID number
- ✅ Detailed Pokemon stats with visual bars
- ✅ Type effectiveness chart (all 18 types)
- ✅ Weakness & resistance information
- ✅ Effort Value (EV) distribution
- ✅ **Team Manager**: Build your 6-Pokemon team
- ✅ Auto-detect team from game screen (OCR)
- ✅ Get battle recommendations vs opponent
- 🔄 Calculators (damage, EVs/IVs) - Coming soon

## 🚀 Installation

### Option 1: Portable Version (Recommended) ⭐
1. Download `PROHelper-1.0.0-portable.zip` from [Releases](https://github.com/[username]/PRO_Overlay/releases)
2. Extract the ZIP file
3. Double-click `RUN.bat` to launch the application
4. No installation needed - portable version works from any location

### Option 2: Installer Version
1. Download `PROHelper-1.0.0-Setup.exe` from Releases
2. Run the installer and follow the prompts
3. Launch PRO Helper from your Start Menu

**Requirements**: Windows 7 or later, 200 MB disk space, Python 3.10+ (backend only)

## 🎮 Quick Start Guide

### Step 1: Configure OCR Zone
1. Open PRO Helper and go to **Settings**
2. Click **Set OCR Zone**
3. Draw a box around where Pokemon names appear in-game
4. Click **Confirm**

### Step 2: Build Your Team
- Go to **Team** tab
- Search for Pokemon and add them, OR
- Use **Detect Team via OCR** to auto-detect

### Step 3: Play
1. Open Pokemon Revolution Online
2. Press **F9** to toggle the overlay
3. When you encounter a Pokemon, the overlay shows:
   - Enemy Pokemon stats
   - Recommended Pokemon to switch to
   - Type effectiveness info

## 📋 How to Use Each Feature

### Pokedex Tab
- Search by name (e.g., "Pikachu") or ID (e.g., "25")
- View stats, types, EVs, and type matchups
- Use the legend to understand type effectiveness

### Team Tab
- Add Pokemon manually or auto-detect from screen
- Click **Active** to set your current Pokemon
- Get recommendations against detected opponents

### Settings Tab
- **OCR Detection Zone**: Where the app looks for enemy Pokemon
- **Auto Battle Mode**: Auto-open overlay during combat

## ⌨️ Keyboard Shortcuts
- **F9** - Toggle overlay on/off
- **Escape** - Cancel OCR zone selection

## 🆘 Troubleshooting

**"Tesseract OCR not found"**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Or run the installer again to install Tesseract

**OCR not detecting Pokemon names**
- Resize the OCR zone to match exactly where names appear
- Try resetting the zone in Settings
- Ensure good contrast in game graphics

**Overlay not showing**
- Press F9 to toggle manually
- Check Settings → Auto Battle Mode
- Ensure PRO Helper window is on top

**"Pokemon not found" error**
- Use correct English name (e.g., "Pikachu" not "Pichu")
- Try searching by ID number instead
- Check internet connection

## 📊 Type Effectiveness Legend
- **×0** = Immune (attack has no effect)
- **×¼, ×½** = Resistant (takes reduced damage)
- **×1** = Normal damage
- **×2, ×4** = Weakness (takes more damage)

## 💾 System Architecture
- **Frontend**: Electron + React + TypeScript
- **Backend**: FastAPI + Python + Tesseract OCR
- **Data**: PokeAPI with local caching

## 📝 Notes
- First launch installs Tesseract OCR (~100MB)
- Internet required to sync Pokemon data
- OCR works best at 1080p resolution or higher
- Keep the app window visible during battles

## 📄 License
MIT License - See LICENSE file

## 🔗 Links
- [PokéAPI](https://pokeapi.co/) - Pokemon data source
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [Pokemon Revolution Online](https://www.pokemonrevolution.net/)

---
**Version**: 1.0.0 | **Last Updated**: February 2025
