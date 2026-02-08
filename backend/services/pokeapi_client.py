"""
Client pour l'API PokeAPI avec système de cache
"""
import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DURATION_DAYS = 30


class PokeAPIClient:
    """Client pour interroger PokeAPI avec cache local"""

    def __init__(self):
        """Initialise le client et crée le répertoire de cache"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, pokemon_identifier: str) -> Path:
        """Retourne le chemin du fichier cache pour un Pokémon"""
        # Normalise le nom (minuscules, pas d'espaces)
        clean_name = str(pokemon_identifier).lower().replace(" ", "-")
        return CACHE_DIR / f"{clean_name}.json"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Vérifie si le cache est encore valide"""
        if not cache_path.exists():
            return False

        modified_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        expiration_time = modified_time + timedelta(days=CACHE_DURATION_DAYS)
        return datetime.now() < expiration_time

    def _read_cache(self, cache_path: Path) -> Optional[Dict[str, Any]]:
        """Lit les données depuis le cache"""
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lecture cache: {e}")
            return None

    def _write_cache(self, cache_path: Path, data: Dict[str, Any]):
        """Écrit les données dans le cache"""
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur écriture cache: {e}")

    def _fetch_pokemon(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Récupère les données d'un Pokémon depuis PokeAPI"""
        try:
            # Requête pokemon
            response = requests.get(f"{POKEAPI_BASE_URL}/pokemon/{identifier}")
            response.raise_for_status()
            pokemon_data = response.json()

            # Requête species pour le nom français et la couleur
            species_url = pokemon_data['species']['url']
            species_response = requests.get(species_url)
            species_response.raise_for_status()
            species_data = species_response.json()

            # Combine les données
            return {
                "pokemon": pokemon_data,
                "species": species_data,
                "cached_at": datetime.now().isoformat()
            }
        except requests.RequestException as e:
            print(f"Erreur PokeAPI: {e}")
            return None

    def get_pokemon(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Récupère les données d'un Pokémon (cache ou API)

        Args:
            identifier: Nom ou ID du Pokémon

        Returns:
            Données du Pokémon ou None si erreur
        """
        cache_path = self._get_cache_path(identifier)

        # Vérifier le cache
        if self._is_cache_valid(cache_path):
            cached_data = self._read_cache(cache_path)
            if cached_data:
                print(f"[CACHE] Cache hit for {identifier}")
                return cached_data

        # Cache invalide ou absent, fetch depuis l'API
        print(f"[FETCH] Fetching {identifier} from PokeAPI...")
        data = self._fetch_pokemon(identifier)

        if data:
            self._write_cache(cache_path, data)
            print(f"[CACHE] Data cached for {identifier}")

        return data

    def clear_cache(self, pokemon_identifier: Optional[str] = None):
        """
        Vide le cache

        Args:
            pokemon_identifier: Si spécifié, vide seulement ce Pokémon, sinon tout
        """
        if pokemon_identifier:
            cache_path = self._get_cache_path(pokemon_identifier)
            if cache_path.exists():
                cache_path.unlink()
                print(f"Cache supprimé pour {pokemon_identifier}")
        else:
            for cache_file in CACHE_DIR.glob("*.json"):
                cache_file.unlink()
            print("Cache entièrement vidé")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        cache_files = list(CACHE_DIR.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            "total_entries": len(cache_files),
            "cache_size_mb": round(total_size / (1024 * 1024), 2),
            "oldest_entry": min((f.stat().st_mtime for f in cache_files), default=None),
            "newest_entry": max((f.stat().st_mtime for f in cache_files), default=None)
        }
