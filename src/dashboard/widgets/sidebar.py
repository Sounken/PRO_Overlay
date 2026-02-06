from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from src.dashboard.styles.theme import Theme


class Sidebar(QFrame):
    
    view_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_view = "pokedex"
        self.init_ui()
        
    def init_ui(self):
        self.setFixedWidth(90)
        self.setStyleSheet(Theme.get_sidebar_style())
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(15)
        
        self.buttons = []
        buttons_config = [
            ("📚", "Pokédex", "pokedex"),
            ("👥", "Équipe", "team"),
            ("🧮", "Calculateurs", "calculator"),
            ("⚙️", "Paramètres", "settings")
        ]
        
        for icon, tooltip, view_name in buttons_config:
            btn = QPushButton(icon)
            btn.setToolTip(tooltip)
            btn.setFixedSize(70, 70)
            btn.setStyleSheet(Theme.get_sidebar_button_style())
            btn.clicked.connect(lambda checked, v=view_name: self.change_view(v))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.buttons.append((btn, view_name))
        
        layout.addStretch()
        self.setLayout(layout)
        
    def change_view(self, view_name):
        self.current_view = view_name
        self.view_changed.emit(view_name)
