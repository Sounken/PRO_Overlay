// Import Electron modules - require() works best for CommonJS compatibility
const { app, BrowserWindow, ipcMain, globalShortcut, screen, Menu } = require('electron');
import { spawn, ChildProcess, execSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import type { BrowserWindow as BrowserWindowType } from 'electron';

let backendProcess: ChildProcess | null = null;
let dashboardWindow: BrowserWindowType | null = null;
let overlayWindow: BrowserWindowType | null = null;
let regionSelectorWindow: BrowserWindowType | null = null;

const BACKEND_PORT = 8000;
const FRONTEND_PORT = 3000;

/**
 * Lance le serveur backend Python
 */
async function startBackend(): Promise<void> {
  console.log('🚀 Starting backend...');

  // Nettoyer les anciens processus backend sur le port
  try {
    execSync(`netstat -ano | find ":${BACKEND_PORT}"`, { encoding: 'utf-8' });
    // Si on arrive ici, il y a un processus sur le port
    execSync(`taskkill /F /IM backend.exe 2>nul || taskkill /F /IM python.exe 2>nul || echo "No process to kill"`, {
      encoding: 'utf-8',
    });
    console.log('[Backend] Cleaned up old processes');
  } catch {
    // Port is free
  }

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

  // Chemin du répertoire backend
  const backendCwd = path.join(__dirname, '..', '..', 'backend');

  if (app.isPackaged) {
    // Mode packagé: lancer le exe directement
    backendProcess = spawn(backendPath, [], {
      cwd: path.dirname(backendPath),
      detached: false, // Important: ne pas détacher le processus
    });
  } else {
    // Mode développement: utiliser spawn() pour une meilleure gestion du processus
    backendProcess = spawn(pythonPath, ['main.py', '--port', String(BACKEND_PORT)], {
      cwd: backendCwd,
      stdio: ['ignore', 'pipe', 'pipe'], // Capture stdout et stderr
    });
  }

  backendProcess?.stdout?.on('data', (data) => {
    console.log(`[Backend] ${data.toString()}`);
  });

  backendProcess?.stderr?.on('data', (data) => {
    console.error(`[Backend Error] ${data.toString()}`);
  });

  backendProcess?.on('error', (err) => {
    console.error(`[Backend] Failed to start: ${err.message}`);
  });

  backendProcess?.on('close', (code) => {
    console.log(`Backend exited with code ${code}`);
  });

  // Attendre que le backend soit prêt (timeout réduit à 15 secondes)
  await waitForBackend(`http://localhost:${BACKEND_PORT}/health`, 15);
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
    ? `file://${path.join(__dirname, '..', 'dist', 'index.html')}`
    : `http://localhost:${FRONTEND_PORT}`;

  dashboardWindow.loadURL(url);

  // F12 pour DevTools (mode dev et production)
  dashboardWindow.webContents.on('before-input-event', (_event: any, input: any) => {
    if (input.key === 'F12') {
      dashboardWindow?.webContents.toggleDevTools();
    }
  });

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

  // Dimensions de l'overlay (augmentées pour afficher les stats + recommendation banner)
  const overlayWidth = 420;
  const overlayHeight = 850;

  // Position en haut à droite avec 10% de marge (20% - 10% = 10%)
  // Puis on décale de +5% en bas
  const marginXPercent = 0.1;
  const marginYPercent = 0.25;
  const x = screenWidth - overlayWidth - (screenWidth * marginXPercent);
  const y = screenHeight * marginYPercent;

  overlayWindow = new BrowserWindow({
    width: overlayWidth,
    height: overlayHeight,
    x: Math.floor(x),
    y: Math.floor(y),
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    focusable: false, // Ne pas prendre le focus du jeu
    hasShadow: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    show: false, // Caché par défaut, toggle avec F9
  });

  // Forcer à rester toujours au premier plan
  overlayWindow.setAlwaysOnTop(true, 'screen-saver', 1);

  const url = app.isPackaged
    ? `file://${path.join(__dirname, '..', 'dist', 'index.html')}#overlay`
    : `http://localhost:${FRONTEND_PORT}#overlay`;

  overlayWindow.loadURL(url);

  // Réappliquer alwaysOnTop quand la fenêtre gagne le focus
  overlayWindow.on('focus', () => {
    overlayWindow?.setAlwaysOnTop(true, 'screen-saver', 1);
  });

  overlayWindow.on('show', () => {
    overlayWindow?.setAlwaysOnTop(true, 'screen-saver', 1);
  });

  overlayWindow.on('closed', () => {
    overlayWindow = null;
  });
}

/**
 * Config helpers
 */
function getConfigPath(): string {
  if (!app.isPackaged) {
    // Development mode: use project root
    // __dirname is dist-electron, so .. goes to frontend, .. goes to project root
    return path.join(__dirname, '..', '..', 'config.json');
  }

  // Packaged mode: try multiple possible locations
  const possiblePaths = [
    path.join(process.resourcesPath, 'config.json'),
    path.join(path.dirname(process.execPath), 'resources', 'config.json'),
    path.join(__dirname, 'config.json'),
  ];

  for (const configPath of possiblePaths) {
    if (fs.existsSync(configPath)) {
      console.log(`[Config] Found config.json at: ${configPath}`);
      return configPath;
    }
  }

  // Default to first option even if it doesn't exist (for error handling)
  console.log(`[Config] Using default path: ${possiblePaths[0]}`);
  return possiblePaths[0];
}

function readConfig(): Record<string, any> {
  const configPath = getConfigPath();
  try {
    if (!fs.existsSync(configPath)) {
      console.error(`[Config] File not found at: ${configPath}`);
      throw new Error(`Config file not found at: ${configPath}`);
    }
    const raw = fs.readFileSync(configPath, 'utf-8');
    return JSON.parse(raw);
  } catch (error) {
    console.error(`[Config] Error reading config: ${error}`);
    throw error;
  }
}

function writeConfig(config: Record<string, any>): void {
  const configPath = getConfigPath();
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
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
    ? `file://${path.join(__dirname, '..', 'dist', 'index.html')}#region-selector`
    : `http://localhost:${FRONTEND_PORT}#region-selector`;

  console.log(`[RegionSelector] Loading URL: ${url}`);
  regionSelectorWindow.loadURL(url);
  regionSelectorWindow.setAlwaysOnTop(true, 'screen-saver');

  regionSelectorWindow.webContents.on('did-finish-load', () => {
    console.log('[RegionSelector] Page loaded successfully');
  });

  regionSelectorWindow.webContents.on('did-fail-load', (_event: any, errorCode: any, errorDescription: any) => {
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
        overlayWindow.setAlwaysOnTop(true, 'screen-saver', 1);
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
   * Avant la fermeture: tuer les processus backend (dernière ligne de défense)
   */
  app.on('before-quit', () => {
  console.log('[before-quit] Final cleanup...');

  // Triple kill strategy
  try {
    execSync('taskkill /F /IM backend.exe /T 2>nul', { stdio: 'ignore' });
    console.log('[before-quit] ✅ Killed backend.exe');
  } catch {}

  try {
    execSync('taskkill /F /IM python.exe /T 2>nul', { stdio: 'ignore' });
    console.log('[before-quit] ✅ Killed python.exe');
  } catch {}

  // Also kill by port (netstat + taskkill)
  try {
    const output = execSync(`netstat -ano | findstr :${BACKEND_PORT}`, { encoding: 'utf-8', stdio: 'pipe' });
    const match = output.match(/\s+(\d+)\s*$/m);
    if (match) {
      const pid = match[1];
      execSync(`taskkill /F /PID ${pid} /T 2>nul`, { stdio: 'ignore' });
      console.log(`[before-quit] ✅ Killed PID ${pid} on port ${BACKEND_PORT}`);
    }
  } catch {}

  if (backendProcess?.pid) {
    try {
      process.kill(-backendProcess.pid); // Kill entire process group
      console.log(`[before-quit] ✅ Killed process group ${backendProcess.pid}`);
    } catch {}
  }

  console.log('[before-quit] ✅ Cleanup complete');
});

/**
 * À la fermeture finale
 */
app.on('quit', () => {
  console.log('👋 Application closed');
});

/**
 * Helper: Kill all backend processes
 * Uses spawn (non-blocking) instead of execSync
 */
function killBackendProcesses(): void {
  // Kill backend.exe, python.exe, python3.exe
  // Using spawn is non-blocking and more reliable than execSync
  spawn('cmd.exe', ['/c', 'taskkill /F /IM backend.exe /T 2>nul & taskkill /F /IM python.exe /T 2>nul & taskkill /F /IM python3.exe /T 2>nul'], {
    detached: false,
    stdio: 'ignore',
    windowsHide: true,
  });

  // Also kill the Node process object directly
  if (backendProcess) {
    try {
      backendProcess.kill('SIGKILL');
    } catch {}
    backendProcess = null;
  }
}

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
    console.log('[window-all-closed] Closing all windows');
    killBackendProcesses();
    globalShortcut.unregisterAll();
    console.log('[window-all-closed] Calling app.quit()');
    app.quit();
  }
});

/**
 * Final cleanup before quit
 */
app.on('before-quit', () => {
  console.log('[before-quit] Final cleanup');
  killBackendProcesses();
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

ipcMain.handle('set-overlay-position', (_event, x: number, y: number) => {
  if (overlayWindow) {
    overlayWindow.setPosition(Math.floor(x), Math.floor(y));
  }
});

ipcMain.handle('get-auto-battle', () => {
  const config = readConfig();
  return config.overlay?.autoBattle ?? false;
});

ipcMain.handle('set-auto-battle', (_event, enabled: boolean) => {
  const config = readConfig();
  if (!config.overlay) config.overlay = {};
  config.overlay.autoBattle = enabled;
  writeConfig(config);
  return true;
});

/**
 * Gestion d'équipe
 */
let teamRegionSelectorWindow: BrowserWindowType | null = null;

function createTeamRegionSelectorWindow(): void {
  teamRegionSelectorWindow = new BrowserWindow({
    fullscreen: true,
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
    ? `file://${path.join(__dirname, '..', 'dist', 'index.html')}#team-region-selector`
    : `http://localhost:${FRONTEND_PORT}#team-region-selector`;

  teamRegionSelectorWindow.loadURL(url);
  teamRegionSelectorWindow.setAlwaysOnTop(true, 'screen-saver');

  teamRegionSelectorWindow.on('closed', () => {
    teamRegionSelectorWindow = null;
  });
}

ipcMain.handle('get-team', () => {
  const config = readConfig();
  return config.team ?? { pokemon: [], active_pokemon: null, team_region: null };
});

ipcMain.handle('save-team', (_event, team: { pokemon: Array<{ name: string; slot: number }>; active_pokemon?: string }) => {
  const config = readConfig();
  if (!config.team) config.team = {};
  config.team.pokemon = team.pokemon;
  config.team.active_pokemon = team.active_pokemon ?? null;
  writeConfig(config);
  return true;
});

ipcMain.handle('add-team-member', (_event, name: string) => {
  const config = readConfig();
  if (!config.team) config.team = { pokemon: [], active_pokemon: null };

  if (config.team.pokemon.length >= 6) {
    return { success: false, error: 'Team is full (max 6)' };
  }

  const nextSlot = (config.team.pokemon || []).length + 1;
  if (!config.team.pokemon) config.team.pokemon = [];
  config.team.pokemon.push({ name, slot: nextSlot });
  writeConfig(config);
  return { success: true };
});

ipcMain.handle('remove-team-member', (_event, slot: number) => {
  const config = readConfig();
  if (!config.team || !config.team.pokemon) return true;

  config.team.pokemon = config.team.pokemon.filter((p: any) => p.slot !== slot);
  // Réordonner les slots
  config.team.pokemon.forEach((p: any, idx: number) => {
    p.slot = idx + 1;
  });
  writeConfig(config);
  return true;
});

ipcMain.handle('set-active-pokemon', (_event, name: string) => {
  const config = readConfig();
  if (!config.team) config.team = {};
  config.team.active_pokemon = name;
  writeConfig(config);
  return true;
});

ipcMain.handle('get-team-region', () => {
  const config = readConfig();
  return config.team?.team_region ?? null;
});

ipcMain.handle('save-team-region', (_event, region: { x: number; y: number; width: number; height: number }) => {
  const config = readConfig();
  const scaleFactor = screen.getPrimaryDisplay().scaleFactor;
  if (!config.team) config.team = { pokemon: [], active_pokemon: null };
  config.team.team_region = {
    enabled: true,
    x: Math.round(region.x * scaleFactor),
    y: Math.round(region.y * scaleFactor),
    width: Math.round(region.width * scaleFactor),
    height: Math.round(region.height * scaleFactor),
  };
  writeConfig(config);
  return true;
});

ipcMain.handle('open-team-region-selector', () => {
  createTeamRegionSelectorWindow();
});

ipcMain.handle('close-team-region-selector', () => {
  if (teamRegionSelectorWindow) {
    teamRegionSelectorWindow.close();
    teamRegionSelectorWindow = null;
  }
});
