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

  const loadData = async () => {
    if (window.electronAPI) {
      const r = await window.electronAPI.getOcrRegion()
      setRegion(r)
      const s = await window.electronAPI.getScreenInfo()
      setScreenInfo(s)
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
    const hasAPI = !!window.electronAPI
    const hasFn = typeof window.electronAPI?.openRegionSelector === 'function'
    alert(`electronAPI: ${hasAPI}, openRegionSelector: ${hasFn}`)
    if (hasFn) {
      await window.electronAPI.openRegionSelector()
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
    </div>
  )
}

export default Settings
