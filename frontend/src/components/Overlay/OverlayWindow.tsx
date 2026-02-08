import { useState, useEffect, useRef } from 'react'
import { pokemonAPI, Pokemon, OCRRegion, teamAPI } from '@/services/api'
import PokemonInfo from './PokemonInfo'
import RecommendationBanner, { TeamRecommendation } from './RecommendationBanner'

function OverlayWindow() {
  const [pokemon, setPokemon] = useState<Pokemon | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [recommendation, setRecommendation] = useState<TeamRecommendation | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const ocrRegionRef = useRef<OCRRegion | undefined>(undefined)
  const windowPosRef = useRef({ x: 0, y: 0 })
  const dragOffsetRef = useRef({ x: 0, y: 0 })
  const lastDetectedRef = useRef<string | null>(null)
  const autoBattleRef = useRef(false)
  const inBattleRef = useRef(false)
  const lastBattleStateChangeRef = useRef(0)
  const teamRef = useRef<string[]>([])
  const activePokemonRef = useRef<string | null>(null)

  // Charge la région OCR, le mode autoBattle, et l'équipe au montage
  useEffect(() => {
    const loadConfig = async () => {
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
        const ab = await window.electronAPI.getAutoBattle()
        autoBattleRef.current = ab

        // Charger l'équipe
        const team = await window.electronAPI.getTeam()
        if (team && team.pokemon) {
          teamRef.current = team.pokemon.map((p: any) => p.name.toLowerCase())
          activePokemonRef.current = team.active_pokemon?.toLowerCase() || null
          console.log('[Team] Loaded team:', teamRef.current, 'Active:', activePokemonRef.current)
        }
      }
    }
    loadConfig()
  }, [])

  const detectPokemon = async () => {
    try {
      // Utiliser l'endpoint debug pour avoir la confiance même si < 25%
      const backendUrl = await window.electronAPI?.getBackendUrl()
      if (!backendUrl) return

      const debugResponse = await fetch(`${backendUrl}/ocr/debug`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          region: ocrRegionRef.current || null,
        }),
      })
      const debugData = await debugResponse.json()

      const now = Date.now()
      const timeSinceLastChange = now - lastBattleStateChangeRef.current

      // Gestion du mode autoBattle: ne basculer que si on détecte un VRAI Pokémon
      // (pas juste une confiance élevée sans résultat)
      const pokemonDetected = debugData.detected_pokemon !== null && debugData.detected_pokemon !== ""

      if (autoBattleRef.current && timeSinceLastChange > 500) {
        if (pokemonDetected && !inBattleRef.current) {
          // Passage de "pas en combat" à "Pokémon détecté" → ouvrir l'overlay
          console.log(`[AutoBattle] Pokemon detected: ${debugData.detected_pokemon} (confiance: ${debugData.confidence.toFixed(1)}%) - opening overlay`)
          inBattleRef.current = true
          lastBattleStateChangeRef.current = now
          window.electronAPI?.toggleOverlay()
        } else if (!pokemonDetected && inBattleRef.current) {
          // Passage de "Pokémon détecté" à "pas de Pokémon" → fermer l'overlay
          console.log(`[AutoBattle] No pokemon detected (confiance: ${debugData.confidence.toFixed(1)}%) - closing overlay`)
          inBattleRef.current = false
          lastBattleStateChangeRef.current = now
          window.electronAPI?.toggleOverlay()
        }
      }

      // Gestion de l'affichage du Pokémon
      if (pokemonDetected) {
        // Un Pokémon est détecté

        // Vérifier si c'est un nouveau Pokémon
        const isPokemonChanged = debugData.detected_pokemon !== lastDetectedRef.current
        const noDataLoaded = pokemon === null

        // Charger les données si: nouveau Pokémon OU pas encore de données chargées
        if (isPokemonChanged || noDataLoaded) {
          console.log(`[OCR] Loading Pokémon: ${debugData.detected_pokemon} (confiance: ${debugData.confidence.toFixed(1)}%, changed: ${isPokemonChanged})`)
          setLoading(true)
          setError(null)
          lastDetectedRef.current = debugData.detected_pokemon

          try {
            const data = await pokemonAPI.getPokemon(debugData.detected_pokemon)
            setPokemon(data)

            // Charger la recommandation d'équipe si une équipe existe
            if (teamRef.current && teamRef.current.length > 0) {
              try {
                console.log('[Team] Getting recommendation for:', debugData.detected_pokemon, 'Team:', teamRef.current)
                const rec = await teamAPI.getRecommendation(
                  debugData.detected_pokemon.toLowerCase(),
                  teamRef.current,
                  activePokemonRef.current || undefined
                )
                console.log('[Team] Recommendation response:', rec)
                setRecommendation(rec)
              } catch (recErr) {
                console.error('[Team] Failed to get recommendation:', recErr)
                setRecommendation(null)
              }
            } else {
              console.log('[Team] No team loaded, skipping recommendation')
              setRecommendation(null)
            }
          } catch (fetchErr) {
            console.error('[OCR] Failed to fetch Pokémon data:', fetchErr)
            setError('Erreur de chargement')
            // Ne pas mettre à jour lastDetectedRef si la fetch a échoué
            lastDetectedRef.current = null
            setRecommendation(null)
          }
        }
      } else {
        // Pas de Pokémon détecté → clear affichage
        setPokemon(null)
        setError(null)
        setRecommendation(null)
        lastDetectedRef.current = null
      }
    } catch (err) {
      console.error('[OCR] Erreur lors de la détection:', err)

      // En cas d'erreur, considérer qu'on n'est pas en combat
      const now = Date.now()
      const timeSinceLastChange = now - lastBattleStateChangeRef.current

      if (autoBattleRef.current && inBattleRef.current && timeSinceLastChange > 500) {
        console.log('[AutoBattle] Error in detection - closing overlay')
        inBattleRef.current = false
        lastBattleStateChangeRef.current = now
        window.electronAPI?.toggleOverlay()
      }

      // Seulement afficher l'erreur si on était en train de charger
      if (loading) {
        setError('Erreur de détection')
        setPokemon(null)
      }
      lastDetectedRef.current = null
    } finally {
      setLoading(false)
    }
  }

  // Détection automatique toutes les 1 seconde
  useEffect(() => {
    const interval = setInterval(() => {
      detectPokemon()
    }, 1000)

    return () => clearInterval(interval)
  }, [])


  // Drag handling
  const handleMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    // Drag sur le titre du Pokemon
    if ((e.target as HTMLElement).closest('h1')) {
      setIsDragging(true)
      dragOffsetRef.current = {
        x: e.clientX,
        y: e.clientY,
      }
    }
  }

  useEffect(() => {
    if (!isDragging || !window.electronAPI) return

    const handleMouseMove = (e: MouseEvent) => {
      const deltaX = e.clientX - dragOffsetRef.current.x
      const deltaY = e.clientY - dragOffsetRef.current.y

      const newX = windowPosRef.current.x + deltaX
      const newY = windowPosRef.current.y + deltaY

      // Appeler l'IPC pour déplacer la vraie fenêtre
      window.electronAPI?.setOverlayPosition(newX, newY)

      // Mettre à jour la position suivie (sans state update = pas de lag)
      windowPosRef.current = {
        x: newX,
        y: newY,
      }

      dragOffsetRef.current = {
        x: e.clientX,
        y: e.clientY,
      }
    }

    const handleMouseUp = () => {
      setIsDragging(false)
    }

    window.addEventListener('mousemove', handleMouseMove)
    window.addEventListener('mouseup', handleMouseUp)

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isDragging])

  return (
    <div
      ref={containerRef}
      onMouseDown={handleMouseDown}
      className="w-full h-full select-none overflow-visible relative"
      style={{
        cursor: isDragging ? 'grabbing' : 'grab',
      }}
    >
      <div className="w-full relative">
        {pokemon ? (
          <div className="relative">
            <PokemonInfo pokemon={pokemon} />
            {/* Recommendation Banner */}
            <RecommendationBanner recommendation={recommendation} />
          </div>
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
    </div>
  )
}

export default OverlayWindow
