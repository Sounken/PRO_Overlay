import { contextBridge, ipcRenderer } from 'electron';

/**
 * API exposée au renderer process
 */
contextBridge.exposeInMainWorld('electronAPI', {
  getBackendUrl: (): Promise<string> => ipcRenderer.invoke('get-backend-url'),
  toggleOverlay: (): Promise<void> => ipcRenderer.invoke('toggle-overlay'),
  getOcrRegion: (): Promise<{ enabled: boolean; x: number; y: number; width: number; height: number } | null> =>
    ipcRenderer.invoke('get-ocr-region'),
  saveOcrRegion: (region: { x: number; y: number; width: number; height: number }): Promise<boolean> =>
    ipcRenderer.invoke('save-ocr-region', region),
  openRegionSelector: (): Promise<void> => ipcRenderer.invoke('open-region-selector'),
  closeRegionSelector: (): Promise<void> => ipcRenderer.invoke('close-region-selector'),
  getScreenInfo: (): Promise<{ width: number; height: number; scaleFactor: number }> =>
    ipcRenderer.invoke('get-screen-info'),
});

// Type definitions pour TypeScript
declare global {
  interface Window {
    electronAPI: {
      getBackendUrl: () => Promise<string>;
      toggleOverlay: () => Promise<void>;
      getOcrRegion: () => Promise<{ enabled: boolean; x: number; y: number; width: number; height: number } | null>;
      saveOcrRegion: (region: { x: number; y: number; width: number; height: number }) => Promise<boolean>;
      openRegionSelector: () => Promise<void>;
      closeRegionSelector: () => Promise<void>;
      getScreenInfo: () => Promise<{ width: number; height: number; scaleFactor: number }>;
    };
  }
}
