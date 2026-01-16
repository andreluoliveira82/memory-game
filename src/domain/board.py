# src/domain/board.py

import random
from typing import List, Optional
from src.domain.card import Card

class Board:
    """
    Representa o tabuleiro do jogo contendo uma grade de cartas.
    
    Responsabilidades:
        - Gerar e embaralhar pares de cartas.
        - Gerenciar o acesso às cartas por coordenadas (linha, coluna).
        - Verificar se o jogo foi concluído.
    """

    def __init__(self, rows: int, cols: int):
        """
        Inicializa o tabuleiro com as dimensões especificadas.
        
        Args:
            rows (int): Número de linhas.
            cols (int): Número de colunas.
            
        Raises:
            ValueError: Se o número total de cartas (rows * cols) for ímpar.
        """
        if (rows * cols) % 2 != 0:
            raise ValueError("O número total de cartas deve ser par para formar pares!")
        
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Card]] = []
        self._initialize_board()

    def _initialize_board(self) -> None:
        """Cria as cartas, embaralha e as distribui na grade."""
        total_pairs = (self.rows * self.cols) // 2
        # Usando letras do alfabeto como valores temporários (A, B, C...)
        # Em um projeto real, isso poderia ser injetado ou vir de um enum
        values = [chr(65 + i) for i in range(total_pairs)] * 2
        random.shuffle(values)

        # Transforma a lista linear em uma matriz (grade)
        for r in range(self.rows):
            row_cards = []
            for c in range(self.cols):
                value = values.pop()
                row_cards.append(Card(value=value))
            self.grid.append(row_cards)

    def get_card(self, row: int, col: int) -> Optional[Card]:
        """
        Retorna a carta em uma posição específica.
        
        Args:
            row (int): Índice da linha.
            col (int): Índice da coluna.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    @property
    def all_matched(self) -> bool:
        """Verifica se todas as cartas do tabuleiro já foram combinadas."""
        return all(card.is_matched for row in self.grid for card in row)

    def reset(self, new_values: list[str]):
        """Reinicia o tabuleiro com novos valores e embaralhamento."""
        random.shuffle(new_values)
        self.grid = []
        

    def __str__(self) -> str:
        """Representação visual simples para o modo CLI."""
        header = "    " + " ".join(str(i) for i in range(self.cols))
        rows_str = [header]
        for i, row in enumerate(self.grid):
            rows_str.append(f"{i} | " + " ".join(str(card) for card in row))
        return "\n".join(rows_str)