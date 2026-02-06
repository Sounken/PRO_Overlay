class Theme:
    
    COLORS = {
        'primary': '#3498db',
        'primary_dark': '#2980b9',
        'secondary': '#2ecc71',
        'secondary_dark': '#27ae60',
        'danger': '#e74c3c',
        'warning': '#f39c12',
        'background': '#1e1e2e',
        'surface': '#2a2a3e',
        'card': '#ffffff',
        'text_primary': '#2c3e50',
        'text_secondary': '#7f8c8d',
        'border': '#e0e0e0',
        'sidebar': '#16213e',
        'sidebar_hover': '#0f3460',
    }
    
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
    
    @staticmethod
    def get_main_window_style():
        return f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {Theme.COLORS['background']},
                    stop:1 #0f0f1e);
            }}
        """
    
    @staticmethod
    def get_sidebar_style():
        return f"""
            QFrame {{
                background-color: {Theme.COLORS['sidebar']};
                border-right: 2px solid rgba(255, 255, 255, 0.1);
            }}
        """
    
    @staticmethod
    def get_sidebar_button_style():
        return f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: 2px solid transparent;
                border-radius: 12px;
                font-size: 24px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {Theme.COLORS['sidebar_hover']};
                border: 2px solid {Theme.COLORS['primary']};
            }}
            QPushButton:pressed {{
                background-color: {Theme.COLORS['primary']};
            }}
        """
    
    @staticmethod
    def get_search_input_style():
        return f"""
            QLineEdit {{
                padding: 14px 18px;
                font-size: 15px;
                border: 2px solid {Theme.COLORS['border']};
                border-radius: 10px;
                background-color: white;
                color: {Theme.COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {Theme.COLORS['primary']};
                background-color: #f8f9fa;
            }}
        """
    
    @staticmethod
    def get_button_style(bg_color, hover_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                transform: scale(0.98);
            }}
        """
    
    @staticmethod
    def get_card_style():
        return f"""
            QFrame {{
                background-color: {Theme.COLORS['card']};
                border-radius: 20px;
                border: 1px solid {Theme.COLORS['border']};
            }}
        """
    
    @staticmethod
    def get_scrollarea_style():
        return """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.1);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(52, 152, 219, 0.5);
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(52, 152, 219, 0.8);
            }
        """
