import random
from abc import ABC, abstractmethod
from typing import List

from src.domain.card import Card


class GameStrategy(ABC):
    """Define como os pares de cartas são gerados."""

    @abstractmethod
    def generate_cards(self, num_pairs: int) -> List[Card]:
        """Deve retornar uma lista de cartas embaralhadas."""
        pass


class EmojiStrategy(GameStrategy):
    """
    Estratégia baseada em bancos de emojis.
    Seleciona aleatoriamente um subconjunto do banco total.
    """

    # Banco de Dados Expandido
    THEMES = {
        "Animais": [
            "🐶",
            "🐱",
            "🐭",
            "🐹",
            "🐰",
            "🦊",
            "🐻",
            "🐼",
            "🐨",
            "🐯",
            "🦁",
            "🐮",
            "🐷",
            "🐸",
            "🐵",
            "🐔",
            "🐧",
            "🐦",
            "🐤",
            "🦆",
            "🦅",
            "🦉",
            "🦇",
            "🐺",
            "🐗",
            "🐴",
            "🦄",
            "🐝",
            "🐛",
            "🦋",
            "🐌",
            "🐞",
            "🐜",
            "🦗",
            "🕷",
            "🦂",
            "🐢",
            "🐍",
            "🦎",
            "🦖",
            "🐙",
            "🦑",
            "🦐",
            "🦞",
            "🦀",
            "🐡",
            "🐠",
            "🐟",
            "🐬",
            "🐳",
        ],
        "Espaço": [
            "🚀",
            "🛸",
            "🌍",
            "🌕",
            "⭐",
            "☄️",
            "👾",
            "👨‍🚀",
            "🔭",
            "🌌",
            "☀️",
            "🪐",
            "🌑",
            "🛰️",
            "👽",
            "🌠",
            "🌤️",
            "⛈️",
            "⛄",
            "🔥",
            "🧨",
            "✨",
            "🎈",
            "🎉",
            "✈️",
            "🛩️",
            "🚁",
            "🚠",
            "🏔️",
            "🌋",
        ],
        "Bandeiras": [
            "🇧🇷",
            "🇺🇸",
            "🇨🇦",
            "🇯🇵",
            "🇰🇷",
            "🇨🇳",
            "🇩🇪",
            "🇫🇷",
            "🇮🇹",
            "🇪🇸",
            "🇬🇧",
            "🇦🇺",
            "🇦🇷",
            "🇨🇱",
            "🇨🇴",
            "🇲🇽",
            "🇵🇹",
            "🇷🇺",
            "🇮🇳",
            "🇿🇦",
            "🇨🇭",
            "🇸🇪",
            "🇳🇴",
            "🇫🇮",
            "🇩🇰",
            "🇳🇱",
            "🇧🇪",
            "🇬🇷",
            "🇹🇷",
            "🇪🇬",
        ],
    }

    def __init__(self, theme: str = "Animais"):
        if theme not in self.THEMES:
            # Fallback seguro
            theme = "Animais"
        self.theme_items = self.THEMES[theme]

    def generate_cards(self, num_pairs: int) -> List[Card]:
        # Validação robusta
        if num_pairs > len(self.theme_items):
            raise ValueError(
                f"O tema precisa de {num_pairs} itens, mas só tem {len(self.theme_items)}. Adicione mais emojis!"
            )

        # Sorteia itens aleatórios do banco grande
        selected = random.sample(self.theme_items, num_pairs)
        cards = []

        for item in selected:
            cards.append(Card(match_id=item, display_content=item))
            cards.append(Card(match_id=item, display_content=item))

        random.shuffle(cards)
        return cards


class MathStrategy(GameStrategy):
    """
    Estratégia Algorítmica: Gera contas na hora.
    Nunca fica sem itens!
    """

    def generate_cards(self, num_pairs: int) -> List[Card]:
        cards = []
        # Gera operações únicas
        operations_set = set()

        while len(operations_set) < num_pairs:
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            # Evita duplicatas (ex: 2+2 e depois outro 2+2)
            op_id = f"{a}+{b}"
            if op_id not in operations_set:
                operations_set.add(op_id)

                result = str(a + b)
                expression = f"{a} + {b}"

                # Match ID é o resultado. Display é diferente.
                cards.append(Card(match_id=result, display_content=expression))
                cards.append(Card(match_id=result, display_content=result))

        random.shuffle(cards)
        return cards


class ChemistryStrategy(GameStrategy):
    """Base de Dados Expandida de Química."""

    ELEMENTS = [
        ("H", "Hidrogênio"),
        ("He", "Hélio"),
        ("Li", "Lítio"),
        ("Be", "Berílio"),
        ("B", "Boro"),
        ("C", "Carbono"),
        ("N", "Nitrogênio"),
        ("O", "Oxigênio"),
        ("F", "Flúor"),
        ("Ne", "Neônio"),
        ("Na", "Sódio"),
        ("Mg", "Magnésio"),
        ("Al", "Alumínio"),
        ("Si", "Silício"),
        ("P", "Fósforo"),
        ("S", "Enxofre"),
        ("Cl", "Cloro"),
        ("K", "Potássio"),
        ("Ca", "Cálcio"),
        ("Sc", "Escândio"),
        ("Ti", "Titânio"),
        ("V", "Vanádio"),
        ("Cr", "Cromo"),
        ("Mn", "Manganês"),
        ("Fe", "Ferro"),
        ("Co", "Cobalto"),
        ("Ni", "Níquel"),
        ("Cu", "Cobre"),
        ("Zn", "Zinco"),
        ("Ga", "Gálio"),
        ("Ge", "Germânio"),
        ("As", "Arsênio"),
        ("Se", "Selênio"),
        ("Br", "Bromo"),
        ("Kr", "Criptônio"),
        ("Rb", "Rubídio"),
        ("Sr", "Estrôncio"),
        ("Y", "Ítrio"),
        ("Zr", "Zircônio"),
        ("Nb", "Nióbio"),
        ("Ag", "Prata"),
        ("Au", "Ouro"),
        ("Hg", "Mercúrio"),
        ("Pb", "Chumbo"),
        ("Sn", "Estanho"),
        ("U", "Urânio"),
        ("Pt", "Platina"),
        ("I", "Iodo"),
    ]

    def generate_cards(self, num_pairs: int) -> List[Card]:
        if num_pairs > len(self.ELEMENTS):
            raise ValueError("Adicione mais elementos químicos na lista!")

        selected = random.sample(self.ELEMENTS, num_pairs)
        cards = []
        for symbol, name in selected:
            # ID único é o símbolo
            cards.append(Card(match_id=symbol, display_content=symbol))
            cards.append(Card(match_id=symbol, display_content=name))

        random.shuffle(cards)
        return cards
