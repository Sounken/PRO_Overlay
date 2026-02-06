import sys
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.overlay.overlay_window import OverlayWindow
from src.utils.hotkeys import HotkeyManager

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erreur: config.json introuvable")
        sys.exit(1)

def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Pokemon PRO Helper")
    
    config = load_config()
    
    overlay = OverlayWindow(config)
    overlay.show()
    
    hotkey_manager = HotkeyManager(overlay, config)
    hotkey_manager.register_hotkeys()
    
    print("Pokemon PRO Helper lancé !")
    print(f"📌 Hotkey toggle: {config['hotkeys']['toggle_overlay'].upper()}")
    print(f"🔄 Hotkey refresh: {config['hotkeys']['refresh_detection'].upper()}")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
