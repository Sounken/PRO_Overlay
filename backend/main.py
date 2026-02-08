"""
Pokemon Revolution Online Helper - Backend FastAPI
Point d'entrée principal du serveur backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import argparse

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
