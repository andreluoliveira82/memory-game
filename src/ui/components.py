# ARQUIVO: src/ui/components.py
"""
Componentes de UI reutilizáveis para o jogo da memória.

Este módulo contém widgets, sistemas de partículas e elementos visuais
que são utilizados em toda a interface do jogo.
"""

import math
import random

import pygame

from src.ui.styles import COLORS


class InputBox:
    """
    Caixa de texto interativa para entrada de dados.

    Permite ao usuário digitar texto com feedback visual de foco.
    Utilizada principalmente na tela de login.
    """

    def __init__(
        self, x: int, y: int, w: int, h: int, font: pygame.font.Font, text: str = ""
    ):
        """
        Inicializa a caixa de entrada.

        Args:
            x: Posição X inicial
            y: Posição Y inicial
            w: Largura da caixa
            h: Altura da caixa
            font: Fonte para renderização do texto
            text: Texto inicial (padrão: vazio)
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = COLORS["card_back"]
        self.color_active = COLORS["accent"]
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """
        Processa eventos de mouse e teclado.

        Args:
            event: Evento do Pygame

        Returns:
            Texto digitado se ENTER foi pressionado, None caso contrário
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 12:
                        self.text += event.unicode

                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Renderiza a caixa de texto na tela."""
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)


class Button:
    """
    Botão interativo com efeito hover e feedback visual.

    Suporta cores customizadas e detecção de clique.
    """

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        text: str,
        font: pygame.font.Font,
        color: tuple = None,
        hover_color: tuple = None,
        text_color: tuple = None,
    ):
        """
        Inicializa o botão.

        Args:
            x, y: Posição do botão
            w, h: Dimensões do botão
            text: Texto exibido
            font: Fonte do texto
            color: Cor padrão (usa tema se None)
            hover_color: Cor ao passar o mouse (usa tema se None)
            text_color: Cor do texto (usa tema se None)
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base_color = color or COLORS["card_back"]
        self.hover_color = hover_color or COLORS["accent"]
        self.text_color = text_color or COLORS["text"]
        self.current_color = self.base_color

    def draw(self, screen: pygame.Surface) -> None:
        """Renderiza o botão com detecção de hover."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.current_color = self.base_color

        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLORS["text"], self.rect, width=2, border_radius=10)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_click(self, event: pygame.event.Event) -> bool:
        """
        Verifica se o botão foi clicado.

        Args:
            event: Evento do Pygame

        Returns:
            True se houve clique válido, False caso contrário
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Particle:
    """
    Partícula individual para efeitos visuais.

    Representa uma única partícula com física, vida útil e renderização.
    """

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: tuple,
        size: int,
        particle_type: str = "circle",
        life: int = 255,
        gravity: float = 0.2,
    ):
        """
        Cria uma partícula.

        Args:
            x, y: Posição inicial
            vx, vy: Velocidade inicial
            color: Cor RGB
            size: Tamanho em pixels
            particle_type: Tipo de renderização ("circle", "star", "square")
            life: Vida útil inicial (0-255)
            gravity: Força da gravidade aplicada
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.type = particle_type
        self.life = life
        self.gravity = gravity
        self.rotation = random.uniform(0, 360)  # Para efeitos rotativos

    def update(self) -> bool:
        """
        Atualiza física e vida da partícula.

        Returns:
            True se a partícula ainda está viva, False se deve ser removida
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 3

        # Adiciona leve arrasto
        self.vx *= 0.98
        self.vy *= 0.98

        self.rotation += 5

        return self.life > 0

    def draw(self, screen: pygame.Surface) -> None:
        """Renderiza a partícula na tela."""
        if self.life <= 0:
            return

        # Alpha blending simulado ajustando cor
        alpha_factor = max(0, min(1, self.life / 255))
        faded_color = tuple(int(c * alpha_factor) for c in self.color)

        pos = (int(self.x), int(self.y))

        if self.type == "circle":
            pygame.draw.circle(
                screen, faded_color, pos, max(1, int(self.size * alpha_factor))
            )

        elif self.type == "star":
            self._draw_star(screen, pos, self.size, faded_color)

        elif self.type == "square":
            rect = pygame.Rect(0, 0, self.size, self.size)
            rect.center = pos
            pygame.draw.rect(screen, faded_color, rect)

    def _draw_star(
        self, screen: pygame.Surface, pos: tuple, size: int, color: tuple
    ) -> None:
        """Desenha uma estrela de 5 pontas."""
        points = []
        for i in range(10):
            angle = math.radians(i * 36 + self.rotation)
            radius = size if i % 2 == 0 else size // 2
            x = pos[0] + radius * math.cos(angle)
            y = pos[1] + radius * math.sin(angle)
            points.append((x, y))

        if len(points) >= 3:
            pygame.draw.polygon(screen, color, points)


class AdvancedParticleSystem:
    """
    Sistema de partículas avançado com múltiplos efeitos visuais.

    Gerencia criação, atualização e renderização de partículas para
    diversos efeitos (acertos, combos, vitória, etc.).
    """

    def __init__(self):
        """Inicializa o sistema de partículas."""
        self.particles: list[Particle] = []

    def emit(
        self,
        x: float,
        y: float,
        color: tuple,
        velocity_range: tuple = (-4, 4),
        count: int = 1,
        particle_type: str = "circle",
        size_range: tuple = (4, 8),
    ) -> None:
        """
        Emite partículas de uma posição.

        Args:
            x, y: Posição de origem
            color: Cor das partículas
            velocity_range: Range de velocidade (min, max)
            count: Quantidade de partículas a emitir
            particle_type: Tipo de partícula
            size_range: Range de tamanho (min, max)
        """
        for _ in range(count):
            vx = random.uniform(*velocity_range)
            vy = random.uniform(-6, -2)
            size = random.randint(*size_range)

            particle = Particle(x, y, vx, vy, color, size, particle_type)
            self.particles.append(particle)

    def sparkle(self, x: float, y: float) -> None:
        """
        Efeito de brilho dourado (para acertos).

        Args:
            x, y: Posição do efeito
        """
        colors = [
            (255, 215, 0),  # Dourado
            (255, 255, 100),  # Amarelo claro
            (255, 200, 50),  # Laranja dourado
        ]

        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice(colors)

            particle = Particle(x, y, vx, vy, color, random.randint(3, 6), "star")
            self.particles.append(particle)

    def firework(self, x: float, y: float) -> None:
        """
        Efeito de fogos de artifício (para combos).

        Args:
            x, y: Posição do efeito
        """
        colors = [
            (255, 0, 100),  # Rosa
            (0, 255, 200),  # Ciano
            (255, 255, 0),  # Amarelo
            (100, 0, 255),  # Roxo
            (255, 100, 0),  # Laranja
        ]

        for color in colors:
            for _ in range(8):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(4, 8)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed

                particle = Particle(
                    x, y, vx, vy, color, random.randint(4, 8), "circle", gravity=0.3
                )
                self.particles.append(particle)

    def rainbow_burst(self, x: float, y: float) -> None:
        """
        Explosão arco-íris (para jogo perfeito).

        Args:
            x, y: Posição do efeito
        """
        rainbow_colors = [
            (255, 0, 0),  # Vermelho
            (255, 127, 0),  # Laranja
            (255, 255, 0),  # Amarelo
            (0, 255, 0),  # Verde
            (0, 0, 255),  # Azul
            (75, 0, 130),  # Índigo
            (148, 0, 211),  # Violeta
        ]

        for color in rainbow_colors:
            for _ in range(12):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(3, 7)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed

                particle = Particle(
                    x, y, vx, vy, color, random.randint(5, 10), "star", gravity=0.15
                )
                self.particles.append(particle)

    def confetti(self, x: float, y: float, count: int = 50) -> None:
        """
        Chuva de confetes (para vitória).

        Args:
            x, y: Posição inicial
            count: Quantidade de confetes
        """
        colors = [
            (255, 0, 100),
            (0, 255, 200),
            (255, 255, 0),
            (100, 0, 255),
            (255, 100, 0),
            (0, 255, 100),
        ]

        for _ in range(count):
            vx = random.uniform(-6, 6)
            vy = random.uniform(-8, -2)
            color = random.choice(colors)
            size = random.randint(4, 8)
            p_type = random.choice(["square", "circle"])

            particle = Particle(x, y, vx, vy, color, size, p_type, gravity=0.25)
            self.particles.append(particle)

    def update_and_draw(self, screen: pygame.Surface) -> None:
        """
        Atualiza física e renderiza todas as partículas.

        Args:
            screen: Superfície do Pygame para desenho
        """
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)
            else:
                particle.draw(screen)

    def clear(self) -> None:
        """Remove todas as partículas ativas."""
        self.particles.clear()

    def explode(self, x: float, y: float) -> None:
        """
        Explosão genérica (compatibilidade com código antigo).

        Args:
            x, y: Posição da explosão
        """
        self.firework(x, y)


class Tween:
    """
    Sistema de interpolação para animações suaves.

    Fornece funções de easing para criar transições naturais.
    """

    @staticmethod
    def linear(t: float) -> float:
        """Interpolação linear (sem aceleração)."""
        return t

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Aceleração quadrática (começa devagar)."""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Desaceleração quadrática (termina devagar)."""
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Aceleração e desaceleração quadrática."""
        return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Desaceleração cúbica (suave)."""
        return 1 - pow(1 - t, 3)

    @staticmethod
    def ease_bounce(t: float) -> float:
        """Efeito de quique (bounce)."""
        if t < 0.5:
            return 8 * t * t * t * t
        return 1 - pow(-2 * t + 2, 4) / 2

    @staticmethod
    def ease_elastic(t: float) -> float:
        """Efeito elástico (overshoot)."""
        c4 = (2 * math.pi) / 3
        if t == 0:
            return 0
        if t == 1:
            return 1
        return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1


class CardFlipAnimation:
    """
    Animação de flip 3D para cartas.

    Simula rotação 3D usando escala 2D para criar efeito de virada.
    """

    def __init__(self, card_rect: pygame.Rect, duration: int = 300):
        """
        Inicializa a animação.

        Args:
            card_rect: Retângulo da carta
            duration: Duração em milissegundos
        """
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.original_rect = card_rect.copy()
        self.rect = card_rect.copy()
        self.is_complete = False

    def update(self) -> bool:
        """
        Atualiza o estado da animação.

        Returns:
            True se ainda está animando, False se completou
        """
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(1.0, elapsed / self.duration)

        # Easing para suavidade
        eased_progress = Tween.ease_out_cubic(progress)

        # Efeito de flip: escala horizontal vai de 1 -> 0 -> 1
        scale = abs(math.cos(eased_progress * math.pi))
        self.rect.width = int(self.original_rect.width * scale)
        self.rect.centerx = self.original_rect.centerx

        if progress >= 1.0:
            self.is_complete = True
            self.rect = self.original_rect.copy()
            return False

        return True

    def draw_back(self, screen: pygame.Surface) -> bool:
        """
        Determina se deve desenhar o verso da carta.

        Returns:
            True se deve mostrar verso, False se deve mostrar frente
        """
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = elapsed / self.duration
        return progress < 0.5  # Metade da animação mostra verso
