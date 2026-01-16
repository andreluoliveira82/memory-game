# ARQUIVO: src/ui/gui.py
import pygame

from src.infrastructure.sound import SoundManager  # Importamos o som
from src.services.game_service import GameService
from src.ui.components import Button  # Importamos nosso botão
from src.ui.styles import COLORS, DIMENSIONS


class GraphicUI:
    def __init__(self, service: GameService, card_size: int = None):
        self.service = service
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Inicializa Som
        self.sounds = SoundManager()

        # Configurações de Grid
        self.card_size = card_size if card_size else DIMENSIONS["card_size"]
        self.grid_width = (service.board.cols * self.card_size) + (
            (service.board.cols - 1) * DIMENSIONS["gap"]
        )

        # Fontes
        try:
            self.font_base_name = "segoeuiemoji"
            self.font_title = pygame.font.SysFont("segoeui", 48, bold=True)
            self.font_stats = pygame.font.SysFont("consolas", 22)
            self.font_msg = pygame.font.SysFont("segoeui", 28)
            self.font_btn = pygame.font.SysFont(
                "segoeui", 24, bold=True
            )  # Fonte para botões
        except:
            self.font_base_name = "arial"
            self.font_title = pygame.font.SysFont("arial", 40, bold=True)
            self.font_stats = pygame.font.SysFont("arial", 20)
            self.font_msg = pygame.font.SysFont("arial", 24)
            self.font_btn = pygame.font.SysFont("arial", 22, bold=True)

        self.message = "Encontre os pares!"
        self.waiting_to_hide = False
        self.hide_timestamp = 0
        self.cards_to_hide = None

        self.saved = False

        # --- PREPARAÇÃO DA TELA DE GAME OVER ---
        # Criamos os botões aqui para não recriar a cada frame (performance)
        # Posições serão calculadas relativas ao centro da tela
        center_x = self.width // 2
        center_y = self.height // 2

        # Botão Jogar Novamente (Verde)
        self.btn_restart = Button(
            x=center_x - 210,
            y=center_y + 50,
            w=200,
            h=60,
            text="Jogar Novamente",
            font=self.font_btn,
            color=COLORS["success"],
            hover_color=(100, 255, 150),
            text_color=(0, 0, 0),
        )

        # Botão Voltar ao Menu (Roxo)
        self.btn_menu = Button(
            x=center_x + 10,
            y=center_y + 50,
            w=200,
            h=60,
            text="Menu Principal",
            font=self.font_btn,
            color=COLORS["card_back"],
            hover_color=COLORS["accent"],
        )

    def update(self):
        """Atualiza lógica temporal."""
        if self.waiting_to_hide:
            if pygame.time.get_ticks() - self.hide_timestamp > 1000:
                self.service.hide_cards(*self.cards_to_hide)
                self.waiting_to_hide = False
                self.cards_to_hide = None
                self.message = "Tente novamente!"

    def handle_click(self, event):
        """
        Processa cliques.
        Retorna uma string de ação ("RESTART" ou "MENU") se clicar nos botões de fim de jogo.
        """
        # 1. Se o jogo acabou, checa cliques nos botões da overlay
        if self.service.board.all_matched:
            if self.btn_restart.check_click(event):
                self.sounds.play("click")
                return "RESTART"

            if self.btn_menu.check_click(event):
                self.sounds.play("click")
                return "MENU"
            return None

        # 2. Se o jogo está rodando, checa cliques nas cartas
        if self.waiting_to_hide:
            return None  # Ignora cliques enquanto espera animação

        # Só processa clique esquerdo nas cartas (event.pos vem direto do pygame.event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for r in range(self.service.board.rows):
                for c in range(self.service.board.cols):
                    rect = self._get_card_rect(r, c)
                    if rect.collidepoint(event.pos):
                        self._process_pick(r, c)
                        break
        return None

    def _process_pick(self, r, c):
        first_pos = self.service.first_selected_pos
        current_pos = (r, c)
        result = self.service.pick_card(r, c)

        if result == "MATCH":
            self.sounds.play("match")  # Toca som de acerto
            combo = self.service.combo_streak
            if combo > 1:
                self.message = f"COMBO x{combo}! (+{100 * combo})"
            else:
                self.message = "Boa! Um par!"

            # Se acabou o jogo, toca som de vitória
            if self.service.board.all_matched:
                self.sounds.play("win")

        elif result == "NO_MATCH":
            self.sounds.play("error")  # Toca som de erro
            self.message = "Ops... errou."
            self.waiting_to_hide = True
            self.hide_timestamp = pygame.time.get_ticks()
            self.cards_to_hide = (first_pos, current_pos)

        elif result == "FIRST_PICK":
            self.sounds.play("flip")  # Toca som de virar carta
            self.message = "Escolha o par..."

    def draw(self):
        """Desenha a tela do jogo."""
        self.screen.fill(COLORS["background"])

        # --- DESENHA O JOGO NORMALMENTE ---
        # Header
        title = self.font_title.render("Memory Game", True, COLORS["accent"])
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))

        # Stats Box
        self._draw_stats()

        # Grid de Cartas
        mouse_pos = pygame.mouse.get_pos()
        for r in range(self.service.board.rows):
            for c in range(self.service.board.cols):
                card = self.service.board.get_card(r, c)
                rect = self._get_card_rect(r, c)
                self._draw_single_card(card, rect, mouse_pos)

        # Footer (só mostra se jogo NÃO acabou, pois o overlay vai cobrir)
        if not self.service.board.all_matched:
            msg_surf = self.font_msg.render(self.message, True, COLORS["accent"])
            msg_rect = msg_surf.get_rect(center=(self.width // 2, self.height - 50))
            self.screen.blit(msg_surf, msg_rect)

        # --- SE ACABOU, DESENHA O OVERLAY DE GAME OVER ---
        if self.service.board.all_matched:
            self._draw_game_over_overlay()

    def _draw_game_over_overlay(self):
        """Cria uma tela semitransparente com o resultado e botões."""
        # 1. Surface transparente escura
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)  # 0=Invisível, 255=Sólido
        overlay.fill((0, 0, 0))  # Preto
        self.screen.blit(overlay, (0, 0))

        # 2. Caixa de Texto de Vitória
        center_x = self.width // 2
        center_y = self.height // 2 - 50

        # Título
        win_text = self.font_title.render("FIM DE JOGO!", True, COLORS["success"])
        win_rect = win_text.get_rect(center=(center_x, center_y - 80))
        self.screen.blit(win_text, win_rect)

        # Pontuação Final
        score_msg = f"Pontuação Final: {self.service.score}"
        score_surf = self.font_msg.render(score_msg, True, COLORS["text"])
        score_rect = score_surf.get_rect(center=(center_x, center_y - 20))
        self.screen.blit(score_surf, score_rect)

        # 3. Desenha os Botões
        self.btn_restart.draw(self.screen)
        self.btn_menu.draw(self.screen)

    def _draw_stats(self):
        # Lógica de stats (mantida igual, resumida para economizar espaço)
        section_w = self.width // 3
        y_pos = 90
        mov_text = f"Movimentos: {self.service.moves}"
        self._draw_stat_box(mov_text, (section_w * 0 + section_w // 2, y_pos))
        score_text = f"Pontos: {self.service.score}"
        self._draw_stat_box(
            score_text,
            (section_w * 1 + section_w // 2, y_pos),
            COLORS["success"] if self.service.combo_streak > 1 else COLORS["text"],
        )
        time_text = f"Tempo: {self.service.get_time_formatted()}"
        self._draw_stat_box(time_text, (section_w * 2 + section_w // 2, y_pos))

    def _draw_stat_box(self, text, pos, color=COLORS["text"]):
        surf = self.font_stats.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=pos))

    # ... (métodos _get_card_rect, _draw_single_card, _draw_dynamic_text mantêm iguais) ...
    # Copie-os do seu arquivo anterior ou mantenha-os se estiver editando apenas as partes acima.
    # Para garantir que funcione, vou colocar os helpers essenciais aqui embaixo:

    def _get_card_rect(self, row, col):
        start_x = (self.width - self.grid_width) // 2
        start_y = DIMENSIONS["header_height"]
        x = start_x + col * (self.card_size + DIMENSIONS["gap"])
        y = start_y + row * (self.card_size + DIMENSIONS["gap"])
        return pygame.Rect(x, y, self.card_size, self.card_size)

    def _draw_single_card(self, card, rect, mouse_pos):
        # (Copie o conteúdo exato do passo anterior para este método)
        # Resumo da lógica:
        bg_color = COLORS["card_back"]
        if not card.is_revealed and not card.is_matched and not self.waiting_to_hide:
            if rect.collidepoint(mouse_pos):
                bg_color = COLORS["card_back_hover"]
        if card.is_revealed:
            bg_color = COLORS["card_face"]
        if card.is_matched:
            bg_color = COLORS["success"]

        # Sombra e Corpo
        shadow = rect.copy()
        shadow.move_ip(4, 4)
        pygame.draw.rect(
            self.screen, (20, 20, 20), shadow, border_radius=DIMENSIONS["border_radius"]
        )
        pygame.draw.rect(
            self.screen, bg_color, rect, border_radius=DIMENSIONS["border_radius"]
        )

        if card.is_revealed or card.is_matched:
            pygame.draw.rect(
                self.screen,
                COLORS["card_border"],
                rect,
                width=2,
                border_radius=DIMENSIONS["border_radius"],
            )
            self._draw_dynamic_text(str(card.display_content), rect)
        else:
            q_surf = self.font_msg.render("?", True, (255, 255, 255, 50))
            self.screen.blit(q_surf, q_surf.get_rect(center=rect.center))

    def _draw_dynamic_text(self, text, rect):
        max_width = rect.width - 10
        font_size = 40
        while font_size > 12:
            font = pygame.font.SysFont(self.font_base_name, font_size)
            text_surf = font.render(text, True, COLORS["text_card"])
            if text_surf.get_width() <= max_width:
                break
            font_size -= 2
        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
