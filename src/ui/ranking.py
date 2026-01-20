# ARQUIVO: src/ui/ranking.py
import pygame

from src.ui.components import Button
from src.ui.styles import COLORS


class RankingUI:
    def __init__(self, repository):
        self.repository = repository

        # Configuração de Fontes
        try:
            self.font_title = pygame.font.SysFont("segoeui", 50, bold=True)
            self.font_row = pygame.font.SysFont("consolas", 20)
            self.font_header = pygame.font.SysFont("segoeui", 24, bold=True)
            self.font_btn = pygame.font.SysFont("segoeui", 20, bold=True)
        except:
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_row = pygame.font.SysFont("arial", 20)
            self.font_header = pygame.font.SysFont("arial", 24)
            self.font_btn = pygame.font.SysFont("arial", 20, bold=True)

        # Botão Voltar (inicializado, posição será ajustada no draw)
        self.btn_back = Button(
            x=0,
            y=0,
            w=200,
            h=50,
            text="Voltar ao Menu",
            font=self.font_btn,
            color=COLORS["card_back"],
            hover_color=COLORS["accent"],
        )

    def draw(self, screen):
        screen.fill(COLORS["background"])
        width = screen.get_width()
        height = screen.get_height()

        # Atualiza posição do botão para centralizar no rodapé
        self.btn_back.rect.centerx = width // 2
        self.btn_back.rect.bottom = height - 40

        # Título
        title = self.font_title.render("Top 10 Jogadores", True, COLORS["accent"])
        screen.blit(title, title.get_rect(center=(width // 2, 60)))

        # Cabeçalho da Tabela
        headers = ["Pos", "Nome", "Pontos", "Tema", "Nível", "Data"]

        # Colunas responsivas (porcentagem da largura)
        col_x = [
            width * 0.08,
            width * 0.20,
            width * 0.45,
            width * 0.60,
            width * 0.75,
            width * 0.90,
        ]

        # Desenha Cabeçalhos
        for i, h in enumerate(headers):
            surf = self.font_header.render(h, True, COLORS["success"])
            rect = surf.get_rect(center=(col_x[i], 130))
            screen.blit(surf, rect)

        # Linha divisória
        pygame.draw.line(screen, COLORS["text"], (40, 150), (width - 40, 150), 2)

        # Dados
        scores = self.repository.get_top_scores(10)
        start_y = 170
        row_height = 45

        for i, entry in enumerate(scores):
            # CÁLCULO DE Y (CORRIGIDO)
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
                    color = (255, 215, 0)  # Gold
                elif i == 1:
                    color = (192, 192, 192)  # Silver
                elif i == 2:
                    color = (205, 127, 50)  # Bronze

                surf = self.font_row.render(text, True, color)
                rect = surf.get_rect(center=(col_x[j], y))
                screen.blit(surf, rect)

        # Desenha Botão Voltar
        self.btn_back.draw(screen)

    def handle_click(self, event):
        if self.btn_back.check_click(event):
            return "BACK"
        return None
