"""
Routes API pour la gestion d'équipe et recommandations
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from models.schemas import OCRRegion, TeamRecommendationRequest
from services import TeamRecommendationEngine, ScreenCapture, OCREngine

router = APIRouter()
recommendation_engine = TeamRecommendationEngine()
ocr_engine = OCREngine(confidence_threshold=25)


@router.post("/recommend")
async def get_team_recommendation(request: TeamRecommendationRequest):
    """
    Obtient une recommandation de Pokémon pour combattre l'adversaire

    Args:
        request: Requête contenant opponent_name, team, active_pokemon

    Returns:
        {
            "recommended_pokemon": str | None,
            "show_recommendation": bool,
            "reasoning": str
        }
    """
    try:
        result = recommendation_engine.recommend_switch(
            request.opponent_name,
            request.team,
            request.active_pokemon
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur recommendation: {str(e)}")


@router.post("/detect-from-zone")
async def detect_team_from_zone(region: OCRRegion):
    """
    Détecte les 6 noms de Pokémon depuis une zone d'écran par OCR

    Args:
        region: Zone à capturer (x, y, width, height)

    Returns:
        {
            "detected_pokemon": [str | None, str | None, ...]  # Liste de 6 noms
        }
    """
    try:
        detected = []
        section_height = region.height // 6

        print(f"[Team OCR] Détection depuis zone: {region.x}, {region.y}, {region.width}x{region.height}")

        # Capture et OCR chaque section (slot)
        with ScreenCapture() as screen:
            for i in range(6):
                section_y = region.y + (i * section_height)

                # Capture la section
                image = screen.capture_region(
                    x=region.x,
                    y=section_y,
                    width=region.width,
                    height=section_height
                )

                # Détecte le Pokémon via OCR
                pokemon_name, confidence = ocr_engine.detect_pokemon(image)

                print(f"[Team OCR] Slot {i+1}: '{pokemon_name}' (confiance: {confidence:.1f}%)")
                detected.append(pokemon_name if pokemon_name else None)

        return {
            "detected_pokemon": detected,
            "count": sum(1 for p in detected if p)
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Tesseract OCR n'est pas installé"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OCR: {str(e)}")
