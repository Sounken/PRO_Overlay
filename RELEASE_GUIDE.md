# Release Guide - PRO Helper v1.0.0

## Preparing a Release

### Prerequisites
1. All code is built and tested
2. Application runs successfully: `RUN.bat`
3. All unnecessary files cleaned (done ✓)

### Creating Release Package

The `release-package/` folder is automatically created with all files needed for distribution.

```bash
# The release-package folder contains:
# - PROHelper/              (application executable and dependencies)
# - RUN.bat                 (launcher for end users)
# - README.md               (documentation)
# - INSTALL.md              (installation guide)
# - QUICK_START.md          (quick start guide)
# - VERSION.txt             (version information)
```

### Distributing via GitHub Releases

1. **Create a ZIP file:**
   ```bash
   cd release-package
   # Right-click > Send to > Compressed folder
   # OR use 7-Zip/WinRAR to create: PROHelper-v1.0.0-portable.zip
   ```

2. **Create GitHub Release:**
   - Go to: https://github.com/yourusername/PRO-Overlay/releases/new
   - Tag: `v1.0.0`
   - Title: `PRO Helper v1.0.0 - Release`
   - Description:
     ```
     ## What's New
     ✅ OCR Detection System
     ✅ Team Management
     ✅ Smart Battle Recommendations
     ✅ Type Matchup Analysis
     ✅ Auto Battle Mode
     ✅ Full Performance Optimization

     ## How to Install
     1. Download `PROHelper-v1.0.0-portable.zip`
     2. Extract to any folder
     3. Double-click `RUN.bat`

     ## System Requirements
     - Windows 10 or later
     - 500MB free disk space
     - Display 1920x1080 or higher (recommended)
     ```

3. **Upload Attachment:**
   - Drag & drop `PROHelper-v1.0.0-portable.zip`

## Building from Source

If you need to rebuild the release package:

```bash
# Build backend
cd backend
python -m PyInstaller build.spec

# Build frontend
cd ../frontend
npm install
npm run build:electron
npm run build

# Update PROHelper folder
cd ..
rm -rf PROHelper
cp -r frontend/release/win-unpacked PROHelper
cp backend/dist/backend.exe PROHelper/resources/backend/backend.exe

# Create release package
rm -rf release-package
mkdir release-package
cp -r PROHelper release-package/
cp README.md INSTALL.md QUICK_START.md release-package/
cp RUN.bat release-package/
```

## Version Management

Current version: **1.0.0**

To increment version for next release:
- Update `frontend/package.json` version field
- Update `backend/build.spec` if needed
- Update `VERSION.txt` in release-package

## Files Not in Git

The following large files are NOT committed but are in `release-package/`:
- `PROHelper/` (contains compiled exe + dependencies - ~200MB)
- `release-package/` (distribution folder)

These are excluded by `.gitignore` since they're generated during build.

## Quality Checklist

Before releasing, verify:
- ✓ `RUN.bat` launches without errors
- ✓ Electron window appears
- ✓ Backend starts automatically
- ✓ F9 toggles overlay correctly
- ✓ OCR region selection works
- ✓ Team management functional
- ✓ Battle recommendations display properly
- ✓ All UI elements responsive
- ✓ No console errors (F12 to check)

---

**Last Updated:** February 8, 2026
**Release Version:** 1.0.0
