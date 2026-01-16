# src/domain/strategies.py

"""
Este módulo define um contrato (GameStrategy) e implementações concretas.
É aqui que a mágica da diversidade acontece.
"""

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
    """Modo Clássico: O par é idêntico (Emoji A com Emoji A)."""

    # Banco de dados de emojis expandido
    THEMES = {
        "Animais": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯"],
        "Frutas": ["🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐", "🍍"],
        "Espaço": ["🚀", "⭐", "🌙", "🌎", "☀️", "☄️", "👽", "📡", "🛰️", "🛸"],
    }

    def __init__(self, theme: str = "Animais"):
        if theme not in self.THEMES:
            raise ValueError(f"Tema desconhecido. Opções: {list(self.THEMES.keys())}")
        self.theme_items = self.THEMES[theme]

    def generate_cards(self, num_pairs: int) -> List[Card]:
        if num_pairs > len(self.theme_items):
            raise ValueError(
                f"O tema '{self.theme_items}' não tem itens suficientes para {num_pairs} pares."
            )

        selected = random.sample(self.theme_items, num_pairs)
        cards = []

        for item in selected:
            # No modo simples, match_id e display são iguais
            cards.append(Card(match_id=item, display_content=item))
            cards.append(Card(match_id=item, display_content=item))

        random.shuffle(cards)
        return cards


class MathStrategy(GameStrategy):
    """Modo Matemático: O par é Operação + Resultado (5+5 com 10)."""

    def generate_cards(self, num_pairs: int) -> List[Card]:
        cards = []
        for _ in range(num_pairs):
            # Gera soma simples para começar (pode evoluir para subtração/multiplicação)
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            result = str(a + b)
            expression = f"{a} + {b}"

            # Carta 1: A expressão (match_id é o resultado)
            cards.append(Card(match_id=result, display_content=expression))
            # Carta 2: O resultado numérico
            cards.append(Card(match_id=result, display_content=result))

        random.shuffle(cards)
        return cards


class ChemistryStrategy(GameStrategy):
    """Modo Educativo: Símbolo Químico <-> Nome do Elemento"""

    ELEMENTS = [
        ("H", "Hidrogênio"),
        ("He", "Hélio"),
        ("Li", "Lítio"),
        ("O", "Oxigênio"),
        ("C", "Carbono"),
        ("Au", "Ouro"),
        ("Ag", "Prata"),
        ("Fe", "Ferro"),
        ("Na", "Sódio"),
        ("Cl", "Cloro"),
        ("K", "Potássio"),
        ("Ca", "Cálcio"),
        ("N", "Nitrogênio"),
        ("Cu", "Cobre"),
        ("Pb", "Chumbo"),
        ("U", "Urânio"),
        ("Sn", "Estanho"),
        ("Hg", "Mercúrio"),
    ]

    def generate_cards(self, num_pairs: int) -> List[Card]:
        if num_pairs > len(self.ELEMENTS):
            # Fallback ou erro se pedir mais elementos do que temos
            raise ValueError("Não há elementos suficientes.")

        selected = random.sample(self.ELEMENTS, num_pairs)
        cards = []
        for symbol, name in selected:
            # Ambos compartilham o ID 'symbol' (ex: 'Au'), mas mostram textos diferentes
            cards.append(Card(match_id=symbol, display_content=symbol))  # Carta Au
            cards.append(Card(match_id=symbol, display_content=name))  # Carta Ouro

        random.shuffle(cards)
        return cards
