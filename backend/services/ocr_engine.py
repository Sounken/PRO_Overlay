"""
Moteur OCR avec Tesseract pour détecter les noms de Pokémon
"""
import pytesseract
from PIL import Image
import re
import os
from typing import Optional, Tuple
from difflib import get_close_matches

# Configuration du chemin Tesseract sur Windows
if os.name == 'nt':  # Windows
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Liste des noms de Pokémon valides (Gen 1-9) - À compléter
POKEMON_NAMES = [
    "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
    "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree",
    "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot",
    "rattata", "raticate", "spearow", "fearow", "ekans", "arbok",
    "pikachu", "raichu", "sandshrew", "sandslash", "nidoran-f", "nidorina", "nidoqueen",
    "nidoran-m", "nidorino", "nidoking", "clefairy", "clefable", "vulpix", "ninetales",
    "jigglypuff", "wigglytuff", "zubat", "golbat", "oddish", "gloom", "vileplume",
    "paras", "parasect", "venonat", "venomoth", "diglett", "dugtrio",
    "meowth", "persian", "psyduck", "golduck", "mankey", "primeape",
    "growlithe", "arcanine", "poliwag", "poliwhirl", "poliwrath", "abra",
    "kadabra", "alakazam", "machop", "machoke", "machamp", "bellsprout",
    "weepinbell", "victreebel", "tentacool", "tentacruel", "geodude", "graveler",
    "golem", "ponyta", "rapidash", "slowpoke", "slowbro", "magnemite",
    "magneton", "farfetchd", "doduo", "dodrio", "seel", "dewgong",
    "grimer", "muk", "shellder", "cloyster", "gastly", "haunter",
    "gengar", "onix", "drowzee", "hypno", "krabby", "kingler",
    "voltorb", "electrode", "exeggcute", "exeggutor", "cubone", "marowak",
    "hitmonlee", "hitmonchan", "lickitung", "koffing", "weezing", "rhyhorn",
    "rhydon", "chansey", "tangela", "kangaskhan", "horsea", "seadra",
    "goldeen", "seaking", "staryu", "starmie", "mr-mime", "scyther",
    "jynx", "electabuzz", "magmar", "pinsir", "tauros", "magikarp",
    "gyarados", "lapras", "ditto", "eevee", "vaporeon", "jolteon",
    "flareon", "porygon", "omanyte", "omastar", "kabuto", "kabutops",
    "aerodactyl", "snorlax", "articuno", "zapdos", "moltres", "dratini",
    "dragonair", "dragonite", "mewtwo", "mew",
    # Gen 2+
    "chikorita", "bayleef", "meganium", "cyndaquil", "quilava", "typhlosion",
    "totodile", "croconaw", "feraligatr", "sentret", "furret", "hoothoot",
    "noctowl", "ledyba", "ledian", "spinarak", "ariados", "crobat",
    "umbreon", "espeon", "tyranitar", "lugia", "ho-oh",
    # Quelques Gen 3-9 populaires
    "treecko", "grovyle", "sceptile", "torchic", "combusken", "blaziken",
    "mudkip", "marshtomp", "swampert", "ralts", "kirlia", "gardevoir",
    "lucario", "garchomp", "greninja", "sylveon", "mimikyu", "dragapult"
    # TODO: Compléter avec tous les Pokémon Gen 1-9
]


class OCREngine:
    """Moteur de reconnaissance de texte pour détecter les Pokémon"""

    def __init__(self, confidence_threshold: int = 60):
        """
        Initialise le moteur OCR

        Args:
            confidence_threshold: Seuil de confiance minimum (0-100)
        """
        self.confidence_threshold = confidence_threshold

        # Configuration Tesseract optimisée pour jeux vidéo
        # PSM 11 = texte épars sans structure particulière
        # --oem 3 = LSTM + Legacy (meilleur pour texte stylisé)
        self.config = '--psm 11 --oem 3'

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Prétraitement de l'image pour améliorer l'OCR sur jeux vidéo

        Args:
            image: Image PIL à traiter

        Returns:
            Image prétraitée
        """
        from PIL import ImageEnhance

        # Agrandissement 2.5x pour texte de jeu vidéo
        width, height = image.size
        image = image.resize((width * 3, height * 3), Image.Resampling.LANCZOS)

        # Augmentation modérée du contraste
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)

        # Augmentation de la saturation des couleurs
        color_enhancer = ImageEnhance.Color(image)
        image = color_enhancer.enhance(1.5)

        # Augmentation modérée de la netteté
        sharpness_enhancer = ImageEnhance.Sharpness(image)
        image = sharpness_enhancer.enhance(2.0)

        # Légère augmentation de la luminosité
        brightness_enhancer = ImageEnhance.Brightness(image)
        image = brightness_enhancer.enhance(1.1)

        return image

    def extract_text(self, image: Image.Image) -> Tuple[str, float]:
        """
        Extrait le texte d'une image

        Args:
            image: Image PIL contenant le texte

        Returns:
            Tuple (texte détecté, niveau de confiance 0-100)
        """
        # Sauvegarde image brute pour debug
        image.save('debug_01_raw.png')

        # Prétraitement
        processed_image = self.preprocess_image(image)

        # Sauvegarde image après preprocessing
        processed_image.save('debug_02_preprocessed.png')

        # Extraction OCR avec données de confiance
        data = pytesseract.image_to_data(
            processed_image,
            config=self.config,
            output_type=pytesseract.Output.DICT
        )

        # Récupère le texte et la confiance
        texts = []
        confidences = []

        for i, conf in enumerate(data['conf']):
            if int(conf) > 0:  # Ignorer les détections sans confiance
                text = data['text'][i].strip()
                if text:
                    texts.append(text)
                    confidences.append(int(conf))

        if not texts:
            return "", 0.0

        # Combine le texte et calcule la confiance moyenne
        full_text = " ".join(texts)
        avg_confidence = sum(confidences) / len(confidences)

        return full_text, avg_confidence

    def clean_pokemon_name(self, text: str) -> str:
        """
        Nettoie le texte pour extraire un nom de Pokémon

        Args:
            text: Texte brut de l'OCR

        Returns:
            Nom de Pokémon nettoyé
        """
        # Convertir en minuscules
        text = text.lower()

        # Supprimer les caractères spéciaux sauf tirets et lettres
        text = re.sub(r'[^a-z\-\s]', '', text)

        # Supprimer les espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def find_closest_pokemon(self, detected_name: str) -> Optional[str]:
        """
        Trouve le Pokémon le plus proche du nom détecté

        Args:
            detected_name: Nom détecté par l'OCR

        Returns:
            Nom du Pokémon le plus proche ou None
        """
        detected_name = self.clean_pokemon_name(detected_name)

        if not detected_name:
            return None

        # Recherche exacte sur la chaîne complète
        if detected_name in POKEMON_NAMES:
            return detected_name

        # Recherche approximative sur la chaîne complète
        matches = get_close_matches(detected_name, POKEMON_NAMES, n=1, cutoff=0.6)
        if matches:
            return matches[0]

        # Chercher mot par mot
        words = detected_name.split()

        for word in words:
            if len(word) < 4:
                continue

            if word in POKEMON_NAMES:
                return word

            word_matches = get_close_matches(word, POKEMON_NAMES, n=1, cutoff=0.7)
            if word_matches:
                return word_matches[0]

        return None

    def detect_pokemon(self, image: Image.Image) -> Tuple[Optional[str], float]:
        """
        Détecte un nom de Pokémon dans une image

        Args:
            image: Image contenant le nom du Pokémon

        Returns:
            Tuple (nom du Pokémon, confiance)
        """
        # Extraction du texte
        text, confidence = self.extract_text(image)

        if confidence < self.confidence_threshold:
            return None, confidence

        pokemon_name = self.find_closest_pokemon(text)

        return pokemon_name, confidence
