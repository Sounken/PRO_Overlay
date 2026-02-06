import axios from 'axios'

// Récupère l'URL du backend depuis Electron
const getBackendUrl = async (): Promise<string> => {
  if (window.electronAPI) {
    return await window.electronAPI.getBackendUrl()
  }
  // Fallback pour le développement
  return 'http://localhost:8000'
}

// Instance Axios configurée
const api = axios.create({
  timeout: 10000,
})

// Intercepteur pour définir l'URL de base dynamiquement
api.interceptors.request.use(async (config) => {
  const baseURL = await getBackendUrl()
  config.baseURL = baseURL
  return config
})

/**
 * Types
 */
export interface PokemonType {
  name: string
  color: string
  icon_url: string
}

export interface PokemonStats {
  hp: number
  attack: number
  defense: number
  sp_attack: number
  sp_defense: number
  speed: number
}

export interface EffortValues {
  hp: number
  attack: number
  defense: number
  sp_attack: number
  sp_defense: number
  speed: number
}

export interface TypeEffectiveness {
  type_name: string
  multiplier: number
  color: string
}

export interface Pokemon {
  id: number
  name: string
  french_name?: string
  types: PokemonType[]
  stats: PokemonStats
  evs: EffortValues
  sprite_url: string
  color: string
  generation: number
  type_effectiveness: Record<string, TypeEffectiveness>
}

export interface OCRDetection {
  pokemon_name: string
  confidence: number
  timestamp: string
}

export interface OCRRegion {
  x: number
  y: number
  width: number
  height: number
}

/**
 * API Methods
 */
export const pokemonAPI = {
  /**
   * Récupère les données d'un Pokémon
   */
  getPokemon: async (identifier: string): Promise<Pokemon> => {
    const response = await api.get(`/pokemon/${identifier}`)
    return response.data
  },

  /**
   * Détecte un Pokémon via OCR
   */
  detectPokemon: async (region?: OCRRegion): Promise<OCRDetection> => {
    const response = await api.post('/ocr/detect', { region })
    return response.data
  },

  /**
   * Récupère les stats du cache
   */
  getCacheStats: async () => {
    const response = await api.get('/cache/stats')
    return response.data
  },

  /**
   * Vide le cache
   */
  clearCache: async (pokemon?: string) => {
    const params = pokemon ? { pokemon } : {}
    const response = await api.delete('/cache/clear', { params })
    return response.data
  },

  /**
   * Vérifie que le backend est prêt
   */
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await api.get('/health')
      return response.data.status === 'ok'
    } catch {
      return false
    }
  },
}

export default api
