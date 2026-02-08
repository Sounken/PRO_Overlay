import { useState, useEffect } from 'react'
import { POKEMON_NAMES } from '@/constants/pokemon'
import { teamAPI } from '@/services/api'

interface TeamMember {
  name: string
  slot: number
}

function Team() {
  const [team, setTeam] = useState<TeamMember[]>([])
  const [activePokemon, setActivePokemon] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const [suggestions, setSuggestions] = useState<string[]>([])

  // Charger l'équipe au montage
  useEffect(() => {
    const loadTeam = async () => {
      if (window.electronAPI) {
        const teamData = await window.electronAPI.getTeam()
        console.log('[Team UI] Loaded team data:', teamData)
        if (teamData && teamData.pokemon) {
          setTeam(teamData.pokemon)
          setActivePokemon(teamData.active_pokemon)
        }
      }
    }
    loadTeam()
  }, [])

  // Sauvegarde l'équipe quand elle change
  const saveTeam = async (newTeam: TeamMember[]) => {
    setTeam(newTeam)
    if (window.electronAPI) {
      console.log('[Team UI] Saving team:', { pokemon: newTeam, active_pokemon: activePokemon })
      await window.electronAPI.saveTeam({
        pokemon: newTeam,
        active_pokemon: activePokemon,
      })
    }
  }

  // Filtrer les suggestions de recherche
  useEffect(() => {
    if (searchInput.length < 1) {
      setSuggestions([])
      return
    }

    const filtered = POKEMON_NAMES.filter(
      (name) =>
        name.startsWith(searchInput.toLowerCase()) &&
        !team.some((p) => p.name === name) // Exclure les Pokémon déjà dans l'équipe
    ).slice(0, 8)

    setSuggestions(filtered)
  }, [searchInput, team])

  // Ajouter un Pokémon à l'équipe
  const handleAddPokemon = async (name: string) => {
    if (team.length >= 6) {
      alert('Team full (max 6 Pokemon)')
      return
    }

    const result = await window.electronAPI?.addTeamMember(name)
    if (result?.success) {
      const newTeam = [...team, { name, slot: team.length + 1 }]
      saveTeam(newTeam)
      setSearchInput('')
      setSuggestions([])
    } else {
      alert(result?.error || 'Error adding Pokemon')
    }
  }

  // Supprimer un Pokémon
  const handleRemoveTeamMember = async (slot: number) => {
    await window.electronAPI?.removeTeamMember(slot)
    const newTeam = team.filter((p) => p.slot !== slot)
    saveTeam(newTeam)
  }

  // Définir le Pokémon actif
  const handleSetActive = async (name: string) => {
    await window.electronAPI?.setActivePokemon(name)
    setActivePokemon(name)
  }

  // Détecter l'équipe via OCR
  const handleDetectTeam = async () => {
    if (window.electronAPI) {
      await window.electronAPI.openTeamRegionSelector()

      // Attendre un peu pour que la région soit sauvegardée, puis détecter
      setTimeout(async () => {
        try {
          const region = await window.electronAPI.getTeamRegion()
          if (region && region.enabled) {
            console.log('[Team OCR] Detecting team from region:', region)
            const result = await teamAPI.detectTeamFromZone(region)
            console.log('[Team OCR] Detected Pokemon:', result)

            // Ajouter les Pokémon détectés à l'équipe
            if (result && result.length > 0) {
              const detected = result.filter((p: string | null) => p !== null) as string[]
              console.log('[Team OCR] Adding detected Pokemon:', detected)

              // Charger l'équipe actuelle pour éviter les stale closures
              const currentTeam = await window.electronAPI.getTeam()
              let updatedTeam = (currentTeam?.pokemon || []).slice()

              for (const pokemonName of detected) {
                if (updatedTeam.length < 6 && !updatedTeam.some((p: any) => p.name === pokemonName)) {
                  updatedTeam.push({ name: pokemonName, slot: updatedTeam.length + 1 })
                }
              }

              setTeam(updatedTeam)
              // Sauvegarde
              if (window.electronAPI) {
                await window.electronAPI.saveTeam({
                  pokemon: updatedTeam,
                  active_pokemon: activePokemon,
                })
              }
            }
          }
        } catch (err) {
          console.error('[Team OCR] Error detecting team:', err)
          alert('Error during OCR detection')
        }
      }, 500)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-2">Team</h1>
      <p className="text-gray-400 mb-8">Create your Pokemon team for battle recommendations</p>

      {/* Search and Add */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">Add Pokemon</h2>
        <div className="relative mb-3">
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search Pokemon (e.g. pikachu, charizard...)"
            className="w-full px-4 py-2 bg-surface border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary"
          />
          {suggestions.length > 0 && (
            <div className="absolute top-full left-0 right-0 bg-surface border border-white/10 rounded-lg mt-1 z-10 max-h-48 overflow-y-auto">
              {suggestions.map((name) => (
                <button
                  key={name}
                  onClick={() => handleAddPokemon(name)}
                  className="w-full text-left px-4 py-2 hover:bg-white/5 transition-colors first:rounded-t-lg last:rounded-b-lg text-white capitalize"
                >
                  {name}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* OCR Detector */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">Auto Detect</h2>
        <button
          onClick={handleDetectTeam}
          className="px-6 py-3 bg-primary hover:bg-primary/80 rounded-lg font-semibold transition-colors"
        >
          Detect Team via OCR
        </button>
      </div>

      {/* Team Display */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Team ({team.length}/6)</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {Array.from({ length: 6 }).map((_, idx) => {
            const member = team.find((p) => p.slot === idx + 1)
            return (
              <div
                key={idx}
                className={`p-3 rounded-lg border-2 transition-colors ${
                  member
                    ? activePokemon === member.name
                      ? 'border-primary bg-primary/20'
                      : 'border-white/10 bg-white/5'
                    : 'border-dashed border-white/10 bg-transparent'
                }`}
              >
                {member ? (
                  <div>
                    <p className="font-semibold capitalize mb-2">{member.name}</p>
                    <div className="flex gap-1">
                      <button
                        onClick={() => handleSetActive(member.name)}
                        className={`text-xs px-2 py-1 rounded transition-colors ${
                          activePokemon === member.name
                            ? 'bg-primary text-white'
                            : 'bg-white/10 text-gray-300 hover:bg-white/20'
                        }`}
                      >
                        {activePokemon === member.name ? '✓ Active' : 'Active'}
                      </button>
                      <button
                        onClick={() => handleRemoveTeamMember(idx + 1)}
                        className="text-xs px-2 py-1 rounded bg-red-500/20 text-red-300 hover:bg-red-500/30 transition-colors"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">Slot {idx + 1}</p>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default Team
