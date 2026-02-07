import { Pokemon } from '@/services/api'
import { motion } from 'framer-motion'

interface PokemonInfoProps {
  pokemon: Pokemon
}

function PokemonInfo({ pokemon }: PokemonInfoProps) {
  const getStatColor = (value: number, maxValue: number = 150): string => {
    const percentage = value / maxValue
    // Dégradé rouge → vert basé sur le pourcentage
    if (percentage <= 0.33) {
      return '#ef4444' // Red
    } else if (percentage <= 0.66) {
      return '#eab308' // Yellow/Orange
    } else {
      return '#22c55e' // Green
    }
  }

  const getMultiplierLabel = (multiplier: number): string => {
    if (multiplier === 0) return '×0'
    if (multiplier === 0.25) return '×¼'
    if (multiplier === 0.5) return '×½'
    if (multiplier === 1) return '×1'
    if (multiplier === 2) return '×2'
    if (multiplier === 4) return '×4'
    return `×${multiplier}`
  }

  const getMultiplierColor = (multiplier: number): string => {
    if (multiplier === 0) return 'text-gray-400'
    if (multiplier < 1) return 'text-secondary'
    if (multiplier === 1) return 'text-gray-400'
    if (multiplier >= 2) return 'text-danger'
    return 'text-gray-400'
  }

  // Récupère uniquement les faiblesses (×2 et ×4)
  const weaknesses = Object.entries(pokemon.type_effectiveness)
    .filter(([_, data]) => data.multiplier >= 2)
    .sort(([_, a], [__, b]) => b.multiplier - a.multiplier)

  // Récupère uniquement les résistances (×0.5 et ×0.25)
  const resistances = Object.entries(pokemon.type_effectiveness)
    .filter(([_, data]) => 0 < data.multiplier && data.multiplier <= 0.5)
    .sort(([_, a], [__, b]) => a.multiplier - b.multiplier)

  // Récupère les immunités (×0)
  const immunities = Object.entries(pokemon.type_effectiveness).filter(
    ([_, data]) => data.multiplier === 0
  )

  // Calcule les EVs obtenus
  const totalEvs = Object.values(pokemon.evs).reduce((sum, ev) => sum + ev, 0)

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="space-y-4"
    >
      {/* Pokemon Header */}
      <div className="flex items-center gap-3">
        <div
          className="w-16 h-16 rounded-lg flex items-center justify-center"
          style={{ backgroundColor: pokemon.color }}
        >
          <img
            src={pokemon.sprite_url}
            alt={pokemon.name}
            className="w-14 h-14 object-contain"
          />
        </div>
        <div>
          <h3 className="text-xl font-bold">{pokemon.name}</h3>
          <div className="flex gap-2 mt-1">
            {pokemon.types.map((type) => (
              <span
                key={type.name}
                className="px-2 py-0.5 rounded text-xs font-semibold uppercase"
                style={{ backgroundColor: type.color }}
              >
                {type.name}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Base Stats */}
      <div className="space-y-2">
        <h4 className="text-sm font-semibold mb-2">📊 Stats</h4>
        {Object.entries(pokemon.stats).map(([stat, value]) => {
          const statLabel = {
            hp: 'HP',
            attack: 'ATK',
            defense: 'DEF',
            sp_attack: 'SP.ATK',
            sp_defense: 'SP.DEF',
            speed: 'SPD',
          }[stat as keyof typeof pokemon.stats] || stat.toUpperCase()

          return (
            <div key={stat} className="flex items-center gap-2 text-xs">
              <span className="w-12 font-semibold">{statLabel}</span>
              <div className="flex-1 h-3 bg-gray-700 rounded-full overflow-hidden">
                <div
                  style={{
                    width: `${(value / 150) * 100}%`,
                    backgroundColor: getStatColor(value),
                  }}
                  className="h-full transition-all duration-300"
                />
              </div>
              <span className="w-10 text-right font-semibold">{value}</span>
            </div>
          )
        })}
      </div>

      {/* Weaknesses */}
      {weaknesses.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-danger mb-2">
            ⚠️ Faiblesses
          </h4>
          <div className="flex flex-wrap gap-2">
            {weaknesses.map(([typeName, data]) => (
              <div
                key={typeName}
                className="px-2 py-1 bg-danger/20 border border-danger/50 rounded text-xs flex items-center gap-1"
              >
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: data.color }}
                />
                <span className="uppercase font-semibold">{typeName}</span>
                <span className={`font-bold ${getMultiplierColor(data.multiplier)}`}>
                  {getMultiplierLabel(data.multiplier)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resistances */}
      {resistances.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-secondary mb-2">
            ✓ Résistances
          </h4>
          <div className="flex flex-wrap gap-2">
            {resistances.map(([typeName, data]) => (
              <div
                key={typeName}
                className="px-2 py-1 bg-secondary/20 border border-secondary/50 rounded text-xs flex items-center gap-1"
              >
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: data.color }}
                />
                <span className="uppercase font-semibold">{typeName}</span>
                <span className={`font-bold ${getMultiplierColor(data.multiplier)}`}>
                  {getMultiplierLabel(data.multiplier)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Immunities */}
      {immunities.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-400 mb-2">
            🛡️ Immunités
          </h4>
          <div className="flex flex-wrap gap-2">
            {immunities.map(([typeName, data]) => (
              <div
                key={typeName}
                className="px-2 py-1 bg-gray-700 border border-gray-600 rounded text-xs flex items-center gap-1"
              >
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: data.color }}
                />
                <span className="uppercase font-semibold">{typeName}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* EVs */}
      {totalEvs > 0 && (
        <div className="p-3 bg-secondary/20 border border-secondary/50 rounded-lg">
          <h4 className="text-sm font-semibold mb-2">💪 EVs Obtenus</h4>
          <div className="flex flex-wrap gap-2 text-xs">
            {Object.entries(pokemon.evs)
              .filter(([_, value]) => value > 0)
              .map(([key, value]) => (
                <span key={key} className="font-semibold">
                  {key.toUpperCase()}: +{value}
                </span>
              ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default PokemonInfo
