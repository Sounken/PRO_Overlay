import { useState, useEffect, useMemo, useCallback } from 'react'

interface Point {
  x: number
  y: number
}

interface Rect {
  x: number
  y: number
  width: number
  height: number
}

function RegionSelector() {
  const [isDrawing, setIsDrawing] = useState(false)
  const [startPoint, setStartPoint] = useState<Point | null>(null)
  const [endPoint, setEndPoint] = useState<Point | null>(null)
  const [showConfirm, setShowConfirm] = useState(false)

  const rect = useMemo<Rect | null>(() => {
    if (!startPoint || !endPoint) return null
    return {
      x: Math.min(startPoint.x, endPoint.x),
      y: Math.min(startPoint.y, endPoint.y),
      width: Math.abs(endPoint.x - startPoint.x),
      height: Math.abs(endPoint.y - startPoint.y),
    }
  }, [startPoint, endPoint])

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (showConfirm) return
    setIsDrawing(true)
    setStartPoint({ x: e.clientX, y: e.clientY })
    setEndPoint({ x: e.clientX, y: e.clientY })
    setShowConfirm(false)
  }, [showConfirm])

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (!isDrawing) return
    setEndPoint({ x: e.clientX, y: e.clientY })
  }, [isDrawing])

  const handleMouseUp = useCallback(() => {
    if (!isDrawing) return
    setIsDrawing(false)
    if (rect && rect.width > 10 && rect.height > 10) {
      setShowConfirm(true)
    }
  }, [isDrawing, rect])

  const handleConfirm = useCallback(async () => {
    if (!rect) return
    await window.electronAPI?.saveOcrRegion(rect)
    await window.electronAPI?.closeRegionSelector()
  }, [rect])

  const handleRetry = useCallback(() => {
    setStartPoint(null)
    setEndPoint(null)
    setShowConfirm(false)
  }, [])

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        window.electronAPI?.closeRegionSelector()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [])

  return (
    <div
      className="fixed inset-0 select-none"
      style={{
        cursor: showConfirm ? 'default' : 'crosshair',
        backgroundColor: 'rgba(0, 0, 0, 0.35)',
      }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      {/* Rectangle de selection */}
      {rect && rect.width > 0 && rect.height > 0 && (
        <div
          className="absolute border-2 border-blue-400"
          style={{
            left: rect.x,
            top: rect.y,
            width: rect.width,
            height: rect.height,
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.35)',
          }}
        />
      )}

      {/* Instructions */}
      {!showConfirm && !isDrawing && !rect && (
        <div className="fixed top-8 left-1/2 -translate-x-1/2 pointer-events-none z-10">
          <div className="bg-black/80 backdrop-blur-sm px-8 py-4 rounded-xl text-center">
            <p className="text-white text-lg font-semibold mb-1">
              Click and drag to select the OCR zone
            </p>
            <p className="text-gray-400 text-sm">
              Select the area where the Pokemon name appears - Press Escape to cancel
            </p>
          </div>
        </div>
      )}

      {/* Boutons confirmer / recommencer */}
      {showConfirm && rect && (
        <div
          className="fixed z-20 flex gap-3"
          style={{
            left: rect.x + rect.width / 2,
            top: rect.y + rect.height + 16,
            transform: 'translateX(-50%)',
          }}
        >
          <button
            onClick={handleConfirm}
            className="px-6 py-3 bg-green-600 hover:bg-green-500 text-white font-semibold rounded-lg shadow-lg transition-colors"
          >
            Confirm
          </button>
          <button
            onClick={handleRetry}
            className="px-6 py-3 bg-gray-600 hover:bg-gray-500 text-white font-semibold rounded-lg shadow-lg transition-colors"
          >
            Retry
          </button>
        </div>
      )}
    </div>
  )
}

export default RegionSelector
