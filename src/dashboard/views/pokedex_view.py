from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
from src.dashboard.styles.theme import Theme
from src.dashboard.widgets.pokemon_card import PokemonCard
from src.data.pokeapi_client import PokeAPIClient


class PokedexView(QWidget):
    
    pokemon_selected = pyqtSignal(dict, dict)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.api_client = PokeAPIClient(
            use_cache=config['api']['use_cache'],
            cache_days=config['api']['cache_duration_days']
        )
        self.current_pokemon = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        title = QLabel("📚 Pokédex")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        search_layout = QHBoxLayout()
        search_layout.setSpacing(15)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un Pokémon (nom anglais ou numéro)...")
        self.search_input.setStyleSheet(Theme.get_search_input_style())
        self.search_input.returnPressed.connect(self.search_pokemon)
        
        search_btn = QPushButton("🔍 Rechercher")
        search_btn.setStyleSheet(Theme.get_button_style(Theme.COLORS['primary'], Theme.COLORS['primary_dark']))
        search_btn.clicked.connect(self.search_pokemon)
        
        overlay_btn = QPushButton("📤 Envoyer à l'overlay")
        overlay_btn.setStyleSheet(Theme.get_button_style(Theme.COLORS['secondary'], Theme.COLORS['secondary_dark']))
        overlay_btn.clicked.connect(self.send_to_overlay)
        
        search_layout.addWidget(self.search_input, 4)
        search_layout.addWidget(search_btn, 1)
        search_layout.addWidget(overlay_btn, 1)
        layout.addLayout(search_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(Theme.get_scrollarea_style())
        
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        self.result_widget.setLayout(self.result_layout)
        scroll.setWidget(self.result_widget)
        
        layout.addWidget(scroll)
        self.setLayout(layout)
        
    def search_pokemon(self):
        name = self.search_input.text().strip()
        if not name:
            return
            
        for i in reversed(range(self.result_layout.count())): 
            self.result_layout.itemAt(i).widget().setParent(None)
        
        loading = QLabel("⏳ Chargement...")
        loading.setStyleSheet("font-size: 18px; color: white; padding: 40px;")
        loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_layout.addWidget(loading)
        
        pokemon = self.api_client.get_pokemon(name)
        
        for i in reversed(range(self.result_layout.count())): 
            self.result_layout.itemAt(i).widget().setParent(None)
        
        if not pokemon:
            error = QLabel(f"❌ Pokémon introuvable: {name}")
            error.setStyleSheet(f"font-size: 18px; color: {Theme.COLORS['danger']}; padding: 40px;")
            error.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.result_layout.addWidget(error)
            self.current_pokemon = None
            return
            
        self.current_pokemon = pokemon
        card = PokemonCard(pokemon)
        self.result_layout.addWidget(card)
        
    def send_to_overlay(self):
        if not self.current_pokemon:
            return
        from src.data.type_matchup import TypeMatchup
        matchup = TypeMatchup.get_weaknesses_resistances(self.current_pokemon['types'])
        self.pokemon_selected.emit(self.current_pokemon, matchup)
