# src/ui/components.py

import pygame
import random

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


class Button:
    def __init__(
        self,
        x,
        y,
        w,
        h,
        text,
        font,
        color=COLORS["card_back"],
        hover_color=COLORS["accent"],
        text_color=COLORS["text"],
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base_color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = color

    def draw(self, screen):
        # 1. Detecta mouse para mudar a cor (Hover)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.current_color = self.base_color

        # 2. Desenha o fundo do botão
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)

        # 3. Desenha a borda
        pygame.draw.rect(screen, COLORS["text"], self.rect, width=2, border_radius=10)

        # 4. Desenha o texto centralizado
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_click(self, event):
        """Retorna True se houve um clique válido neste botão."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color):
        # Cria uma partícula com velocidade e vida aleatória
        self.particles.append({
            "x": x, "y": y,
            "vx": random.uniform(-4, 4),
            "vy": random.uniform(-6, -2), # Sobe
            "life": 255,
            "color": color,
            "size": random.randint(4, 8)
        })

    def update_and_draw(self, screen):
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.2 # Gravidade
            p["life"] -= 3 # Fade out
            
            if p["life"] <= 0:
                self.particles.remove(p)
                continue
            
            # Desenha com transparência (Gambiarra: desenha solido pois Alpha no pygame é lento sem surface separada)
            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

    def explode(self, x, y):
        colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
        for _ in range(30): # 30 particulas por explosão
            self.emit(x, y, random.choice(colors))