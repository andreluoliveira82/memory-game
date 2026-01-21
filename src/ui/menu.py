# ARQUIVO: src/ui/menu.py
"""
Menu principal do jogo.

Permite seleção de tema, dificuldade e acesso a outras telas
(ranking, estatísticas, configurações).
"""

import pygame

import src.ui.styles as styles


class MenuUI:
    """
    Interface do menu principal.

    Gerencia a seleção de tema de jogo e dificuldade, além de
    fornecer acesso às telas secundárias.
    """

    def __init__(self):
        """Inicializa o menu."""
        self.font_title = pygame.font.SysFont("segoeui", 60, bold=True)
        self.font_icon = pygame.font.SysFont("segoeuiemoji", 60)
        self.font_btn = pygame.font.SysFont("segoeui", 18, bold=True)
        self.font_sub = pygame.font.SysFont("segoeui", 18)

        self.state = "THEME_SELECT"

        # Botões de Tema
        self.theme_buttons = [
            {"text": "Animais", "icon": "🐶", "value": "Animais", "rect": None},
            {"text": "Espaço", "icon": "🚀", "value": "Espaço", "rect": None},
            {"text": "Matemática", "icon": "∑", "value": "Matemática", "rect": None},
            {"text": "Química", "icon": "🧪", "value": "Química", "rect": None},
            {"text": "Bandeiras", "icon": "🏴", "value": "Bandeiras", "rect": None},
        ]

        # Botões de Dificuldade
        self.difficulty_buttons = [
            {
                "text": "Fácil",
                "sub": "Grade 4x4 - Normal",
                "value": (4, 4),
                "rect": None,
                "color": (80, 250, 123),
            },
            {
                "text": "Médio",
                "sub": "Grade 6x4 - Desafio",
                "value": (6, 4),
                "rect": None,
                "color": (255, 184, 108),
            },
            {
                "text": "Difícil",
                "sub": "Grade 6x6 - Hardcore",
                "value": (6, 6),
                "rect": None,
                "color": (255, 85, 85),
            },
        ]

        self.current_buttons = self.theme_buttons

        # Áreas clicáveis do rodapé
        self.ranking_btn_rect = None
        self.stats_btn_rect = None
        self.settings_btn_rect = None
        self.back_btn_rect = None

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renderiza o menu.

        Args:
            screen: Superfície do Pygame
        """
        screen.fill(styles.COLORS["background"])
        width, height = screen.get_width(), screen.get_height()

        # Título
        title_text = (
            "Escolha o Tema" if self.state == "THEME_SELECT" else "Nível de Dificuldade"
        )
        title_surf = self.font_title.render(title_text, True, styles.COLORS["accent"])
        title_rect = title_surf.get_rect(center=(width // 2, 80))
        screen.blit(title_surf, title_rect)

        # Renderização condicional
        if self.state == "THEME_SELECT":
            self._draw_grid_menu(screen, width)
            self._draw_footer_buttons(screen, width, height, show_main_actions=True)
        else:
            self._draw_list_menu(screen, width)
            self._draw_footer_buttons(
                screen, width, height, show_main_actions=False, show_back=True
            )

    def _draw_grid_menu(self, screen: pygame.Surface, width: int) -> None:
        """Desenha menu em grade (para temas)."""
        cols = 3
        tile_size = 140
        gap = 20
        total_w = (cols * tile_size) + ((cols - 1) * gap)
        start_x = (width - total_w) // 2
        start_y = 180

        mouse_pos = pygame.mouse.get_pos()

        for i, btn in enumerate(self.theme_buttons):
            row = i // cols
            col = i % cols
            x = start_x + col * (tile_size + gap)
            y = start_y + row * (tile_size + gap)

            btn_rect = pygame.Rect(x, y, tile_size, tile_size)
            btn["rect"] = btn_rect

            is_hover = btn_rect.collidepoint(mouse_pos)
            if is_hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            shadow = btn_rect.copy()
            shadow.move_ip(4, 4)
            pygame.draw.rect(screen, (30, 30, 30), shadow, border_radius=15)

            bg_color = (
                styles.COLORS["card_back_hover"]
                if is_hover
                else styles.COLORS["card_back"]
            )
            pygame.draw.rect(screen, bg_color, btn_rect, border_radius=15)
            pygame.draw.rect(
                screen, styles.COLORS["accent"], btn_rect, width=2, border_radius=15
            )

            icon_surf = self.font_icon.render(btn["icon"], True, styles.COLORS["text"])
            screen.blit(
                icon_surf,
                icon_surf.get_rect(center=(btn_rect.centerx, btn_rect.centery - 15)),
            )

            text_surf = self.font_btn.render(btn["text"], True, styles.COLORS["accent"])
            screen.blit(
                text_surf,
                text_surf.get_rect(center=(btn_rect.centerx, btn_rect.centery + 35)),
            )

    def _draw_list_menu(self, screen: pygame.Surface, width: int) -> None:
        """Desenha menu em lista (para dificuldades)."""
        start_y = 180
        btn_w, btn_h = 350, 80
        gap = 25
        mouse_pos = pygame.mouse.get_pos()

        for i, btn in enumerate(self.difficulty_buttons):
            btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
            btn_rect.center = (width // 2, start_y + i * (btn_h + gap))
            btn["rect"] = btn_rect

            is_hover = btn_rect.collidepoint(mouse_pos)
            if is_hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            base_color = btn.get("color", styles.COLORS["card_back"])
            draw_color = (
                base_color if not is_hover else [min(c + 30, 255) for c in base_color]
            )

            pygame.draw.rect(screen, draw_color, btn_rect, border_radius=12)
            pygame.draw.rect(
                screen, styles.COLORS["text"], btn_rect, width=2, border_radius=12
            )

            txt_surf = self.font_title.render(btn["text"], True, (40, 40, 40))
            txt_surf = pygame.transform.rotozoom(txt_surf, 0, 0.7)
            screen.blit(
                txt_surf,
                (btn_rect.x + 30, btn_rect.centery - txt_surf.get_height() // 2),
            )

            sub_surf = self.font_sub.render(btn["sub"], True, (60, 60, 60))
            screen.blit(
                sub_surf,
                (
                    btn_rect.right - sub_surf.get_width() - 20,
                    btn_rect.centery - sub_surf.get_height() // 2,
                ),
            )

    def _draw_footer_buttons(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
        show_main_actions: bool = False,
        show_back: bool = False,
    ) -> None:
        """Desenha botões do rodapé."""
        mouse_pos = pygame.mouse.get_pos()

        if show_main_actions:
            btn_w = 130
            gap = 12
            total_w = 3 * btn_w + 2 * gap
            start_x = (width - total_w) // 2
            y = height - 70

            r_rect = pygame.Rect(start_x, y, btn_w, 45)
            self.ranking_btn_rect = r_rect
            self._draw_footer_btn(screen, r_rect, "Ranking", mouse_pos, "🏆")

            s_rect = pygame.Rect(start_x + btn_w + gap, y, btn_w, 45)
            self.stats_btn_rect = s_rect
            self._draw_footer_btn(screen, s_rect, "Stats", mouse_pos, "📊")

            cfg_rect = pygame.Rect(start_x + 2 * (btn_w + gap), y, btn_w, 45)
            self.settings_btn_rect = cfg_rect
            self._draw_footer_btn(screen, cfg_rect, "Config", mouse_pos, "⚙️")
        else:
            self.ranking_btn_rect = None
            self.stats_btn_rect = None
            self.settings_btn_rect = None

        if show_back:
            btn_rect = pygame.Rect(40, height - 70, 120, 40)
            self.back_btn_rect = btn_rect

            is_hover = btn_rect.collidepoint(mouse_pos)
            color = (60, 60, 60) if not is_hover else (80, 80, 80)
            if is_hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            pygame.draw.rect(screen, color, btn_rect, border_radius=8)
            lbl = self.font_btn.render("← Voltar", True, styles.COLORS["text"])
            screen.blit(lbl, lbl.get_rect(center=btn_rect.center))
        else:
            self.back_btn_rect = None

    def _draw_footer_btn(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        text: str,
        mouse_pos: tuple,
        emoji: str = "",
    ) -> None:
        """Desenha um botão do rodapé."""
        is_hover = rect.collidepoint(mouse_pos)
        color = (
            styles.COLORS["card_back_hover"] if is_hover else styles.COLORS["card_back"]
        )
        if is_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(
            screen, styles.COLORS["accent"], rect, width=2, border_radius=10
        )

        # Renderiza apenas texto (sem emoji problemático)
        lbl = self.font_btn.render(text, True, styles.COLORS["accent"])
        screen.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_click(self, pos: tuple) -> tuple | None:
        """Processa clique no menu."""
        for btn in self.current_buttons:
            if btn["rect"] and btn["rect"].collidepoint(pos):
                return (self.state, btn["value"])

        if self.ranking_btn_rect and self.ranking_btn_rect.collidepoint(pos):
            return ("ACTION", "RANKING")

        if self.stats_btn_rect and self.stats_btn_rect.collidepoint(pos):
            return ("ACTION", "STATS")

        if self.settings_btn_rect and self.settings_btn_rect.collidepoint(pos):
            return ("ACTION", "SETTINGS")

        if self.back_btn_rect and self.back_btn_rect.collidepoint(pos):
            return ("ACTION", "BACK")

        return None

    def switch_to_difficulty(self) -> None:
        """Muda para tela de seleção de dificuldade."""
        self.state = "DIFFICULTY_SELECT"
        self.current_buttons = self.difficulty_buttons

    def reset(self) -> None:
        """Reseta o menu para o estado inicial."""
        self.state = "THEME_SELECT"
        self.current_buttons = self.theme_buttons
        self.ranking_btn_rect = None
        self.stats_btn_rect = None
        self.settings_btn_rect = None
        self.back_btn_rect = None
