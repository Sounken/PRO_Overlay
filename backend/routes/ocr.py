"""
Routes API pour la détection OCR
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime

from models.schemas import OCRDetectionRequest, OCRDetectionResponse
from services import ScreenCapture, OCREngine

router = APIRouter()
ocr_engine = OCREngine(confidence_threshold=25)  # Seuil bas pour jeux vidéo


@router.post("/detect", response_model=OCRDetectionResponse)
async def detect_pokemon(request: OCRDetectionRequest):
    """
    Détecte le nom d'un Pokémon via OCR sur une région de l'écran

    Args:
        request: Région à capturer (ou None pour zone de combat centrale)

    Returns:
        Nom du Pokémon détecté et niveau de confiance
    """
    try:
        # Capture de la région
        with ScreenCapture() as screen:
            if request.region:
                # Région spécifiée par l'utilisateur
                image = screen.capture_region(
                    x=request.region.x,
                    y=request.region.y,
                    width=request.region.width,
                    height=request.region.height
                )
            else:
                # Zone de combat centrale (retire 20% de chaque côté)
                screen_width, screen_height = screen.get_screen_size()
                margin_x = int(screen_width * 0.2)
                margin_y = int(screen_height * 0.2)

                image = screen.capture_region(
                    x=margin_x,
                    y=margin_y,
                    width=screen_width - (2 * margin_x),
                    height=screen_height - (2 * margin_y)
                )

        # Détection OCR
        pokemon_name, confidence = ocr_engine.detect_pokemon(image)

        if not pokemon_name:
            print(f"[OCR] Confiance: {confidence:.1f}% (seuil: {ocr_engine.confidence_threshold}%)")
            raise HTTPException(
                status_code=404,
                detail=f"Aucun Pokémon détecté (confiance: {confidence:.1f}%)"
            )

        return OCRDetectionResponse(
            pokemon_name=pokemon_name,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        # Re-raise les HTTPException (404 notamment)
        raise
    except FileNotFoundError as e:
        # Tesseract non installé
        raise HTTPException(
            status_code=500,
            detail="Tesseract OCR n'est pas installé. Installez-le avec: choco install tesseract"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OCR: {str(e)}")


@router.get("/test")
async def test_ocr():
    """Endpoint de test pour vérifier que l'OCR fonctionne"""
    return {
        "status": "OCR engine ready",
        "engine": "tesseract",
        "confidence_threshold": ocr_engine.confidence_threshold
    }


@router.post("/debug")
async def debug_ocr(request: OCRDetectionRequest):
    """
    Endpoint de debug - retourne la confiance exacte même si < threshold
    """
    try:
        with ScreenCapture() as screen:
            if request.region:
                image = screen.capture_region(
                    x=request.region.x,
                    y=request.region.y,
                    width=request.region.width,
                    height=request.region.height
                )
            else:
                screen_width, screen_height = screen.get_screen_size()
                margin_x = int(screen_width * 0.2)
                margin_y = int(screen_height * 0.2)
                image = screen.capture_region(
                    x=margin_x,
                    y=margin_y,
                    width=screen_width - (2 * margin_x),
                    height=screen_height - (2 * margin_y)
                )

        # Extraction brute du texte et confiance
        text, confidence = ocr_engine.extract_text(image)
        pokemon_name = ocr_engine.find_closest_pokemon(text)

        return {
            "raw_text": text,
            "confidence": confidence,
            "confidence_threshold": ocr_engine.confidence_threshold,
            "detected_pokemon": pokemon_name,
            "passed_threshold": confidence >= ocr_engine.confidence_threshold
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")
