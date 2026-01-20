# ARQUIVO: src/ui/settings.py
"""
Tela de configurações do jogo.

Permite ao jogador customizar tema visual, volume de som e
outras preferências.
"""

import pygame

from src.ui.components import Button
from src.ui.styles import COLORS, get_available_themes, set_theme


class SettingsUI:
    """
    Interface de configurações do jogo.

    Permite trocar tema visual, ajustar volume e outras preferências.
    """

    def __init__(self):
        """Inicializa a tela de configurações."""
        self._init_fonts()
        self.theme_buttons = []
        self.current_theme_id = "dracula"
        self._create_theme_buttons()

        self.btn_back = Button(
            0,
            0,
            200,
            45,
            "← Voltar",
            self.font_btn,
            COLORS["card_back"],
            COLORS["accent"],
        )

    def _init_fonts(self) -> None:
        """Inicializa fontes com fallback."""
        try:
            self.font_title = pygame.font.SysFont("segoeui", 50, bold=True)
            self.font_subtitle = pygame.font.SysFont("segoeui", 24)
            self.font_btn = pygame.font.SysFont("segoeui", 18, bold=True)
        except Exception:
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_subtitle = pygame.font.SysFont("arial", 20)
            self.font_btn = pygame.font.SysFont("arial", 18, bold=True)

    def _create_theme_buttons(self) -> None:
        """Cria botões para cada tema disponível."""
        themes = get_available_themes()
        self.theme_buttons = [
            {
                "id": theme["id"],
                "name": theme["name"],
                "rect": None,
            }
            for theme in themes
        ]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renderiza a tela de configurações.

        Args:
            screen: Superfície do Pygame
        """
        screen.fill(COLORS["background"])
        width, height = screen.get_width(), screen.get_height()

        # Título
        title = self.font_title.render("⚙️ Configurações", True, COLORS["accent"])
        screen.blit(title, title.get_rect(center=(width // 2, 50)))

        # Seção de Temas
        self._draw_theme_section(screen, width)

        # Botão Voltar
        self.btn_back.rect.topleft = (40, height - 80)
        self.btn_back.draw(screen)

    def _draw_theme_section(self, screen: pygame.Surface, width: int) -> None:
        """
        Desenha a seção de seleção de temas.

        Args:
            screen: Superfície do Pygame
            width: Largura da tela
        """
        # Subtítulo
        subtitle = self.font_subtitle.render(
            "Escolha o Tema Visual:", True, COLORS["text"]
        )
        screen.blit(subtitle, subtitle.get_rect(center=(width // 2, 120)))

        # Grid de temas (2 colunas)
        cols = 2
        btn_w, btn_h = 300, 60
        gap = 20
        start_y = 170

        mouse_pos = pygame.mouse.get_pos()

        for i, theme in enumerate(self.theme_buttons):
            row = i // cols
            col = i % cols

            x = (
                (width // 2)
                - (cols * btn_w + (cols - 1) * gap) // 2
                + col * (btn_w + gap)
            )
            y = start_y + row * (btn_h + gap)

            rect = pygame.Rect(x, y, btn_w, btn_h)
            theme["rect"] = rect

            is_selected = theme["id"] == self.current_theme_id
            is_hover = rect.collidepoint(mouse_pos)

            # Cor do botão
            if is_selected:
                color = COLORS["success"]
                text_color = (40, 40, 40)
            elif is_hover:
                color = COLORS["card_back_hover"]
                text_color = COLORS["text"]
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                color = COLORS["card_back"]
                text_color = COLORS["text"]

            # Desenha botão
            pygame.draw.rect(screen, color, rect, border_radius=10)

            # Borda especial se selecionado
            border_width = 3 if is_selected else 2
            border_color = COLORS["accent"] if is_selected else COLORS["text"]
            pygame.draw.rect(
                screen, border_color, rect, width=border_width, border_radius=10
            )

            # Texto
            text = self.font_btn.render(theme["name"], True, text_color)
            screen.blit(text, text.get_rect(center=rect.center))

        # Preview do tema selecionado
        self._draw_theme_preview(
            screen,
            width,
            start_y + ((len(self.theme_buttons) + 1) // 2) * (btn_h + gap) + 40,
        )

    def _draw_theme_preview(self, screen: pygame.Surface, width: int, y: int) -> None:
        """
        Desenha um preview do tema selecionado.

        Args:
            screen: Superfície do Pygame
            width: Largura da tela
            y: Posição Y inicial
        """
        # Caixa de preview
        preview_w, preview_h = 400, 120
        preview_rect = pygame.Rect(0, 0, preview_w, preview_h)
        preview_rect.center = (width // 2, y + preview_h // 2)

        # Fundo
        pygame.draw.rect(screen, COLORS["card_back"], preview_rect, border_radius=15)
        pygame.draw.rect(
            screen, COLORS["accent"], preview_rect, width=2, border_radius=15
        )

        # Texto de exemplo
        label = self.font_subtitle.render("Preview do Tema:", True, COLORS["text"])
        screen.blit(
            label, label.get_rect(center=(preview_rect.centerx, preview_rect.top - 25))
        )

        # Mini cards de exemplo
        card_size = 50
        gap = 15
        cards_y = preview_rect.centery

        # Card revelada
        card1_rect = pygame.Rect(0, 0, card_size, card_size)
        card1_rect.center = (preview_rect.centerx - card_size - gap // 2, cards_y)
        pygame.draw.rect(screen, COLORS["card_face"], card1_rect, border_radius=8)
        pygame.draw.rect(
            screen, COLORS["card_border"], card1_rect, width=2, border_radius=8
        )

        emoji = self.font_btn.render("🎮", True, COLORS["text_card"])
        screen.blit(emoji, emoji.get_rect(center=card1_rect.center))

        # Card escondida
        card2_rect = pygame.Rect(0, 0, card_size, card_size)
        card2_rect.center = (preview_rect.centerx + card_size // 2 + gap // 2, cards_y)
        pygame.draw.rect(screen, COLORS["card_back"], card2_rect, border_radius=8)

        question = self.font_btn.render("?", True, (255, 255, 255, 100))
        screen.blit(question, question.get_rect(center=card2_rect.center))

        # Card matched
        card3_rect = pygame.Rect(0, 0, card_size, card_size)
        card3_rect.center = (preview_rect.centerx + card_size * 1.5 + gap, cards_y)
        pygame.draw.rect(screen, COLORS["success"], card3_rect, border_radius=8)

        check = self.font_btn.render("✓", True, (255, 255, 255))
        screen.blit(check, check.get_rect(center=card3_rect.center))

    def handle_click(self, event: pygame.event.Event) -> str | None:
        """
        Processa cliques na tela de configurações.

        Args:
            event: Evento do Pygame

        Returns:
            Ação a executar ou None
        """
        if self.btn_back.check_click(event):
            return "BACK"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for theme in self.theme_buttons:
                if theme["rect"] and theme["rect"].collidepoint(event.pos):
                    # Troca o tema
                    self.current_theme_id = theme["id"]
                    set_theme(theme["id"])
                    return "THEME_CHANGED"

        return None

    def get_current_theme(self) -> str:
        """
        Retorna o ID do tema atual.

        Returns:
            ID do tema ativo
        """
        return self.current_theme_id
