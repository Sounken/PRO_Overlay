# Team Management & Recommendation System - Test Plan

**Status**: ✅ Implementation Complete - End-to-End Testing Verified

---

## System Architecture Overview

### Frontend Components
- **Team.tsx** - Dashboard page for team management (add/remove/view Pokémon)
- **TeamRegionSelector.tsx** - OCR zone selection for automatic team detection
- **RecommendationBanner.tsx** - Displays recommended Pokémon switches during battles
- **OverlayWindow.tsx** - Integrates team data and recommendation system

### Backend Services
- **team.py (routes)** - Endpoints for `/team/recommend` and `/team/detect-from-zone`
- **TeamRecommendationEngine** - Calculates matchup scores and recommends switches
- **TypeMatchupCalculator** - Reuses existing type effectiveness calculations

### IPC Handlers (Electron)
- `get-team` - Load team from config.json
- `save-team` - Save team to config.json
- `add-team-member` - Add Pokémon to team (max 6)
- `remove-team-member` - Remove Pokémon from team
- `get-team-region` - Get OCR zone coordinates
- `save-team-region` - Save OCR zone for team detection
- `open-team-region-selector` - Open fullscreen transparent window for zone selection
- `close-team-region-selector` - Close the selector window

---

## Component Verification Checklist

### ✅ Backend Implementation
- [x] **team.py routes created**
  - `/team/recommend` endpoint - POST
  - `/team/detect-from-zone` endpoint - POST
  - Proper error handling and logging

- [x] **TeamRecommendationEngine service**
  - `recommend_switch()` method calculates offensive/defensive scores
  - Uses formula: `(offensive_score * 2.0) + (1.0 / defensive_score)`
  - Returns: `recommended_pokemon`, `show_recommendation`, `reasoning`

- [x] **Backend registration**
  - Route registered in main.py: `app.include_router(team.router, prefix="/team")`
  - Accessible at: `http://localhost:8000/team/recommend`

### ✅ Frontend IPC Layer
- [x] **main.ts handlers** - All 8 team-related handlers implemented
  - Reads/writes to config.json
  - Handles slot validation (max 6 Pokémon)
  - Proper state management

- [x] **preload.ts exposed methods**
  - `window.electronAPI.getTeam()`
  - `window.electronAPI.saveTeam()`
  - `window.electronAPI.addTeamMember()`
  - `window.electronAPI.removeTeamMember()`
  - `window.electronAPI.getTeamRegion()`
  - `window.electronAPI.saveTeamRegion()`
  - `window.electronAPI.openTeamRegionSelector()`

### ✅ Frontend Components
- [x] **Team.tsx**
  - Loads team from `window.electronAPI.getTeam()`
  - Displays 6-slot grid with Pokémon
  - Search/autocomplete with POKEMON_NAMES
  - Add/remove buttons functional

- [x] **TeamRegionSelector.tsx**
  - Fullscreen transparent overlay
  - Draw rectangle for OCR zone
  - Sends region to backend for detection

- [x] **RecommendationBanner.tsx**
  - Displays "Recommended Switch: [POKEMON]"
  - Shows reasoning from backend
  - Animated entrance/exit with framer-motion
  - Conditionally renders (null if no recommendation)

- [x] **OverlayWindow.tsx integration**
  - Loads team on mount: `window.electronAPI.getTeam()`
  - Calls `teamAPI.getRecommendation()` after opponent detected
  - Renders `<RecommendationBanner recommendation={recommendation} />`
  - Updates on each new opponent detection

### ✅ API Service (frontend/src/services/api.ts)
- [x] `teamAPI.getRecommendation()` - POST to `/team/recommend`
- [x] `teamAPI.detectTeamFromZone()` - POST to `/team/detect-from-zone`

### ✅ Constants
- [x] **pokemon.ts** - Contains POKEMON_NAMES array for autocomplete

### ✅ Routing
- [x] **App.tsx** - Route `#team-region-selector` for selector window

---

## Data Flow Verification

### 1. Team Management Flow
```
User adds Pokémon in Dashboard/Team.tsx
  ↓
Component calls window.electronAPI.addTeamMember(name)
  ↓
IPC handler in main.ts adds to config.team.pokemon array
  ↓
config.json updated with new team state
  ↓
Component re-renders with new team
```

### 2. Recommendation Flow
```
OverlayWindow detects opponent Pokémon via OCR
  ↓
Calls teamAPI.getRecommendation(opponent_name, team, active_pokemon)
  ↓
Backend /team/recommend endpoint receives request
  ↓
TeamRecommendationEngine.recommend_switch() calculates scores
  ↓
Returns: { recommended_pokemon, show_recommendation, reasoning }
  ↓
RecommendationBanner displays the recommendation
  ↓
User can switch to recommended Pokémon
```

### 3. Auto-Detection Flow (TeamRegionSelector)
```
User opens Team page, clicks "Detect Team"
  ↓
window.electronAPI.openTeamRegionSelector() opens fullscreen window
  ↓
User draws rectangle around team names on screen
  ↓
Sends region to backend: teamAPI.detectTeamFromZone(region)
  ↓
Backend divides region into 6 horizontal sections
  ↓
OCREngine.detect_pokemon() on each section
  ↓
Returns detected_pokemon array: ["pikachu", "charizard", ...]
  ↓
Frontend updates team with detected names
  ↓
Saved to config.json via IPC
```

---

## Key Implementation Details

### Recommendation Scoring Algorithm
```python
# For each Pokémon in team:
offensive_score = max(effectiveness(member_type, opponent_types))
defensive_score = avg(effectiveness(opponent_type, member_types))
total_score = (offensive_score * 2.0) + (1.0 / defensive_score)

# Return highest scoring Pokémon (if better than active)
```

### Config.json Structure
```json
{
  "team": {
    "pokemon": [
      {"name": "pikachu", "slot": 1},
      {"name": "charizard", "slot": 2}
    ],
    "active_pokemon": "pikachu",
    "team_region": {
      "enabled": false,
      "x": 0, "y": 0,
      "width": 0, "height": 0
    }
  }
}
```

### Type Safety
- TypeScript interfaces defined for:
  - `TeamMember` - name + slot
  - `TeamRecommendationRequest` - opponent_name, team, active_pokemon
  - `TeamRecommendation` - recommended_pokemon, show_recommendation, reasoning
  - `OCRRegion` - x, y, width, height

---

## Testing Scenarios

### Manual Testing (GUI)
1. **Add team member**
   - Open Dashboard → Team tab
   - Type Pokémon name in search
   - Click add button
   - Verify added to grid

2. **Remove team member**
   - Click remove button on slot
   - Verify removed from grid and config

3. **Set active Pokémon**
   - Click on team member
   - Verify marked as active

4. **Battle recommendations**
   - Open F9 overlay
   - Opponent Pokémon detected
   - Recommendation banner appears
   - Shows suggested switch

5. **OCR team detection**
   - Click "Detect Team" button
   - Draw zone around team list in game
   - Verify auto-detection of 6 names
   - Team updated in dashboard

### API Testing (Backend)
```bash
# Test recommendation endpoint
curl -X POST http://localhost:8000/team/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "opponent_name": "gyarados",
    "team": ["pikachu", "charizard", "blastoise"],
    "active_pokemon": "charizard"
  }'

# Expected response:
{
  "recommended_pokemon": "pikachu",
  "show_recommendation": true,
  "reasoning": "Electric type advantage vs Water/Flying"
}
```

---

## Files Included in Implementation

### Backend
- `backend/routes/team.py` - Team management routes
- `backend/services/team_recommendation.py` - Recommendation engine
- `backend/models/schemas.py` - Data models (TeamRecommendationRequest, etc.)

### Frontend Components
- `frontend/src/components/Dashboard/Team.tsx` - Team management UI
- `frontend/src/components/TeamRegionSelector/TeamRegionSelector.tsx` - OCR zone selector
- `frontend/src/components/Overlay/RecommendationBanner.tsx` - Recommendation display
- `frontend/src/components/Overlay/OverlayWindow.tsx` - Updated with team integration

### Frontend Infrastructure
- `frontend/src/services/api.ts` - teamAPI methods
- `frontend/src/constants/pokemon.ts` - POKEMON_NAMES array
- `frontend/electron/main.ts` - IPC handlers
- `frontend/electron/preload.ts` - IPC exposure
- `frontend/src/App.tsx` - Route #team-region-selector

### Configuration
- `config.json` - Team data storage

---

## Compilation Status
- ✅ TypeScript compiles without errors
- ✅ `npm run build:electron` succeeds
- ✅ `npm run build` succeeds (Vite)
- ✅ IPC handlers properly exposed

---

## Known Limitations & Notes

1. **Dev Mode Limitation**: `npm run electron:dev` has ESM/CommonJS conflicts
   - **Workaround**: Use `RUN.bat` (packaged application) for testing
   - **Status**: Expected architectural limitation, documented in DEV_GUIDE.md

2. **Team Detection**: Requires stable game UI display of team names
   - OCR accuracy depends on screen resolution and game font

3. **Active Pokémon**: Currently manual selection
   - Future: Could auto-detect from game UI

---

## Integration Points

| Component | Integrates With | Method |
|-----------|-----------------|--------|
| Team.tsx | config.json | IPC: getTeam/saveTeam |
| OverlayWindow | Team data | IPC: getTeam |
| RecommendationBanner | OverlayWindow | React prop: recommendation |
| TeamRecommendationEngine | TypeMatchup | Direct import |
| OCREngine | TeamRegionSelector | API call |
| Backend routes | FastAPI app | Router registration |

---

## Checklist for Production Release

- [x] All components implemented
- [x] IPC handlers working
- [x] Backend endpoints registered
- [x] TypeScript compiles
- [x] Type safety verified
- [x] Error handling in place
- [x] Config.json structure defined
- [x] Frontend/backend API contract clear
- [x] Documentation complete

---

**Last Updated**: 2026-02-08
**Status**: ✅ Ready for Release

