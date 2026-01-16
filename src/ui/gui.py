import pygame

from src.services.game_service import GameService
from src.ui.styles import COLORS, DIMENSIONS


class GraphicUI:
    # Adicione card_size como argumento opcional
    def __init__(self, service: GameService, card_size: int = None):
        self.service = service
        self.screen = pygame.display.get_surface()

        # Se não passar tamanho, usa o padrão do styles.py
        self.card_size = card_size if card_size else DIMENSIONS["card_size"]

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # --- USA self.card_size AGORA ---
        self.grid_width = (service.board.cols * self.card_size) + (
            (service.board.cols - 1) * DIMENSIONS["gap"]
        )
        # Fontes
        try:
            # Fonte Emoji (Segoe UI Emoji no Windows)
            self.font_base_name = "segoeuiemoji"
            self.font_title = pygame.font.SysFont("segoeui", 48, bold=True)
            self.font_stats = pygame.font.SysFont(
                "consolas", 22
            )  # Fonte monoespaçada para números
            self.font_msg = pygame.font.SysFont("segoeui", 28)
        except Exception:
            self.font_base_name = "arial"
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_stats = pygame.font.SysFont("arial", 20)
            self.font_msg = pygame.font.SysFont("arial", 24)

        self.message = "Encontre os pares!"

        # Controle de Animação
        self.waiting_to_hide = False
        self.hide_timestamp = 0
        self.cards_to_hide = None
        self.saved = False

    def update(self):
        # Lógica de delay ao errar
        if self.waiting_to_hide:
            if pygame.time.get_ticks() - self.hide_timestamp > 1000:
                self.service.hide_cards(*self.cards_to_hide)
                self.waiting_to_hide = False
                self.cards_to_hide = None
                self.message = "Tente novamente!"

        if self.service.board.all_matched:
            self.message = "VENCEDOR! ESC para Sair."

    def handle_click(self, pos):
        if self.waiting_to_hide or self.service.board.all_matched:
            return

        for r in range(self.service.board.rows):
            for c in range(self.service.board.cols):
                rect = self._get_card_rect(r, c)
                if rect.collidepoint(pos):
                    self._process_pick(r, c)
                    break

    def _process_pick(self, r, c):
        first_pos = self.service.first_selected_pos
        current_pos = (r, c)
        result = self.service.pick_card(r, c)

        if result == "MATCH":
            combo = self.service.combo_streak
            if combo > 1:
                self.message = f"COMBO x{combo}! (+{100 * combo})"
            else:
                self.message = "Boa! Um par!"
        elif result == "NO_MATCH":
            self.message = "Ops... errou."
            self.waiting_to_hide = True
            self.hide_timestamp = pygame.time.get_ticks()
            self.cards_to_hide = (first_pos, current_pos)
        elif result == "FIRST_PICK":
            self.message = "Escolha o par..."

    def draw(self):
        self.screen.fill(COLORS["background"])
        mouse_pos = pygame.mouse.get_pos()

        # --- 1. CABEÇALHO ORGANIZADO ---
        # Linha 1: Título Centralizado
        title_surf = self.font_title.render("Memory Game", True, COLORS["accent"])
        title_rect = title_surf.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title_surf, title_rect)

        # Linha 2: Estatísticas (Espaçadas igualmente)
        # Vamos dividir a largura em 3 seções virtuais
        section_w = self.width // 3
        y_pos = 90

        # Movimentos (Esquerda)
        mov_text = f"Movimentos: {self.service.moves}"
        self._draw_stat_box(mov_text, (section_w * 0 + section_w // 2, y_pos))

        # Pontos (Centro - Destaque se tiver combo)
        color_score = (
            COLORS["success"] if self.service.combo_streak > 1 else COLORS["text"]
        )
        score_text = f"Pontos: {self.service.score}"
        self._draw_stat_box(
            score_text, (section_w * 1 + section_w // 2, y_pos), color=color_score
        )

        # Tempo (Direita)
        time_text = f"Tempo: {self.service.get_time_formatted()}"
        self._draw_stat_box(time_text, (section_w * 2 + section_w // 2, y_pos))

        # --- 2. GRID DE CARTAS ---
        for r in range(self.service.board.rows):
            for c in range(self.service.board.cols):
                card = self.service.board.get_card(r, c)
                rect = self._get_card_rect(r, c)
                self._draw_single_card(card, rect, mouse_pos)

        # --- 3. RODAPÉ ---
        msg_surf = self.font_msg.render(self.message, True, COLORS["accent"])
        msg_rect = msg_surf.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(msg_surf, msg_rect)

    def _draw_stat_box(self, text, center_pos, color=COLORS["text"]):
        """Helper para desenhar status centralizado"""
        surf = self.font_stats.render(text, True, color)
        rect = surf.get_rect(center=center_pos)
        self.screen.blit(surf, rect)

    def _get_card_rect(self, row, col):
        start_x = (self.width - self.grid_width) // 2
        start_y = DIMENSIONS["header_height"]

        # --- USA self.card_size AQUI TAMBÉM ---
        x = start_x + col * (self.card_size + DIMENSIONS["gap"])
        y = start_y + row * (self.card_size + DIMENSIONS["gap"])

        # Retorna retângulo com tamanho dinâmico
        return pygame.Rect(x, y, self.card_size, self.card_size)

    def _draw_single_card(self, card, rect, mouse_pos):
        bg_color = COLORS["card_back"]

        # Hover logic
        if not card.is_revealed and not card.is_matched and not self.waiting_to_hide:
            if rect.collidepoint(mouse_pos):
                bg_color = COLORS["card_back_hover"]

        if card.is_revealed:
            bg_color = COLORS["card_face"]
        if card.is_matched:
            bg_color = COLORS["success"]

        # Desenho Sombra e Corpo
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

            # --- TEXTO DINÂMICO ---
            self._draw_dynamic_text(str(card.display_content), rect)
        else:
            # ? no verso
            q_surf = self.font_msg.render("?", True, (255, 255, 255, 50))
            q_rect = q_surf.get_rect(center=rect.center)
            self.screen.blit(q_surf, q_rect)

    def _draw_dynamic_text(self, text, rect):
        """Reduz o tamanho da fonte até caber no cartão (Magic Scaling)."""
        max_width = rect.width - 10  # Margem interna de 5px
        font_size = 40  # Começa grande

        # Loop para encontrar o maior tamanho possível
        while font_size > 12:
            font = pygame.font.SysFont(self.font_base_name, font_size)
            text_surf = font.render(text, True, COLORS["text_card"])
            if text_surf.get_width() <= max_width:
                break  # Cabe!
            font_size -= 2  # Tenta menor

        # Renderiza centralizado
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
