from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class OverlayWindow(QWidget):
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.current_pokemon = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setup_geometry()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        self.title_label = QLabel("🎮 PRO Helper")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 180);
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        self.pokemon_label = QLabel("Aucun Pokémon sélectionné")
        self.pokemon_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 160);
                padding: 8px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        self.pokemon_label.setWordWrap(True)
        
        self.matchup_label = QLabel("")
        self.matchup_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 160);
                padding: 8px;
                border-radius: 5px;
                font-size: 11px;
            }
        """)
        self.matchup_label.setWordWrap(True)
        
        self.ev_label = QLabel("")
        self.ev_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 160);
                padding: 8px;
                border-radius: 5px;
                font-size: 11px;
            }
        """)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.pokemon_label)
        layout.addWidget(self.matchup_label)
        layout.addWidget(self.ev_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def setup_geometry(self):
        from PyQt6.QtGui import QGuiApplication
        
        screen = QGuiApplication.primaryScreen().geometry()
        
        width = int(screen.width() * self.config['overlay']['width_percent'] / 100)
        height = int(screen.height() * self.config['overlay']['height_percent'] / 100)
        
        x = screen.width() - width - 20
        y = 20
        
        self.setGeometry(x, y, width, height)
        
    def update_pokemon(self, pokemon_data, matchup_data):
        if not pokemon_data:
            return
            
        self.current_pokemon = pokemon_data
        
        types_str = " / ".join([t.upper() for t in pokemon_data['types']])
        info_text = f"📛 {pokemon_data['name']} (#{pokemon_data['id']})\n"
        info_text += f"🏷️ {types_str}\n"
        info_text += f"💪 HP:{pokemon_data['stats']['hp']} ATK:{pokemon_data['stats']['attack']} DEF:{pokemon_data['stats']['defense']}"
        self.pokemon_label.setText(info_text)
        
        matchup_text = "⚔️ FAIBLESSES / RÉSISTANCES\n\n"
        if matchup_data['quad_weak']:
            matchup_text += f"🔴 x4: {', '.join([t.upper() for t in matchup_data['quad_weak']])}\n"
        if matchup_data['weak']:
            matchup_text += f"🟠 x2: {', '.join([t.upper() for t in matchup_data['weak']])}\n"
        if matchup_data['resistant']:
            matchup_text += f"🟢 x0.5: {', '.join([t.upper() for t in matchup_data['resistant']])}\n"
        if matchup_data['quad_resistant']:
            matchup_text += f"🟢 x0.25: {', '.join([t.upper() for t in matchup_data['quad_resistant']])}\n"
        if matchup_data['immune']:
            matchup_text += f"⚪ x0: {', '.join([t.upper() for t in matchup_data['immune']])}\n"
        self.matchup_label.setText(matchup_text)
        
        if pokemon_data['evs']:
            ev_text = "💎 EVs: "
            ev_list = [f"+{ev['value']} {ev['stat'].upper()}" for ev in pokemon_data['evs']]
            ev_text += ", ".join(ev_list)
            self.ev_label.setText(ev_text)
        else:
            self.ev_label.setText("💎 Aucun EV")
        
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
