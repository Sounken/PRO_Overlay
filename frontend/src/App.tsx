import { useEffect, useState } from 'react'
import Dashboard from './components/Dashboard/Dashboard'
import OverlayWindow from './components/Overlay/OverlayWindow'
import RegionSelector from './components/RegionSelector/RegionSelector'

type AppMode = 'dashboard' | 'overlay' | 'region-selector'

function App() {
  const [mode, setMode] = useState<AppMode>('dashboard')

  useEffect(() => {
    const checkMode = () => {
      const hash = window.location.hash
      if (hash === '#overlay') setMode('overlay')
      else if (hash === '#region-selector') setMode('region-selector')
      else setMode('dashboard')
    }

    checkMode()
    window.addEventListener('hashchange', checkMode)

    return () => window.removeEventListener('hashchange', checkMode)
  }, [])

  // Rendre le body transparent en mode overlay
  useEffect(() => {
    if (mode === 'overlay') {
      document.body.classList.add('overlay-mode')
    } else {
      document.body.classList.remove('overlay-mode')
    }
  }, [mode])

  switch (mode) {
    case 'overlay':
      return <OverlayWindow />
    case 'region-selector':
      return <RegionSelector />
    default:
      return <Dashboard />
  }
}

export default App
