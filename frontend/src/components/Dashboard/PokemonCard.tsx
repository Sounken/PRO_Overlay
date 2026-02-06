import { motion } from 'framer-motion'
import { Pokemon } from '@/services/api'
import TypeGrid from './TypeGrid'

interface PokemonCardProps {
  pokemon: Pokemon
}

function PokemonCard({ pokemon }: PokemonCardProps) {
  const statNames = {
    hp: 'HP',
    attack: 'Attaque',
    defense: 'Défense',
    sp_attack: 'Atq. Spé',
    sp_defense: 'Déf. Spé',
    speed: 'Vitesse',
  }

  const getStatColor = (value: number): string => {
    if (value >= 150) return '#2ecc71'
    if (value >= 100) return '#3498db'
    if (value >= 70) return '#f39c12'
    return '#e74c3c'
  }

  const getStatPercentage = (value: number): number => {
    return Math.min((value / 255) * 100, 100)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      {/* Header Section */}
      <div className="flex items-start gap-8 mb-8">
        {/* Sprite */}
        <div
          className="relative w-64 h-64 rounded-2xl flex items-center justify-center"
          style={{ backgroundColor: pokemon.color }}
        >
          <img
            src={pokemon.sprite_url}
            alt={pokemon.name}
            className="w-56 h-56 object-contain drop-shadow-2xl"
          />
          {/* Generation Badge */}
          <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-bold">
            Gen {pokemon.generation}
          </div>
        </div>

        {/* Info */}
        <div className="flex-1">
          {/* Name */}
          <div className="mb-4">
            <h2 className="text-5xl font-bold mb-1">{pokemon.name}</h2>
            {pokemon.french_name && (
              <p className="text-2xl text-gray-400">{pokemon.french_name}</p>
            )}
            <p className="text-gray-500 mt-2">#{pokemon.id.toString().padStart(3, '0')}</p>
          </div>

          {/* Types */}
          <div className="flex gap-3 mb-6">
            {pokemon.types.map((type) => (
              <img src={type.icon_url} alt={type.name} className="w-40 h-10" />
            ))}
          </div>

          {/* Stats */}
          <div className="space-y-3">
            <h3 className="text-xl font-bold mb-3">Statistiques</h3>
            {Object.entries(pokemon.stats).map(([key, value]) => {
              const statName = statNames[key as keyof typeof statNames] || key
              return (
                <div key={key}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-white">
                      {statName}
                    </span>
                    <span className="text-sm font-bold text-white">{value}</span>
                  </div>
                  <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${getStatPercentage(value)}%` }}
                      transition={{ duration: 0.5, delay: 0.1 }}
                      className="h-full rounded-full"
                      style={{ backgroundColor: getStatColor(value) }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* EVs Section */}
      <div className="mb-8 p-6 bg-black/20 rounded-xl">
        <h3 className="text-xl font-bold mb-3">Effort Values (EVs)</h3>
        <div className="grid grid-cols-6 gap-4">
          {Object.entries(pokemon.evs).map(([key, value]) => (
            <div key={key} className="text-center">
              <p className="text-sm text-gray-400 mb-1">
                {statNames[key as keyof typeof statNames]}
              </p>
              <p
                className={`text-2xl font-bold ${
                  value > 0 ? 'text-secondary' : 'text-gray-600'
                }`}
              >
                +{value}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Type Effectiveness Grid */}
      <TypeGrid typeEffectiveness={pokemon.type_effectiveness} />
    </motion.div>
  )
}

export default PokemonCard
