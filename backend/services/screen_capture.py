"""
Service de capture d'écran avec mss
"""
import mss
import mss.tools
from PIL import Image
from typing import Optional, Tuple
from io import BytesIO


class ScreenCapture:
    """Gestionnaire de capture d'écran"""

    def __init__(self):
        """Initialise le gestionnaire de capture"""
        self.sct = mss.mss()

    def capture_region(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> Image.Image:
        """
        Capture une région de l'écran

        Args:
            x, y: Position de la région (None = tout l'écran)
            width, height: Dimensions de la région

        Returns:
            Image PIL de la région capturée
        """
        if x is None or y is None or width is None or height is None:
            # Capture tout l'écran principal
            monitor = self.sct.monitors[1]
        else:
            monitor = {
                "top": y,
                "left": x,
                "width": width,
                "height": height
            }

        # Capture
        screenshot = self.sct.grab(monitor)

        # Convertir en Image PIL
        img = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.bgra,
            "raw",
            "BGRX"
        )

        return img

    def get_screen_size(self) -> Tuple[int, int]:
        """Retourne la taille de l'écran principal"""
        monitor = self.sct.monitors[1]
        return monitor["width"], monitor["height"]

    def save_screenshot(self, path: str, region: Optional[dict] = None):
        """
        Sauvegarde une capture d'écran

        Args:
            path: Chemin du fichier de sortie
            region: Région à capturer (None = tout l'écran)
        """
        if region:
            img = self.capture_region(**region)
        else:
            img = self.capture_region()

        img.save(path)
        print(f"Screenshot saved to {path}")

    def close(self):
        """Ferme le gestionnaire de capture"""
        self.sct.close()

    def __enter__(self):
        """Support du context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme proprement le gestionnaire"""
        self.close()
