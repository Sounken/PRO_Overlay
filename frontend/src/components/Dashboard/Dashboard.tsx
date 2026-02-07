import { useState } from 'react'
import Sidebar from './Sidebar'
import Pokedex from './Pokedex'
import Settings from './Settings'

type View = 'pokedex' | 'team' | 'calculators' | 'settings'

function Dashboard() {
  const [currentView, setCurrentView] = useState<View>('pokedex')

  const renderView = () => {
    switch (currentView) {
      case 'pokedex':
        return <Pokedex />
      case 'team':
        return (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-400 text-xl">Gestion d'équipe - À venir</p>
          </div>
        )
      case 'calculators':
        return (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-400 text-xl">Calculateurs - À venir</p>
          </div>
        )
      case 'settings':
        return <Settings />
      default:
        return <Pokedex />
    }
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar currentView={currentView} onViewChange={setCurrentView} />
      <main className="flex-1 overflow-auto p-8">{renderView()}</main>
    </div>
  )
}

export default Dashboard
