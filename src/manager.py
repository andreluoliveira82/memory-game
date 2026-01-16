import os

import pygame

from src.domain.board import Board
from src.domain.strategies import ChemistryStrategy, EmojiStrategy, MathStrategy
from src.infrastructure.repository import ScoreRepository
from src.services.game_service import GameService
from src.ui.components import InputBox
from src.ui.gui import GraphicUI
from src.ui.menu import MenuUI
from src.ui.ranking import RankingUI  # Vamos criar este arquivo no Passo 4
from src.ui.styles import COLORS, DIMENSIONS


class GameManager:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        pygame.init()

        # Tamanho padrão para o Menu
        self.menu_size = (900, 750)
        self.screen = pygame.display.set_mode(self.menu_size)
        pygame.display.set_caption("Memória Pythônica V3")
        self.clock = pygame.time.Clock()

        self.repository = ScoreRepository()
        self.state = "LOGIN"

        self.menu = MenuUI()
        self.ranking_ui = RankingUI(self.repository)  # Tela de Ranking
        self.game_ui = None
        self.player_name = ""

        self.font_login = pygame.font.SysFont("segoeui", 40)
        self.input_box = InputBox(300, 350, 300, 60, self.font_login)

        self.selected_theme = None
        self.selected_difficulty_label = ""

    def start_game(self, difficulty_tuple):
        rows, cols = difficulty_tuple
        self.current_difficulty = difficulty_tuple

        # --- LÓGICA DE TAMANHO DINÂMICO ---
        # Se tiver muitas linhas (Difícil), usa cartas menores (Compact Mode)
        current_card_size = DIMENSIONS["card_size"]
        if rows >= 6:
            current_card_size = 85  # Reduz de 110 para 85
            # Ajuste fino para fonte não ficar gigante em cards pequenos

        # Calcula multiplicador de dificuldade
        multiplier = 1.0
        if rows == 4 and cols == 4:
            self.selected_difficulty_label = "Fácil"
            multiplier = 1.0
        elif cols == 4:
            self.selected_difficulty_label = "Médio"
            multiplier = 1.5
        else:
            self.selected_difficulty_label = "Difícil"
            multiplier = 2.0

        # 2. Seleção de Estratégia
        if self.selected_theme == "Matemática":
            strategy = MathStrategy()
        elif self.selected_theme == "Química":
            strategy = ChemistryStrategy()
        else:
            strategy = EmojiStrategy(theme=self.selected_theme)

        try:
            board = Board(rows=rows, cols=cols, strategy=strategy)
            service = GameService(board, difficulty_multiplier=multiplier)

            # CÁLCULO DA JANELA COM O NOVO TAMANHO DE CARTA
            req_width = (cols * (current_card_size + DIMENSIONS["gap"])) + 100
            req_height = (
                DIMENSIONS["header_height"]
                + (rows * (current_card_size + DIMENSIONS["gap"]))
                + 120
            )  # +120 margem footer

            # Define tamanho final
            final_w = max(self.menu_size[0], req_width)
            final_h = max(self.menu_size[1], req_height)

            self.screen = pygame.display.set_mode((final_w, final_h))

            # --- PASSA O TAMANHO DA CARTA PARA A UI ---
            self.game_ui = GraphicUI(service, card_size=current_card_size)
            self.game_ui.screen = self.screen
            self.state = "GAME"

        except ValueError as e:
            print(f"Erro Fatal: {e}")

    def return_to_menu(self):
        self.state = "MENU"
        # Garante que centraliza novamente ao redimensionar
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen = pygame.display.set_mode(self.menu_size)
        self.menu.reset()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # --- LOGIN ---
                if self.state == "LOGIN":
                    name = self.input_box.handle_event(event)
                    if name:
                        self.player_name = name
                        self.state = "MENU"

                # --- MENU ---
                elif self.state == "MENU":
                    if (
                        event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                    ):  # Fix scroll
                        # Checa clique no botão de Ranking (vamos adicionar no MenuUI)
                        if self.menu.check_ranking_click(event.pos):
                            self.state = "RANKING"
                        else:
                            result = self.menu.handle_click(event.pos)
                            if result:
                                type, value = result
                                if type == "THEME_SELECT":
                                    self.selected_theme = value
                                    self.menu.switch_to_difficulty()
                                elif type == "DIFFICULTY_SELECT":
                                    self.start_game(value)

                # --- RANKING ---
                elif self.state == "RANKING":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"

                # --- GAME ---
                elif self.state == "GAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.return_to_menu()

                    # O 'check_click' agora é feito dentro do handle_click da UI
                    # Nós passamos o evento inteiro pra lá, não só a posição
                    action = self.game_ui.handle_click(event)

                    # Verifica ações retornadas pelos botões de Game Over
                    if action == "MENU":
                        self.return_to_menu()
                    elif action == "RESTART":
                        # Reinicia com a mesma dificuldade e tema atual
                        # A dificuldade está salva em self.selected_difficulty_label?
                        # Precisamos recuperar a tupla (rows, cols)
                        # Dica: Podemos salvar a tupla em self.current_difficulty no start_game
                        self.start_game(self.current_difficulty)

                    # Verifica se precisa salvar (Lógica mantida)
                    if (
                        self.game_ui.service.board.all_matched
                        and not self.game_ui.saved
                    ):
                        self.repository.save_score(
                            self.player_name,
                            self.game_ui.service.score,
                            self.selected_theme,
                            self.selected_difficulty_label,
                        )
                        self.game_ui.saved = True

            # --- DESENHO ---
            self.screen.fill(COLORS["background"])

            if self.state == "LOGIN":
                self._draw_login()
            elif self.state == "MENU":
                self.menu.draw(self.screen)
            elif self.state == "RANKING":
                self.ranking_ui.draw(self.screen)
            elif self.state == "GAME":
                self.game_ui.update()
                self.game_ui.draw()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def _draw_login(self):
        # (Mesmo código anterior)
        title = self.font_login.render("Digite seu Nome:", True, COLORS["text"])
        title_rect = title.get_rect(center=(450, 280))
        self.screen.blit(title, title_rect)
        self.input_box.draw(self.screen)
        hint = pygame.font.SysFont("arial", 20).render(
            "ENTER para confirmar", True, COLORS["accent"]
        )
        self.screen.blit(hint, (360, 420))
