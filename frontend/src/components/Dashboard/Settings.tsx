import { useState, useEffect } from 'react'

interface OcrRegion {
  enabled: boolean
  x: number
  y: number
  width: number
  height: number
}

interface ScreenInfo {
  width: number
  height: number
  scaleFactor: number
}

function Settings() {
  const [region, setRegion] = useState<OcrRegion | null>(null)
  const [screenInfo, setScreenInfo] = useState<ScreenInfo | null>(null)
  const [autoBattle, setAutoBattle] = useState(false)

  const loadData = async () => {
    if (window.electronAPI) {
      const r = await window.electronAPI.getOcrRegion()
      setRegion(r)
      const s = await window.electronAPI.getScreenInfo()
      setScreenInfo(s)
      const ab = await window.electronAPI.getAutoBattle()
      setAutoBattle(ab)
    }
  }

  useEffect(() => {
    loadData()

    // Reload when window regains focus (after region selection)
    const onFocus = () => loadData()
    window.addEventListener('focus', onFocus)
    return () => window.removeEventListener('focus', onFocus)
  }, [])

  const handleSelectRegion = async () => {
    if (window.electronAPI?.openRegionSelector) {
      await window.electronAPI.openRegionSelector()
    }
  }

  const handleToggleAutoBattle = async () => {
    const newValue = !autoBattle
    setAutoBattle(newValue)
    if (window.electronAPI?.setAutoBattle) {
      await window.electronAPI.setAutoBattle(newValue)
    }
  }

  const previewWidth = 300
  const previewHeight = screenInfo
    ? (previewWidth * screenInfo.height) / screenInfo.width
    : 170

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-2">Parametres</h1>
      <p className="text-gray-400 mb-8">Configuration de l'application</p>

      {/* OCR Region */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">Zone de detection OCR</h2>

        {region && region.enabled ? (
          <div>
            <p className="text-sm text-gray-300 mb-4">
              Zone actuelle : ({region.x}, {region.y}) - {region.width}x{region.height} px
            </p>

            {/* Visual preview */}
            {screenInfo && (
              <div
                className="relative bg-gray-800 rounded-lg mb-4 border border-gray-700"
                style={{ width: previewWidth, height: previewHeight }}
              >
                <div
                  className="absolute border-2 border-blue-500 bg-blue-500/20 rounded-sm"
                  style={{
                    left: (region.x / (screenInfo.width * screenInfo.scaleFactor)) * previewWidth,
                    top: (region.y / (screenInfo.height * screenInfo.scaleFactor)) * previewHeight,
                    width: (region.width / (screenInfo.width * screenInfo.scaleFactor)) * previewWidth,
                    height: (region.height / (screenInfo.height * screenInfo.scaleFactor)) * previewHeight,
                  }}
                />
                <span className="absolute bottom-1 right-2 text-xs text-gray-500">
                  {screenInfo.width}x{screenInfo.height}
                  {screenInfo.scaleFactor > 1 && ` (${screenInfo.scaleFactor * 100}%)`}
                </span>
              </div>
            )}
          </div>
        ) : (
          <p className="text-sm text-gray-400 mb-4">
            Aucune zone configuree. La detection utilise la zone centrale de l'ecran (60%).
          </p>
        )}

        <button
          onClick={handleSelectRegion}
          className="px-6 py-3 bg-primary hover:bg-primary/80 rounded-lg font-semibold transition-colors"
        >
          {region?.enabled ? 'Redefinir la zone' : 'Definir la zone OCR'}
        </button>
      </div>

      {/* Auto Battle Mode */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Mode Combat Automatique</h2>
        <p className="text-sm text-gray-400 mb-6">
          L'overlay s'activera automatiquement quand vous detectez un Pokemon en combat et se fermera quand le combat se termine.
        </p>

        <div className="flex items-center gap-4">
          <button
            onClick={handleToggleAutoBattle}
            className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
              autoBattle
                ? 'bg-green-600 hover:bg-green-700'
                : 'bg-gray-700 hover:bg-gray-600'
            }`}
          >
            {autoBattle ? '✓ Active' : '○ Inactif'}
          </button>
          <span className="text-sm text-gray-400">
            {autoBattle
              ? 'Mode automatique activé'
              : 'Cliquez pour activer le mode automatique'}
          </span>
        </div>
      </div>
    </div>
  )
}

export default Settings
