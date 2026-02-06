"""
Service de calcul de l'efficacité des types Pokémon
"""
from typing import List, Dict

# Couleurs officielles des types Pokémon
TYPE_COLORS = {
    "normal": "#A8A878",
    "fire": "#F08030",
    "water": "#6890F0",
    "electric": "#F8D030",
    "grass": "#78C850",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "dark": "#705848",
    "steel": "#B8B8D0",
    "fairy": "#EE99AC"
}

# Tableau d'efficacité des types (attaquant → défenseur → multiplicateur)
TYPE_EFFECTIVENESS = {
    "normal": {
        "rock": 0.5, "ghost": 0, "steel": 0.5
    },
    "fire": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5,
        "dragon": 0.5, "steel": 2
    },
    "water": {
        "fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5
    },
    "electric": {
        "water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5
    },
    "grass": {
        "fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5,
        "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5
    },
    "ice": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2,
        "dragon": 2, "steel": 0.5
    },
    "fighting": {
        "normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5,
        "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5
    },
    "poison": {
        "grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0,
        "fairy": 2
    },
    "ground": {
        "fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5,
        "rock": 2, "steel": 2
    },
    "flying": {
        "electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5
    },
    "psychic": {
        "fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5
    },
    "bug": {
        "fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5,
        "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5, "fairy": 0.5
    },
    "rock": {
        "fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2,
        "steel": 0.5
    },
    "ghost": {
        "normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5
    },
    "dragon": {
        "dragon": 2, "steel": 0.5, "fairy": 0
    },
    "dark": {
        "fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5
    },
    "steel": {
        "fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5,
        "fairy": 2
    },
    "fairy": {
        "fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5
    }
}


class TypeMatchupCalculator:
    """Calculateur d'efficacité des types"""

    @staticmethod
    def get_type_color(type_name: str) -> str:
        """Retourne la couleur d'un type"""
        return TYPE_COLORS.get(type_name.lower(), "#777777")

    @staticmethod
    def calculate_effectiveness(attacking_type: str, defending_types: List[str]) -> float:
        """
        Calcule l'efficacité d'un type attaquant contre un/des type(s) défenseur(s)

        Args:
            attacking_type: Type de l'attaque
            defending_types: Type(s) du défenseur (1 ou 2 types)

        Returns:
            Multiplicateur final (produit des multiplicateurs)
        """
        attacking_type = attacking_type.lower()
        multiplier = 1.0

        for defending_type in defending_types:
            defending_type = defending_type.lower()
            effectiveness = TYPE_EFFECTIVENESS.get(attacking_type, {})
            type_multiplier = effectiveness.get(defending_type, 1.0)
            multiplier *= type_multiplier

        return multiplier

    @staticmethod
    def get_all_type_effectiveness(defending_types: List[str]) -> Dict[str, Dict]:
        """
        Calcule l'efficacité de tous les types contre un Pokémon défenseur

        Args:
            defending_types: Type(s) du Pokémon défenseur

        Returns:
            Dictionnaire {type: {multiplier, color}}
        """
        result = {}
        all_types = list(TYPE_COLORS.keys())

        for attacking_type in all_types:
            multiplier = TypeMatchupCalculator.calculate_effectiveness(
                attacking_type, defending_types
            )
            result[attacking_type] = {
                "multiplier": multiplier,
                "color": TYPE_COLORS[attacking_type]
            }

        return result

    @staticmethod
    def get_weaknesses(defending_types: List[str]) -> List[str]:
        """Retourne les types super efficaces (×2 ou ×4) contre ce Pokémon"""
        effectiveness = TypeMatchupCalculator.get_all_type_effectiveness(defending_types)
        return [
            type_name for type_name, data in effectiveness.items()
            if data["multiplier"] >= 2.0
        ]

    @staticmethod
    def get_resistances(defending_types: List[str]) -> List[str]:
        """Retourne les types peu efficaces (×0.5 ou ×0.25) contre ce Pokémon"""
        effectiveness = TypeMatchupCalculator.get_all_type_effectiveness(defending_types)
        return [
            type_name for type_name, data in effectiveness.items()
            if 0 < data["multiplier"] <= 0.5
        ]

    @staticmethod
    def get_immunities(defending_types: List[str]) -> List[str]:
        """Retourne les types sans effet (×0) contre ce Pokémon"""
        effectiveness = TypeMatchupCalculator.get_all_type_effectiveness(defending_types)
        return [
            type_name for type_name, data in effectiveness.items()
            if data["multiplier"] == 0
        ]
