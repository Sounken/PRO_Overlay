from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from src.dashboard.widgets.sidebar import Sidebar
from src.dashboard.views.pokedex_view import PokedexView
from src.dashboard.styles.theme import Theme


class DashboardWindow(QMainWindow):
    
    pokemon_selected = pyqtSignal(dict, dict)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.current_view = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Pokemon PRO Helper - Dashboard")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet(Theme.get_main_window_style())
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        self.sidebar.view_changed.connect(self.switch_view)
        main_layout.addWidget(self.sidebar)
        
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_container.setLayout(self.content_layout)
        main_layout.addWidget(self.content_container)
        
        central.setLayout(main_layout)
        
        self.switch_view("pokedex")
        
    def switch_view(self, view_name):
        for i in reversed(range(self.content_layout.count())): 
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        if view_name == "pokedex":
            view = PokedexView(self.config)
            view.pokemon_selected.connect(self.pokemon_selected.emit)
            self.current_view = view
        elif view_name == "team":
            view = self.create_placeholder("👥 Gestion d'Équipe")
            self.current_view = view
        elif view_name == "calculator":
            view = self.create_placeholder("🧮 Calculateurs")
            self.current_view = view
        elif view_name == "settings":
            view = self.create_placeholder("⚙️ Paramètres")
            self.current_view = view
        
        self.content_layout.addWidget(self.current_view)
        
    def create_placeholder(self, title):
        from PyQt6.QtWidgets import QLabel
        from PyQt6.QtCore import Qt
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"{title}\n\nFonctionnalité à venir...")
        label.setStyleSheet("font-size: 24px; color: white;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget
