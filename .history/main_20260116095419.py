from src.domain.board import Board
from src.services.game_service import GameService
from src.ui.console.py import ConsoleUI 

def main():
    # Configuração inicial (Injeção de Dependência manual)
    # Podemos facilmente mudar rows/cols aqui
    board = Board(rows=4, cols=4)
    service = GameService(board)
    ui = ConsoleUI(service)

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n\nJogo encerrado. Até a próxima!")

if __name__ == "__main__":
    main()