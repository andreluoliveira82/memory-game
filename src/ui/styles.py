# src/ui/styles.py

COLORS = {
    "background": (40, 42, 54),  # Dracula Background
    "text": (248, 248, 242),  # Dracula Foreground
    "accent": (139, 233, 253),  # Dracula Cyan
    "card_back": (98, 114, 164),  # Dracula Comment/Purple
    "card_back_hover": (118, 134, 184),
    "card_face": (255, 255, 255),
    "card_border": (255, 255, 255),
    "success": (80, 250, 123),  # Dracula Green
    "error": (255, 85, 85),  # Dracula Red
    "warning": (255, 184, 108),  # Dracula Orange
    "text_card": (40, 42, 54),
}

DIMENSIONS = {
    "card_size": 110,
    "gap": 15,
    "border_radius": 12,
    "header_height": 160,
    "btn_height": 60,
    "btn_width": 250,
}

THEMES = {
    "dracula": {
        "background": (40, 42, 54),
        "text": (248, 248, 242),
        "accent": (139, 233, 253),
        "card_back": (98, 114, 164),
        "card_back_hover": (118, 134, 184),
        "card_face": (255, 255, 255),
        "card_border": (255, 255, 255),
    },
    "light": {
        "background": (245, 245, 250),
        "text": (30, 30, 40),
        "accent": (70, 130, 255),
        "card_back": (200, 210, 230),
        "card_back_hover": (180, 200, 220),
        "card_face": (255, 255, 255),
        "card_border": (30, 30, 40),
    },
    "ocean": {
        "background": (15, 40, 80),
        "accent": (0, 255, 200),
        "text": (220, 240, 255),
        "card_back": (10, 30, 60),
        "card_back_hover": (30, 50, 90),
        "card_face": (255, 255, 255),
        "card_border": (30, 30, 40),
    },
}
