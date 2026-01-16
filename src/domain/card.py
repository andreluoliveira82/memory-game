# src/domain/card.py

from dataclasses import dataclass, field


@dataclass
class Card:
    """
    Representa uma carta individual no jogo da memória.
    
    Responsável por manter o estado de visibilidade e identificação da carta.
    
    Attributes:
        value (str): O conteúdo da carta (ex: 'A', 'B', emoji).
        is_revealed (bool): Se a carta está atualmente virada para cima.
        is_matched (bool): Se a carta já encontrou seu par correspondente.
    """
    value: str
    is_revealed: bool = False
    is_matched: bool = False

    def reveal(self) -> None:
        """Revela a carta, tornando-a visível."""
        if not self.is_matched:
            self.is_revealed = True

    def hide(self) -> None:
        """Vira a carta para baixo, caso não tenha sido combinada"""
        if not self.is_matched:
            self.is_revealed = False

    def mark_as_matched(self) -> None:
        """Define que a carta encontrou seu par e deve ficar visível permanentemente."""
        self.is_matched = True
        self.is_revealed = True

    def __repr__(self) -> str:
        return f"{self.value}" if self.is_revealed else "?"