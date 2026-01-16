import os
import time
from src.services.game_service import GameService

class ConsoleUI:
    """
    Interface de Linha de Comando (CLI) para o Jogo da Memória.
    
    Responsável por capturar inputs, renderizar o tabuleiro no terminal
    e gerenciar o timing de exibição das cartas.
    """

    def __init__(self, service: GameService):
        self.service = service

    def clear_screen(self):
        """Limpa o console de acordo com o Sistema Operacional."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(self, message: str = ""):
        """Renderiza o estado atual do tabuleiro e uma mensagem ao usuário."""
        self.clear_screen()
        print("=== JOGO DA MEMÓRIA PYTHONICA ===")
        print(f"Movimentos: {self.service.moves}\n")
        print(self.service.board)
        print(f"\nStatus: {message}")

    def get_input(self) -> tuple[int, int]:
        """Solicita e valida as coordenadas do jogador."""
        while True:
            try:
                raw_input = input("\nDigite a posição (linha coluna) ou 'q' para sair: ").strip()
                if raw_input.lower() == 'q':
                    exit()
                
                r, c = map(int, raw_input.split())
                return r, c
            except (ValueError, IndexError):
                print("⚠️ Entrada inválida! Digite dois números separados por espaço (ex: 0 1).")

    def run(self):
        """Loop principal da interface de console."""
        last_message = "Escolha sua primeira carta!"
        
        while not self.service.board.all_matched:
            self.display_board(last_message)
            r, c = self.get_input()
            
            # Armazenamos a posição da primeira carta caso precisemos escondê-la depois
            current_pos = (r, c)
            first_pos = self.service.first_selected_pos
            
            result = self.service.pick_card(r, c)

            if result == "INVALID":
                last_message = "❌ Posição inválida ou carta já revelada!"
            elif result == "FIRST_PICK":
                last_message = "Agora escolha o par!"
            elif result == "MATCH":
                last_message = "✅ Boa! Você encontrou um par!"
            elif result == "NO_MATCH":
                # Lógica de "Peek": Mostra a carta errada por 1.5s e depois esconde
                self.display_board("❌ Não foi dessa vez...")
                time.sleep(1.5)
                self.service.hide_cards(first_pos, current_pos)
                last_message = "Tente novamente!"

        self.display_board("🎉 PARABÉNS! Você completou o jogo!")
        print(f"Total de movimentos: {self.service.moves}")