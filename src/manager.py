# ARQUIVO: src/manager.py
"""
Gerenciador principal do jogo (State Manager).

Controla o fluxo entre telas (login, menu, jogo, ranking, configurações)
e gerencia o ciclo de vida da aplicação.
"""

import os

import pygame

import src.ui.styles as styles  # Import do módulo inteiro
from src.domain.board import Board
from src.domain.strategies import ChemistryStrategy, EmojiStrategy, MathStrategy
from src.infrastructure.repository import ScoreRepository
from src.services.game_service import GameService
from src.ui.components import InputBox
from src.ui.gui import GraphicUI
from src.ui.menu import MenuUI
from src.ui.ranking import RankingUI
from src.ui.settings import SettingsUI
from src.ui.statistics import StatisticsUI
from src.ui.styles import DIMENSIONS


class GameManager:
    """
    Gerenciador central do jogo.

    Implementa uma máquina de estados para controlar o fluxo da aplicação:
    LOGIN → MENU → GAME/RANKING/STATS/SETTINGS
    """

    def __init__(self):
        """Inicializa o gerenciador e todos os subsistemas."""
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        self.menu_size = (900, 750)
        self.screen = pygame.display.set_mode(self.menu_size)
        pygame.display.set_caption("Memória Pythônica V3")
        self.clock = pygame.time.Clock()

        self.repository = ScoreRepository()
        self.state = "LOGIN"

        # Inicializa todas as telas
        self.menu = MenuUI()
        self.ranking_ui = RankingUI(self.repository)
        self.stats_ui = StatisticsUI(self.repository)
        self.settings_ui = SettingsUI()

        self.game_ui = None
        self.player_name = ""

        self.font_login = pygame.font.SysFont("segoeui", 40)
        self.input_box = InputBox(300, 350, 300, 60, self.font_login)

        self.selected_theme = None
        self.selected_difficulty_label = ""
        self.current_difficulty = (4, 4)

    def start_game(self, difficulty_tuple: tuple) -> None:
        """
        Inicia uma nova partida.

        Args:
            difficulty_tuple: Tupla (rows, cols) definindo a grade
        """
        rows, cols = difficulty_tuple
        self.current_difficulty = difficulty_tuple

        current_card_size = DIMENSIONS["card_size"]
        if rows >= 6:
            current_card_size = 85

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

        if self.selected_theme == "Matemática":
            strategy = MathStrategy()
        elif self.selected_theme == "Química":
            strategy = ChemistryStrategy()
        else:
            strategy = EmojiStrategy(theme=self.selected_theme)

        try:
            board = Board(rows=rows, cols=cols, strategy=strategy)
            service = GameService(board, difficulty_multiplier=multiplier)

            req_width = (cols * (current_card_size + DIMENSIONS["gap"])) + 100
            req_height = (
                DIMENSIONS["header_height"]
                + (rows * (current_card_size + DIMENSIONS["gap"]))
                + 120
            )

            final_w = max(self.menu_size[0], req_width)
            final_h = max(self.menu_size[1], req_height)

            self.screen = pygame.display.set_mode((final_w, final_h))
            self.game_ui = GraphicUI(service, card_size=current_card_size)
            self.game_ui.screen = self.screen
            self.game_ui.set_theme(
                self.selected_theme
            )  # Define o tema para buscar fatos
            self.state = "GAME"

        except ValueError as e:
            print(f"Erro Fatal: {e}")

    def return_to_menu(self) -> None:
        """Retorna ao menu principal."""
        self.state = "MENU"
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen = pygame.display.set_mode(self.menu_size)
        self.menu.reset()

    def run(self) -> None:
        """Loop principal da aplicação."""
        running = True
        while running:
            if self.state != "MENU":
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        result = self.menu.handle_click(event.pos)

                        if result:
                            type_action, value = result

                            if type_action == "ACTION":
                                if value == "RANKING":
                                    self.state = "RANKING"
                                elif value == "STATS":
                                    self.state = "STATS"
                                elif value == "SETTINGS":
                                    self.state = "SETTINGS"
                                elif value == "BACK":
                                    self.menu.reset()

                            elif type_action == "THEME_SELECT":
                                self.selected_theme = value
                                self.menu.switch_to_difficulty()
                            elif type_action == "DIFFICULTY_SELECT":
                                self.start_game(value)

                # --- RANKING ---
                elif self.state == "RANKING":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.ranking_ui.handle_click(event) == "BACK":
                            self.state = "MENU"

                # --- STATS ---
                elif self.state == "STATS":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.stats_ui.handle_click(event) == "BACK":
                            self.state = "MENU"

                # --- SETTINGS ---
                elif self.state == "SETTINGS":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = self.settings_ui.handle_click(event)
                        if action == "BACK":
                            self.state = "MENU"
                        elif action == "THEME_CHANGED":
                            # Força recriação das telas para aplicar novo tema
                            self._recreate_ui_screens()

                # --- GAME ---
                elif self.state == "GAME":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.return_to_menu()

                    action = self.game_ui.handle_click(event)

                    if action == "MENU":
                        self.game_ui.reset_animations()  # Limpa antes de sair
                        self.return_to_menu()
                    elif action == "RESTART":
                        self.game_ui.reset_animations()  # Limpa antes de reiniciar
                        self.start_game(self.current_difficulty)
                    elif action == "RANKING":
                        self.return_to_menu()
                        self.state = "RANKING"

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
            self.screen.fill(styles.COLORS["background"])

            if self.state == "LOGIN":
                self._draw_login()
            elif self.state == "MENU":
                self.menu.draw(self.screen)
            elif self.state == "RANKING":
                self.ranking_ui.draw(self.screen)
            elif self.state == "STATS":
                self.stats_ui.draw(self.screen)
            elif self.state == "SETTINGS":
                self.settings_ui.draw(self.screen)
            elif self.state == "GAME":
                self.game_ui.update()
                self.game_ui.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def _draw_login(self) -> None:
        """Renderiza a tela de login."""
        title = self.font_login.render("Digite seu Nome:", True, styles.COLORS["text"])
        title_rect = title.get_rect(center=(450, 280))
        self.screen.blit(title, title_rect)
        self.input_box.draw(self.screen)
        hint = pygame.font.SysFont("arial", 20).render(
            "ENTER para confirmar", True, styles.COLORS["accent"]
        )
        self.screen.blit(hint, (360, 420))

    def _recreate_ui_screens(self) -> None:
        """
        Recria todas as telas da UI após mudança de tema.

        Isso garante que as cores sejam atualizadas imediatamente.
        """
        # Recria todas as instâncias das telas
        self.menu = MenuUI()
        self.ranking_ui = RankingUI(self.repository)
        self.stats_ui = StatisticsUI(self.repository)
        # settings_ui não precisa recriar pois está na tela ativa

        # Recria input box com novo tema
        self.input_box = InputBox(300, 350, 300, 60, self.font_login)
