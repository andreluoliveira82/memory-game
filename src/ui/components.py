# src/ui/components.py

import pygame

from src.ui.styles import COLORS


class InputBox:
    """Caixa de texto simples para entrada de dados no Pygame."""

    def __init__(self, x, y, w, h, font, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = COLORS["card_back"]
        self.color_active = COLORS["accent"]
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Se clicou na caixa, ativa. Senão, desativa.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Retorna o texto ao dar Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limita a 12 caracteres
                    if len(self.text) < 12:
                        self.text += event.unicode

                # Re-renderiza o texto
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        # Desenha a caixa
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        # Centraliza o texto verticalmente
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)
