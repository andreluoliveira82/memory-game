import time
from typing import Optional, Tuple

from src.domain.board import Board


class GameService:
    def __init__(self, board: Board):
        self.board = board
        self.moves = 0
        self.score = 0
        self.start_time = time.time()
        self.end_time = None  # Para travar o relógio
        self.first_selected_pos: Optional[Tuple[int, int]] = None

        # Gamification
        self.combo_streak = 0  # Contador de acertos seguidos

    def get_time_formatted(self):
        """Retorna tempo formatado. Se jogo acabou, usa o tempo final."""
        if self.end_time:
            total_seconds = int(self.end_time - self.start_time)
        else:
            total_seconds = int(time.time() - self.start_time)

        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def pick_card(self, row: int, col: int) -> str:
        card = self.board.get_card(row, col)

        if not card or card.is_revealed or card.is_matched:
            return "INVALID"

        card.reveal()

        if self.first_selected_pos is None:
            self.first_selected_pos = (row, col)
            return "FIRST_PICK"

        # Segunda carta escolhida
        self.moves += 1
        r1, c1 = self.first_selected_pos
        first_card = self.board.get_card(r1, c1)
        self.first_selected_pos = None

        if first_card.match_id == card.match_id:
            # --- LÓGICA DE MATCH & COMBO ---
            first_card.mark_as_matched()
            card.mark_as_matched()

            self.combo_streak += 1

            # Fórmula: Base (100) * Multiplicador de Combo
            points = 100 * self.combo_streak
            self.score += points

            # Verifica Vitória
            if self.board.all_matched:
                self.end_time = time.time()  # Trava o relógio
                # Bônus de tempo: (1 ponto por segundo economizado de uma base de 3 min)
                # Opcional, por enquanto vamos focar no combo

            return "MATCH"
        else:
            # --- LÓGICA DE ERRO ---
            self.combo_streak = 0  # Reseta combo
            # Penalidade leve
            self.score = max(0, self.score - 20)
            return "NO_MATCH"

    def hide_cards(self, pos1, pos2):
        c1 = self.board.get_card(*pos1)
        c2 = self.board.get_card(*pos2)
        if c1:
            c1.hide()
        if c2:
            c2.hide()
