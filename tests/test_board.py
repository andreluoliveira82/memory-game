import pytest
from src.domain.board import Board

def test_board_initialization_creates_correct_number_of_cards():
    """Garante que o tabuleiro tem o tamanho correto."""
    rows, cols = 4, 4
    board = Board(rows, cols)
    assert len(board.grid) == rows
    assert len(board.grid[0]) == cols

def test_board_contains_only_pairs():
    """Garante que cada valor de carta aparece exatamente duas vezes."""
    rows, cols = 2, 4  # 8 cartas, 4 pares
    board = Board(rows, cols)
    
    # Coleta todos os valores das cartas em uma lista simples
    all_values = [card.value for row in board.grid for card in row]
    
    # Verifica se para cada valor único, a contagem é exatamente 2
    for val in set(all_values):
        assert all_values.count(val) == 2

def test_board_raises_error_on_odd_total_cards():
    """Garante que o sistema impede tabuleiros com total de cartas ímpar."""
    with pytest.raises(ValueError, match="O número total de cartas deve ser par"):
        Board(3, 3)