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
  setOverlayPosition: (x: number, y: number): Promise<void> =>
    ipcRenderer.invoke('set-overlay-position', x, y),
  getAutoBattle: (): Promise<boolean> =>
    ipcRenderer.invoke('get-auto-battle'),
  setAutoBattle: (enabled: boolean): Promise<boolean> =>
    ipcRenderer.invoke('set-auto-battle', enabled),
  // Team management
  getTeam: (): Promise<any> =>
    ipcRenderer.invoke('get-team'),
  saveTeam: (team: any): Promise<boolean> =>
    ipcRenderer.invoke('save-team', team),
  addTeamMember: (name: string): Promise<{ success: boolean; error?: string }> =>
    ipcRenderer.invoke('add-team-member', name),
  removeTeamMember: (slot: number): Promise<boolean> =>
    ipcRenderer.invoke('remove-team-member', slot),
  setActivePokemon: (name: string): Promise<boolean> =>
    ipcRenderer.invoke('set-active-pokemon', name),
  getTeamRegion: (): Promise<{ enabled: boolean; x: number; y: number; width: number; height: number } | null> =>
    ipcRenderer.invoke('get-team-region'),
  saveTeamRegion: (region: { x: number; y: number; width: number; height: number }): Promise<boolean> =>
    ipcRenderer.invoke('save-team-region', region),
  openTeamRegionSelector: (): Promise<void> =>
    ipcRenderer.invoke('open-team-region-selector'),
  closeTeamRegionSelector: (): Promise<void> =>
    ipcRenderer.invoke('close-team-region-selector'),
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
      setOverlayPosition: (x: number, y: number) => Promise<void>;
      getAutoBattle: () => Promise<boolean>;
      setAutoBattle: (enabled: boolean) => Promise<boolean>;
      // Team management
      getTeam: () => Promise<any>;
      saveTeam: (team: any) => Promise<boolean>;
      addTeamMember: (name: string) => Promise<{ success: boolean; error?: string }>;
      removeTeamMember: (slot: number) => Promise<boolean>;
      setActivePokemon: (name: string) => Promise<boolean>;
      getTeamRegion: () => Promise<{ enabled: boolean; x: number; y: number; width: number; height: number } | null>;
      saveTeamRegion: (region: { x: number; y: number; width: number; height: number }) => Promise<boolean>;
      openTeamRegionSelector: () => Promise<void>;
      closeTeamRegionSelector: () => Promise<void>;
    };
  }
}
