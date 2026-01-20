# ARQUIVO: src/infrastructure/repository.py
import json
import os
from datetime import datetime
from typing import Dict, List


class ScoreRepository:
    """Gerencia a persistência dos recordes e estatísticas em arquivo JSON."""

    FILE_PATH = "scores.json"

    def save_score(self, player_name: str, score: int, theme: str, difficulty: str):
        data = self._load_file()
        timestamp = datetime.now().strftime("%d/%m %H:%M")

        new_entry = {
            "name": player_name,
            "score": score,
            "theme": theme,
            "difficulty": difficulty,
            "date": timestamp,
        }
        data.append(new_entry)

        # Ordena por Score, mas NÃO apaga mais o histórico
        data.sort(key=lambda x: x["score"], reverse=True)
        self._save_file(data)

    def get_top_scores(
        self, limit=10, difficulty_filter=None, theme_filter=None
    ) -> List[Dict]:
        """Retorna scores filtrados por Dificuldade E Tema."""
        data = self._load_file()

        # 1. Filtro de Dificuldade
        if difficulty_filter:
            data = [d for d in data if d["difficulty"] == difficulty_filter]

        # 2. Filtro de Tema
        if theme_filter:
            data = [d for d in data if d["theme"] == theme_filter]

        # 3. Ordena e Corta
        data.sort(key=lambda x: x["score"], reverse=True)
        return data[:limit]

    def get_statistics(self) -> Dict:
        """Gera dados agregados para o Dashboard."""
        data = self._load_file()
        if not data:
            return {}

        stats = {
            "total_games": len(data),
            "best_score": max(d["score"] for d in data),
            "themes_count": {},
            "difficulty_count": {},
        }

        for entry in data:
            t = entry["theme"]
            stats["themes_count"][t] = stats["themes_count"].get(t, 0) + 1

            d = entry["difficulty"]
            stats["difficulty_count"][d] = stats["difficulty_count"].get(d, 0) + 1

        if stats["themes_count"]:
            stats["favorite_theme"] = max(
                stats["themes_count"], key=stats["themes_count"].get
            )
        else:
            stats["favorite_theme"] = "-"

        return stats

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
