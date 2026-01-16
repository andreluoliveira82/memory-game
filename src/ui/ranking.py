import pygame

from src.ui.styles import COLORS


class RankingUI:
    def __init__(self, repository):
        self.repository = repository
        try:
            self.font_title = pygame.font.SysFont("segoeui", 50, bold=True)
            self.font_row = pygame.font.SysFont(
                "consolas", 24
            )  # Consolas alinha melhor números
            self.font_header = pygame.font.SysFont("segoeui", 28, bold=True)
        except Exception:
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_row = pygame.font.SysFont("arial", 20)
            self.font_header = pygame.font.SysFont("arial", 24)

    def draw(self, screen):
        screen.fill(COLORS["background"])
        width = screen.get_width()

        # Título
        title = self.font_title.render("Top 10 Jogadores", True, COLORS["accent"])
        screen.blit(title, title.get_rect(center=(width // 2, 50)))

        # Cabeçalho da Tabela
        headers = ["Pos", "Nome", "Pontos", "Tema", "Nível"]
        # Posições X fixas para alinhar colunas (Design de Tabela)
        col_x = [width * 0.1, width * 0.2, width * 0.5, width * 0.7, width * 0.85]

        for i, h in enumerate(headers):
            surf = self.font_header.render(h, True, COLORS["success"])
            screen.blit(surf, (col_x[i], 120))

        pygame.draw.line(screen, COLORS["text"], (50, 150), (width - 50, 150), 2)

        # Dados
        scores = self.repository.get_top_scores(10)
        start_y = 170

        for i, entry in enumerate(scores):
            y = start_y + (i * 40)

            # Formatação dos dados
            row_data = [
                str(i + 1),
                entry["name"][:12],  # Limita tamanho do nome
                str(entry["score"]),
                entry["theme"],
                entry["difficulty"],
            ]

            for j, text in enumerate(row_data):
                color = COLORS["text"]
                if i == 0:
                    color = (255, 215, 0)  # Ouro para o 1º lugar

                surf = self.font_row.render(text, True, color)
                screen.blit(surf, (col_x[j], y))

        # Footer
        hint = pygame.font.SysFont("arial", 20).render(
            "Pressione ESC para voltar ao Menu", True, COLORS["accent"]
        )
        screen.blit(hint, hint.get_rect(center=(width // 2, screen.get_height() - 50)))
