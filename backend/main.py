"""
Pokemon Revolution Online Helper - Backend FastAPI
Point d'entrée principal du serveur backend
"""
import sys
import os

# Fix Windows console encoding for UTF-8 (required for EasyOCR progress bar)
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if sys.stdout:
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr:
        sys.stderr.reconfigure(encoding='utf-8')

# Fix Pillow 11.x compatibility - restore ANTIALIAS constant for EasyOCR
# EasyOCR uses deprecated PIL.Image.ANTIALIAS which was removed in Pillow 11
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        # ANTIALIAS was an alias for LANCZOS in older Pillow versions
        Image.ANTIALIAS = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else 1
except Exception as e:
    print(f"Warning: Could not patch PIL.Image.ANTIALIAS: {e}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import argparse
import logging

# Configure logging to display all debug info
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from routes import ocr, pokemon, cache, team

app = FastAPI(
    title="PRO Helper API",
    description="Backend API for Pokemon Revolution Online Helper",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(ocr.router, prefix="/ocr", tags=["OCR"])
app.include_router(pokemon.router, prefix="/pokemon", tags=["Pokemon"])
app.include_router(cache.router, prefix="/cache", tags=["Cache"])
app.include_router(team.router, prefix="/team", tags=["Team"])


@app.get("/")
async def root():
    """Route racine"""
    return {
        "message": "PRO Helper API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Endpoint de santé pour vérifier que le backend est prêt"""
    return {"status": "ok"}


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port du serveur")
    parser.add_argument("--host", type=str, default="localhost", help="Host du serveur")
    args = parser.parse_args()

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info"
    )


if __name__ == "__main__":
    main()
