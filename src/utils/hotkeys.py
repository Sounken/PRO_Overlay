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
        
        print("✅ Hotkeys enregistrées")
