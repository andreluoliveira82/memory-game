import pygame

from src.ui.styles import COLORS, DIMENSIONS


class MenuUI:
    def __init__(self):
        self.font_title = pygame.font.SysFont("segoeui", 60, bold=True)
        self.font_btn = pygame.font.SysFont("segoeui", 30)
        self.state = "THEME_SELECT"  # Novo controle interno

        # Botões de Temas
        self.theme_buttons = [
            {"text": "🐶 Animais", "value": "Animais", "rect": None},
            {"text": "🚀 Espaço", "value": "Espaço", "rect": None},
            {"text": "🧮 Matemática", "value": "Matemática", "rect": None},
            {"text": "🧪 Química", "value": "Química", "rect": None},  # Novo!
        ]

        # Botões de Dificuldade
        self.difficulty_buttons = [
            {"text": "🟢 Fácil (4x4)", "value": (4, 4), "rect": None},
            {"text": "🟡 Médio (6x4)", "value": (6, 4), "rect": None},
            {"text": "🔴 Difícil (6x6)", "value": (6, 6), "rect": None},
        ]

        self.current_buttons = self.theme_buttons  # Começa mostrando temas

    def draw(self, screen):
        screen.fill(COLORS["background"])

        title_text = (
            "Escolha o Tema" if self.state == "THEME_SELECT" else "Nível de Dificuldade"
        )
        title_surf = self.font_title.render(title_text, True, COLORS["accent"])
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        start_y = 200

        # Desenha a lista atual de botões
        for i, btn in enumerate(self.current_buttons):
            btn_rect = pygame.Rect(0, 0, 300, 60)
            btn_rect.center = (screen.get_width() // 2, start_y + i * 80)
            btn["rect"] = btn_rect

            color = COLORS["card_back"]
            if btn_rect.collidepoint(mouse_pos):
                color = COLORS["card_back_hover"]
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            pygame.draw.rect(
                screen, color, btn_rect, border_radius=DIMENSIONS["border_radius"]
            )
            pygame.draw.rect(
                screen,
                COLORS["accent"],
                btn_rect,
                width=2,
                border_radius=DIMENSIONS["border_radius"],
            )

            text_surf = self.font_btn.render(btn["text"], True, COLORS["text"])
            text_rect = text_surf.get_rect(center=btn_rect.center)
            screen.blit(text_surf, text_rect)

    def handle_click(self, pos):
        """Retorna (Tipo, Valor) ou None"""
        for btn in self.current_buttons:
            if btn["rect"].collidepoint(pos):
                return (self.state, btn["value"])
        return None

    def switch_to_difficulty(self):
        self.state = "DIFFICULTY_SELECT"
        self.current_buttons = self.difficulty_buttons

    def reset(self):
        self.state = "THEME_SELECT"
        self.current_buttons = self.theme_buttons
