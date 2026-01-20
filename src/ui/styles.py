# ARQUIVO: src/ui/styles.py
"""
Sistema de temas visuais e constantes de estilo.

Fornece múltiplas paletas de cores e dimensões configuráveis
para toda a interface do jogo.
"""

# ========================================
# PALETAS DE CORES (TEMAS)
# ========================================

THEMES = {
    "dracula": {
        "name": "🌙 Dracula (Escuro)",
        "background": (40, 42, 54),
        "text": (248, 248, 242),
        "accent": (139, 233, 253),
        "card_back": (98, 114, 164),
        "card_back_hover": (118, 134, 184),
        "card_face": (255, 255, 255),
        "card_border": (255, 255, 255),
        "success": (80, 250, 123),
        "error": (255, 85, 85),
        "warning": (255, 184, 108),
        "text_card": (40, 42, 54),
    },
    "light": {
        "name": "☀️ Modo Claro",
        "background": (245, 245, 250),
        "text": (30, 30, 40),
        "accent": (70, 130, 255),
        "card_back": (200, 210, 230),
        "card_back_hover": (180, 190, 220),
        "card_face": (255, 255, 255),
        "card_border": (70, 130, 255),
        "success": (40, 180, 99),
        "error": (231, 76, 60),
        "warning": (230, 126, 34),
        "text_card": (30, 30, 40),
    },
    "ocean": {
        "name": "🌊 Oceano Profundo",
        "background": (15, 40, 80),
        "text": (200, 240, 255),
        "accent": (0, 255, 200),
        "card_back": (30, 60, 120),
        "card_back_hover": (40, 80, 150),
        "card_face": (240, 250, 255),
        "card_border": (0, 255, 200),
        "success": (0, 230, 180),
        "error": (255, 100, 120),
        "warning": (255, 200, 100),
        "text_card": (15, 40, 80),
    },
    "forest": {
        "name": "🌲 Floresta Mística",
        "background": (25, 35, 25),
        "text": (230, 240, 220),
        "accent": (144, 238, 144),
        "card_back": (60, 80, 60),
        "card_back_hover": (80, 100, 80),
        "card_face": (240, 255, 240),
        "card_border": (144, 238, 144),
        "success": (50, 205, 50),
        "error": (220, 20, 60),
        "warning": (255, 215, 0),
        "text_card": (25, 35, 25),
    },
    "sunset": {
        "name": "🌅 Pôr do Sol",
        "background": (50, 30, 50),
        "text": (255, 240, 245),
        "accent": (255, 140, 180),
        "card_back": (120, 80, 120),
        "card_back_hover": (140, 100, 140),
        "card_face": (255, 250, 250),
        "card_border": (255, 140, 180),
        "success": (255, 105, 180),
        "error": (220, 20, 60),
        "warning": (255, 165, 0),
        "text_card": (50, 30, 50),
    },
    "cyber": {
        "name": "🤖 Cyberpunk",
        "background": (10, 10, 20),
        "text": (0, 255, 255),
        "accent": (255, 0, 255),
        "card_back": (30, 0, 60),
        "card_back_hover": (50, 0, 100),
        "card_face": (255, 255, 255),
        "card_border": (0, 255, 255),
        "success": (0, 255, 100),
        "error": (255, 0, 100),
        "warning": (255, 255, 0),
        "text_card": (10, 10, 20),
    },
}

# Tema padrão
CURRENT_THEME = "dracula"


def get_colors(theme_name: str = None) -> dict:
    """
    Retorna a paleta de cores de um tema.
    
    Args:
        theme_name: Nome do tema (None = tema atual)
        
    Returns:
        Dicionário com as cores do tema
        
    Raises:
        KeyError: Se o tema não existir
    """
    if theme_name is None:
        theme_name = CURRENT_THEME
    
    if theme_name not in THEMES:
        raise KeyError(f"Tema '{theme_name}' não existe. Disponíveis: {list(THEMES.keys())}")
    
    return THEMES[theme_name].copy()


def set_theme(theme_name: str) -> dict:
    """
    Define o tema ativo globalmente.
    
    Args:
        theme_name: Nome do tema a ativar
        
    Returns:
        Dicionário com as cores do novo tema
        
    Raises:
        KeyError: Se o tema não existir
    """
    global CURRENT_THEME, COLORS
    
    if theme_name not in THEMES:
        raise KeyError(f"Tema '{theme_name}' não existe. Disponíveis: {list(THEMES.keys())}")
    
    CURRENT_THEME = theme_name
    COLORS = get_colors(theme_name)
    return COLORS


def get_available_themes() -> list[dict]:
    """
    Lista todos os temas disponíveis.
    
    Returns:
        Lista de dicionários com info de cada tema
        [{'id': 'dracula', 'name': '🌙 Dracula (Escuro)'}, ...]
    """
    return [
        {"id": theme_id, "name": theme_data["name"]}
        for theme_id, theme_data in THEMES.items()
    ]


# Cores ativas (inicializa com tema padrão)
COLORS = get_colors(CURRENT_THEME)


# ========================================
# DIMENSÕES E CONSTANTES
# ========================================

DIMENSIONS = {
    "card_size": 110,
    "gap": 15,
    "border_radius": 12,
    "header_height": 160,
    "btn_height": 60,
    "btn_width": 250,
}


# ========================================
# CONFIGURAÇÕES DE ANIMAÇÃO
# ========================================

ANIMATION_SETTINGS = {
    "card_flip_duration": 300,  # ms
    "particle_lifetime": 255,  # frames
    "transition_speed": 0.15,  # para fade in/out
    "bounce_intensity": 1.2,  # multiplicador do efeito bounce
}


# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def interpolate_color(color1: tuple, color2: tuple, t: float) -> tuple:
    """
    Interpola entre duas cores.
    
    Args:
        color1: Cor inicial (R, G, B)
        color2: Cor final (R, G, B)
        t: Progresso da interpolação (0.0 a 1.0)
        
    Returns:
        Cor interpolada (R, G, B)
    """
    t = max(0.0, min(1.0, t))  # Clamp
    return tuple(
        int(c1 + (c2 - c1) * t)
        for c1, c2 in zip(color1, color2)
    )


def brighten_color(color: tuple, factor: float = 1.2) -> tuple:
    """
    Clareia uma cor.
    
    Args:
        color: Cor RGB
        factor: Fator de claridade (>1 = mais claro, <1 = mais escuro)
        
    Returns:
        Cor clareada (R, G, B)
    """
    return tuple(min(255, int(c * factor)) for c in color)


def darken_color(color: tuple, factor: float = 0.8) -> tuple:
    """
    Escurece uma cor.
    
    Args:
        color: Cor RGB
        factor: Fator de escurecimento (0.0 a 1.0)
        
    Returns:
        Cor escurecida (R, G, B)
    """
    return tuple(int(c * factor) for c in color)