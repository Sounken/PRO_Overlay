import { Pokemon } from '@/services/api'

interface PokemonInfoProps {
  pokemon: Pokemon
}

function PokemonInfo({ pokemon }: PokemonInfoProps) {
  // Récupère uniquement les faiblesses (×2 et ×4)
  const weaknesses = Object.entries(pokemon.type_effectiveness)
    .filter(([_, data]) => data.multiplier >= 2)
    .sort(([_, a], [__, b]) => b.multiplier - a.multiplier)
    .slice(0, 3)

  // Récupère uniquement les résistances (×0.5 et ×0.25)
  const resistances = Object.entries(pokemon.type_effectiveness)
    .filter(([_, data]) => 0 < data.multiplier && data.multiplier <= 0.5)
    .sort(([_, a], [__, b]) => a.multiplier - b.multiplier)
    .slice(0, 3)

  // Récupère les EVs obtenus
  const totalEvs = Object.values(pokemon.evs).reduce((sum, ev) => sum + ev, 0)
  const evEntry = Object.entries(pokemon.evs).find(([_, v]) => v > 0)

  const getStatGlowColor = (value: number, maxValue: number = 150) => {
    const percentage = value / maxValue
    if (percentage >= 0.66) return '#55ee66'
    if (percentage >= 0.4) return '#ffcc00'
    return '#ff4422'
  }

  const getStatBarWidth = (value: number, maxValue: number = 150) => {
    return Math.min((value / maxValue) * 100, 100)
  }

  return (
    <div className="relative w-full bg-[#1e1e26] rounded-[30px] p-6 shadow-2xl border border-white/10 overflow-visible">
      {/* ID Badge */}
      <div className="absolute top-4 right-6 text-7xl font-black text-white/5 select-none tracking-tighter">
        #{String(pokemon.id).padStart(4, '0')}
      </div>

      <div className="relative z-10">
        {/* Titre et Types */}
        <h1 className="text-2xl font-bold tracking-tight uppercase italic mb-3">{pokemon.name}</h1>
        <div className="flex gap-2">
          {pokemon.types.map((type) => (
            <img
              key={type.name}
              src={type.icon_url}
              alt={type.name}
              className="w-[86px] h-5"
            />
          ))}
        </div>
      </div>

      {/* Pokemon Image */}
      <div className="relative h-44 flex justify-center items-center -mt-4">
        <div
          className="absolute w-32 h-32 rounded-full blur-3xl opacity-30"
          style={{ backgroundColor: pokemon.color }}
        ></div>
        <img
          src={pokemon.sprite_url}
          alt={pokemon.name}
          className="relative z-10 w-40 drop-shadow-[0_10px_20px_rgba(0,0,0,0.5)] transition-transform"
        />
      </div>

      {/* Stats */}
      <div className="space-y-3 mt-2">
        {Object.entries(pokemon.stats).map(([statKey, value]) => {
          const statLabel = {
            hp: 'PV',
            attack: 'ATK',
            defense: 'DEF',
            sp_attack: 'SPAT',
            sp_defense: 'SPDF',
            speed: 'VIT',
          }[statKey as keyof typeof pokemon.stats] || statKey.toUpperCase()

          const glowColor = getStatGlowColor(value)
          const barWidth = getStatBarWidth(value)

          return (
            <div key={statKey} className="flex items-center gap-3">
              <span className="w-8 text-[11px] font-bold text-gray-400">{statLabel}</span>
              <span className="w-6 text-sm font-bold text-right">{value}</span>
              <div className="flex-1 h-1.5 bg-black rounded-full overflow-hidden shadow-inner">
                <div
                  className="h-full rounded-full transition-all duration-300"
                  style={{
                    width: `${barWidth}%`,
                    backgroundColor: glowColor,
                    boxShadow: `0 0 8px ${glowColor}`,
                  }}
                ></div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Faiblesses et Résistances */}
      <div className="grid grid-cols-2 gap-3 mt-4">
        <div>
          <h4 className="text-[10px] uppercase font-bold text-gray-400 mb-2 tracking-widest">
            Weaknesses
          </h4>
          <div className="flex flex-wrap gap-1">
            {weaknesses.map(([typeName, data]) => (
              <div
                key={typeName}
                className="flex flex-col items-center px-2 py-1 rounded-lg border-2 border-white/10"
                style={{ backgroundColor: data.color + '33', borderColor: data.color }}
              >
                <span className="text-[11px] font-black leading-tight">
                  {typeName.toUpperCase().slice(0, 5)}
                </span>
                <span className="text-[10px] font-bold text-white">
                  {data.multiplier === 4 ? '×4' : '×2'}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div>
          <h4 className="text-[10px] uppercase font-bold text-gray-400 mb-2 tracking-widest">
            Resistances
          </h4>
          <div className="flex flex-wrap gap-1">
            {resistances.map(([typeName, data]) => (
              <div
                key={typeName}
                className="flex flex-col items-center px-2 py-1 rounded-lg border-2 border-white/10"
                style={{ backgroundColor: data.color + '33', borderColor: data.color }}
              >
                <span className="text-[11px] font-black leading-tight">
                  {typeName.toUpperCase().slice(0, 5)}
                </span>
                <span className="text-[10px] font-bold text-white">
                  {data.multiplier === 0.25 ? '÷4' : '÷2'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* EVs */}
      {totalEvs > 0 && evEntry && (
        <div className="mt-6 flex items-stretch bg-gradient-to-r from-[#2a2a35] to-[#1e1e26] rounded-xl border border-white/10 overflow-hidden">
          <div className="bg-white/5 px-3 py-2 text-[10px] font-black text-gray-400 flex items-center border-r border-white/5">
            EV
          </div>
          <div className="flex-1 px-3 py-2 text-[12px] font-bold text-[#00b844] flex items-center justify-center tracking-wide">
            +{evEntry[1]} {evEntry[0].toUpperCase()}
          </div>
        </div>
      )}
    </div>
  )
}

export default PokemonInfo
