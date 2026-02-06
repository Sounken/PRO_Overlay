import { useState } from 'react'
import { pokemonAPI, Pokemon } from '@/services/api'
import PokemonCard from './PokemonCard'
import { motion } from 'framer-motion'

function Pokedex() {
  const [search, setSearch] = useState('')
  const [pokemon, setPokemon] = useState<Pokemon | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!search.trim()) return

    setLoading(true)
    setError(null)
    setPokemon(null)

    try {
      const data = await pokemonAPI.getPokemon(search.toLowerCase().trim())
      setPokemon(data)
    } catch (err) {
      setError(`Pokémon "${search}" non trouvé`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Pokédex</h1>
        <p className="text-gray-400">
          Recherchez un Pokémon par nom anglais ou numéro
        </p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Ex: Gengar, 94, Pikachu..."
            className="flex-1 px-6 py-4 bg-surface rounded-xl border border-white/10 focus:border-primary focus:outline-none transition-colors text-lg"
          />
          <motion.button
            type="submit"
            disabled={loading}
            className="px-8 py-4 bg-primary hover:bg-primary/80 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? 'Recherche...' : 'Rechercher'}
          </motion.button>
        </div>
      </form>

      {/* Error */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-danger/20 border border-danger/50 rounded-xl p-4 mb-8"
        >
          <p className="text-danger font-medium">{error}</p>
        </motion.div>
      )}

      {/* Pokemon Card */}
      {pokemon && <PokemonCard pokemon={pokemon} />}

      {/* Empty State */}
      {!pokemon && !error && !loading && (
        <div className="text-center py-20">
          <p className="text-6xl mb-4">🔍</p>
          <p className="text-gray-400 text-lg">
            Recherchez un Pokémon pour afficher ses informations
          </p>
        </div>
      )}
    </div>
  )
}

export default Pokedex
