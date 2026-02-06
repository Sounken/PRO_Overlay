"""
Routes API pour la gestion du cache
"""
from fastapi import APIRouter
from typing import Optional

from models.schemas import CacheStats
from services import PokeAPIClient

router = APIRouter()
client = PokeAPIClient()


@router.get("/stats", response_model=CacheStats)
async def get_cache_stats():
    """Retourne les statistiques du cache"""
    stats = client.get_cache_stats()
    return CacheStats(**stats)


@router.delete("/clear")
async def clear_cache(pokemon: Optional[str] = None):
    """
    Vide le cache

    Args:
        pokemon: Nom du Pokémon (optionnel, sinon vide tout)

    Returns:
        Message de confirmation
    """
    client.clear_cache(pokemon)

    if pokemon:
        return {"message": f"Cache supprimé pour {pokemon}"}
    else:
        return {"message": "Cache entièrement vidé"}
