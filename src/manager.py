import pygame

from src.domain.board import Board
from src.domain.strategies import ChemistryStrategy, EmojiStrategy, MathStrategy
from src.services.game_service import GameService
from src.ui.gui import GraphicUI
from src.ui.menu import MenuUI


class GameManager:
    def __init__(self):
        pygame.init()
        # Janela base (tamanho inicial, pode mudar dependendo do grid)
        self.screen = pygame.display.set_mode((800, 700))
        pygame.display.set_caption("Memória Pythônica V2")
        self.clock = pygame.time.Clock()
        self.selected_theme = None  # Armazena o tema temporariamente
        self.state = "MENU"  # MENU ou GAME
        self.menu = MenuUI()
        self.game_ui = None  # Será criado quando o jogo começar

    def start_game(self, difficulty):
        """Inicia o jogo combinando o Tema salvo + Dificuldade escolhida"""
        rows, cols = difficulty

        # Fábrica de Estratégias
        if self.selected_theme == "Matemática":
            strategy = MathStrategy()
        elif self.selected_theme == "Química":
            strategy = ChemistryStrategy()
        else:
            strategy = EmojiStrategy(theme=self.selected_theme)

        # Injeta Rows e Cols dinâmicos
        try:
            board = Board(rows=rows, cols=cols, strategy=strategy)
            service = GameService(board)
            self.game_ui = GraphicUI(service)
            self.game_ui.screen = self.screen
            self.state = "GAME"
        except ValueError as e:
            print(f"Erro: {e}")

    def run(self):
        running = True

        while running:
            # Reseta cursor para seta padrão (menu muda para mãozinha)
            if self.state != "MENU":
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Eventos do MENU
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            result = self.menu.handle_click(event.pos)
                            if result:
                                type, value = result
                                if type == "THEME_SELECT":
                                    self.selected_theme = value
                                    self.menu.switch_to_difficulty()
                                elif type == "DIFFICULTY_SELECT":
                                    self.start_game(value)

                # Eventos do Jogo
                elif self.state == "GAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                            self.menu.reset()  # Volta para escolha de temas
                            self.selected_theme = None

                    # Delega eventos de clique para a UI do jogo
                    # (Precisamos adaptar levemente o GraphicUI para não ter loop próprio)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.game_ui.waiting_to_hide:  # Acesso direto simples
                            self.game_ui.handle_click(event.pos)

            # --- LOOP DE DESENHO ---
            if self.state == "MENU":
                self.menu.draw(self.screen)

            elif self.state == "GAME":
                # Executa lógica de tempo do jogo (cards hiding)
                self.game_ui.update()
                self.game_ui.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
