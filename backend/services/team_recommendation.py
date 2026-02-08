"""
Moteur de recommandation pour les Pokémon d'équipe
"""
from typing import List, Optional, Dict, Any
from services import PokeAPIClient, TypeMatchupCalculator


class TeamRecommendationEngine:
    """Calcule les recommandations de Pokémon basées sur l'efficacité des types"""

    def __init__(self):
        self.client = PokeAPIClient()
        self.type_calc = TypeMatchupCalculator

    def calculate_matchup_score(
        self,
        attacker_types: List[str],
        defender_types: List[str]
    ) -> float:
        """
        Calcule le score offensif: meilleur type attaquant vs défenseur

        Args:
            attacker_types: Types du Pokémon attaquant
            defender_types: Types du Pokémon défenseur

        Returns:
            Meilleure efficacité parmi les types de l'attaquant
        """
        max_effectiveness = 0.0

        for att_type in attacker_types:
            eff = self.type_calc.calculate_effectiveness(att_type, defender_types)
            max_effectiveness = max(max_effectiveness, eff)

        return max_effectiveness

    def calculate_defensive_score(
        self,
        attacker_types: List[str],
        defender_types: List[str]
    ) -> float:
        """
        Calcule le score défensif: résistance aux types adverses

        Args:
            attacker_types: Types du Pokémon évalué
            defender_types: Types du Pokémon adverse

        Returns:
            Score défensif moyen (plus bas = mieux)
        """
        if not attacker_types:
            return 1.0

        total = 0.0
        for def_type in attacker_types:
            eff = self.type_calc.calculate_effectiveness(def_type, defender_types)
            total += eff

        return total / len(attacker_types)

    def recommend_switch(
        self,
        opponent_name: str,
        team: List[str],
        active_pokemon: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Recommande le meilleur Pokémon à utiliser contre l'adversaire

        Args:
            opponent_name: Nom du Pokémon adverse
            team: Liste des noms des Pokémon de l'équipe
            active_pokemon: Pokémon actuellement actif

        Returns:
            {
                "recommended_pokemon": str | None,
                "show_recommendation": bool,
                "reasoning": str
            }
        """
        try:
            print(f"[Team] Recommendation request: opponent={opponent_name}, team={team}, active={active_pokemon}")
            # Récupère les données du Pokémon adverse
            opponent_data = self.client.get_pokemon(opponent_name)

            if not opponent_data:
                return {
                    "recommended_pokemon": None,
                    "show_recommendation": False,
                    "reasoning": "Pokémon adverse non trouvé"
                }

            # Extrait les types adverses
            pokemon_data = opponent_data["pokemon"]
            opponent_types = [t["type"]["name"] for t in pokemon_data["types"]]

            best_score = -1.0
            best_pokemon = None
            best_offensive = 0.0
            best_defensive = 0.0

            # Scores du Pokémon actif (pour comparaison)
            active_score = -1.0
            active_offensive = 0.0
            active_defensive = 0.0

            # Évalue chaque Pokémon de l'équipe
            for member_name in team:
                if not member_name:  # Skip None entries
                    continue

                try:
                    member_data = self.client.get_pokemon(member_name)
                    if not member_data:
                        continue

                    member_pokemon = member_data["pokemon"]
                    member_types = [t["type"]["name"] for t in member_pokemon["types"]]

                    # Calcule les scores
                    offensive = self.calculate_matchup_score(
                        member_types,
                        opponent_types
                    )
                    defensive = self.calculate_defensive_score(
                        opponent_types,
                        member_types
                    )

                    # Score combiné (offensif pondéré 2x)
                    total_score = (offensive * 2.0) + (1.0 / defensive)

                    print(f"[Team] {member_name.upper()}: types={member_types}, offensive={offensive:.1f}x, defensive={defensive:.2f}x, score={total_score:.2f}")

                    # Garder le score du Pokémon actif
                    if member_name == active_pokemon:
                        active_score = total_score
                        active_offensive = offensive
                        active_defensive = defensive

                    # Trouver le meilleur Pokémon
                    if total_score > best_score:
                        best_score = total_score
                        best_pokemon = member_name
                        best_offensive = offensive
                        best_defensive = defensive

                except Exception as e:
                    print(f"[Team] Erreur évaluation {member_name}: {e}")
                    continue

            # Vérifie si une recommandation de changement est vraiment nécessaire
            # Ne recommander que si:
            # 1. Le meilleur Pokémon a un avantage offensif > 1.0x (super-efficace)
            # 2. Le meilleur est strictement mieux que le Pokémon actif
            should_recommend = (
                best_pokemon is not None and
                best_offensive > 1.0 and  # Avantage offensif significatif (super-efficace)
                active_pokemon is not None and  # Un Pokémon actif existe
                best_score > active_score  # Le meilleur est strictement mieux
            )

            if should_recommend:
                reasoning = (
                    f"{best_pokemon.upper()} a un avantage offensif "
                    f"({best_offensive:.1f}x) contre {opponent_name.upper()}"
                )
                recommended = best_pokemon
                show_recommendation = True
            else:
                reasoning = "Aucun changement recommandé"
                recommended = None
                show_recommendation = False

            result = {
                "recommended_pokemon": recommended,
                "show_recommendation": show_recommendation,
                "reasoning": reasoning
            }
            print(f"[Team] Recommendation result: {result}")
            return result

        except Exception as e:
            print(f"[Team] Erreur recommendation: {e}")
            return {
                "recommended_pokemon": None,
                "show_recommendation": False,
                "reasoning": f"Erreur: {str(e)}"
            }
