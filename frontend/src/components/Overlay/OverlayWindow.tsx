import { useState, useEffect, useRef } from 'react'
import { pokemonAPI, Pokemon, OCRRegion } from '@/services/api'
import PokemonInfo from './PokemonInfo'
import { motion } from 'framer-motion'

function OverlayWindow() {
  const [pokemon, setPokemon] = useState<Pokemon | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)
  const ocrRegionRef = useRef<OCRRegion | undefined>(undefined)
  const windowPosRef = useRef({ x: 0, y: 0 })
  const dragOffsetRef = useRef({ x: 0, y: 0 })
  const lastDetectedRef = useRef<string | null>(null)
  const autoBattleRef = useRef(false)
  const inBattleRef = useRef(false)
  const lastBattleStateChangeRef = useRef(0)

  // Charge la région OCR et le mode autoBattle au montage
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

      // Détection du combat basée sur la confiance (>= 25%)
      const inCombat = debugData.confidence >= 25

      // Gestion du mode autoBattle: basculer l'overlay si l'état de combat a changé
      if (autoBattleRef.current && timeSinceLastChange > 500) {
        if (inCombat && !inBattleRef.current) {
          // Passage de "pas en combat" à "en combat" → ouvrir l'overlay
          console.log(`[AutoBattle] Combat detected (confiance: ${debugData.confidence.toFixed(1)}%) - opening overlay`)
          inBattleRef.current = true
          lastBattleStateChangeRef.current = now
          window.electronAPI?.toggleOverlay()
        } else if (!inCombat && inBattleRef.current) {
          // Passage de "en combat" à "pas en combat" → fermer l'overlay
          console.log(`[AutoBattle] Combat ended (confiance: ${debugData.confidence.toFixed(1)}%) - closing overlay`)
          inBattleRef.current = false
          lastBattleStateChangeRef.current = now
          window.electronAPI?.toggleOverlay()
        }
      }

      // Gestion de l'affichage du Pokémon
      if (inCombat && debugData.detected_pokemon) {
        // En combat et un Pokémon est détecté

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
          } catch (fetchErr) {
            console.error('[OCR] Failed to fetch Pokémon data:', fetchErr)
            setError('Erreur de chargement')
            // Ne pas mettre à jour lastDetectedRef si la fetch a échoué
            lastDetectedRef.current = null
          }
        }
      } else if (!inCombat) {
        // Pas en combat → clear affichage
        setPokemon(null)
        setError(null)
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

  // Détection automatique toutes les 2 secondes
  useEffect(() => {
    const interval = setInterval(() => {
      detectPokemon()
    }, 2000)

    return () => clearInterval(interval)
  }, [])


  // Drag handling
  const handleMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    // Ne drag que si on clique sur le header
    if ((e.target as HTMLElement).closest('.overlay-header')) {
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
      className="w-full h-full glass p-4 rounded-2xl flex flex-col select-none overflow-hidden"
      style={{
        cursor: isDragging ? 'grabbing' : 'grab',
        background: 'rgba(30, 30, 46, 0.8)',
        backdropFilter: 'blur(10px)',
        borderRadius: '1rem',
      }}
    >
        {/* Header - Draggable */}
        <div className="overlay-header flex items-center justify-between mb-4 cursor-grab active:cursor-grabbing">
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
        <div className="flex-1 overflow-y-auto pr-2">
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
    </div>
  )
}

export default OverlayWindow
