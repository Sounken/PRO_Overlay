import { TypeEffectiveness } from '@/services/api'

interface TypeGridProps {
  typeEffectiveness: Record<string, TypeEffectiveness>
}

function TypeGrid({ typeEffectiveness }: TypeGridProps) {
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
    if (multiplier === 0) return 'bg-gray-700 text-gray-400'
    if (multiplier < 1) return 'bg-secondary/20 text-secondary border-secondary/50'
    if (multiplier === 1) return 'bg-white/5 text-gray-400 border-white/10'
    if (multiplier === 2) return 'bg-danger/20 text-danger border-danger/50'
    if (multiplier >= 4) return 'bg-danger text-white border-danger'
    return 'bg-white/5 text-gray-400'
  }

  const sortedTypes = Object.entries(typeEffectiveness).sort(([a], [b]) =>
    a.localeCompare(b)
  )

  return (
    <div>
      <h3 className="text-xl font-bold mb-4">Type Effectiveness</h3>
      <div className="grid grid-cols-6 gap-3">
        {sortedTypes.map(([typeName, data]) => (
          <div
            key={typeName}
            className={`p-3 rounded-lg border ${getMultiplierColor(
              data.multiplier
            )} transition-all hover:scale-105`}
          >
            <div className="flex items-center gap-2 mb-2">
              <div
                className="w-4 h-4 rounded-full"
                style={{ backgroundColor: data.color }}
              />
              <span className="text-xs font-semibold uppercase">{typeName}</span>
            </div>
            <p className="text-lg font-bold text-center">
              {getMultiplierLabel(data.multiplier)}
            </p>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="mt-6 p-4 bg-black/20 rounded-lg">
        <p className="text-sm text-gray-400 mb-2 font-semibold">Legend:</p>
        <div className="flex flex-wrap gap-4 text-xs">
          <span className="text-gray-400">
            <span className="font-bold">×0</span> = Immune
          </span>
          <span className="text-secondary">
            <span className="font-bold">×¼, ×½</span> = Resist
          </span>
          <span className="text-gray-400">
            <span className="font-bold">×1</span> = Normal
          </span>
          <span className="text-danger">
            <span className="font-bold">×2, ×4</span> = Weakness
          </span>
        </div>
      </div>
    </div>
  )
}

export default TypeGrid
