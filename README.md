# 🎮 Memory Game — Versão 3.0  
Um jogo da memória moderno, modular e extensível, desenvolvido em **Python + Pygame**, seguindo princípios de **Clean Architecture**.

---

## 🏷️ Badges
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![Architecture-Clean](https://img.shields.io/badge/Architecture-Clean%20Architecture-purple)
![Status-Stable](https://img.shields.io/badge/Status-V3%20Stable-brightgreen)

---

## 📘 Visão Geral
O **Memory Game** é uma aplicação desktop com foco em **educação**, **gamificação** e **extensibilidade**.  
A arquitetura limpa permite adicionar novos temas, modos e interfaces sem alterar regras de negócio.

### ✨ Destaques
- 🎨 **Interface Moderna** — Tema *Dracula*, animações, partículas/confetti.  
- 🧠 **Multitemas** — Emojis, Matemática, Química.  
- 🏆 **Gamificação** — Pontuação, combos, estrelas e ranking local.  
- 🔊 **Áudio Completo** — Flip, match, erro, vitória, clique.  
- 🔄 **Fluxo Completo** — Login → Menu → Jogo → Game Over → Ranking.

---

## 📂 Estrutura do Projeto

```plaintext
memory-game/
├── assets/                  # Recursos estáticos
│   └── sounds/              # Arquivos .wav (flip, match, error, win, click)
├── src/
│   ├── domain/              # Regras de Negócio Puras (Enterprise Logic)
│   │   ├── board.py         # Lógica da grade e pares
│   │   ├── card.py          # Estado da carta (revelada, par encontrado)
│   │   └── strategies.py    # Strategy Pattern para geração de conteúdo
│   ├── infrastructure/      # Acesso a dados e IO
│   │   ├── repository.py    # Persistência de Score (JSON)
│   │   └── sound.py         # Gerenciador de Áudio (Pygame Mixer)
│   ├── services/            # Casos de Uso (Application Logic)
│   │   └── game_service.py  # Pontuação, combos e regras do jogo
│   ├── ui/                  # Interface do Usuário (Pygame)
│   │   ├── components.py    # Botões, inputs, partículas
│   │   ├── gui.py           # Tela do jogo + overlay de Game Over
│   │   ├── menu.py          # Tela de seleção de tema e dificuldade
│   │   ├── ranking.py       # Leaderboard local
│   │   └── styles.py        # Cores, dimensões e tema visual
│   └── manager.py           # State Manager (máquina de estados)
├── tests/                   # Testes automatizados (Pytest)
├── scores.json              # Banco de dados local
├── run_game.py              # Ponto de entrada
└── pyproject.toml           # Dependências
```


## 🧩 Arquitetura e Design Patterns

### 🔧 Strategy Pattern
Permite múltiplos tipos de conteúdo sem alterar o tabuleiro:

| Estratégia         | Exemplo            |
|--------------------|--------------------|
| EmojiStrategy      | 🐶🐶, 🚀🚀          |
| MathStrategy       | “2+2” ↔ “4”        |
| ChemistryStrategy  | “Fe” ↔ “Ferro”     |

---

### 🔄 State Pattern
O `GameManager` controla o fluxo:

LOGIN → MENU → GAME → RANKING
---

### 💾 Repository Pattern
A persistência de scores é isolada em `repository.py`.  
Fácil migração para SQLite/PostgreSQL no futuro.

---

## 🏆 Regras do Jogo

### 🎯 Sistema de Pontuação
- **100 pontos por par correto**
- **Combo progressivo:** x1, x2, x3…
- **Multiplicador por dificuldade:**
  - Fácil: **1.0x**
  - Médio: **1.5x**
  - Difícil: **2.0x**
- **Erros:** reduzem pontos e zeram combo

---

### ⭐ Sistema de Estrelas
Baseado na eficiência:

| Estrelas | Desempenho            |
|----------|------------------------|
| ⭐⭐⭐     | Perfeito ou quase      |
| ⭐⭐      | Bom                    |
| ⭐       | Completou, mas com erros |

---

## 🚀 Instalação e Execução

### 📌 Pré-requisitos
- Python **3.10+**
- Pygame
- Arquivos `.wav` em `assets/sounds/`

### 📦 Instalar dependências
```bash
pip install pygame pytest
```

## ▶️ Rodar o jogo

```
python run_game.py
```

## 🧪 Rodar testes

```
pytest tests/
```

# 🛠️ Como Estender o Projeto

## ➕ Adicionar um novo tema

Edite strategies.py:

```
"Dinossauros": ["🦖", "🦕", "🌋"]
```

Registre no menu (menu.py):

```
{"text": "Dinos", "icon": "🦖", "value": "Dinossauros", "rect": None}
```

## 🎨 Alterar o design
Modifique o dicionário COLORS em styles.py.


# 🌐 Roadmap — Versão 4 (Migração Web)

## Backend (API)
* Reutilizar domain + services
* Criar API com Flask/FastAPI
* Endpoints:
    * /start_game
    * /pick_card
* Migrar JSON → SQLite/PostgreSQL

## Frontend (Web)
* Reescrever UI em HTML5/CSS3/JS
* Framework sugerido: React ou Vue
* Consumir API Python

# 📌 Status Atual
### ✔️ Versão Desktop V3.0 — Finalizada e Estável

