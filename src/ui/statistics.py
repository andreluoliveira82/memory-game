# ARQUIVO: src/ui/statistics.py
import pygame

from src.ui.components import Button
from src.ui.styles import COLORS


class StatisticsUI:
    def __init__(self, repository):
        self.repository = repository

        try:
            self.font_title = pygame.font.SysFont("segoeui", 48, bold=True)
            self.font_big = pygame.font.SysFont("segoeui", 36, bold=True)
            self.font_label = pygame.font.SysFont("segoeui", 18)
            self.font_btn = pygame.font.SysFont("segoeui", 20, bold=True)
        except:
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_big = pygame.font.SysFont("arial", 30, bold=True)
            self.font_label = pygame.font.SysFont("arial", 16)
            self.font_btn = pygame.font.SysFont("arial", 20, bold=True)

        self.btn_back = Button(
            0,
            0,
            200,
            45,
            "Voltar ao Menu",
            self.font_btn,
            COLORS["card_back"],
            COLORS["accent"],
        )

    def draw(self, screen):
        screen.fill(COLORS["background"])
        width, height = screen.get_width(), screen.get_height()

        stats = self.repository.get_statistics()
        if not stats or stats["total_games"] == 0:
            self._draw_empty_state(screen, width, height)
            return

        title = self.font_title.render("Dashboard do Jogador", True, COLORS["accent"])
        screen.blit(title, title.get_rect(center=(width // 2, 50)))

        # Cards
        self._draw_card(
            screen,
            100,
            100,
            200,
            100,
            "Total de Jogos",
            str(stats["total_games"]),
            COLORS["success"],
        )
        self._draw_card(
            screen,
            320,
            100,
            200,
            100,
            "Maior Pontuação",
            str(stats["best_score"]),
            (255, 215, 0),
        )
        self._draw_card(
            screen,
            540,
            100,
            220,
            100,
            "Tema Favorito",
            str(stats["favorite_theme"]),
            COLORS["accent"],
        )

        # Gráfico
        self._draw_bar_chart(screen, stats["themes_count"], 100, 280, width - 200, 300)

        # Rodapé
        self.btn_back.rect.centerx = width // 2
        self.btn_back.rect.bottom = height - 30
        self.btn_back.draw(screen)

    def _draw_card(self, screen, x, y, w, h, title, value, color):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, (50, 52, 64), rect, border_radius=15)
        pygame.draw.rect(screen, color, rect, width=2, border_radius=15)

        title_surf = self.font_label.render(title, True, (200, 200, 200))
        val_surf = self.font_big.render(value, True, color)

        screen.blit(
            title_surf, title_surf.get_rect(center=(rect.centerx, rect.centery - 15))
        )
        screen.blit(
            val_surf, val_surf.get_rect(center=(rect.centerx, rect.centery + 15))
        )

    def _draw_bar_chart(self, screen, data_dict, x, y, w, h):
        if not data_dict:
            return

        lbl = self.font_btn.render("Partidas por Tema", True, COLORS["text"])
        screen.blit(lbl, (x, y - 30))

        # Eixos
        pygame.draw.line(screen, (150, 150, 150), (x, y + h), (x + w, y + h), 2)
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x, y + h), 2)

        count = len(data_dict)
        bar_width = min(60, (w / count) * 0.6)
        gap = (w / count) * 0.4
        max_val = max(data_dict.values()) if data_dict else 1

        for i, (key, val) in enumerate(data_dict.items()):
            bar_h = (val / max_val) * (h - 40)
            bar_x = x + (gap / 2) + i * (bar_width + gap)
            bar_y = y + h - bar_h

            bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_h)

            color_factor = min(255, int(val * 50))
            color = (100, color_factor, 200)

            pygame.draw.rect(screen, color, bar_rect, border_radius=5)

            val_txt = self.font_label.render(str(val), True, COLORS["text"])
            screen.blit(
                val_txt, val_txt.get_rect(center=(bar_rect.centerx, bar_rect.top - 10))
            )

            key_txt = self.font_label.render(key[:6], True, (180, 180, 180))
            screen.blit(
                key_txt, key_txt.get_rect(center=(bar_rect.centerx, y + h + 15))
            )

    def _draw_empty_state(self, screen, w, h):
        msg = self.font_big.render(
            "Sem dados ainda. Jogue uma partida!", True, COLORS["text"]
        )
        screen.blit(msg, msg.get_rect(center=(w // 2, h // 2)))
        self.btn_back.rect.centerx = w // 2
        self.btn_back.rect.bottom = h - 50
        self.btn_back.draw(screen)

    def handle_click(self, event):
        if self.btn_back.check_click(event):
            return "BACK"
        return None
