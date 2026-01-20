# ARQUIVO: src/ui/gui.py
import pygame

from src.infrastructure.sound import SoundManager
from src.services.game_service import GameService
from src.ui.components import Button, ParticleSystem
from src.ui.styles import COLORS, DIMENSIONS


class GraphicUI:
    def __init__(self, service: GameService, card_size: int = None):
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

        # --- INICIALIZAÇÃO DE FONTES ---
        try:
            self.font_base_name = "segoeuiemoji"
            self.font_title = pygame.font.SysFont("segoeui", 48, bold=True)
            self.font_stats = pygame.font.SysFont("consolas", 22)
            self.font_msg = pygame.font.SysFont("segoeui", 28)
            # Fonte levemente menor para caber nos botões confortavelmente
            self.font_btn = pygame.font.SysFont("segoeui", 20, bold=True)
            self.font_emoji = pygame.font.SysFont("segoeuiemoji", 60)
            self.font_score_big = pygame.font.SysFont(
                "segoeui", 55, bold=True
            )  # Fonte destaque
        except:
            self.font_base_name = "arial"
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_stats = pygame.font.SysFont("arial", 20)
            self.font_msg = pygame.font.SysFont("arial", 24)
            self.font_btn = pygame.font.SysFont("arial", 20, bold=True)
            self.font_emoji = pygame.font.SysFont("arial", 60)
            self.font_score_big = pygame.font.SysFont("arial", 50, bold=True)

        # Sistemas Visuais
        self.particles = ParticleSystem()
        self.stars_earned = 0
        self.animation_triggered = False

        self.message = "Encontre os pares!"
        self.waiting_to_hide = False
        self.hide_timestamp = 0
        self.cards_to_hide = None

        self.saved = False

        # --- BOTÕES DE GAME OVER ---
        # Inicializamos aqui, mas as posições exatas são definidas no draw()
        # para garantir centralização dinâmica

        # Botão Principal (Destaque)
        self.btn_restart = Button(
            x=0,
            y=0,
            w=220,
            h=50,
            text="Jogar Novamente",
            font=self.font_btn,
            color=COLORS["success"],
            hover_color=(100, 255, 150),
            text_color=(40, 40, 40),
        )

        # Botões Secundários (Lado a Lado)
        self.btn_menu = Button(
            x=0,
            y=0,
            w=140,
            h=45,
            text="Menu",
            font=self.font_btn,
            color=COLORS["card_back"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text"],
        )

        self.btn_ranking = Button(
            x=0,
            y=0,
            w=140,
            h=45,
            text="Ranking",
            font=self.font_btn,
            color=COLORS["card_back"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text"],
        )

    def _calculate_stars(self):
        pairs = (self.service.board.rows * self.service.board.cols) // 2
        moves = self.service.moves
        if moves <= pairs * 1.5:
            return 3
        elif moves <= pairs * 2.5:
            return 2
        return 1

    def update(self):
        if self.waiting_to_hide:
            if pygame.time.get_ticks() - self.hide_timestamp > 1000:
                self.service.hide_cards(*self.cards_to_hide)
                self.waiting_to_hide = False
                self.cards_to_hide = None
                self.message = "Tente novamente!"

    def handle_click(self, event):
        # 1. Se o jogo acabou, checa cliques nos botões da overlay
        if self.service.board.all_matched:
            if self.btn_restart.check_click(event):
                self.sounds.play("click")
                return "RESTART"
            if self.btn_menu.check_click(event):
                self.sounds.play("click")
                return "MENU"
            if self.btn_ranking.check_click(event):
                self.sounds.play("click")
                return "RANKING"  # Nova Ação
            return None

        # 2. Jogo rodando
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

    def _process_pick(self, r, c):
        first_pos = self.service.first_selected_pos
        current_pos = (r, c)
        result = self.service.pick_card(r, c)

        if result == "MATCH":
            self.sounds.play("match")
            combo = self.service.combo_streak
            if combo > 1:
                self.message = f"COMBO x{combo}! (+{100 * combo})"
            else:
                self.message = "Boa! Um par!"

            if self.service.board.all_matched:
                self.sounds.play("win")

        elif result == "NO_MATCH":
            self.sounds.play("error")
            self.message = "Ops... errou."
            self.waiting_to_hide = True
            self.hide_timestamp = pygame.time.get_ticks()
            self.cards_to_hide = (first_pos, current_pos)

        elif result == "FIRST_PICK":
            self.sounds.play("flip")
            self.message = "Escolha o par..."

    def draw(self):
        self.screen.fill(COLORS["background"])

        title = self.font_title.render("Memory Game", True, COLORS["accent"])
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))

        self._draw_stats()

        mouse_pos = pygame.mouse.get_pos()
        for r in range(self.service.board.rows):
            for c in range(self.service.board.cols):
                card = self.service.board.get_card(r, c)
                rect = self._get_card_rect(r, c)
                self._draw_single_card(card, rect, mouse_pos)

        if not self.service.board.all_matched:
            msg_surf = self.font_msg.render(self.message, True, COLORS["accent"])
            msg_rect = msg_surf.get_rect(center=(self.width // 2, self.height - 50))
            self.screen.blit(msg_surf, msg_rect)

        if self.service.board.all_matched:
            self._draw_game_over_overlay()
            self.particles.update_and_draw(self.screen)

    def _draw_game_over_overlay(self):
        if not self.animation_triggered:
            self.stars_earned = self._calculate_stars()
            self.particles.explode(self.width // 2, self.height // 2)
            self.animation_triggered = True

        # Fundo Transparente
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(210)  # Um pouco mais escuro para focar no modal
        overlay.fill((15, 15, 20))
        self.screen.blit(overlay, (0, 0))

        # Painel Central (Aumentei a altura para caber melhor)
        card_w, card_h = 480, 460
        cx, cy = self.width // 2, self.height // 2
        card_rect = pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (cx, cy)

        # Desenho do Painel
        pygame.draw.rect(self.screen, (50, 52, 64), card_rect, border_radius=20)
        pygame.draw.rect(
            self.screen, COLORS["accent"], card_rect, width=2, border_radius=20
        )

        # --- LAYOUT INTERNO DO CARD ---

        # 1. Título
        lbl = self.font_title.render("NÍVEL CONCLUÍDO!", True, COLORS["success"])
        self.screen.blit(lbl, lbl.get_rect(center=(cx, cy - 170)))

        # 2. Estrelas
        star_str = "⭐" * self.stars_earned
        base_stars = self.font_emoji.render("⭐" * 3, True, (80, 80, 90))
        gold_stars = self.font_emoji.render(star_str, True, (255, 215, 0))

        stars_y = cy - 110
        self.screen.blit(base_stars, base_stars.get_rect(center=(cx, stars_y)))
        if self.stars_earned > 0:
            # Pequeno ajuste de alinhamento visual se necessário
            self.screen.blit(gold_stars, gold_stars.get_rect(center=(cx, stars_y)))

        # 3. Pontuação Principal (Grande)
        score_lbl = self.font_stats.render("PONTUAÇÃO FINAL", True, (180, 180, 180))
        score_val = self.font_score_big.render(
            str(self.service.score), True, COLORS["text"]
        )

        self.screen.blit(score_lbl, score_lbl.get_rect(center=(cx, cy - 40)))
        self.screen.blit(score_val, score_val.get_rect(center=(cx, cy + 10)))

        # 4. Tempo (Menor)
        time_str = f"Tempo: {self.service.get_time_formatted()}"
        time_surf = self.font_msg.render(time_str, True, COLORS["accent"])
        self.screen.blit(time_surf, time_surf.get_rect(center=(cx, cy + 60)))

        # 5. Botões
        # Restart (Grande)
        self.btn_restart.rect.center = (cx, cy + 130)
        self.btn_restart.draw(self.screen)

        # Menu e Ranking (Lado a Lado abaixo)
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

    # --- Métodos Helpers (Mantidos Iguais) ---
    def _draw_result_stat(self, label, value, x, y):
        lbl_surf = self.font_stats.render(label, True, (180, 180, 180))
        val_surf = self.font_title.render(value, True, COLORS["text"])
        self.screen.blit(lbl_surf, lbl_surf.get_rect(center=(x, y - 20)))
        self.screen.blit(val_surf, val_surf.get_rect(center=(x, y + 20)))

    def _draw_stats(self):
        section_w = self.width // 3
        y_pos = 90
        mov_text = f"Movimentos: {self.service.moves}"
        self._draw_stat_box(mov_text, (section_w * 0 + section_w // 2, y_pos))
        score_text = f"Pontos: {self.service.score}"
        self._draw_stat_box(
            score_text,
            (section_w * 1 + section_w // 2, y_pos),
            COLORS["success"] if self.service.combo_streak > 1 else COLORS["text"],
        )
        time_text = f"Tempo: {self.service.get_time_formatted()}"
        self._draw_stat_box(time_text, (section_w * 2 + section_w // 2, y_pos))

    def _draw_stat_box(self, text, pos, color=COLORS["text"]):
        surf = self.font_stats.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=pos))

    def _get_card_rect(self, row, col):
        start_x = (self.width - self.grid_width) // 2
        start_y = DIMENSIONS["header_height"]
        x = start_x + col * (self.card_size + DIMENSIONS["gap"])
        y = start_y + row * (self.card_size + DIMENSIONS["gap"])
        return pygame.Rect(x, y, self.card_size, self.card_size)

    def _draw_single_card(self, card, rect, mouse_pos):
        bg_color = COLORS["card_back"]
        if not card.is_revealed and not card.is_matched and not self.waiting_to_hide:
            if rect.collidepoint(mouse_pos):
                bg_color = COLORS["card_back_hover"]
        if card.is_revealed:
            bg_color = COLORS["card_face"]
        if card.is_matched:
            bg_color = COLORS["success"]

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
                COLORS["card_border"],
                rect,
                width=2,
                border_radius=DIMENSIONS["border_radius"],
            )
            self._draw_dynamic_text(str(card.display_content), rect)
        else:
            q_surf = self.font_msg.render("?", True, (255, 255, 255, 50))
            self.screen.blit(q_surf, q_surf.get_rect(center=rect.center))

    def _draw_dynamic_text(self, text, rect):
        max_width = rect.width - 10
        font_size = 40
        while font_size > 12:
            font = pygame.font.SysFont(self.font_base_name, font_size)
            text_surf = font.render(text, True, COLORS["text_card"])
            if text_surf.get_width() <= max_width:
                break
            font_size -= 2
        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
