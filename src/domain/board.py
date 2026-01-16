# src/domain/board.py
from typing import List, Optional

from src.domain.card import Card
from src.domain.strategies import EmojiStrategy, GameStrategy


class Board:
    def __init__(self, rows: int, cols: int, strategy: GameStrategy = None):
        if (rows * cols) % 2 != 0:
            raise ValueError("O número total de cartas deve ser par!")

        self.rows = rows
        self.cols = cols
        self.grid: List[List[Card]] = []

        # Se nenhuma estratégia for passada, usa o padrão (Emojis de Animais)
        self.strategy = strategy if strategy else EmojiStrategy(theme="Animais")

        self.reset()

    def reset(self, new_strategy: GameStrategy = None) -> None:
        """Reinicia o jogo, opcionalmente trocando a estratégia/tema."""
        if new_strategy:
            self.strategy = new_strategy

        num_pairs = (self.rows * self.cols) // 2
        cards = self.strategy.generate_cards(num_pairs)

        # Preenche a grid (transforma lista linear em matriz)
        self.grid = []
        iterator = iter(cards)
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(next(iterator))
            self.grid.append(row)

    def get_card(self, row: int, col: int) -> Optional[Card]:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    @property
    def all_matched(self) -> bool:
        return all(card.is_matched for row in self.grid for card in row)

    def __str__(self) -> str:
        # Atualizado para usar display_content
        header = "    " + " ".join(str(i) for i in range(self.cols))
        rows_str = [header]
        for i, row in enumerate(self.grid):
            rows_str.append(f"{i} | " + " ".join(str(card) for card in row))
        return "\n".join(rows_str)
