import argparse

from src.domain.board import Board

# Importando as novas estratégias
from src.domain.strategies import EmojiStrategy, MathStrategy
from src.services.game_service import GameService
from src.ui.console import ConsoleUI
from src.ui.gui import GraphicUI


def main():
    parser = argparse.ArgumentParser(description="Jogo da Memória V2")
    parser.add_argument(
        "--mode", choices=["cli", "gui"], default="gui", help="Interface do jogo"
    )
    # Adicionando argumento para testar temas
    parser.add_argument(
        "--theme",
        choices=["animais", "math", "space"],
        default="animais",
        help="Escolha o tema",
    )
    args = parser.parse_args()

    # --- SELEÇÃO DE ESTRATÉGIA ---
    if args.theme == "math":
        strategy = MathStrategy()
        print("🧮 Iniciando Modo Matemático!")
    elif args.theme == "space":
        strategy = EmojiStrategy(theme="Espaço")
        print("🚀 Iniciando Modo Espacial!")
    else:
        strategy = EmojiStrategy(theme="Animais")
        print("🐶 Iniciando Modo Animais!")

    # Injeção de dependência: O Board recebe a estratégia escolhida
    board = Board(rows=4, cols=4, strategy=strategy)
    service = GameService(board)

    if args.mode == "cli":
        ui = ConsoleUI(service)
    else:
        ui = GraphicUI(service)

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nJogo encerrado.")


if __name__ == "__main__":
    main()
