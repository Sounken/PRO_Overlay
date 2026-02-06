import keyboard

class HotkeyManager:
    
    def __init__(self, overlay, config):
        self.overlay = overlay
        self.config = config
        
    def register_hotkeys(self):
        hotkeys = self.config['hotkeys']
        
        keyboard.add_hotkey(
            hotkeys['toggle_overlay'],
            self.overlay.toggle_visibility
        )
        
        keyboard.add_hotkey(
            hotkeys['refresh_detection'],
            self.overlay.detect_pokemon
        )
        
        print("✅ Hotkeys enregistrées")
