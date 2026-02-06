import requests
import json
import os
from datetime import datetime, timedelta

class PokeAPIClient:
    
    BASE_URL = "https://pokeapi.co/api/v2"
    CACHE_DIR = "data/cache"
    
    POKEMON_COLORS = {
        'black': '#4a4a4a',
        'blue': '#4a9bd1',
        'brown': '#9b7653',
        'gray': '#7a7a7a',
        'green': '#5cb85c',
        'pink': '#f8a5c2',
        'purple': '#765595',
        'red': '#e74c3c',
        'white': '#e0e0e0',
        'yellow': '#f1c40f'
    }
    
    def __init__(self, use_cache=True, cache_days=30):
        self.use_cache = use_cache
        self.cache_days = cache_days
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        
    def _get_cache_path(self, pokemon_name):
        return os.path.join(self.CACHE_DIR, f"{pokemon_name.lower()}.json")
        
    def _is_cache_valid(self, cache_path):
        if not os.path.exists(cache_path):
            return False
            
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - file_time < timedelta(days=self.cache_days)
        
    def _save_cache(self, pokemon_name, data):
        cache_path = self._get_cache_path(pokemon_name)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    def _load_cache(self, pokemon_name):
        cache_path = self._get_cache_path(pokemon_name)
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_type_icon(self, type_url):
        try:
            response = requests.get(type_url, timeout=5)
            type_data = response.json()
            return type_data['sprites']['generation-ix']['scarlet-violet']['name_icon']
        except:
            return None
            
    def get_pokemon(self, pokemon_name):
        pokemon_name = pokemon_name.lower().strip()
        
        if self.use_cache and self._is_cache_valid(self._get_cache_path(pokemon_name)):
            print(f"📦 Cache: {pokemon_name}")
            return self._load_cache(pokemon_name)
            
        try:
            print(f"🌐 API: {pokemon_name}")
            response = requests.get(f"{self.BASE_URL}/pokemon/{pokemon_name}", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            species_response = requests.get(data['species']['url'], timeout=5)
            species_data = species_response.json()
            
            french_name = data['name'].capitalize()
            for name_entry in species_data.get('names', []):
                if name_entry['language']['name'] == 'fr':
                    french_name = name_entry['name']
                    break
            
            types_with_icons = []
            for type_entry in data['types']:
                type_icon = self._get_type_icon(type_entry['type']['url'])
                types_with_icons.append({
                    'name': type_entry['type']['name'],
                    'slot': type_entry['slot'],
                    'icon': type_icon
                })
            
            color_name = species_data.get('color', {}).get('name', 'gray')
            color_hex = self.POKEMON_COLORS.get(color_name, '#7a7a7a')
            
            pokemon_data = {
                'name': data['name'].capitalize(),
                'french_name': french_name,
                'id': data['id'],
                'types': [t['name'] for t in types_with_icons],
                'types_detailed': types_with_icons,
                'color': color_hex,
                'color_name': color_name,
                'stats': {
                    stat['stat']['name']: stat['base_stat'] 
                    for stat in data['stats']
                },
                'sprite': data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'],
                'evs': [
                    {'stat': stat['stat']['name'], 'value': stat['effort']}
                    for stat in data['stats'] 
                    if stat['effort'] > 0
                ],
                'generation': species_data['generation']['name'],
                'capture_rate': species_data.get('capture_rate', 0)
            }
            
            if self.use_cache:
                self._save_cache(pokemon_name, pokemon_data)
                
            return pokemon_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur API: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"❌ Pokémon introuvable: {pokemon_name}")
            return None
