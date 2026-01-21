# ARQUIVO: src/ui/gui.py
"""
Interface gráfica principal do jogo da memória.

Gerencia renderização do tabuleiro, estatísticas, animações e interações
do jogador durante uma partida.
"""

import pygame

import src.ui.styles as styles
from src.domain.facts import FactsDatabase
from src.infrastructure.sound import SoundManager
from src.services.game_service import GameService
from src.ui.components import (
    AdvancedParticleSystem,
    Button,
    CardFlipAnimation,
)
from src.ui.flashcard import FlashcardManager
from src.ui.styles import DIMENSIONS


class GraphicUI:
    """
    Interface gráfica do jogo usando Pygame.

    Responsável por toda a lógica de apresentação, incluindo renderização
    de cartas, estatísticas, animações e tela de Game Over.
    """

    def __init__(self, service: GameService, card_size: int = None):
        """
        Inicializa a interface gráfica.

        Args:
            service: Instância do serviço de jogo contendo a lógica
            card_size: Tamanho customizado das cartas (padrão: do tema)
        """
        self.service = service
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Inicializa Som
        self.sounds = SoundManager()

        # Configurações de Grid
        self.card_size = card_size if card_size else DIMENSIONS["card_size"]
        self.grid_width = (service.board.cols * self.card_size) + (
            (service.board.cols - 1) * DIMENSIONS["gap"]
        )

        # Inicialização de Fontes
        self._init_fonts()

        # Sistemas Visuais Avançados
        self.particles = AdvancedParticleSystem()
        self.flashcards = FlashcardManager()
        self.flip_animations: dict[tuple, CardFlipAnimation] = {}

        # Armazena tema atual para buscar fatos
        self.current_theme = None

        self.stars_earned = 0
        self.animation_triggered = False

        self.message = "Encontre os pares!"
        self.waiting_to_hide = False
        self.hide_timestamp = 0
        self.cards_to_hide = None

        self.saved = False

        # Botões de Game Over
        self._init_game_over_buttons()

    def _init_fonts(self) -> None:
        """Inicializa todas as fontes do jogo com fallback."""
        try:
            self.font_base_name = "segoeuiemoji"
            self.font_title = pygame.font.SysFont("segoeui", 48, bold=True)
            self.font_stats = pygame.font.SysFont("consolas", 22)
            self.font_msg = pygame.font.SysFont("segoeui", 28)
            self.font_btn = pygame.font.SysFont("segoeui", 20, bold=True)
            self.font_emoji = pygame.font.SysFont("segoeuiemoji", 60)
            self.font_score_big = pygame.font.SysFont("segoeui", 55, bold=True)
        except:
            self.font_base_name = "arial"
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_stats = pygame.font.SysFont("arial", 20)
            self.font_msg = pygame.font.SysFont("arial", 24)
            self.font_btn = pygame.font.SysFont("arial", 20, bold=True)
            self.font_emoji = pygame.font.SysFont("arial", 60)
            self.font_score_big = pygame.font.SysFont("arial", 50, bold=True)

    def _init_game_over_buttons(self) -> None:
        """Inicializa botões da tela de Game Over."""
        self.btn_restart = Button(
            x=0,
            y=0,
            w=220,
            h=50,
            text="Jogar Novamente",
            font=self.font_btn,
            color=styles.COLORS["success"],
            hover_color=(100, 255, 150),
            text_color=(40, 40, 40),
        )

        self.btn_menu = Button(
            x=0,
            y=0,
            w=140,
            h=45,
            text="Menu",
            font=self.font_btn,
            color=styles.COLORS["card_back"],
            hover_color=styles.COLORS["accent"],
            text_color=styles.COLORS["text"],
        )

        self.btn_ranking = Button(
            x=0,
            y=0,
            w=140,
            h=45,
            text="Ranking",
            font=self.font_btn,
            color=styles.COLORS["card_back"],
            hover_color=styles.COLORS["accent"],
            text_color=styles.COLORS["text"],
        )

    def _calculate_stars(self) -> int:
        """
        Calcula quantas estrelas o jogador ganhou baseado na eficiência.

        Returns:
            Número de estrelas (1-3)
        """
        pairs = (self.service.board.rows * self.service.board.cols) // 2
        moves = self.service.moves

        if moves <= pairs * 1.5:
            return 3
        elif moves <= pairs * 2.5:
            return 2
        return 1

    def update(self) -> None:
        """Atualiza estado das animações e timers."""
        # Limpa animações completadas
        completed_anims = [
            key for key, anim in self.flip_animations.items() if not anim.update()
        ]
        for key in completed_anims:
            del self.flip_animations[key]

        # Atualiza flashcards
        self.flashcards.update()

        if self.waiting_to_hide:
            if pygame.time.get_ticks() - self.hide_timestamp > 1000:
                self.service.hide_cards(*self.cards_to_hide)
                self.waiting_to_hide = False
                self.cards_to_hide = None
                self.message = "Tente novamente!"

    def handle_click(self, event: pygame.event.Event) -> str | None:
        """
        Processa cliques do mouse.

        Args:
            event: Evento do Pygame

        Returns:
            Ação a ser executada ("RESTART", "MENU", "RANKING") ou None
        """
        if self.service.board.all_matched:
            if self.btn_restart.check_click(event):
                self.sounds.play("click")
                return "RESTART"
            if self.btn_menu.check_click(event):
                self.sounds.play("click")
                return "MENU"
            if self.btn_ranking.check_click(event):
                self.sounds.play("click")
                return "RANKING"
            return None

        if self.waiting_to_hide:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for r in range(self.service.board.rows):
                for c in range(self.service.board.cols):
                    rect = self._get_card_rect(r, c)
                    if rect.collidepoint(event.pos):
                        self._process_pick(r, c)
                        break
        return None

    def set_theme(self, theme_name: str) -> None:
        """
        Define o tema atual do jogo (para buscar fatos).

        Args:
            theme_name: Nome do tema (ex: "Química", "Animais")
        """
        self.current_theme = theme_name

    def reset_animations(self) -> None:
        """Limpa todas as animações e efeitos visuais."""
        self.particles.clear()
        self.flashcards.clear()
        self.flip_animations.clear()
        self.animation_triggered = False
        print("🧹 Animações limpas!")  # Debug

    def _process_pick(self, r: int, c: int) -> None:
        """
        Processa a escolha de uma carta pelo jogador.

        Args:
            r: Linha da carta
            c: Coluna da carta
        """
        first_pos = self.service.first_selected_pos
        current_pos = (r, c)
        result = self.service.pick_card(r, c)

        card_rect = self._get_card_rect(r, c)
        self.flip_animations[current_pos] = CardFlipAnimation(card_rect)

        if result == "MATCH":
            self.sounds.play("match")
            combo = self.service.combo_streak

            # Busca fato educacional
            card = self.service.board.get_card(r, c)
            if card and self.current_theme:
                fact = FactsDatabase.get_fact(self.current_theme, card.match_id)
                if fact:
                    # Exibe flashcard no centro da tela
                    flashcard_pos = (self.width // 2, self.height // 2 + 100)
                    self.flashcards.add_flashcard(fact, flashcard_pos)
                    print(
                        f"✅ Flashcard exibido: {fact.get('name', card.match_id)}"
                    )  # Debug
                else:
                    print(
                        f"⚠️ Nenhum fato encontrado para: {self.current_theme} / {card.match_id}"
                    )  # Debug

            if combo == 1:
                self.particles.sparkle(card_rect.centerx, card_rect.centery)
                self.message = "Boa! Um par!"
            elif combo >= 5:
                self.particles.firework(card_rect.centerx, card_rect.centery)
                self.message = f"🔥 COMBO x{combo}! (+{100 * combo})"
            else:
                self.particles.sparkle(card_rect.centerx, card_rect.centery)
                self.message = f"COMBO x{combo}! (+{100 * combo})"

            if self.service.board.all_matched:
                self.sounds.play("win")

                stars = self._calculate_stars()
                if stars == 3:
                    self.particles.rainbow_burst(self.width // 2, self.height // 2)
                else:
                    self.particles.confetti(self.width // 2, self.height // 2)

        elif result == "NO_MATCH":
            self.sounds.play("error")
            self.message = "Ops... errou."
            self.waiting_to_hide = True
            self.hide_timestamp = pygame.time.get_ticks()
            self.cards_to_hide = (first_pos, current_pos)

        elif result == "FIRST_PICK":
            self.sounds.play("flip")
            self.message = "Escolha o par..."

    def draw(self) -> None:
        """Renderiza toda a interface do jogo."""
        self.screen.fill(styles.COLORS["background"])

        title = self.font_title.render("Memory Game", True, styles.COLORS["accent"])
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))

        self._draw_stats()

        mouse_pos = pygame.mouse.get_pos()
        for r in range(self.service.board.rows):
            for c in range(self.service.board.cols):
                card = self.service.board.get_card(r, c)
                rect = self._get_card_rect(r, c)
                self._draw_single_card(card, rect, mouse_pos, (r, c))

        if not self.service.board.all_matched:
            msg_surf = self.font_msg.render(self.message, True, styles.COLORS["accent"])
            msg_rect = msg_surf.get_rect(center=(self.width // 2, self.height - 50))
            self.screen.blit(msg_surf, msg_rect)

        if self.service.board.all_matched:
            self._draw_game_over_overlay()

        # Partículas e Flashcards (sempre por cima)
        self.particles.update_and_draw(self.screen)
        self.flashcards.draw(self.screen)

    def _draw_game_over_overlay(self) -> None:
        """Renderiza a tela de Game Over com resultados e botões."""
        if not self.animation_triggered:
            self.stars_earned = self._calculate_stars()
            self.animation_triggered = True

        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(210)
        overlay.fill((15, 15, 20))
        self.screen.blit(overlay, (0, 0))

        card_w, card_h = 480, 460
        cx, cy = self.width // 2, self.height // 2
        card_rect = pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (cx, cy)

        pygame.draw.rect(self.screen, (50, 52, 64), card_rect, border_radius=20)
        pygame.draw.rect(
            self.screen, styles.COLORS["accent"], card_rect, width=2, border_radius=20
        )

        lbl = self.font_title.render("NÍVEL CONCLUÍDO!", True, styles.COLORS["success"])
        self.screen.blit(lbl, lbl.get_rect(center=(cx, cy - 170)))

        star_str = "⭐" * self.stars_earned
        base_stars = self.font_emoji.render("⭐" * 3, True, (80, 80, 90))
        gold_stars = self.font_emoji.render(star_str, True, (255, 215, 0))

        stars_y = cy - 110
        self.screen.blit(base_stars, base_stars.get_rect(center=(cx, stars_y)))
        if self.stars_earned > 0:
            self.screen.blit(gold_stars, gold_stars.get_rect(center=(cx, stars_y)))

        score_lbl = self.font_stats.render("PONTUAÇÃO FINAL", True, (180, 180, 180))
        score_val = self.font_score_big.render(
            str(self.service.score), True, styles.COLORS["text"]
        )

        self.screen.blit(score_lbl, score_lbl.get_rect(center=(cx, cy - 40)))
        self.screen.blit(score_val, score_val.get_rect(center=(cx, cy + 10)))

        time_str = f"Tempo: {self.service.get_time_formatted()}"
        time_surf = self.font_msg.render(time_str, True, styles.COLORS["accent"])
        self.screen.blit(time_surf, time_surf.get_rect(center=(cx, cy + 60)))

        self.btn_restart.rect.center = (cx, cy + 130)
        self.btn_restart.draw(self.screen)

        button_gap = 20
        total_w_secondary = (
            self.btn_menu.rect.width + self.btn_ranking.rect.width + button_gap
        )
        start_x_secondary = (
            cx - (total_w_secondary // 2) + (self.btn_menu.rect.width // 2)
        )

        self.btn_menu.rect.center = (start_x_secondary, cy + 190)
        self.btn_ranking.rect.center = (
            start_x_secondary + self.btn_menu.rect.width + button_gap,
            cy + 190,
        )

        self.btn_menu.draw(self.screen)
        self.btn_ranking.draw(self.screen)

    def _draw_stats(self) -> None:
        """Renderiza as estatísticas do jogo (movimentos, pontos, tempo)."""
        section_w = self.width // 3
        y_pos = 90

        mov_text = f"Movimentos: {self.service.moves}"
        self._draw_stat_box(mov_text, (section_w * 0 + section_w // 2, y_pos))

        score_text = f"Pontos: {self.service.score}"
        score_color = (
            styles.COLORS["success"]
            if self.service.combo_streak > 1
            else styles.COLORS["text"]
        )
        self._draw_stat_box(
            score_text, (section_w * 1 + section_w // 2, y_pos), score_color
        )

        time_text = f"Tempo: {self.service.get_time_formatted()}"
        self._draw_stat_box(time_text, (section_w * 2 + section_w // 2, y_pos))

    def _draw_stat_box(self, text: str, pos: tuple, color: tuple = None) -> None:
        """Renderiza uma caixa de estatística individual."""
        if color is None:
            color = styles.COLORS["text"]
        surf = self.font_stats.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=pos))

    def _get_card_rect(self, row: int, col: int) -> pygame.Rect:
        """Calcula o retângulo de uma carta no grid."""
        start_x = (self.width - self.grid_width) // 2
        start_y = DIMENSIONS["header_height"]
        x = start_x + col * (self.card_size + DIMENSIONS["gap"])
        y = start_y + row * (self.card_size + DIMENSIONS["gap"])
        return pygame.Rect(x, y, self.card_size, self.card_size)

    def _draw_single_card(
        self, card, rect: pygame.Rect, mouse_pos: tuple, pos: tuple
    ) -> None:
        """Renderiza uma carta individual com animações."""
        if pos in self.flip_animations:
            anim = self.flip_animations[pos]
            rect = anim.rect

        bg_color = styles.COLORS["card_back"]
        if not card.is_revealed and not card.is_matched and not self.waiting_to_hide:
            if rect.collidepoint(mouse_pos):
                bg_color = styles.COLORS["card_back_hover"]
        if card.is_revealed:
            bg_color = styles.COLORS["card_face"]
        if card.is_matched:
            bg_color = styles.COLORS["success"]

        shadow = rect.copy()
        shadow.move_ip(4, 4)
        pygame.draw.rect(
            self.screen, (20, 20, 20), shadow, border_radius=DIMENSIONS["border_radius"]
        )

        pygame.draw.rect(
            self.screen, bg_color, rect, border_radius=DIMENSIONS["border_radius"]
        )

        if card.is_revealed or card.is_matched:
            pygame.draw.rect(
                self.screen,
                styles.COLORS["card_border"],
                rect,
                width=2,
                border_radius=DIMENSIONS["border_radius"],
            )
            self._draw_dynamic_text(str(card.display_content), rect)
        else:
            q_surf = self.font_msg.render("?", True, (255, 255, 255, 50))
            self.screen.blit(q_surf, q_surf.get_rect(center=rect.center))

    def _draw_dynamic_text(self, text: str, rect: pygame.Rect) -> None:
        """Renderiza texto ajustando tamanho da fonte automaticamente."""
        max_width = rect.width - 10
        font_size = 40

        while font_size > 12:
            font = pygame.font.SysFont(self.font_base_name, font_size)
            text_surf = font.render(text, True, styles.COLORS["text_card"])
            if text_surf.get_width() <= max_width:
                break
            font_size -= 2

        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
