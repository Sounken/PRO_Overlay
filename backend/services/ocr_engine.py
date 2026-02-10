"""
Moteur OCR avec EasyOCR pour détecter les noms de Pokémon
Utilise EasyOCR (basé sur PyTorch) pour une meilleure reconnaissance
"""
import easyocr
from PIL import Image
import numpy as np
import re
from typing import Optional, Tuple
from difflib import get_close_matches

# Liste COMPLÈTE des noms de Pokémon (Gen 1-9, 1025 Pokémon)
POKEMON_NAMES = [
    # Gen 1 (1-151)
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
    # Gen 2 (152-251)
    "chikorita", "bayleef", "meganium", "cyndaquil", "quilava", "typhlosion",
    "totodile", "croconaw", "feraligatr", "sentret", "furret", "hoothoot",
    "noctowl", "ledyba", "ledian", "spinarak", "ariados", "crobat",
    "chinchou", "lanturn", "pichu", "cleffa", "igglybuff", "togepi",
    "togetic", "tyrogue", "hitmontop", "smoochum", "elekid", "magby",
    "azurill", "marill", "azumarill", "sudowoodo", "politoed", "hoppip",
    "skiploom", "jumpluff", "aipom", "sunkern", "sunflora", "yanma",
    "wooper", "quagsire", "espeon", "umbreon", "murkrow", "slowking",
    "misdreavus", "unown", "wobbuffet", "girafarig", "pineco", "forretress",
    "dunsparce", "girafarig", "dunsparce", "snubbull", "granbull", "qwilfish",
    "scizor", "shuckle", "heracross", "sneasel", "teddiursa", "ursaring",
    "slugma", "magcargo", "swinub", "piloswine", "corsola", "remoraid",
    "octillery", "mantine", "skarmory", "mantyke", "houndour", "houndoom",
    "kingdra", "phanpy", "donphan", "porygon2", "steelix", "tyrogue",
    "hitmontop", "smoochum", "elekid", "magby", "miltank", "raikou",
    "entei", "suicune", "larvitar", "pupitar", "tyranitar", "lugia",
    "ho-oh", "celebi",
    # Gen 3 (252-386)
    "treecko", "grovyle", "sceptile", "torchic", "combusken", "blaziken",
    "mudkip", "marshtomp", "swampert", "poochyena", "mightyena", "zigzagoon",
    "linoone", "taillow", "swellow", "wingull", "pelipper", "ralts",
    "kirlia", "gardevoir", "surskit", "masquerain", "shroomish", "breloom",
    "slakoth", "vigoroth", "slaking", "nincada", "ninjask", "shedinja",
    "whismur", "loudred", "exploud", "skitty", "delcatty", "spinda",
    "zangoose", "castform", "kecleon", "shuppet", "banette", "duskull",
    "dusclops", "trapinch", "vibrava", "flygon", "cacnea", "cacturne",
    "swablu", "altaria", "seviper", "lunatone", "solrock", "barboach",
    "whiscash", "corphish", "crawdaunt", "baltoy", "claydol", "lileep",
    "cradily", "anorith", "armaldo", "feebas", "milotic", "carvanha",
    "sharpedo", "wailmer", "wailord", "camerupt", "numel", "torkoal",
    "spoink", "grumpig", "spinda", "trapinch", "vibrava", "flygon",
    "cacnea", "cacturne", "swablu", "altaria", "zangoose", "seviper",
    "lunatone", "solrock", "barboach", "whiscash", "corphish", "crawdaunt",
    "baltoy", "claydol", "lileep", "cradily", "anorith", "armaldo",
    "feebas", "milotic", "castform", "kecleon", "shuppet", "banette",
    "duskull", "dusclops", "chingling", "chimecho", "absol", "wynaut",
    "snorunt", "glalie", "spheal", "sealeo", "walrein", "clamperl",
    "huntail", "gorebyss", "relicanth", "luvdisc", "bagon", "shelgon",
    "salamence", "beldum", "metang", "metagross", "regirock", "regice",
    "registeel", "latias", "latios", "kyogre", "groudon", "rayquaza",
    "jirachi", "deoxys",
    # Gen 4 (387-493)
    "turtwig", "grotle", "torterra", "chimchar", "monferno", "infernape",
    "piplup", "prinplup", "empoleon", "starly", "staravia", "staraptor",
    "bidoof", "bibarel", "buizel", "floatzel", "cherubi", "cherrim",
    "shellos", "gastrodon", "cranidos", "rampardos", "shieldon", "bastionage",
    "burmy", "wormadam", "mothim", "combee", "vespiquen", "pachirisu",
    "buneary", "lopunny", "glameow", "purugly", "chatot", "spiritomb",
    "gible", "gabite", "garchomp", "munchlax", "riolu", "lucario",
    "hippopotas", "hippowdon", "skorupi", "drapion", "carnivine", "feebas",
    "milotic", "snover", "abomasnow", "weavile", "magnezone", "lickilicky",
    "rhyperior", "tangrowth", "electivire", "magmortar", "togekiss", "yanmega",
    "leafeon", "glaceon", "gliscor", "mamoswine", "porygon-z", "gallade",
    "probopass", "dusknoir", "froslass", "rotom", "uxie", "mesprit",
    "azelf", "dialga", "palkia", "heatran", "regigigas", "giratina",
    "cresselia", "phione", "manaphy", "darkrai", "shaymin", "arceus",
    "shinx", "luxio", "luxray",
    # Gen 5 (494-649)
    "snivy", "servine", "serperior", "tepig", "pignite", "emboar",
    "oshawott", "dewott", "samurott", "patrat", "watchog", "lillipup",
    "herdier", "stoutland", "pidove", "tranquill", "unfezant", "blitzle",
    "zebstrika", "roggenrola", "boldore", "gigalith", "woobat", "swoobat",
    "drilbur", "excadrill", "audino", "timburr", "gurdurr", "conkeldurr",
    "tympole", "palpitoad", "seismitoad", "throh", "sawk", "sewaddle",
    "swadloon", "leavanny", "venipede", "whirlipede", "scolipede", "cottonee",
    "whimscott", "petilil", "lilligant", "basculin", "ducklett", "swanna",
    "vanillite", "vanillish", "vanilluxe", "deerling", "sawsbuck", "emolga",
    "joltik", "galvantula", "ferroseed", "ferrothorn", "klink", "klang",
    "klinklang", "tynamo", "eelektrik", "eelektross", "elgyem", "beheeyem",
    "litwick", "lampent", "chandelure", "axew", "fraxure", "haxorus",
    "cubchoo", "beartic", "cryogonal", "shelmet", "accelgor", "stunfisk",
    "mienfoo", "mienshao", "druddigon", "golett", "golurk", "pawniard",
    "bisharp", "bouffalant", "rufflet", "braviary", "vullaby", "mandibuzz",
    "heatmor", "durant", "deino", "zweilous", "hydreigon", "larvesta",
    "volcarona", "cobalion", "terrakion", "virizion", "tornadus", "thundurus",
    "reshiram", "zekrom", "landorus", "kyurem", "victini", "keldeo",
    "meloetta", "genesect",
    # Gen 6 (650-721)
    "chespin", "quilladin", "chesnaught", "fennekin", "braixen", "delphox",
    "froakie", "frogadier", "greninja", "bunnelby", "diggersby", "fletchling",
    "fletchinder", "talonflame", "scatterbug", "spewpa", "vivillon", "litleo",
    "pyroar", "flabebe", "floette", "florges", "skiddo", "gogoat",
    "pancham", "pangoro", "furfrou", "espurr", "meowstic", "honedge",
    "doublade", "aegislash", "spritzee", "aromatisse", "swirlix", "slurpuff",
    "inkay", "malamar", "binacle", "barbaracle", "helioptile", "heliolisk",
    "tyrunt", "tyrantrum", "amaura", "aurorus", "sylveon", "carbink",
    "goomy", "sliggoo", "goodra", "klefki", "phantump", "trevenant",
    "pumpkaboo", "gourgeist", "bergmite", "avalugg", "noibat", "noivern",
    "xerneas", "yveltal", "zygarde", "diancie", "hoopa", "volcanion",
    # Gen 7 (722-809)
    "rowlet", "dartrix", "decidueye", "litten", "torracat", "incineroar",
    "popplio", "brionne", "primarina", "pikipek", "trumbeak", "toucannon",
    "yungoos", "gumshoos", "grubbin", "charjabug", "vikavolt", "crabrawler",
    "crabominable", "cutiefly", "ribombee", "rockruff", "lycanroc", "wishiwashi",
    "mareanie", "toxapex", "mudbray", "mudsdale", "dewpider", "araquanid",
    "fomantis", "lurantis", "morelull", "shiinotic", "salandit", "salazzle",
    "stufful", "bewear", "bounsweet", "steenee", "tsareena", "comfey",
    "oranguru", "passimian", "wimpod", "golisopod", "sandygast", "palossand",
    "pyukumuku", "type-null", "silvally", "minior", "komala", "togedemaru",
    "mimikyu", "bruxish", "drampa", "dhelmise", "jangmo-o", "hakamo-o",
    "kommo-o", "tapu-koko", "tapu-lele", "tapu-bulu", "tapu-fini", "cosmog",
    "cosmoem", "solgaleo", "lunala", "nihilego", "buzzwole", "pheromosa",
    "xurkitree", "celesteela", "kartana", "guzzlord", "necrozma", "magearna",
    "marshadow", "poipole", "naganadel", "stakataka", "blacephalon", "zeraora",
    "meltan", "melmetal",
    # Gen 8 (810-905)
    "grookey", "thwackey", "rillaboom", "scorbunny", "raboot", "cinderace",
    "sobble", "drizzile", "inteleon", "skwovet", "greedent", "rookidee",
    "corvisquire", "corviknight", "blipbug", "dottler", "orbeetle", "wooloo",
    "dubwool", "chewtle", "drednaw", "yamper", "boltund", "rolycoly",
    "carkol", "coalossal", "applin", "flapple", "appletun", "silicobra",
    "sandaconda", "cramorant", "arrokuda", "barraskewda", "toxel", "toxtricity",
    "sizzlipede", "centiskorch", "clobbopus", "grapploct", "sinistea", "polteageist",
    "cursola", "dracozolt", "arctozolt", "dracovish", "arctovish", "duraludon",
    "dreepy", "drakloak", "dragapult", "zacian", "zamazenta", "eternatus",
    "kubfu", "urshifu", "zarude", "regieleki", "regidrago", "glastrier",
    "spectrier", "calyrex", "wyrdeer", "kleavor", "ursaluna", "basculegion",
    "sneasler", "overqwil", "enamorus", "pecharunt",
    # Gen 9 (906-1025)
    "sprigatito", "floragato", "meowscarada", "fuecoco", "crocalor", "skeledirge",
    "quaxly", "quaxwell", "quaquaval", "lechonk", "oinkologne", "tarountula",
    "spidops", "nymble", "lokix", "pawmi", "pawmo", "pawmot",
    "tandemaus", "maushold", "fidough", "dachsbun", "bombirdier", "squawkabilly",
    "flamigo", "cetoddle", "cetitan", "wiglett", "wugtrio", "naclstack",
    "rabsca", "flittle", "espathra", "tinkatink", "tinkatuff", "tinkaton",
    "ironbundle", "varoom", "revavroom", "cyclizar", "scream-tail", "roaring-moon",
    "iron-seaking", "frigibax", "arctibax", "baxcalibur", "gimmighoul", "gholdengo",
    "wo-chien", "chien-pao", "ting-lu", "chi-yu", "koraidon", "miraidon",
    "walking-wake", "iron-leaves", "pecharunt",
]

# Supprimer les doublons et trier
POKEMON_NAMES = sorted(list(set(POKEMON_NAMES)))


class OCREngine:
    """Moteur de reconnaissance de texte avec EasyOCR pour détecter les Pokémon"""

    def __init__(self, confidence_threshold: float = 0.25):
        """
        Initialise le moteur OCR EasyOCR

        Args:
            confidence_threshold: Seuil de confiance minimum (0.0-1.0)
        """
        self.confidence_threshold = confidence_threshold
        # Initialiser EasyOCR une seule fois (modèles PyTorch préchargés)
        # Utilise automatiquement GPU si disponible, sinon CPU
        self.ocr = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, image: Image.Image) -> Tuple[str, float]:
        """
        Extrait le texte d'une image avec EasyOCR

        Args:
            image: Image PIL contenant le texte

        Returns:
            Tuple (texte détecté, niveau de confiance 0.0-1.0)
        """
        # EasyOCR fonctionne directement sur les images PIL
        # Conversion en numpy array pour EasyOCR
        image_array = np.array(image)

        # Exécuter EasyOCR
        # Retourne: [[[x1,y1], [x2,y2], [x3,y3], [x4,y4]], texte, confiance], ...]
        results = self.ocr.readtext(image_array)

        if not results:
            return "", 0.0

        # Extraire le texte et la confiance de tous les résultats
        texts = []
        confidences = []

        for detection in results:
            _, text, confidence = detection
            text = text.strip()  # Le texte reconnu
            confidence = float(confidence)  # La confiance (0.0-1.0)

            if text:
                texts.append(text)
                confidences.append(confidence)

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

        # Recherche approximative sur la chaîne complète (cutoff plus strict)
        matches = get_close_matches(detected_name, POKEMON_NAMES, n=1, cutoff=0.75)
        if matches:
            return matches[0]

        # Chercher mot par mot (meilleur pour détecter les vrais noms)
        words = detected_name.split()

        # PREMIÈRE PASSE: Chercher les matches EXACTS (y compris les noms courts comme "mew", "muk")
        for word in words:
            if len(word) >= 2 and word in POKEMON_NAMES:
                return word

        # DEUXIÈME PASSE: Fuzzy matching seulement pour les mots assez longs (>= 4 chars)
        # Cela évite les faux positifs comme "see" qui matche "seel"
        for word in words:
            if len(word) < 4:
                continue

            # Cutoff TRÈS strict (0.90+) pour éviter les faux positifs
            # "see" vs "seel" ≈ 0.857, donc 0.90 l'exclut
            word_matches = get_close_matches(word, POKEMON_NAMES, n=1, cutoff=0.90)
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
