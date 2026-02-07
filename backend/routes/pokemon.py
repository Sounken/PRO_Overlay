"""
Routes API pour les données Pokémon
"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from models.schemas import PokemonResponse, PokemonStats, EffortValues, PokemonType
from services import PokeAPIClient, TypeMatchupCalculator

router = APIRouter()
client = PokeAPIClient()


def extract_french_name(species_data: dict) -> Optional[str]:
    """Extrait le nom français depuis les données species"""
    for name_entry in species_data.get("names", []):
        if name_entry["language"]["name"] == "fr":
            return name_entry["name"]
    return None


def extract_generation(species_data: dict) -> int:
    """Extrait le numéro de génération"""
    gen_url = species_data.get("generation", {}).get("url", "")
    # URL format: .../generation/1/
    try:
        return int(gen_url.rstrip("/").split("/")[-1])
    except (ValueError, IndexError):
        return 1


def extract_evs(pokemon_data: dict) -> EffortValues:
    """Extrait les EVs depuis les stats"""
    evs = {
        "hp": 0,
        "attack": 0,
        "defense": 0,
        "sp_attack": 0,
        "sp_defense": 0,
        "speed": 0
    }

    stat_mapping = {
        "hp": "hp",
        "attack": "attack",
        "defense": "defense",
        "special-attack": "sp_attack",
        "special-defense": "sp_defense",
        "speed": "speed"
    }

    for stat in pokemon_data.get("stats", []):
        stat_name = stat["stat"]["name"]
        effort = stat["effort"]

        if stat_name in stat_mapping:
            evs[stat_mapping[stat_name]] = effort

    return EffortValues(**evs)


def extract_stats(pokemon_data: dict) -> PokemonStats:
    """Extrait les stats de base"""
    stats = {}

    stat_mapping = {
        "hp": "hp",
        "attack": "attack",
        "defense": "defense",
        "special-attack": "sp_attack",
        "special-defense": "sp_defense",
        "speed": "speed"
    }

    for stat in pokemon_data.get("stats", []):
        stat_name = stat["stat"]["name"]
        base_stat = stat["base_stat"]

        if stat_name in stat_mapping:
            stats[stat_mapping[stat_name]] = base_stat

    return PokemonStats(**stats)


def extract_types(pokemon_data: dict) -> list[PokemonType]:
    """Extrait les types avec icônes et couleurs depuis PokeAPI"""
    types = []

    for type_entry in pokemon_data.get("types", []):
        type_name = type_entry["type"]["name"]
        type_url = type_entry["type"]["url"]

        icon_url = ""
        try:
            # Récupère les données du type pour obtenir le sprite
            import requests
            type_response = requests.get(type_url)
            type_response.raise_for_status()
            type_data = type_response.json()

            # Extrait le sprite de generation-ix/scarlet-violet s'il existe
            sprites = type_data.get("sprites", {})
            if sprites and isinstance(sprites, dict):
                gen_ix = sprites.get("generation-ix", {})
                if gen_ix and isinstance(gen_ix, dict):
                    scarlet_violet = gen_ix.get("scarlet-violet", {})
                    if scarlet_violet and isinstance(scarlet_violet, dict):
                        icon_url = scarlet_violet.get("name_icon", "")
        except Exception as e:
            print(f"Erreur récupération sprite type {type_name}: {e}")

        # Fallback si pas de sprite trouvé
        if not icon_url:
            TYPE_IDS = {
                "normal": 1, "fighting": 2, "flying": 3, "poison": 4,
                "ground": 5, "rock": 6, "bug": 7, "ghost": 8,
                "steel": 9, "fire": 10, "water": 11, "grass": 12,
                "electric": 13, "psychic": 14, "ice": 15, "dragon": 16,
                "dark": 17, "fairy": 18
            }
            type_id = TYPE_IDS.get(type_name, 1)
            icon_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-ix/scarlet-violet/{type_id}.png"

        types.append(PokemonType(
            name=type_name,
            color=TypeMatchupCalculator.get_type_color(type_name),
            icon_url=icon_url
        ))

    return types


@router.get("/{identifier}", response_model=PokemonResponse)
async def get_pokemon(identifier: str):
    """
    Récupère les données complètes d'un Pokémon

    Args:
        identifier: Nom (anglais) ou ID du Pokémon

    Returns:
        Données complètes du Pokémon
    """
    # Récupérer depuis PokeAPI (avec cache)
    data = client.get_pokemon(identifier)

    if not data:
        raise HTTPException(status_code=404, detail=f"Pokémon '{identifier}' non trouvé")

    pokemon_data = data["pokemon"]
    species_data = data["species"]

    # Extraire les types
    types = extract_types(pokemon_data)
    type_names = [t.name for t in types]

    # Calculer l'efficacité des types
    type_effectiveness = TypeMatchupCalculator.get_all_type_effectiveness(type_names)

    # Construire la réponse
    response = PokemonResponse(
        id=pokemon_data["id"],
        name=pokemon_data["name"],
        french_name=extract_french_name(species_data),
        types=types,
        stats=extract_stats(pokemon_data),
        evs=extract_evs(pokemon_data),
        sprite_url=pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
        color=species_data["color"]["name"],
        generation=extract_generation(species_data),
        type_effectiveness={
            type_name: {
                "type_name": type_name,
                "multiplier": data["multiplier"],
                "color": data["color"]
            }
            for type_name, data in type_effectiveness.items()
        }
    )

    return response
