# src/domain/card.py
from dataclasses import dataclass


@dataclass
class Card:
    match_id: str  # Identificador único do par (ex: "10")
    display_content: str  # O que aparece na tela (ex: "5 + 5" ou "10")
    is_revealed: bool = False
    is_matched: bool = False

    def reveal(self) -> None:
        if not self.is_matched:
            self.is_revealed = True

    def hide(self) -> None:
        if not self.is_matched:
            self.is_revealed = False

    def mark_as_matched(self) -> None:
        self.is_matched = True
        self.is_revealed = True

    def __repr__(self) -> str:
        # Útil para debug no console
        return f"[{self.display_content}]" if self.is_revealed else "[?]"
