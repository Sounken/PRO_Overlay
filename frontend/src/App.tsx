import { useEffect, useState } from 'react'
import Dashboard from './components/Dashboard/Dashboard'
import OverlayWindow from './components/Overlay/OverlayWindow'

function App() {
  const [isOverlay, setIsOverlay] = useState(false)

  useEffect(() => {
    // Détecte si on est en mode overlay via le hash
    const checkMode = () => {
      setIsOverlay(window.location.hash === '#overlay')
    }

    checkMode()
    window.addEventListener('hashchange', checkMode)

    return () => window.removeEventListener('hashchange', checkMode)
  }, [])

  return isOverlay ? <OverlayWindow /> : <Dashboard />
}

export default App
