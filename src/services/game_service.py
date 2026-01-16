from typing import Optional, Tuple
from src.domain.board import Board
from src.domain.card import Card

class GameService:
    """
    Orquestrador das regras de negócio do Jogo da Memória.
    
    Gerencia o estado da rodada (primeira ou segunda carta escolhida),
    valida movimentos e rastreia o progresso.
    """

    def __init__(self, board: Board):
        self.board = board
        self.moves = 0
        self.first_selected_pos: Optional[Tuple[int, int]] = None

    def pick_card(self, row: int, col: int) -> str:
        """
        Processa a escolha de uma carta pelo jogador.
        
        Returns:
            str: Mensagem indicando o resultado da ação (MATCH, NO_MATCH, FIRST_PICK, INVALID).
        """
        card = self.board.get_card(row, col)

        # Validações básicas
        if not card or card.is_revealed or card.is_matched:
            return "INVALID"

        card.reveal()

        # Se for a primeira carta da rodada
        if self.first_selected_pos is None:
            self.first_selected_pos = (row, col)
            return "FIRST_PICK"

        # Se for a segunda carta, comparamos com a primeira
        self.moves += 1
        r1, c1 = self.first_selected_pos
        first_card = self.board.get_card(r1, c1)
        
        self.first_selected_pos = None  # Reseta para a próxima rodada

        if first_card.value == card.value:
            first_card.mark_as_matched()
            card.mark_as_matched()
            return "MATCH"
        else:
            # Note: A UI será responsável por chamar o 'hide' após um delay
            # ou o service pode retornar os objetos para a UI gerenciar.
            return "NO_MATCH"

    def hide_cards(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        """Desvira duas cartas caso não sejam um par."""
        c1 = self.board.get_card(*pos1)
        c2 = self.board.get_card(*pos2)
        if c1: c1.hide()
        if c2: c2.hide()