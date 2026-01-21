# ARQUIVO: src/ui/flashcard.py
"""
Componente de flashcard educacional.

Exibe popups com informações interessantes quando o jogador
acerta um par, enriquecendo a experiência educacional.
"""

import pygame

import src.ui.styles as styles
from src.ui.components import Tween


class Flashcard:
    """
    Popup educacional que aparece ao acertar pares.

    Exibe fatos interessantes com animação de entrada suave.
    """

    def __init__(
        self, fact_data: dict, position: tuple, duration: int = 5000
    ):  # Aumentado para 5 segundos
        """
        Inicializa o flashcard.

        Args:
            fact_data: Dicionário com informações do fato
            position: Tupla (x, y) da posição central
            duration: Tempo de exibição em milissegundos
        """
        self.data = fact_data
        self.position = position
        self.duration = duration
        self.start_time = pygame.time.get_ticks()

        # Animação
        self.alpha = 0
        self.scale = 0.5
        self.is_active = True

        # Dimensões
        self.width = 400
        self.height = 180

        # Fontes
        self._init_fonts()

    def _init_fonts(self) -> None:
        """Inicializa fontes com fallback."""
        try:
            self.font_title = pygame.font.SysFont("segoeui", 22, bold=True)
            self.font_fact = pygame.font.SysFont("segoeui", 16)
            self.font_extra = pygame.font.SysFont("segoeui", 14, italic=True)
            self.font_emoji = pygame.font.SysFont("segoeuiemoji", 40)
        except:
            self.font_title = pygame.font.SysFont("arial", 20, bold=True)
            self.font_fact = pygame.font.SysFont("arial", 14)
            self.font_extra = pygame.font.SysFont("arial", 12, italic=True)
            self.font_emoji = pygame.font.SysFont("arial", 36)

    def update(self) -> bool:
        """
        Atualiza animação do flashcard.

        Returns:
            True se ainda está ativo, False se deve ser removido
        """
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(1.0, elapsed / self.duration)

        # Fade in nos primeiros 10%, fade out nos últimos 20%
        if progress < 0.1:
            # Fade in com bounce
            t = progress / 0.1
            self.alpha = int(255 * Tween.ease_out_cubic(t))
            self.scale = 0.5 + 0.5 * Tween.ease_bounce(t)
        elif progress > 0.8:
            # Fade out
            t = (progress - 0.8) / 0.2
            self.alpha = int(255 * (1 - t))
            self.scale = 1.0 - 0.2 * t
        else:
            # Totalmente visível
            self.alpha = 255
            self.scale = 1.0

        if progress >= 1.0:
            self.is_active = False
            return False

        return True

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renderiza o flashcard na tela.

        Args:
            screen: Superfície do Pygame
        """
        if not self.is_active:
            return

        # Cria superfície com alpha
        card_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Dimensões escaladas
        scaled_w = int(self.width * self.scale)
        scaled_h = int(self.height * self.scale)

        # Fundo do card com sombra
        shadow_rect = pygame.Rect(4, 4, self.width - 8, self.height - 8)
        pygame.draw.rect(card_surface, (0, 0, 0, 100), shadow_rect, border_radius=15)

        card_rect = pygame.Rect(0, 0, self.width - 8, self.height - 8)

        # Cor de fundo baseada no tema
        bg_color = (*styles.COLORS["card_face"], self.alpha)
        pygame.draw.rect(card_surface, bg_color, card_rect, border_radius=15)

        # Borda colorida
        border_color = (*styles.COLORS["accent"], self.alpha)
        pygame.draw.rect(
            card_surface, border_color, card_rect, width=3, border_radius=15
        )

        # Renderiza conteúdo
        self._draw_content(card_surface)

        # Escala a superfície
        if self.scale != 1.0:
            card_surface = pygame.transform.scale(card_surface, (scaled_w, scaled_h))

        # Posiciona e desenha
        x = self.position[0] - scaled_w // 2
        y = self.position[1] - scaled_h // 2
        screen.blit(card_surface, (x, y))

    def _draw_content(self, surface: pygame.Surface) -> None:
        """
        Desenha o conteúdo textual do flashcard.

        Args:
            surface: Superfície onde desenhar
        """
        y_offset = 15

        # Emoji (se disponível)
        if "emoji" in self.data:
            emoji_surf = self.font_emoji.render(
                self.data["emoji"], True, (*styles.COLORS["text_card"], self.alpha)
            )
            emoji_rect = emoji_surf.get_rect(center=(self.width // 2, y_offset + 25))
            surface.blit(emoji_surf, emoji_rect)
            y_offset += 60

        # Título (nome do item)
        if "name" in self.data:
            title_surf = self.font_title.render(
                self.data["name"], True, (*styles.COLORS["text_card"], self.alpha)
            )
            title_rect = title_surf.get_rect(center=(self.width // 2, y_offset))
            surface.blit(title_surf, title_rect)
            y_offset += 30

        # Fato principal
        if "fact" in self.data:
            fact_text = self.data["fact"]
            # Quebra de linha automática
            words = fact_text.split()
            lines = []
            current_line = []

            for word in words:
                test_line = " ".join(current_line + [word])
                test_surf = self.font_fact.render(test_line, True, (0, 0, 0))
                if test_surf.get_width() > self.width - 40:
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)

            if current_line:
                lines.append(" ".join(current_line))

            # Renderiza linhas
            for line in lines[:2]:  # Máximo 2 linhas
                line_surf = self.font_fact.render(
                    line, True, (*styles.COLORS["text_card"], self.alpha)
                )
                line_rect = line_surf.get_rect(center=(self.width // 2, y_offset))
                surface.blit(line_surf, line_rect)
                y_offset += 22

        # Informação extra (menor)
        if "extra" in self.data:
            extra_surf = self.font_extra.render(
                self.data["extra"], True, (*styles.COLORS["accent"], self.alpha)
            )
            extra_rect = extra_surf.get_rect(center=(self.width // 2, self.height - 20))
            surface.blit(extra_surf, extra_rect)


class FlashcardManager:
    """
    Gerenciador de múltiplos flashcards na tela.

    Controla a exibição sequencial de flashcards para evitar
    sobreposição e poluição visual.
    """

    def __init__(self):
        """Inicializa o gerenciador."""
        self.flashcards: list[Flashcard] = []
        self.max_simultaneous = 2  # Máximo de flashcards simultâneos

    def add_flashcard(self, fact_data: dict, position: tuple) -> None:
        """
        Adiciona um novo flashcard.

        Args:
            fact_data: Dados do fato educacional
            position: Posição central (x, y)
        """
        # Remove flashcards antigos se houver muitos
        if len(self.flashcards) >= self.max_simultaneous:
            # Remove o mais antigo
            self.flashcards.pop(0)

        # Ajusta posição se houver outro flashcard
        adjusted_position = position
        if self.flashcards:
            # Desloca verticalmente para não sobrepor
            adjusted_position = (position[0], position[1] + 100)

        flashcard = Flashcard(fact_data, adjusted_position)
        self.flashcards.append(flashcard)

    def update(self) -> None:
        """Atualiza todos os flashcards ativos."""
        for flashcard in self.flashcards[:]:
            if not flashcard.update():
                self.flashcards.remove(flashcard)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renderiza todos os flashcards ativos.

        Args:
            screen: Superfície do Pygame
        """
        for flashcard in self.flashcards:
            flashcard.draw(screen)

    def clear(self) -> None:
        """Remove todos os flashcards."""
        self.flashcards.clear()

    def has_active_flashcards(self) -> bool:
        """
        Verifica se há flashcards ativos.

        Returns:
            True se há flashcards sendo exibidos
        """
        return len(self.flashcards) > 0
