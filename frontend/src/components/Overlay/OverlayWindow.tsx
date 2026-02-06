import { useState, useEffect } from 'react'
import { pokemonAPI, Pokemon } from '@/services/api'
import PokemonInfo from './PokemonInfo'
import { motion } from 'framer-motion'

function OverlayWindow() {
  const [pokemon, setPokemon] = useState<Pokemon | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Simule la détection OCR automatique
  const detectPokemon = async () => {
    setLoading(true)
    setError(null)

    try {
      // Détection OCR (capture automatique de la région définie)
      const detection = await pokemonAPI.detectPokemon()

      // Récupère les données du Pokémon détecté
      const data = await pokemonAPI.getPokemon(detection.pokemon_name)
      setPokemon(data)
    } catch (err) {
      setError('Aucun Pokémon détecté')
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
