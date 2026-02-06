"""
Modèles Pydantic pour les données de l'API
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class OCRRegion(BaseModel):
    """Région de l'écran pour la détection OCR"""
    x: int
    y: int
    width: int
    height: int


class OCRDetectionRequest(BaseModel):
    """Requête de détection OCR"""
    region: Optional[OCRRegion] = None  # Si None, capture tout l'écran


class OCRDetectionResponse(BaseModel):
    """Réponse de détection OCR"""
    pokemon_name: str
    confidence: float
    timestamp: str


class TypeEffectiveness(BaseModel):
    """Efficacité d'un type contre un autre"""
    type_name: str
    multiplier: float  # 0, 0.25, 0.5, 1, 2, 4
    color: str  # Couleur officielle du type


class PokemonStats(BaseModel):
    """Statistiques d'un Pokémon"""
    hp: int
    attack: int
    defense: int
    sp_attack: int = Field(alias="special-attack")
    sp_defense: int = Field(alias="special-defense")
    speed: int

    class Config:
        populate_by_name = True


class EffortValues(BaseModel):
    """EVs obtenus en battant ce Pokémon"""
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int


class PokemonType(BaseModel):
    """Type d'un Pokémon"""
    name: str
    color: str
    icon_url: str


class PokemonResponse(BaseModel):
    """Réponse complète d'un Pokémon"""
    id: int
    name: str  # Nom anglais
    french_name: Optional[str] = None
    types: List[PokemonType]
    stats: PokemonStats
    evs: EffortValues
    sprite_url: str
    color: str  # Couleur dominante
    generation: int
    type_effectiveness: Dict[str, TypeEffectiveness]  # Tableau des 18 types


class TeamPokemon(BaseModel):
    """Pokémon dans l'équipe du joueur"""
    pokemon_id: int
    nickname: Optional[str] = None
    level: int
    moves: List[str]  # Noms des attaques


class BattleRecommendation(BaseModel):
    """Recommandation pour un combat"""
    best_move: Optional[str] = None  # Meilleure attaque à utiliser
    switch_to: Optional[str] = None  # Pokémon à envoyer
    type_advantages: List[str]  # Types efficaces contre l'adversaire
    warnings: List[str]  # Avertissements (ex: très efficace contre toi)


class CacheStats(BaseModel):
    """Statistiques du cache"""
    total_entries: int
    cache_size_mb: float
    oldest_entry: Optional[str] = None
    newest_entry: Optional[str] = None
