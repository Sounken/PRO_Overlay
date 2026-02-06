from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class OverlayWindow(QWidget):
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        self.setup_timer()
        
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
        
        self.title_label = QLabel("🎮 PRO Helper")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 180);
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        
        self.pokemon_label = QLabel("En attente de détection...")
        self.pokemon_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 160);
                padding: 8px;
                border-radius: 5px;
            }
        """)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.pokemon_label)
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
        
    def setup_timer(self):
        self.detection_timer = QTimer()
        self.detection_timer.timeout.connect(self.detect_pokemon)
        self.detection_timer.start(2000)
        
    def detect_pokemon(self):
        # TODO: Implémenter OCR + API call
        pass
        
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
