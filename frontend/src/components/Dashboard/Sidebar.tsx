import { motion } from 'framer-motion'

interface SidebarProps {
  currentView: string
  onViewChange: (view: 'pokedex' | 'team' | 'calculators' | 'settings') => void
}

function Sidebar({ currentView, onViewChange }: SidebarProps) {
  const menuItems = [
    { id: 'pokedex', label: 'Pokédex', icon: '📖' },
    { id: 'team', label: 'Équipe', icon: '⚔️' },
    { id: 'calculators', label: 'Calculateurs', icon: '🧮' },
    { id: 'settings', label: 'Paramètres', icon: '⚙️' },
  ]

  return (
    <aside className="bg-sidebar w-64 flex flex-col border-r border-white/10">
      {/* Header */}
      <div className="p-6 border-b border-white/10">
        <h1 className="text-2xl font-bold text-primary">PRO Helper</h1>
        <p className="text-sm text-gray-400 mt-1">Pokemon Revolution Online</p>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const isActive = currentView === item.id
          return (
            <motion.button
              key={item.id}
              onClick={() =>
                onViewChange(item.id as 'pokedex' | 'team' | 'calculators' | 'settings')
              }
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary text-white'
                  : 'text-gray-300 hover:bg-white/5'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </motion.button>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-white/10">
        <p className="text-xs text-gray-500 text-center">Version 1.0.0</p>
      </div>
    </aside>
  )
}

export default Sidebar
