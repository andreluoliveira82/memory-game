# ARQUIVO: src/ui/ranking.py
import pygame

from src.ui.components import Button
from src.ui.styles import COLORS


class RankingUI:
    def __init__(self, repository):
        self.repository = repository

        try:
            self.font_title = pygame.font.SysFont("segoeui", 50, bold=True)
            self.font_row = pygame.font.SysFont("consolas", 18)
            self.font_header = pygame.font.SysFont("segoeui", 22, bold=True)
            self.font_btn = pygame.font.SysFont("segoeui", 16, bold=True)
        except:
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_row = pygame.font.SysFont("arial", 18)
            self.font_header = pygame.font.SysFont("arial", 22)
            self.font_btn = pygame.font.SysFont("arial", 16, bold=True)

        self.difficulty_filter = None
        self.theme_filter = None

        # Filtros Dificuldade
        self.diff_filters = [
            {"label": "Todos Níveis", "value": None},
            {"label": "Fácil", "value": "Fácil"},
            {"label": "Médio", "value": "Médio"},
            {"label": "Difícil", "value": "Difícil"},
        ]

        # Filtros Tema
        self.theme_filters = [
            {"label": "Todos Temas", "value": None},
            {"label": "Animais", "value": "Animais"},
            {"label": "Espaço", "value": "Espaço"},
            {"label": "Matemática", "value": "Matemática"},
            {"label": "Química", "value": "Química"},
            {"label": "Bandeiras", "value": "Bandeiras"},
        ]

        self.btn_back = Button(
            0,
            0,
            200,
            40,
            "Voltar ao Menu",
            self.font_btn,
            COLORS["card_back"],
            COLORS["accent"],
        )

    def draw(self, screen):
        screen.fill(COLORS["background"])
        width, height = screen.get_width(), screen.get_height()

        title = self.font_title.render("Ranking Global", True, COLORS["accent"])
        screen.blit(title, title.get_rect(center=(width // 2, 40)))

        # Desenhar Filtros
        self._draw_filter_row(
            screen, self.diff_filters, width, y=90, selected_val=self.difficulty_filter
        )
        self._draw_filter_row(
            screen, self.theme_filters, width, y=135, selected_val=self.theme_filter
        )

        # Cabeçalho
        headers = ["Pos", "Nome", "Pontos", "Tema", "Nível", "Data"]
        col_x = [width * p for p in [0.08, 0.20, 0.45, 0.60, 0.75, 0.90]]

        header_y = 180
        for i, h in enumerate(headers):
            surf = self.font_header.render(h, True, COLORS["success"])
            screen.blit(surf, surf.get_rect(center=(col_x[i], header_y)))

        pygame.draw.line(
            screen, COLORS["text"], (40, header_y + 20), (width - 40, header_y + 20), 2
        )

        # Busca Dados
        scores = self.repository.get_top_scores(
            10, difficulty_filter=self.difficulty_filter, theme_filter=self.theme_filter
        )

        start_y = header_y + 40
        row_height = 35

        if not scores:
            msg = self.font_header.render(
                "Nenhum registro encontrado.", True, (100, 100, 100)
            )
            screen.blit(msg, msg.get_rect(center=(width // 2, start_y + 50)))

        for i, entry in enumerate(scores):
            y = start_y + (i * row_height)
            row_data = [
                str(i + 1),
                entry["name"][:12],
                str(entry["score"]),
                entry["theme"][:9],
                entry["difficulty"][:3],
                entry.get("date", "--/--"),
            ]

            for j, text in enumerate(row_data):
                color = COLORS["text"]
                if i == 0:
                    color = (255, 215, 0)
                elif i == 1:
                    color = (192, 192, 192)
                elif i == 2:
                    color = (205, 127, 50)

                surf = self.font_row.render(text, True, color)
                screen.blit(surf, surf.get_rect(center=(col_x[j], y)))

        # Rodapé
        self.btn_back.rect.centerx = width // 2
        self.btn_back.rect.bottom = height - 30
        self.btn_back.draw(screen)

    def _draw_filter_row(self, screen, filters, width, y, selected_val):
        btn_w, btn_h = 110, 30
        gap = 8
        total_w = (len(filters) * btn_w) + ((len(filters) - 1) * gap)
        start_x = (width - total_w) // 2
        mouse_pos = pygame.mouse.get_pos()

        for i, f in enumerate(filters):
            rect = pygame.Rect(start_x + i * (btn_w + gap), y, btn_w, btn_h)
            f["rect"] = rect

            is_selected = selected_val == f["value"]
            is_hover = rect.collidepoint(mouse_pos)

            if is_selected:
                color = COLORS["accent"]
                text_color = COLORS["background"]
            else:
                color = COLORS["card_back_hover"] if is_hover else COLORS["card_back"]
                text_color = COLORS["text"]

            if is_hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            pygame.draw.rect(screen, color, rect, border_radius=6)
            if is_selected:
                pygame.draw.rect(
                    screen, (255, 255, 255), rect, width=2, border_radius=6
                )

            font = self.font_btn
            lbl = font.render(f["label"], True, text_color)
            if lbl.get_width() > btn_w - 4:
                lbl = pygame.transform.scale(lbl, (btn_w - 10, lbl.get_height()))

            screen.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_click(self, event):
        if self.btn_back.check_click(event):
            return "BACK"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for f in self.diff_filters:
                if f["rect"] and f["rect"].collidepoint(event.pos):
                    self.difficulty_filter = f["value"]
                    return "FILTER_CHANGED"

            for f in self.theme_filters:
                if f["rect"] and f["rect"].collidepoint(event.pos):
                    self.theme_filter = f["value"]
                    return "FILTER_CHANGED"
        return None
