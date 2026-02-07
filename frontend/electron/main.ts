import { app, BrowserWindow, ipcMain, globalShortcut, screen, Menu } from 'electron';
import { spawn, ChildProcess, execSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let backendProcess: ChildProcess | null = null;
let dashboardWindow: BrowserWindow | null = null;
let overlayWindow: BrowserWindow | null = null;
let regionSelectorWindow: BrowserWindow | null = null;

const BACKEND_PORT = 8000;
const FRONTEND_PORT = 3000;

/**
 * Lance le serveur backend Python
 */
async function startBackend(): Promise<void> {
  console.log('🚀 Starting backend...');

  // Chemin du backend compilé
  const backendPath = app.isPackaged
    ? path.join(process.resourcesPath, 'backend', 'backend.exe')
    : path.join(__dirname, '..', '..', 'backend', 'main.py');

  // Trouver le chemin Python (py launcher donne le vrai chemin, pas l'alias Windows Store)
  let pythonPath = 'python3';
  if (!app.isPackaged) {
    const commands = [
      'py -c "import sys; print(sys.executable)"',
      'python -c "import sys; print(sys.executable)"',
    ];
    for (const cmd of commands) {
      try {
        const result = execSync(cmd, { encoding: 'utf-8', timeout: 5000 }).trim();
        if (result && fs.existsSync(result)) {
          pythonPath = result;
          console.log(`[Backend] Python found at: ${pythonPath}`);
          break;
        }
      } catch {
        // Try next command
      }
    }
  }

  const command = app.isPackaged ? backendPath : pythonPath;
  const args = app.isPackaged ? [] : [backendPath, '--port', BACKEND_PORT.toString()];

  // Lancement du subprocess
  backendProcess = spawn(command, args, {
    cwd: app.isPackaged ? path.dirname(backendPath) : path.join(__dirname, '..', '..', 'backend'),
  });

  backendProcess.stdout?.on('data', (data) => {
    console.log(`[Backend] ${data.toString()}`);
  });

  backendProcess.stderr?.on('data', (data) => {
    console.error(`[Backend Error] ${data.toString()}`);
  });

  backendProcess.on('error', (err) => {
    console.error(`[Backend] Failed to start: ${err.message}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend exited with code ${code}`);
  });

  // Attendre que le backend soit prêt
  await waitForBackend(`http://localhost:${BACKEND_PORT}/health`);
  console.log('✅ Backend ready!');
}

/**
 * Attend que le backend réponde
 */
async function waitForBackend(url: string, maxAttempts = 30): Promise<void> {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const response = await fetch(url);
      if (response.ok) {
        return;
      }
    } catch (error) {
      // Backend pas encore prêt
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  throw new Error('Backend failed to start in time');
}

/**
 * Crée la fenêtre Dashboard
 */
function createDashboardWindow(): void {
  // Supprimer la barre de menu
  Menu.setApplicationMenu(null);

  dashboardWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    title: 'PRO Helper - Dashboard',
    backgroundColor: '#1e1e2e',
  });

  const url = app.isPackaged
    ? `file://${path.join(__dirname, '..', 'index.html')}`
    : `http://localhost:${FRONTEND_PORT}`;

  dashboardWindow.loadURL(url);

  // F12 pour DevTools en mode dev
  if (!app.isPackaged) {
    dashboardWindow.webContents.on('before-input-event', (_event, input) => {
      if (input.key === 'F12') {
        dashboardWindow?.webContents.toggleDevTools();
      }
    });
  }

  dashboardWindow.on('closed', () => {
    dashboardWindow = null;
  });
}

/**
 * Crée la fenêtre Overlay
 */
function createOverlayWindow(): void {
  const primaryDisplay = screen.getPrimaryDisplay();
  const { width: screenWidth, height: screenHeight } = primaryDisplay.workAreaSize;

  // Dimensions de l'overlay
  const overlayWidth = 400;
  const overlayHeight = 500;

  // Position en haut à droite avec 20% de marge
  const marginPercent = 0.2;
  const x = screenWidth - overlayWidth - (screenWidth * marginPercent);
  const y = screenHeight * marginPercent;

  overlayWindow = new BrowserWindow({
    width: overlayWidth,
    height: overlayHeight,
    x: Math.floor(x),
    y: Math.floor(y),
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    show: false, // Caché par défaut, toggle avec F9
  });

  const url = app.isPackaged
    ? `file://${path.join(__dirname, '..', 'index.html')}#overlay`
    : `http://localhost:${FRONTEND_PORT}#overlay`;

  overlayWindow.loadURL(url);

  overlayWindow.on('closed', () => {
    overlayWindow = null;
  });
}

/**
 * Config helpers
 */
function getConfigPath(): string {
  return app.isPackaged
    ? path.join(process.resourcesPath, 'config.json')
    : path.join(__dirname, '..', '..', 'config.json');
}

function readConfig(): Record<string, any> {
  const raw = fs.readFileSync(getConfigPath(), 'utf-8');
  return JSON.parse(raw);
}

function writeConfig(config: Record<string, any>): void {
  fs.writeFileSync(getConfigPath(), JSON.stringify(config, null, 2), 'utf-8');
}

/**
 * Crée la fenêtre de sélection de zone OCR
 */
function createRegionSelectorWindow(): void {
  console.log('[RegionSelector] Creating window...');

  if (regionSelectorWindow) {
    console.log('[RegionSelector] Window already exists, focusing');
    regionSelectorWindow.focus();
    return;
  }

  const primaryDisplay = screen.getPrimaryDisplay();
  const { width, height } = primaryDisplay.size;
  console.log(`[RegionSelector] Screen size: ${width}x${height}`);

  regionSelectorWindow = new BrowserWindow({
    x: 0,
    y: 0,
    width: width,
    height: height,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    resizable: false,
    fullscreenable: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  const url = app.isPackaged
    ? `file://${path.join(__dirname, '..', 'index.html')}#region-selector`
    : `http://localhost:${FRONTEND_PORT}#region-selector`;

  console.log(`[RegionSelector] Loading URL: ${url}`);
  regionSelectorWindow.loadURL(url);
  regionSelectorWindow.setAlwaysOnTop(true, 'screen-saver');

  regionSelectorWindow.webContents.on('did-finish-load', () => {
    console.log('[RegionSelector] Page loaded successfully');
  });

  regionSelectorWindow.webContents.on('did-fail-load', (_event, errorCode, errorDescription) => {
    console.error(`[RegionSelector] Failed to load: ${errorCode} - ${errorDescription}`);
  });

  regionSelectorWindow.on('closed', () => {
    console.log('[RegionSelector] Window closed');
    regionSelectorWindow = null;
  });
}

/**
 * Toggle l'overlay avec F9
 */
function registerHotkeys(): void {
  globalShortcut.register('F9', () => {
    if (overlayWindow) {
      if (overlayWindow.isVisible()) {
        overlayWindow.hide();
      } else {
        overlayWindow.show();
      }
    }
  });
}

/**
 * Initialisation de l'application
 */
app.on('ready', async () => {
  try {
    await startBackend();
    createDashboardWindow();
    createOverlayWindow();
    registerHotkeys();
  } catch (error) {
    console.error('Failed to start application:', error);
    app.quit();
  }
});

/**
 * Fermeture propre
 */
app.on('quit', () => {
  if (backendProcess) {
    backendProcess.kill();
    console.log('Backend process terminated');
  }
  globalShortcut.unregisterAll();
});

/**
 * macOS: Re-créer la fenêtre si toutes sont fermées
 */
app.on('activate', () => {
  if (dashboardWindow === null) {
    createDashboardWindow();
  }
});

/**
 * Fermer l'app si toutes les fenêtres sont fermées (sauf macOS)
 */
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

/**
 * IPC handlers
 */
ipcMain.handle('get-backend-url', () => {
  return `http://localhost:${BACKEND_PORT}`;
});

ipcMain.handle('toggle-overlay', () => {
  if (overlayWindow) {
    if (overlayWindow.isVisible()) {
      overlayWindow.hide();
    } else {
      overlayWindow.show();
    }
  }
});

ipcMain.handle('get-ocr-region', () => {
  const config = readConfig();
  return config.ocr?.region ?? null;
});

ipcMain.handle('save-ocr-region', (_event, region: { x: number; y: number; width: number; height: number }) => {
  const config = readConfig();
  const scaleFactor = screen.getPrimaryDisplay().scaleFactor;
  config.ocr.region = {
    enabled: true,
    x: Math.round(region.x * scaleFactor),
    y: Math.round(region.y * scaleFactor),
    width: Math.round(region.width * scaleFactor),
    height: Math.round(region.height * scaleFactor),
  };
  writeConfig(config);
  return true;
});

ipcMain.handle('open-region-selector', () => {
  console.log('[IPC] open-region-selector called');
  createRegionSelectorWindow();
});

ipcMain.handle('close-region-selector', () => {
  if (regionSelectorWindow) {
    regionSelectorWindow.close();
    regionSelectorWindow = null;
  }
});

ipcMain.handle('get-screen-info', () => {
  const primaryDisplay = screen.getPrimaryDisplay();
  return {
    width: primaryDisplay.size.width,
    height: primaryDisplay.size.height,
    scaleFactor: primaryDisplay.scaleFactor,
  };
});
