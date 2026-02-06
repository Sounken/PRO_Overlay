import requests
import json
import os
from datetime import datetime, timedelta

class PokeAPIClient:
    """Client pour interagir avec PokeAPI"""
    
    BASE_URL = "https://pokeapi.co/api/v2"
    CACHE_DIR = "data/cache"
    
    def __init__(self, use_cache=True, cache_days=30):
        self.use_cache = use_cache
        self.cache_days = cache_days
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """Crée le dossier cache s'il n'existe pas"""
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        
    def _get_cache_path(self, pokemon_name):
        """Retourne le chemin du fichier cache"""
        return os.path.join(self.CACHE_DIR, f"{pokemon_name.lower()}.json")
        
    def _is_cache_valid(self, cache_path):
        """Vérifie si le cache est encore valide"""
        if not os.path.exists(cache_path):
            return False
            
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - file_time < timedelta(days=self.cache_days)
        
    def _save_cache(self, pokemon_name, data):
        """Sauvegarde les données en cache"""
        cache_path = self._get_cache_path(pokemon_name)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    def _load_cache(self, pokemon_name):
        """Charge les données depuis le cache"""
        cache_path = self._get_cache_path(pokemon_name)
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def get_pokemon(self, pokemon_name):
        pokemon_name = pokemon_name.lower().strip()
        
        # Vérifier cache
        if self.use_cache and self._is_cache_valid(self._get_cache_path(pokemon_name)):
            print(f"📦 Chargement depuis cache: {pokemon_name}")
            return self._load_cache(pokemon_name)
            
        # Requête API
        try:
            print(f"🌐 Récupération depuis API: {pokemon_name}")
            response = requests.get(f"{self.BASE_URL}/pokemon/{pokemon_name}", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Extraction des données importantes
            pokemon_data = {
                'name': data['name'].capitalize(),
                'id': data['id'],
                'types': [t['type']['name'] for t in data['types']],
                'stats': {
                    stat['stat']['name']: stat['base_stat'] 
                    for stat in data['stats']
                },
                'sprite': data['sprites']['front_default'],
                'evs': [
                    {'stat': stat['stat']['name'], 'value': stat['effort']}
                    for stat in data['stats'] 
                    if stat['effort'] > 0
                ]
            }
            
            # Sauvegarder en cache
            if self.use_cache:
                self._save_cache(pokemon_name, pokemon_data)
                
            return pokemon_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur API: {e}")
            return None
        except KeyError as e:
            print(f"❌ Pokémon introuvable: {pokemon_name}")
            return None
