import { app, BrowserWindow, ipcMain, globalShortcut, screen } from 'electron';
import { spawn, ChildProcess } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let backendProcess: ChildProcess | null = null;
let dashboardWindow: BrowserWindow | null = null;
let overlayWindow: BrowserWindow | null = null;

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

  // Commande à exécuter
  // Sur Windows, utiliser 'py' (Python launcher) plutôt que 'python'
  const pythonCommand = process.platform === 'win32' ? 'py' : 'python3';
  const command = app.isPackaged ? backendPath : pythonCommand;
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
  dashboardWindow = new BrowserWindow({
    width: 1200,
    height: 800,
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

  // DevTools en mode développement
  if (!app.isPackaged) {
    dashboardWindow.webContents.openDevTools();
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
