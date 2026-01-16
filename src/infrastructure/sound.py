# ARQUIVO: src/infrastructure/sound.py
import os

import pygame


class SoundManager:
    """Gerencia o carregamento e execução de efeitos sonoros."""

    def __init__(self):
        # Inicializa o mixer do Pygame (44.1kHz, 16bit, stereo, buffer 2048)
        try:
            pygame.mixer.init(44100, -16, 2, 2048)
            self.enabled = True
        except Exception as e:
            print(f"Erro ao iniciar som: {e}")
            self.enabled = False

        # Dicionário para guardar os sons carregados
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        """Tenta carregar os arquivos .wav da pasta assets/sounds."""
        if not self.enabled:
            return

        # Caminho base: pasta do projeto/assets/sounds
        base_path = os.path.join("assets", "sounds")

        # Lista de sons que queremos usar
        sound_files = {
            "flip": "flip.wav",  # Virar carta
            "match": "match.wav",  # Acerto
            "error": "error.wav",  # Erro
            "win": "win.wav",  # Vitória
            "click": "click.wav",  # Clique em botão
        }

        for name, filename in sound_files.items():
            full_path = os.path.join(base_path, filename)
            if os.path.exists(full_path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(full_path)
                    # Ajuste de volume (0.0 a 1.0)
                    self.sounds[name].set_volume(0.5)
                except:
                    print(f"Não foi possível ler o arquivo: {full_path}")
            else:
                # Silenciosamente ignora se não tiver o arquivo ainda
                pass

    def play(self, sound_name):
        """Toca um som pelo nome (ex: 'match')."""
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
