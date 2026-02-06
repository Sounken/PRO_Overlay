import { contextBridge, ipcRenderer } from 'electron';

/**
 * API exposée au renderer process
 */
contextBridge.exposeInMainWorld('electronAPI', {
  /**
   * Récupère l'URL du backend
   */
  getBackendUrl: (): Promise<string> => ipcRenderer.invoke('get-backend-url'),

  /**
   * Toggle l'overlay
   */
  toggleOverlay: (): Promise<void> => ipcRenderer.invoke('toggle-overlay'),
});

// Type definitions pour TypeScript
declare global {
  interface Window {
    electronAPI: {
      getBackendUrl: () => Promise<string>;
      toggleOverlay: () => Promise<void>;
    };
  }
}
