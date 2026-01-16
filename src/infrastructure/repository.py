import json
import os
from typing import Dict, List


class ScoreRepository:
    """Gerencia a persistência dos recordes em arquivo JSON."""

    FILE_PATH = "scores.json"

    def save_score(self, player_name: str, score: int, theme: str, difficulty: str):
        """Salva uma nova entrada de pontuação."""
        data = self._load_file()

        new_entry = {
            "name": player_name,
            "score": score,
            "theme": theme,
            "difficulty": difficulty,
        }
        data.append(new_entry)

        # Ordena por pontuação (maior para menor) e mantém top 50
        data.sort(key=lambda x: x["score"], reverse=True)
        data = data[:50]

        self._save_file(data)

    def get_top_scores(self, limit=10) -> List[Dict]:
        """Retorna os melhores scores."""
        data = self._load_file()
        return data[:limit]

    def _load_file(self) -> List[Dict]:
        if not os.path.exists(self.FILE_PATH):
            return []
        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_file(self, data: List[Dict]):
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar score: {e}")
