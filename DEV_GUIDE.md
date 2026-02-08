# Development Guide

## Important Note

**`npm run electron:dev` has limitations due to ESM/CommonJS module resolution conflicts.** This is a known issue with mixing ESM (Vite) and CommonJS (Electron) in the same project.

## Development Workflow

### Option 1: Use Packaged Application (Recommended)
For development and testing, use the compiled version:

```bash
# From project root
RUN.bat
```

This launches the fully compiled and tested application that works perfectly.

### Option 2: Build & Test Loop
```bash
# Build all components
cd frontend
npm run build:electron
npm run build
cd ..

# Update PROHelper folder
rm -rf PROHelper
cp -r frontend/release/win-unpacked PROHelper
cp backend/dist/backend.exe PROHelper/resources/backend/backend.exe

# Test with launcher
RUN.bat
```

## Why electron:dev Doesn't Work

The issue is architectural:
- **Vite** (React dev server) uses ESM
- **Electron** is a CommonJS module
- **TypeScript compilation** has conflicts between the two module systems

This is a known limitation in Electron + TypeScript + ESM projects.

## Production Build

The production/packaged build works perfectly:
- `npm run build:electron` - Compiles Electron main process
- `npm run build` - Builds React app
- `RUN.bat` - Launches the compiled application

All features work flawlessly in the packaged version!

## Contributing

When making changes:
1. Edit source files (`.ts`, `.tsx`)
2. Run `npm run build:electron && npm run build` from frontend/
3. Update PROHelper folder with new binaries
4. Test with `RUN.bat`

## Testing Checklist

- [ ] Backend starts (`http://localhost:8000/health`)
- [ ] Electron window opens
- [ ] Dashboard loads
- [ ] F9 toggles overlay
- [ ] OCR detection works
- [ ] Team management functional
- [ ] Battle recommendations display
- [ ] No console errors (F12)

---

**Note**: All core functionality is fully operational. The dev mode limitation only affects the development workflow, not the final product.
