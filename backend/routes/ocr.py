"""
Routes API pour la détection OCR
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime

from models.schemas import OCRDetectionRequest, OCRDetectionResponse
from services import ScreenCapture, OCREngine

router = APIRouter()
ocr_engine = OCREngine(confidence_threshold=40)  # Abaissé pour debug


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

        # Sauvegarde debug (optionnel)
        import os
        debug_dir = os.path.join(os.path.dirname(__file__), '..', 'debug')
        os.makedirs(debug_dir, exist_ok=True)
        debug_path = os.path.join(debug_dir, 'last_capture.png')
        image.save(debug_path)
        print(f"[OCR Debug] Capture sauvegardée: {debug_path}")

        # Détection OCR
        pokemon_name, confidence = ocr_engine.detect_pokemon(image)

        # Logs pour debug
        print(f"[OCR Debug] Confiance: {confidence:.1f}%")
        print(f"[OCR Debug] Pokemon détecté: {pokemon_name}")

        if not pokemon_name:
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
