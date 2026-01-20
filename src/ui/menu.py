# ARQUIVO: src/ui/menu.py
import pygame

from src.ui.styles import COLORS


class MenuUI:
    def __init__(self):
        self.font_title = pygame.font.SysFont("segoeui", 60, bold=True)
        self.font_icon = pygame.font.SysFont("segoeuiemoji", 60)
        self.font_btn = pygame.font.SysFont("segoeui", 22, bold=True)
        self.font_sub = pygame.font.SysFont("segoeui", 18)

        self.state = "THEME_SELECT"

        # --- BOTÕES DE TEMA ---
        self.theme_buttons = [
            {"text": "Animais", "icon": "🐶", "value": "Animais", "rect": None},
            {"text": "Espaço", "icon": "🚀", "value": "Espaço", "rect": None},
            {"text": "Matemática", "icon": "∑", "value": "Matemática", "rect": None},
            {"text": "Química", "icon": "🧪", "value": "Química", "rect": None},
            {"text": "Bandeiras", "icon": "🏴", "value": "Bandeiras", "rect": None},
        ]

        # --- BOTÕES DE DIFICULDADE (Melhorados) ---
        self.difficulty_buttons = [
            {
                "text": "Fácil",
                "sub": "Grade 4x4 - Normal",
                "value": (4, 4),
                "rect": None,
                "color": (80, 250, 123),
            },  # Verde
            {
                "text": "Médio",
                "sub": "Grade 6x4 - Desafio",
                "value": (6, 4),
                "rect": None,
                "color": (255, 184, 108),
            },  # Laranja
            {
                "text": "Difícil",
                "sub": "Grade 6x6 - Hardcore",
                "value": (6, 6),
                "rect": None,
                "color": (255, 85, 85),
            },  # Vermelho
        ]

        self.current_buttons = self.theme_buttons
        self.ranking_btn_rect = None
        self.back_btn_rect = None  # Botão voltar genérico

    def draw(self, screen):
        screen.fill(COLORS["background"])
        width, height = screen.get_width(), screen.get_height()

        # Título
        title_text = (
            "Escolha o Tema" if self.state == "THEME_SELECT" else "Nível de Dificuldade"
        )
        title_surf = self.font_title.render(title_text, True, COLORS["accent"])
        title_rect = title_surf.get_rect(center=(width // 2, 80))
        screen.blit(title_surf, title_rect)

        # Renderização condicional
        if self.state == "THEME_SELECT":
            self._draw_grid_menu(screen, width)
            self._draw_footer_buttons(screen, width, height, show_ranking=True)
        else:
            self._draw_list_menu(screen, width)
            self._draw_footer_buttons(
                screen, width, height, show_ranking=False, show_back=True
            )

    def _draw_grid_menu(self, screen, width):
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

            # Hover
            is_hover = btn_rect.collidepoint(mouse_pos)
            if is_hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            # Sombra e Fundo
            shadow = btn_rect.copy()
            shadow.move_ip(4, 4)
            pygame.draw.rect(screen, (30, 30, 30), shadow, border_radius=15)

            bg_color = COLORS["card_back_hover"] if is_hover else COLORS["card_back"]
            pygame.draw.rect(screen, bg_color, btn_rect, border_radius=15)
            pygame.draw.rect(
                screen, COLORS["accent"], btn_rect, width=2, border_radius=15
            )

            # Ícone e Texto
            icon_surf = self.font_icon.render(btn["icon"], True, COLORS["text"])
            screen.blit(
                icon_surf,
                icon_surf.get_rect(center=(btn_rect.centerx, btn_rect.centery - 15)),
            )

            text_surf = self.font_btn.render(btn["text"], True, COLORS["accent"])
            screen.blit(
                text_surf,
                text_surf.get_rect(center=(btn_rect.centerx, btn_rect.centery + 35)),
            )

    def _draw_list_menu(self, screen, width):
        # Design vertical limpo para dificuldade
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

            # Cor baseada na dificuldade (Verde/Laranja/Vermelho)
            base_color = btn.get("color", COLORS["card_back"])
            draw_color = (
                base_color if not is_hover else [min(c + 30, 255) for c in base_color]
            )

            # Desenho
            pygame.draw.rect(screen, draw_color, btn_rect, border_radius=12)
            pygame.draw.rect(
                screen, COLORS["text"], btn_rect, width=2, border_radius=12
            )

            # Texto Principal (Esquerda)
            txt_surf = self.font_title.render(
                btn["text"], True, (40, 40, 40)
            )  # Texto escuro
            # Reduz um pouco o tamanho
            txt_surf = pygame.transform.rotozoom(txt_surf, 0, 0.7)
            screen.blit(
                txt_surf,
                (btn_rect.x + 30, btn_rect.centery - txt_surf.get_height() // 2),
            )

            # Subtexto (Direita)
            sub_surf = self.font_sub.render(btn["sub"], True, (60, 60, 60))
            screen.blit(
                sub_surf,
                (
                    btn_rect.right - sub_surf.get_width() - 20,
                    btn_rect.centery - sub_surf.get_height() // 2,
                ),
            )

    def _draw_footer_buttons(
        self, screen, width, height, show_ranking=False, show_back=False
    ):
        mouse_pos = pygame.mouse.get_pos()

        if show_ranking:
            btn_rect = pygame.Rect(0, 0, 200, 50)
            btn_rect.center = (width // 2, height - 80)
            self.ranking_btn_rect = btn_rect

            is_hover = btn_rect.collidepoint(mouse_pos)
            color = COLORS["card_back_hover"] if is_hover else COLORS["card_back"]

            pygame.draw.rect(screen, color, btn_rect, border_radius=10)
            pygame.draw.rect(
                screen, COLORS["accent"], btn_rect, width=2, border_radius=10
            )

            lbl = self.font_btn.render("🏆 Ver Ranking", True, COLORS["accent"])
            screen.blit(lbl, lbl.get_rect(center=btn_rect.center))
        else:
            self.ranking_btn_rect = None

        if show_back:
            btn_rect = pygame.Rect(40, height - 70, 120, 40)
            self.back_btn_rect = btn_rect

            is_hover = btn_rect.collidepoint(mouse_pos)
            color = (60, 60, 60) if not is_hover else (80, 80, 80)

            pygame.draw.rect(screen, color, btn_rect, border_radius=8)
            lbl = self.font_btn.render("⬅ Voltar", True, COLORS["text"])
            screen.blit(lbl, lbl.get_rect(center=btn_rect.center))
        else:
            self.back_btn_rect = None

    def handle_click(self, pos):
        # 1. Checa botões da lista principal
        for btn in self.current_buttons:
            if btn["rect"] and btn["rect"].collidepoint(pos):
                return (self.state, btn["value"])

        # 2. Checa Ranking
        if self.ranking_btn_rect and self.ranking_btn_rect.collidepoint(pos):
            return ("ACTION", "RANKING")

        # 3. Checa Voltar
        if self.back_btn_rect and self.back_btn_rect.collidepoint(pos):
            return ("ACTION", "BACK")

        return None

    def switch_to_difficulty(self):
        self.state = "DIFFICULTY_SELECT"
        self.current_buttons = self.difficulty_buttons

    def reset(self):
        self.state = "THEME_SELECT"
        self.current_buttons = self.theme_buttons
        self.ranking_btn_rect = None
        self.back_btn_rect = None
