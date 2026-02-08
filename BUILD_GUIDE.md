# PRO Helper - Build Guide

Step-by-step instructions to build the executable.

## Prerequisites Check

Before building, verify you have everything installed:

```bash
# Check Python
py --version
# Should show Python 3.10+

# Check Node.js
node --version
# Should show v18+

# Check npm
npm --version
# Should show 9+
```

If any are missing, install them before continuing.

---

## Option 1: Automated Build (Recommended)

### Step 1: Run the Build Script

```bash
# Navigate to the project root
cd PRO-Overlay

# Run the build script (double-click or command line)
build.bat
```

The script will:
1. Create Python virtual environment
2. Install Python dependencies
3. Compile backend to exe
4. Install Node dependencies
5. Build React app
6. Package with Electron-Builder

**Estimated time**: 5-15 minutes (depending on internet speed)

### Step 2: Find Your Files

After successful build, files are in:
- `frontend/release/PROHelper Setup 1.0.0.exe` - Installer
- `frontend/release/PROHelper 1.0.0.exe` - Portable

---

## Option 2: Manual Build (Troubleshooting)

If the automated script fails, follow these steps:

### Backend Build

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
py -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Show detailed output
pip install pyinstaller

# Build with PyInstaller (shows errors)
pyinstaller build.spec -v

# Check result
dir dist
# Should show: backend.exe
```

### Frontend Build

```bash
# Navigate to frontend folder
cd frontend

# Install Node dependencies
npm install

# Compile TypeScript
npm run build:electron

# Build React app
npm run build

# Package application
npm run package

# Check result
dir release
# Should show: PROHelper Setup 1.0.0.exe
```

---

## Common Build Errors & Solutions

### Error: "Python not found" or "py not recognized"

**Cause**: Python is not in your PATH

**Solution**:
1. Uninstall Python completely
2. Reinstall from https://www.python.org/
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Restart your computer
5. Try again

### Error: "Node not found" or "npm not recognized"

**Cause**: Node.js is not installed or not in PATH

**Solution**:
1. Download Node.js from https://nodejs.org/ (LTS version)
2. Run the installer
3. Use default installation settings
4. Restart your computer
5. Try again

### Error: "ModuleNotFoundError" or "No module named..."

**Cause**: Python dependencies not installed

**Solution**:
```bash
cd backend
venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Error: "pyinstaller: command not found"

**Cause**: PyInstaller not installed

**Solution**:
```bash
cd backend
venv\Scripts\activate.bat
pip install pyinstaller
pyinstaller build.spec -v
```

### Error: "Cannot find module 'electron'"

**Cause**: Node modules not installed

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run package
```

### Error: "ABORTING BUILD. DATA COLLECTION ERROR"

**Cause**: PyInstaller found import errors

**Solution**:
```bash
cd backend
# Check your Python imports are correct
python -c "import main"
# This will show the actual error

# Then fix the import issues
```

---

## Verifying Your Build

### Test Backend Executable

```bash
# Navigate to backend dist folder
cd backend\dist

# Run the backend
backend.exe

# You should see:
# INFO:     Started server process
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

Stop with Ctrl+C

### Test Frontend/Electron

```bash
cd frontend

# Test in dev mode first
npm run electron:dev

# The app should launch with DevTools open
# Try the features quickly
```

---

## File Structure After Build

```
PRO-Overlay/
├── backend/
│   ├── dist/
│   │   └── backend.exe          ← Backend executable
│   ├── build/                   ← PyInstaller build files
│   └── venv/                    ← Virtual environment
│
├── frontend/
│   ├── dist/                    ← React build files
│   ├── dist-electron/           ← Electron main process
│   ├── release/
│   │   ├── PROHelper Setup 1.0.0.exe    ← Installer
│   │   └── PROHelper 1.0.0.exe          ← Portable
│   └── node_modules/            ← Node dependencies
│
└── config.json
```

---

## Distribution & Testing

### For Users

Distribute these files:
- `PROHelper Setup 1.0.0.exe` - For installation
- `PROHelper 1.0.0.exe` - For portable use

### For Testing

1. Uninstall any previous version
2. Run the installer fresh
3. Test OCR zone selection
4. Test Pokemon search
5. Test overlay (F9)
6. Test team management

---

## Rebuilding After Changes

### After Code Changes

```bash
# For backend changes:
cd backend
pyinstaller build.spec -y

# For frontend changes:
cd frontend
npm run build
npm run package

# For both:
# Just run build.bat again
```

### Clean Rebuild

```bash
# Remove old build files
cd backend
rmdir /s dist build

# Remove old frontend builds
cd ../frontend
rmdir /s dist dist-electron release
rmdir /s node_modules

# Run build.bat fresh
cd ..
build.bat
```

---

## Advanced Options

### Build for Different Windows Versions

Edit `frontend/package.json`:

```json
"win": {
  "target": ["nsis", "portable"],
  "certificateFile": "path/to/cert.pfx"  // For code signing
}
```

### Reduce Installer Size

In `build.spec`:

```python
upx=True  # Use UPX compression
```

### Create 32-bit Version

```bash
cd frontend
npm run package -- --win --ia32
```

---

## Getting Help

If you're still stuck:

1. **Check the full error output**:
   - Run commands manually without redirection
   - Copy the full error message

2. **Check requirements**:
   - `backend/requirements.txt` - All Python packages
   - `frontend/package.json` - All Node packages

3. **Check system**:
   - Enough disk space (>500MB free)
   - Admin privileges to install
   - Antivirus not blocking build tools

4. **Isolate the problem**:
   - Try manual steps from Option 2
   - See which step exactly fails
   - Report that specific error

---

**Version**: 1.0.0 | February 2025
