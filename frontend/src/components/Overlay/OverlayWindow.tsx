import { useState, useEffect, useRef } from 'react'
import { pokemonAPI, Pokemon, OCRRegion } from '@/services/api'
import PokemonInfo from './PokemonInfo'
import { motion } from 'framer-motion'

function OverlayWindow() {
  const [pokemon, setPokemon] = useState<Pokemon | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const ocrRegionRef = useRef<OCRRegion | undefined>(undefined)

  // Charge la région OCR sauvegardée
  useEffect(() => {
    const loadRegion = async () => {
      if (window.electronAPI) {
        const config = await window.electronAPI.getOcrRegion()
        if (config && config.enabled) {
          ocrRegionRef.current = {
            x: config.x,
            y: config.y,
            width: config.width,
            height: config.height,
          }
        }
      }
    }
    loadRegion()
  }, [])

  const detectPokemon = async () => {
    setLoading(true)
    setError(null)

    try {
      const detection = await pokemonAPI.detectPokemon(ocrRegionRef.current)
      const data = await pokemonAPI.getPokemon(detection.pokemon_name)
      setPokemon(data)
    } catch (err) {
      setError('Aucun Pokemon detecte')
      setPokemon(null)
    } finally {
      setLoading(false)
    }
  }

  // Détection automatique toutes les 2 secondes
  useEffect(() => {
    const interval = setInterval(() => {
      detectPokemon()
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="w-full h-full glass p-4 rounded-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold">PRO Overlay</h2>
        <div className="flex items-center gap-2">
          {loading && (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full"
            />
          )}
          <span className="text-xs text-gray-400">F9 pour toggle</span>
        </div>
      </div>

      {/* Content */}
      {pokemon ? (
        <PokemonInfo pokemon={pokemon} />
      ) : (
        <div className="flex flex-col items-center justify-center h-64 text-center">
          {error ? (
            <>
              <p className="text-4xl mb-2">❌</p>
              <p className="text-sm text-gray-400">{error}</p>
            </>
          ) : (
            <>
              <p className="text-4xl mb-2">🔍</p>
              <p className="text-sm text-gray-400">
                Détection automatique en cours...
              </p>
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default OverlayWindow
