"""
Routes API pour la détection OCR
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
import traceback

from models.schemas import OCRDetectionRequest, OCRDetectionResponse
from services import ScreenCapture, OCREngine

logger = logging.getLogger(__name__)

router = APIRouter()
ocr_engine = OCREngine(confidence_threshold=0.50)  # 50% de confiance minimum (strict mais pas trop)


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
        logger.info("[OCR DEBUG] Starting debug OCR request")

        with ScreenCapture() as screen:
            if request.region:
                logger.info(f"[OCR DEBUG] Capturing region: {request.region}")
                image = screen.capture_region(
                    x=request.region.x,
                    y=request.region.y,
                    width=request.region.width,
                    height=request.region.height
                )
            else:
                logger.info("[OCR DEBUG] No region specified, using center 60% of screen")
                screen_width, screen_height = screen.get_screen_size()
                margin_x = int(screen_width * 0.2)
                margin_y = int(screen_height * 0.2)
                image = screen.capture_region(
                    x=margin_x,
                    y=margin_y,
                    width=screen_width - (2 * margin_x),
                    height=screen_height - (2 * margin_y)
                )

        logger.info(f"[OCR DEBUG] Image captured: {image.size if image else 'None'}")

        # Extraction brute du texte et confiance
        text, confidence = ocr_engine.extract_text(image)
        logger.info(f"[OCR DEBUG] Extracted text: '{text}' (confidence: {confidence})")

        pokemon_name = ocr_engine.find_closest_pokemon(text)
        logger.info(f"[OCR DEBUG] Detected Pokemon: {pokemon_name}")

        return {
            "raw_text": text,
            "confidence": confidence,
            "confidence_threshold": ocr_engine.confidence_threshold,
            "detected_pokemon": pokemon_name,
            "passed_threshold": confidence >= ocr_engine.confidence_threshold
        }
    except Exception as e:
        error_msg = f"Debug error: {str(e)}\n{traceback.format_exc()}"
        logger.error(f"[OCR DEBUG ERROR] {error_msg}")
        raise HTTPException(status_code=500, detail=str(e))
