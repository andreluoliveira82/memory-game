import pygame
from src.services.game_service import GameService

# Constantes de Estilo
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
CARD_SIZE = 120
GAP = 10
COLORS = {
    "background": (30, 30, 30),
    "card_hidden": (70, 70, 70),
    "card_revealed": (200, 200, 200),
    "card_matched": (50, 200, 50),
    "text": (255, 255, 255),
    "primary": (0, 150, 255)
}

class GraphicUI:
    """Interface Gráfica usando Pygame para o Jogo da Memória."""

    def __init__(self, service: GameService):
        pygame.init()
        self.service = service
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Memória Pythônica")
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()

    def _get_card_rect(self, row: int, col: int) -> pygame.Rect:
        """Calcula a posição do retângulo da carta na tela."""
        # Centralizando o tabuleiro levemente
        offset_x = (SCREEN_WIDTH - (self.service.board.cols * (CARD_SIZE + GAP))) // 2
        offset_y = 100 
        x = offset_x + col * (CARD_SIZE + GAP)
        y = offset_y + row * (CARD_SIZE + GAP)
        return pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)

    def _draw(self, message: str):
        """Desenha todos os elementos na tela."""
        self.screen.fill(COLORS["background"])

        # Desenha Título e Movimentos
        title_surf = self.font.render("Jogo da Memória", True, COLORS["primary"])
        self.screen.blit(title_surf, (20, 20))
        
        moves_surf = self.small_font.render(f"Movimentos: {self.service.moves}", True, COLORS["text"])
        self.screen.blit(moves_surf, (20, 70))

        # Desenha as Cartas
        for r in range(self.service.board.rows):
            for c in range(self.service.board.cols):
                card = self.service.board.get_card(r, c)
                rect = self._get_card_rect(r, c)
                
                # Define a cor baseada no estado
                color = COLORS["card_hidden"]
                if card.is_matched:
                    color = COLORS["card_matched"]
                elif card.is_revealed:
                    color = COLORS["card_revealed"]

                pygame.draw.rect(self.screen, color, rect, border_radius=8)

                # Se revelada ou par, mostra o texto/valor
                if card.is_revealed or card.is_matched:
                    text_surf = self.font.render(str(card.value), True, (0, 0, 0))
                    text_rect = text_surf.get_rect(center=rect.center)
                    self.screen.blit(text_surf, text_rect)

        # Mensagem de Status
        status_surf = self.small_font.render(message, True, COLORS["primary"])
        self.screen.blit(status_surf, (20, SCREEN_HEIGHT - 50))

        pygame.display.flip()

    def run(self):
        """Loop principal da GUI."""
        running = True
        msg = "Clique em uma carta!"
        pending_hide = None # Para gerenciar o delay de cartas erradas

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and not pending_hide:
                    mouse_pos = pygame.mouse.get_pos()
                    self._handle_click(mouse_pos)

            # Lógica de "Peek" (esconder cartas erradas após delay)
            if pending_hide:
                pygame.time.delay(1000) # Pausa de 1 segundo
                self.service.hide_cards(*pending_hide)
                pending_hide = None
                msg = "Tente novamente!"

            if self.service.board.all_matched:
                msg = "PARABÉNS! Você venceu!"

            self._draw(msg)
            self.clock.tick(30)

        pygame.quit()

    def _handle_click(self, pos):
        """Converte clique em tela para coordenada de tabuleiro."""
        for r in range(self.service.board.rows):
            for c in range(self.service.board.cols):
                rect = self._get_card_rect(r, c)
                if rect.collidepoint(pos):
                    # Guardamos a posição da primeira carta se for o caso
                    first_pos = self.service.first_selected_pos
                    current_pos = (r, c)
                    
                    result = self.service.pick_card(r, c)
                    
                    if result == "NO_MATCH":
                        # Forçamos um desenho para mostrar a segunda carta antes de esconder
                        self._draw("Não foi dessa vez...")
                        pygame.time.delay(500)
                        self.service.hide_cards(first_pos, current_pos)