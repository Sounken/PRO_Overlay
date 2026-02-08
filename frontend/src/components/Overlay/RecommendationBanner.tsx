import { motion, AnimatePresence } from 'framer-motion'

export interface TeamRecommendation {
  recommended_pokemon: string | null
  show_recommendation: boolean
  reasoning: string
}

interface RecommendationBannerProps {
  recommendation: TeamRecommendation | null
}

function RecommendationBanner({ recommendation }: RecommendationBannerProps) {
  if (!recommendation || !recommendation.show_recommendation || !recommendation.recommended_pokemon) {
    return null
  }

  return (
    <AnimatePresence>
      <motion.div
        key="recommendation-banner"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.3 }}
        className="absolute left-0 right-0 top-full mt-3 z-50"
      >
        <div
          className="mx-0 rounded-[20px] px-4 py-3 border border-white/10 backdrop-blur-sm"
          style={{
            background: 'linear-gradient(135deg, rgba(34,34,46,0.95), rgba(24,24,32,0.95))',
            boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          }}
        >
          <div className="flex items-center gap-3">
            <span className="text-xl">🔄</span>
            <div className="flex-1 min-w-0">
              <p className="text-xs text-gray-400 font-semibold uppercase tracking-wide leading-tight">
                Changement conseillé
              </p>
              <p className="text-base font-bold text-white uppercase truncate">
                {recommendation.recommended_pokemon}
              </p>
            </div>
          </div>
          {recommendation.reasoning && (
            <p className="text-xs text-gray-500 mt-2 italic">
              {recommendation.reasoning}
            </p>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  )
}

export default RecommendationBanner
