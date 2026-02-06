from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import requests


class PokemonCard(QWidget):
    
    def __init__(self, pokemon):
        super().__init__()
        self.pokemon = pokemon
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        content = QFrame()
        content.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.pokemon['color']},
                    stop:1 {self.adjust_color(self.pokemon['color'], -30)});
                border-radius: 20px;
            }}
        """)
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(30)
        
        left_section = self.create_left_section()
        content_layout.addLayout(left_section, 1)
        
        right_section = self.create_right_section()
        content_layout.addLayout(right_section, 1)
        
        content.setLayout(content_layout)
        main_layout.addWidget(content)
        
        self.setLayout(main_layout)
        
    def create_left_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        name_label = QLabel(self.pokemon.get('french_name', self.pokemon['name']).upper())
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(name_label)
        
        pokemon_container = QHBoxLayout()
        pokemon_container.setSpacing(0)
        
        gen_label = QLabel(self.get_generation_text())
        gen_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 2px;
                writing-mode: vertical-rl;
            }
        """)
        gen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        gen_container = QWidget()
        gen_layout = QVBoxLayout()
        gen_layout.setContentsMargins(0, 0, 20, 0)
        gen_layout.addWidget(gen_label, alignment=Qt.AlignmentFlag.AlignCenter)
        gen_container.setLayout(gen_layout)
        pokemon_container.addWidget(gen_container)
        
        if self.pokemon.get('sprite'):
            sprite_label = QLabel()
            try:
                response = requests.get(self.pokemon['sprite'], timeout=5)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                sprite_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except:
                sprite_label.setText("🎨")
                sprite_label.setStyleSheet("font-size: 80px; color: white;")
            sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pokemon_container.addWidget(sprite_label)
        
        layout.addLayout(pokemon_container)
        
        return layout
        
    def create_right_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        types_layout = QVBoxLayout()
        types_layout.setSpacing(15)
        
        for type_data in self.pokemon.get('types_detailed', []):
            type_frame = QFrame()
            type_frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    padding: 15px;
                }
            """)
            
            type_layout = QHBoxLayout()
            type_layout.setContentsMargins(10, 10, 10, 10)
            
            if type_data.get('icon'):
                icon_label = QLabel()
                try:
                    response = requests.get(type_data['icon'], timeout=3)
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    icon_label.setPixmap(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                except:
                    icon_label.setText("🏷️")
                    icon_label.setStyleSheet("font-size: 40px;")
                type_layout.addWidget(icon_label)
            
            type_frame.setLayout(type_layout)
            types_layout.addWidget(type_frame)
        
        layout.addLayout(types_layout)
        
        stats_title = QLabel("STATISTIQUES")
        stats_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(stats_title)
        
        stats_order = [
            ('hp', 'HP'),
            ('attack', 'ATT'),
            ('defense', 'DEF'),
            ('special-attack', 'SP.ATT'),
            ('special-defense', 'SP.DEF'),
            ('speed', 'VIT')
        ]
        
        for stat_key, stat_label in stats_order:
            stat_value = self.pokemon['stats'][stat_key]
            
            stat_row = QHBoxLayout()
            stat_row.setSpacing(15)
            
            label = QLabel(f"{stat_label}")
            label.setFixedWidth(90)
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            stat_row.addWidget(label)
            
            value_label = QLabel(str(stat_value))
            value_label.setFixedWidth(50)
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            value_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            stat_row.addWidget(value_label)
            
            progress = QProgressBar()
            progress.setMaximum(255)
            progress.setValue(stat_value)
            progress.setTextVisible(False)
            progress.setFixedHeight(25)
            
            bar_color = self.get_stat_color(stat_value)
            progress.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 12px;
                    background-color: rgba(0, 0, 0, 0.3);
                }}
                QProgressBar::chunk {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {bar_color},
                        stop:1 {self.adjust_color(bar_color, 30)});
                    border-radius: 12px;
                }}
            """)
            stat_row.addWidget(progress, 2)
            
            layout.addLayout(stat_row)
        
        layout.addStretch()
        
        return layout
        
    def get_generation_text(self):
        gen_map = {
            'generation-i': 'G E N E R A T I O N  I',
            'generation-ii': 'G E N E R A T I O N  I I',
            'generation-iii': 'G E N E R A T I O N  I I I',
            'generation-iv': 'G E N E R A T I O N  I V',
            'generation-v': 'G E N E R A T I O N  V',
            'generation-vi': 'G E N E R A T I O N  V I',
            'generation-vii': 'G E N E R A T I O N  V I I',
            'generation-viii': 'G E N E R A T I O N  V I I I',
            'generation-ix': 'G E N E R A T I O N  I X',
        }
        return gen_map.get(self.pokemon.get('generation', ''), 'G E N E R A T I O N')
        
    def get_stat_color(self, value):
        if value >= 150:
            return '#27ae60'
        elif value >= 120:
            return '#2ecc71'
        elif value >= 90:
            return '#f39c12'
        elif value >= 60:
            return '#e67e22'
        else:
            return '#e74c3c'
            
    def adjust_color(self, hex_color, amount):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        return f'#{r:02x}{g:02x}{b:02x}'
