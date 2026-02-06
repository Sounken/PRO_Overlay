class TypeMatchup:
    """Calcul des efficacités de types"""
    
    # Tableau d'efficacité (attaquant -> défenseur)
    EFFECTIVENESS = {
        'normal': {
            'rock': 0.5, 'ghost': 0, 'steel': 0.5
        },
        'fire': {
            'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 2, 'bug': 2, 
            'rock': 0.5, 'dragon': 0.5, 'steel': 2
        },
        'water': {
            'fire': 2, 'water': 0.5, 'grass': 0.5, 'ground': 2, 
            'rock': 2, 'dragon': 0.5
        },
        'electric': {
            'water': 2, 'electric': 0.5, 'grass': 0.5, 'ground': 0, 
            'flying': 2, 'dragon': 0.5
        },
        'grass': {
            'fire': 0.5, 'water': 2, 'grass': 0.5, 'poison': 0.5, 
            'ground': 2, 'flying': 0.5, 'bug': 0.5, 'rock': 2, 
            'dragon': 0.5, 'steel': 0.5
        },
        'ice': {
            'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 0.5, 
            'ground': 2, 'flying': 2, 'dragon': 2, 'steel': 0.5
        },
        'fighting': {
            'normal': 2, 'ice': 2, 'poison': 0.5, 'flying': 0.5, 
            'psychic': 0.5, 'bug': 0.5, 'rock': 2, 'ghost': 0, 
            'dark': 2, 'steel': 2, 'fairy': 0.5
        },
        'poison': {
            'grass': 2, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 
            'ghost': 0.5, 'steel': 0, 'fairy': 2
        },
        'ground': {
            'fire': 2, 'electric': 2, 'grass': 0.5, 'poison': 2, 
            'flying': 0, 'bug': 0.5, 'rock': 2, 'steel': 2
        },
        'flying': {
            'electric': 0.5, 'grass': 2, 'fighting': 2, 'bug': 2, 
            'rock': 0.5, 'steel': 0.5
        },
        'psychic': {
            'fighting': 2, 'poison': 2, 'psychic': 0.5, 'dark': 0, 
            'steel': 0.5
        },
        'bug': {
            'fire': 0.5, 'grass': 2, 'fighting': 0.5, 'poison': 0.5, 
            'flying': 0.5, 'psychic': 2, 'ghost': 0.5, 'dark': 2, 
            'steel': 0.5, 'fairy': 0.5
        },
        'rock': {
            'fire': 2, 'ice': 2, 'fighting': 0.5, 'ground': 0.5, 
            'flying': 2, 'bug': 2, 'steel': 0.5
        },
        'ghost': {
            'normal': 0, 'psychic': 2, 'ghost': 2, 'dark': 0.5
        },
        'dragon': {
            'dragon': 2, 'steel': 0.5, 'fairy': 0
        },
        'dark': {
            'fighting': 0.5, 'psychic': 2, 'ghost': 2, 'dark': 0.5, 
            'fairy': 0.5
        },
        'steel': {
            'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2, 
            'rock': 2, 'steel': 0.5, 'fairy': 2
        },
        'fairy': {
            'fire': 0.5, 'fighting': 2, 'poison': 0.5, 'dragon': 2, 
            'dark': 2, 'steel': 0.5
        }
    }
    
    @staticmethod
    def get_defensive_matchup(defender_types):
        """
        Calcule les multiplicateurs défensifs pour un Pokémon
        
        Args:
            defender_types: liste des types du défenseur (ex: ['water', 'flying'])
            
        Returns:
            dict: {type_attaquant: multiplicateur}
        """
        matchups = {}
        
        # Tous les types possibles
        all_types = list(TypeMatchup.EFFECTIVENESS.keys())
        
        for attacking_type in all_types:
            multiplier = 1.0
            
            # Calculer pour chaque type défensif
            for defender_type in defender_types:
                if attacking_type in TypeMatchup.EFFECTIVENESS:
                    effectiveness = TypeMatchup.EFFECTIVENESS[attacking_type]
                    if defender_type in effectiveness:
                        multiplier *= effectiveness[defender_type]
                        
            matchups[attacking_type] = multiplier
            
        return matchups
    
    @staticmethod
    def get_weaknesses_resistances(defender_types):
        """
        Retourne faiblesses et résistances formatées
        
        Returns:
            dict: {
                'immune': [types],
                'quad_weak': [types],
                'weak': [types],
                'resistant': [types],
                'quad_resistant': [types]
            }
        """
        matchups = TypeMatchup.get_defensive_matchup(defender_types)
        
        result = {
            'immune': [],
            'quad_weak': [],
            'weak': [],
            'resistant': [],
            'quad_resistant': []
        }
        
        for attack_type, multiplier in matchups.items():
            if multiplier == 0:
                result['immune'].append(attack_type)
            elif multiplier >= 4:
                result['quad_weak'].append(attack_type)
            elif multiplier >= 2:
                result['weak'].append(attack_type)
            elif multiplier <= 0.25:
                result['quad_resistant'].append(attack_type)
            elif multiplier <= 0.5:
                result['resistant'].append(attack_type)
                
        return result
