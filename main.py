import argparse
from src.domain.board import Board
from src.services.game_service import GameService
from src.ui.console import ConsoleUI
from src.ui.gui import GraphicUI

def main():
    # Configuração de argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Jogo da Memória em Python")
    parser.add_argument('--mode', choices=['cli', 'gui'], default='gui', 
                        help="Escolha o modo de jogo (padrão: gui)")
    args = parser.parse_args()

    # Setup do Core (Independente de UI)
    board = Board(rows=4, cols=4)
    service = GameService(board)

    # Fábrica de UI
    if args.mode == 'cli':
        ui = ConsoleUI(service)
    else:
        ui = GraphicUI(service)

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nJogo encerrado.")

if __name__ == "__main__":
    main()