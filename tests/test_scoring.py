import pytest

from src.domain.board import Board
from src.domain.card import Card
from src.services.game_service import GameService


# Mock simples para injetar no Board
class MockStrategy:
    def generate_cards(self, num_pairs):
        # Gera 2 pares fixos: A-A e B-B
        return [
            Card(match_id="A", display_content="A"),
            Card(match_id="A", display_content="A"),
            Card(match_id="B", display_content="B"),
            Card(match_id="B", display_content="B"),
        ]


@pytest.fixture
def game_service():
    # Setup: Cria um tabuleiro 2x2 com estratégia controlada
    board = Board(rows=2, cols=2, strategy=MockStrategy())
    # Injeta multiplicador de dificuldade 1.5 (Nível Médio)
    return GameService(board, difficulty_multiplier=1.5)


def test_basic_match_score(game_service):
    """Testa se um match simples calcula pontos corretamente com multiplicador."""
    # Simula escolha do par "A" (posições 0,0 e 0,1 no grid 2x2)
    game_service.pick_card(0, 0)
    result = game_service.pick_card(0, 1)

    assert result == "MATCH"
    # Cálculo: 100 (base) * 1 (combo) * 1.5 (mult) = 150
    assert game_service.score == 150
    assert game_service.combo_streak == 1


def test_combo_streak_increases_score(game_service):
    """Testa se acertar dois seguidos aumenta o Combo e a pontuação exponencialmente."""
    # 1º Match (A-A)
    game_service.pick_card(0, 0)
    game_service.pick_card(0, 1)
    score_after_first = 150  # Já validado acima

    # 2º Match (B-B) (posições 1,0 e 1,1)
    game_service.pick_card(1, 0)
    game_service.pick_card(1, 1)

    # Cálculo 2º Match: 100 (base) * 2 (combo) * 1.5 (mult) = 300 pontos
    # Total esperado: 150 + 300 = 450
    assert game_service.combo_streak == 2
    assert game_service.score == 450


def test_mismatch_resets_combo_and_penalizes(game_service):
    """Testa se errar zera o combo e tira pontos."""
    # Começa com pontuação inicial para não testar negativo
    game_service.score = 100
    game_service.combo_streak = 5  # Simula um combo alto

    # Tenta errar (A com B)
    game_service.pick_card(0, 0)  # A
    result = game_service.pick_card(1, 0)  # B

    assert result == "NO_MATCH"
    assert game_service.combo_streak == 0  # Resetou?
    assert game_service.score == 80  # Perdeu 20 pontos?
