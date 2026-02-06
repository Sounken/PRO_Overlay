from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton, QScrollArea, 
                              QFrame, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import requests
from src.data.pokeapi_client import PokeAPIClient
from src.data.type_matchup import TypeMatchup


class DashboardWindow(QMainWindow):
    
    pokemon_selected = pyqtSignal(dict, dict)
    
    TYPE_COLORS = {
        'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0',
        'electric': '#F8D030', 'grass': '#78C850', 'ice': '#98D8D8',
        'fighting': '#C03028', 'poison': '#A040A0', 'ground': '#E0C068',
        'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
        'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8',
        'dark': '#705848', 'steel': '#B8B8D0', 'fairy': '#EE99AC'
    }
    
    TYPE_NAMES_FR = {
        'normal': 'Normal', 'fire': 'Feu', 'water': 'Eau',
        'electric': 'Électrik', 'grass': 'Plante', 'ice': 'Glace',
        'fighting': 'Combat', 'poison': 'Poison', 'ground': 'Sol',
        'flying': 'Vol', 'psychic': 'Psy', 'bug': 'Insecte',
        'rock': 'Roche', 'ghost': 'Spectre', 'dragon': 'Dragon',
        'dark': 'Ténèbres', 'steel': 'Acier', 'fairy': 'Fée'
    }
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.api_client = PokeAPIClient(
            use_cache=config['api']['use_cache'],
            cache_days=config['api']['cache_duration_days']
        )
        self.current_pokemon = None
        self.current_view = "pokedex"
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Pokemon PRO Helper - Dashboard")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #f5f6fa;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_area.setLayout(self.content_layout)
        main_layout.addWidget(self.content_area)
        
        central_widget.setLayout(main_layout)
        
        self.show_pokedex_view()
        
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(80)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 3px solid #34495e;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(10)
        
        buttons_config = [
            ("📚", "Pokédex", "pokedex"),
            ("👥", "Équipe", "team"),
            ("🧮", "Calculs", "calculator"),
            ("⚙️", "Config", "settings")
        ]
        
        for icon, tooltip, view_name in buttons_config:
            btn = QPushButton(icon)
            btn.setToolTip(tooltip)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495e;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 24px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
            """)
            btn.clicked.connect(lambda checked, v=view_name: self.switch_view(v))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        layout.addStretch()
        sidebar.setLayout(layout)
        return sidebar
        
    def switch_view(self, view_name):
        self.current_view = view_name
        
        for i in reversed(range(self.content_layout.count())): 
            self.content_layout.itemAt(i).widget().setParent(None)
        
        if view_name == "pokedex":
            self.show_pokedex_view()
        elif view_name == "team":
            self.show_team_view()
        elif view_name == "calculator":
            self.show_calculator_view()
        elif view_name == "settings":
            self.show_settings_view()
            
    def show_pokedex_view(self):
        title = QLabel("📚 Pokédex")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        self.content_layout.addWidget(title)
        
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nom anglais ou #numéro (ex: charizard, pikachu, 6)...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #3498db;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border: 2px solid #2980b9;
                background-color: white;
            }
        """)
        self.search_input.returnPressed.connect(self.search_pokemon)
        
        search_btn = QPushButton("🔍 Rechercher")
        search_btn.setStyleSheet(self.get_button_style("#3498db", "#2980b9"))
        search_btn.clicked.connect(self.search_pokemon)
        
        send_overlay_btn = QPushButton("📤 Overlay")
        send_overlay_btn.setStyleSheet(self.get_button_style("#27ae60", "#229954"))
        send_overlay_btn.clicked.connect(self.send_to_overlay)
        
        search_layout.addWidget(self.search_input, 4)
        search_layout.addWidget(search_btn, 1)
        search_layout.addWidget(send_overlay_btn, 1)
        search_frame.setLayout(search_layout)
        self.content_layout.addWidget(search_frame)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_layout.setContentsMargins(0, 10, 0, 0)
        self.result_widget.setLayout(self.result_layout)
        scroll.setWidget(self.result_widget)
        
        self.content_layout.addWidget(scroll)
        
    def get_button_style(self, bg_color, hover_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
        
    def search_pokemon(self):
        pokemon_name = self.search_input.text().strip()
        if not pokemon_name:
            return
        
        for i in reversed(range(self.result_layout.count())): 
            self.result_layout.itemAt(i).widget().setParent(None)
        
        loading = QLabel("⏳ Recherche en cours...")
        loading.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 20px;")
        self.result_layout.addWidget(loading)
        
        pokemon = self.api_client.get_pokemon(pokemon_name)
        
        for i in reversed(range(self.result_layout.count())): 
            self.result_layout.itemAt(i).widget().setParent(None)
        
        if not pokemon:
            error = QLabel(f"❌ Pokémon introuvable: {pokemon_name}")
            error.setStyleSheet("font-size: 16px; color: #e74c3c; padding: 20px;")
            self.result_layout.addWidget(error)
            self.current_pokemon = None
            return
            
        self.current_pokemon = pokemon
        self.display_pokemon_detailed(pokemon)
        
    def display_pokemon_detailed(self, pokemon):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
            }
        """)
        card_layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        
        left_header = QVBoxLayout()
        display_name = pokemon.get('french_name', pokemon['name'])
        name_id = QLabel(f"#{pokemon['id']:03d}  {display_name}")
        name_id.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50;")
        left_header.addWidget(name_id)
        
        types_layout = QHBoxLayout()
        for ptype in pokemon['types']:
            type_label = QLabel(self.TYPE_NAMES_FR[ptype])
            type_label.setStyleSheet(self.get_type_badge_style(ptype))
            types_layout.addWidget(type_label)
        types_layout.addStretch()
        left_header.addLayout(types_layout)
        
        header_layout.addLayout(left_header, 3)
        
        if pokemon['sprite']:
            sprite_label = QLabel()
            try:
                response = requests.get(pokemon['sprite'], timeout=5)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                sprite_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except:
                sprite_label.setText("🖼️")
                sprite_label.setStyleSheet("font-size: 48px;")
            header_layout.addWidget(sprite_label, 1, Qt.AlignmentFlag.AlignRight)
        
        card_layout.addLayout(header_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #bdc3c7; margin: 15px 0;")
        card_layout.addWidget(separator)
        
        info_grid = QHBoxLayout()
        
        info_items = [
            ("🧬", "Génération", self.get_generation(pokemon['id'])),
            ("🎯", "Catch Rate", pokemon.get('capture_rate', 'N/A')),
            ("⭐", "Total Base", sum(pokemon['stats'].values())),
            ("🌍", "Obtainability", "Standard")
        ]
        
        for icon, label, value in info_items:
            info_box = QFrame()
            info_box.setStyleSheet("""
                QFrame {
                    background-color: #ecf0f1;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
            info_layout = QVBoxLayout()
            info_layout.setSpacing(5)
            
            icon_label = QLabel(f"{icon} {label}")
            icon_label.setStyleSheet("font-size: 11px; color: #7f8c8d; font-weight: bold;")
            value_label = QLabel(str(value))
            value_label.setStyleSheet("font-size: 18px; color: #2c3e50; font-weight: bold;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            info_layout.addWidget(icon_label)
            info_layout.addWidget(value_label)
            info_box.setLayout(info_layout)
            info_grid.addWidget(info_box)
        
        card_layout.addLayout(info_grid)
        
        stats_label = QLabel("📊 Statistiques de Base")
        stats_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 20px;")
        card_layout.addWidget(stats_label)
        
        stats_order = [
            ('hp', '💚 HP', '#FF5959'),
            ('attack', '⚔️ Attack', '#F5AC78'),
            ('defense', '🛡️ Defense', '#FAE078'),
            ('special-attack', '✨ Sp. Atk', '#9DB7F5'),
            ('special-defense', '🌟 Sp. Def', '#A7DB8D'),
            ('speed', '⚡ Speed', '#FA92B2')
        ]
        
        for stat_key, stat_label, color in stats_order:
            stat_value = pokemon['stats'][stat_key]
            
            stat_row = QHBoxLayout()
            stat_row.setSpacing(10)
            
            label = QLabel(stat_label)
            label.setFixedWidth(120)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            stat_row.addWidget(label)
            
            progress = QProgressBar()
            progress.setMaximum(255)
            progress.setValue(stat_value)
            progress.setTextVisible(False)
            progress.setFixedHeight(28)
            progress.setStyleSheet(f"""
                QProgressBar {{
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                    background-color: #ecf0f1;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 3px;
                }}
            """)
            stat_row.addWidget(progress, 3)
            
            value_label = QLabel(str(stat_value))
            value_label.setMinimumWidth(50)
            value_label.setMaximumWidth(50)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; padding: 5px;")
            stat_row.addWidget(value_label)
            
            card_layout.addLayout(stat_row)
        
        matchup_label = QLabel("⚔️ Sensibilités aux Types")
        matchup_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 25px; margin-bottom: 10px;")
        card_layout.addWidget(matchup_label)
        
        matchup = TypeMatchup.get_defensive_matchup(pokemon['types'])
        
        type_grid = QGridLayout()
        type_grid.setSpacing(8)
        type_grid.setContentsMargins(0, 0, 0, 0)
        
        all_types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice',
                     'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
                     'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
        
        row, col = 0, 0
        for ptype in all_types:
            multiplier = matchup.get(ptype, 1.0)
            
            type_frame = QFrame()
            type_frame.setFixedSize(120, 65)
            
            bg_color = self.TYPE_COLORS[ptype]
            
            if multiplier == 0:
                mult_text = "× 0"
                border_color = "#95a5a6"
                border_width = "4"
            elif multiplier == 0.25:
                mult_text = "× ¼"
                border_color = "#27ae60"
                border_width = "4"
            elif multiplier == 0.5:
                mult_text = "× ½"
                border_color = "#27ae60"
                border_width = "3"
            elif multiplier == 2:
                mult_text = "× 2"
                border_color = "#e67e22"
                border_width = "3"
            elif multiplier == 4:
                mult_text = "× 4"
                border_color = "#e74c3c"
                border_width = "4"
            else:
                mult_text = ""
                border_color = "#d0d0d0"
                border_width = "2"
            
            type_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border: {border_width}px solid {border_color};
                    border-radius: 8px;
                }}
            """)
            
            type_layout = QVBoxLayout()
            type_layout.setContentsMargins(5, 8, 5, 8)
            type_layout.setSpacing(3)
            
            type_name = QLabel(self.TYPE_NAMES_FR[ptype])
            type_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            type_name.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
            type_layout.addWidget(type_name)
            
            if mult_text:
                mult_label = QLabel(mult_text)
                mult_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                mult_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
                type_layout.addWidget(mult_label)
            
            type_frame.setLayout(type_layout)
            type_grid.addWidget(type_frame, row, col)
            
            col += 1
            if col >= 6:
                col = 0
                row += 1
        
        card_layout.addLayout(type_grid)
        
        if pokemon['evs']:
            ev_label = QLabel("💎 Effort Values (EVs)")
            ev_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 20px;")
            card_layout.addWidget(ev_label)
            
            ev_text = ', '.join([f"+{ev['value']} {ev['stat'].upper()}" for ev in pokemon['evs']])
            ev_display = QLabel(ev_text)
            ev_display.setStyleSheet("font-size: 14px; color: #27ae60; background-color: #d5f4e6; padding: 10px; border-radius: 5px;")
            card_layout.addWidget(ev_display)
        
        card.setLayout(card_layout)
        self.result_layout.addWidget(card)
        
    def get_type_badge_style(self, ptype):
        color = self.TYPE_COLORS.get(ptype.lower(), '#777')
        return f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 8px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }}
        """
        
    def get_generation(self, pokemon_id):
        if pokemon_id <= 151:
            return "I"
        elif pokemon_id <= 251:
            return "II"
        elif pokemon_id <= 386:
            return "III"
        elif pokemon_id <= 493:
            return "IV"
        elif pokemon_id <= 649:
            return "V"
        elif pokemon_id <= 721:
            return "VI"
        elif pokemon_id <= 809:
            return "VII"
        elif pokemon_id <= 905:
            return "VIII"
        else:
            return "IX"
            
    def show_team_view(self):
        title = QLabel("👥 Gestion d'Équipe")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.content_layout.addWidget(title)
        
        info = QLabel("Fonctionnalité à venir...")
        info.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 20px;")
        self.content_layout.addWidget(info)
        
    def show_calculator_view(self):
        title = QLabel("🧮 Calculateurs")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.content_layout.addWidget(title)
        
        info = QLabel("Fonctionnalité à venir...")
        info.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 20px;")
        self.content_layout.addWidget(info)
        
    def show_settings_view(self):
        title = QLabel("⚙️ Configuration")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        self.content_layout.addWidget(title)
        
        info = QLabel("Fonctionnalité à venir...")
        info.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 20px;")
        self.content_layout.addWidget(info)
        
    def send_to_overlay(self):
        if not self.current_pokemon:
            return
            
        matchup = TypeMatchup.get_weaknesses_resistances(self.current_pokemon['types'])
        self.pokemon_selected.emit(self.current_pokemon, matchup)
