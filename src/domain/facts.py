# ARQUIVO: src/domain/facts.py
"""
Base de dados de fatos educacionais para o jogo.

Contém informações interessantes sobre elementos químicos, animais,
países, conceitos matemáticos e muito mais.
"""

from typing import Dict, Optional


class FactsDatabase:
    """
    Gerenciador de fatos educacionais organizados por tema.

    Fornece informações contextuais que enriquecem a experiência
    de aprendizado do jogador.
    """

    # Base de dados central
    FACTS: Dict[str, Dict[str, dict]] = {
        "Química": {
            "H": {
                "name": "Hidrogênio",
                "fact": "É o elemento mais abundante do universo, representando 75% da matéria!",
                "emoji": "💧",
                "color": (100, 180, 255),
                "extra": "Símbolo: H | Número Atômico: 1",
            },
            "He": {
                "name": "Hélio",
                "fact": "Faz balões flutuarem porque é mais leve que o ar!",
                "emoji": "🎈",
                "color": (255, 200, 100),
                "extra": "Símbolo: He | Número Atômico: 2",
            },
            "C": {
                "name": "Carbono",
                "fact": "Base de toda vida na Terra! Está presente em todos os seres vivos.",
                "emoji": "💎",
                "color": (50, 50, 50),
                "extra": "Símbolo: C | Número Atômico: 6",
            },
            "O": {
                "name": "Oxigênio",
                "fact": "Essencial para a respiração! Representa 21% do ar que respiramos.",
                "emoji": "🌬️",
                "color": (100, 200, 255),
                "extra": "Símbolo: O | Número Atômico: 8",
            },
            "Fe": {
                "name": "Ferro",
                "fact": "É o 4º elemento mais abundante da crosta terrestre! Usado há 5000 anos.",
                "emoji": "🔩",
                "color": (200, 100, 50),
                "extra": "Símbolo: Fe | Número Atômico: 26",
            },
            "Au": {
                "name": "Ouro",
                "fact": "Não enferruja e é excelente condutor! Usado em eletrônicos de precisão.",
                "emoji": "💰",
                "color": (255, 215, 0),
                "extra": "Símbolo: Au | Número Atômico: 79",
            },
            "Ag": {
                "name": "Prata",
                "fact": "Melhor condutor de eletricidade de todos os elementos!",
                "emoji": "🥈",
                "color": (192, 192, 192),
                "extra": "Símbolo: Ag | Número Atômico: 47",
            },
            "Cu": {
                "name": "Cobre",
                "fact": "Usado em fios elétricos por sua excelente condutividade!",
                "emoji": "🔌",
                "color": (184, 115, 51),
                "extra": "Símbolo: Cu | Número Atômico: 29",
            },
            "Na": {
                "name": "Sódio",
                "fact": "Componente do sal de cozinha (NaCl)! Essencial para o corpo humano.",
                "emoji": "🧂",
                "color": (255, 255, 150),
                "extra": "Símbolo: Na | Número Atômico: 11",
            },
            "Ca": {
                "name": "Cálcio",
                "fact": "Fundamental para ossos e dentes fortes! Presente no leite.",
                "emoji": "🦴",
                "color": (255, 255, 255),
                "extra": "Símbolo: Ca | Número Atômico: 20",
            },
            "Zn": {
                "name": "Zinco",
                "fact": "Essencial para o sistema imunológico! Ajuda na cicatrização.",
                "emoji": "💊",
                "color": (150, 150, 160),
                "extra": "Símbolo: Zn | Número Atômico: 30",
            },
            "Al": {
                "name": "Alumínio",
                "fact": "Metal leve e resistente! Usado em aviões e embalagens.",
                "emoji": "✈️",
                "color": (200, 200, 210),
                "extra": "Símbolo: Al | Número Atômico: 13",
            },
            "F": {
                "name": "Flúor",
                "fact": "Protege os dentes contra cáries! Presente em pastas de dente.",
                "emoji": "🦷",
                "color": (220, 255, 220),
                "extra": "Símbolo: F | Número Atômico: 9",
            },
            "Pb": {
                "name": "Chumbo",
                "fact": "Metal pesado muito denso! Usado em proteção contra raios-X.",
                "emoji": "⚠️",
                "color": (100, 100, 120),
                "extra": "Símbolo: Pb | Número Atômico: 82",
            },
            "U": {
                "name": "Urânio",
                "fact": "Elemento radioativo! Usado em usinas nucleares.",
                "emoji": "☢️",
                "color": (100, 200, 100),
                "extra": "Símbolo: U | Número Atômico: 92",
            },
            "As": {
                "name": "Arsênio",
                "fact": "Usado em semicondutores! Também tem aplicações em medicina.",
                "emoji": "🔬",
                "color": (150, 180, 150),
                "extra": "Símbolo: As | Número Atômico: 33",
            },
            "Zr": {
                "name": "Zircônio",
                "fact": "Extremamente resistente à corrosão! Usado em jóias e reatores.",
                "emoji": "💍",
                "color": (200, 200, 200),
                "extra": "Símbolo: Zr | Número Atômico: 40",
            },
            "Pt": {
                "name": "Platina",
                "fact": "Mais raro que ouro! Usado em catalisadores automotivos.",
                "emoji": "⚗️",
                "color": (230, 230, 230),
                "extra": "Símbolo: Pt | Número Atômico: 78",
            },
            "Sn": {
                "name": "Estanho",
                "fact": "Usado em soldas eletrônicas! Muito maleável.",
                "emoji": "🔧",
                "color": (180, 180, 190),
                "extra": "Símbolo: Sn | Número Atômico: 50",
            },
            "Hg": {
                "name": "Mercúrio",
                "fact": "Único metal líquido em temperatura ambiente!",
                "emoji": "🌡️",
                "color": (200, 200, 220),
                "extra": "Símbolo: Hg | Número Atômico: 80",
            },
            "I": {
                "name": "Iodo",
                "fact": "Essencial para a tireoide! Presente no sal iodado.",
                "emoji": "🧂",
                "color": (120, 0, 120),
                "extra": "Símbolo: I | Número Atômico: 53",
            },
            "N": {
                "name": "Nitrogênio",
                "fact": "Compõe 78% do ar que respiramos!",
                "emoji": "💨",
                "color": (100, 150, 255),
                "extra": "Símbolo: N | Número Atômico: 7",
            },
            "P": {
                "name": "Fósforo",
                "fact": "Presente no DNA e ATP! Essencial para energia celular.",
                "emoji": "⚡",
                "color": (255, 100, 100),
                "extra": "Símbolo: P | Número Atômico: 15",
            },
            "S": {
                "name": "Enxofre",
                "fact": "Cheiro de ovo podre! Usado em pólvora e borracha.",
                "emoji": "🎆",
                "color": (255, 255, 100),
                "extra": "Símbolo: S | Número Atômico: 16",
            },
            "Cl": {
                "name": "Cloro",
                "fact": "Desinfeta água de piscina! Forma o sal com sódio (NaCl).",
                "emoji": "🏊",
                "color": (100, 255, 100),
                "extra": "Símbolo: Cl | Número Atômico: 17",
            },
            "K": {
                "name": "Potássio",
                "fact": "Regula batimentos cardíacos! Abundante em bananas.",
                "emoji": "🍌",
                "color": (255, 200, 100),
                "extra": "Símbolo: K | Número Atômico: 19",
            },
        },
        "Animais": {
            "🐶": {
                "name": "Cachorro",
                "fact": "Possui 300 milhões de receptores olfativos! 50x mais que humanos.",
                "scientific": "Canis lupus familiaris",
                "curiosity": "Podem entender até 250 palavras e gestos!",
            },
            "🐱": {
                "name": "Gato",
                "fact": "Passa 70% da vida dormindo! Isso é cerca de 16 horas por dia.",
                "scientific": "Felis catus",
                "curiosity": "Ronronam a 26 vibrações por segundo!",
            },
            "🐘": {
                "name": "Elefante",
                "fact": "Maior animal terrestre! Pode pesar até 6 toneladas.",
                "scientific": "Loxodonta africana",
                "curiosity": "Têm memória excepcional e podem reconhecer amigos após anos!",
            },
            "🦁": {
                "name": "Leão",
                "fact": "Rei da selva! Rugido pode ser ouvido a 8km de distância.",
                "scientific": "Panthera leo",
                "curiosity": "São os únicos felinos que vivem em grupos (alcateias)!",
            },
            "🐬": {
                "name": "Golfinho",
                "fact": "Um dos animais mais inteligentes! Usam ecolocalização para caçar.",
                "scientific": "Delphinus delphis",
                "curiosity": "Cada golfinho tem um 'apito' único, como um nome!",
            },
            "🦅": {
                "name": "Águia",
                "fact": "Visão 8x mais aguçada que humanos! Conseguem ver uma presa a 3km.",
                "scientific": "Aquila chrysaetos",
                "curiosity": "Podem voar a mais de 300 km/h em mergulho!",
            },
            "🐝": {
                "name": "Abelha",
                "fact": "Polinizam 1/3 dos alimentos que comemos! Essenciais para agricultura.",
                "scientific": "Apis mellifera",
                "curiosity": "Uma colmeia pode ter até 80.000 abelhas!",
            },
            "🐙": {
                "name": "Polvo",
                "fact": "Têm 3 corações e sangue azul! Extremamente inteligentes.",
                "scientific": "Octopus vulgaris",
                "curiosity": "Podem mudar de cor em menos de 1 segundo!",
            },
        },
        "Bandeiras": {
            "🇧🇷": {
                "name": "Brasil",
                "fact": "Único país que fala português na América! 5º maior país do mundo.",
                "capital": "Brasília",
                "population": "215 milhões",
                "curiosity": "Possui a maior floresta tropical do planeta!",
            },
            "🇺🇸": {
                "name": "Estados Unidos",
                "fact": "50 estados unidos! Nome oficial: United States of America.",
                "capital": "Washington D.C.",
                "population": "331 milhões",
                "curiosity": "A bandeira já teve 27 versões diferentes!",
            },
            "🇯🇵": {
                "name": "Japão",
                "fact": "Terra do Sol Nascente! Composto por mais de 6.800 ilhas.",
                "capital": "Tóquio",
                "population": "125 milhões",
                "curiosity": "Possui mais de 200 vulcões, 60 ativos!",
            },
            "🇫🇷": {
                "name": "França",
                "fact": "País mais visitado do mundo! Recebe 90 milhões de turistas/ano.",
                "capital": "Paris",
                "population": "67 milhões",
                "curiosity": "Inventou o cinema e a fotografia!",
            },
            "🇨🇳": {
                "name": "China",
                "fact": "País mais populoso! 1,4 bilhão de habitantes.",
                "capital": "Pequim",
                "population": "1.4 bilhões",
                "curiosity": "A Grande Muralha tem mais de 21.000 km!",
            },
        },
        "Espaço": {
            "🚀": {
                "name": "Foguete",
                "fact": "Precisa atingir 28.000 km/h para escapar da gravidade terrestre!",
                "curiosity": "O primeiro foguete foi lançado em 1926 por Robert Goddard.",
            },
            "🌍": {
                "name": "Terra",
                "fact": "Único planeta conhecido com vida! Tem 4,5 bilhões de anos.",
                "curiosity": "71% da superfície é coberta por água!",
            },
            "🌕": {
                "name": "Lua",
                "fact": "Está se afastando da Terra 3,8 cm por ano!",
                "curiosity": "Apenas 12 pessoas já pisaram na Lua.",
            },
            "⭐": {
                "name": "Estrela",
                "fact": "O Sol é uma estrela de tamanho médio! Existem bilhões maiores.",
                "curiosity": "Estrelas nascem em nuvens de gás chamadas nebulosas.",
            },
            "🪐": {
                "name": "Saturno",
                "fact": "Seus anéis são feitos de gelo e rocha! Tem 82 luas conhecidas.",
                "curiosity": "É tão leve que flutuaria na água!",
            },
        },
        "Matemática": {
            "2+2": {
                "result": "4",
                "fact": "A soma mais básica! Fundamento da aritmética.",
                "curiosity": "2+2=4 é verdade em qualquer sistema numérico acima da base 3!",
            },
            "3+5": {
                "result": "8",
                "fact": "Exemplo de adição com números diferentes!",
                "curiosity": "A propriedade comutativa diz que 3+5 = 5+3!",
            },
            "10-3": {
                "result": "7",
                "fact": "Subtração representa 'tirar' ou 'diferença'.",
                "curiosity": "É a operação inversa da adição!",
            },
            "4x4": {
                "result": "16",
                "fact": "Multiplicação é uma soma repetida! 4+4+4+4 = 16",
                "curiosity": "16 é um número quadrado perfeito: 4²!",
            },
        },
    }

    @classmethod
    def get_fact(cls, theme: str, identifier: str) -> Optional[dict]:
        """
        Busca um fato educacional.

        Args:
            theme: Tema do jogo (ex: "Química", "Animais")
            identifier: Identificador do item (ex: "Fe", "🐶")

        Returns:
            Dicionário com informações educacionais ou None
        """
        if theme not in cls.FACTS:
            return None

        return cls.FACTS[theme].get(identifier)

    @classmethod
    def has_facts(cls, theme: str) -> bool:
        """
        Verifica se um tema possui fatos cadastrados.

        Args:
            theme: Nome do tema

        Returns:
            True se o tema tem fatos, False caso contrário
        """
        return theme in cls.FACTS

    @classmethod
    def get_all_themes(cls) -> list[str]:
        """
        Retorna lista de todos os temas com fatos.

        Returns:
            Lista de nomes de temas
        """
        return list(cls.FACTS.keys())

    @classmethod
    def add_fact(cls, theme: str, identifier: str, fact_data: dict) -> None:
        """
        Adiciona um novo fato à base de dados.

        Args:
            theme: Tema do jogo
            identifier: Identificador único
            fact_data: Dicionário com informações do fato
        """
        if theme not in cls.FACTS:
            cls.FACTS[theme] = {}

        cls.FACTS[theme][identifier] = fact_data

    @classmethod
    def get_random_fact(cls, theme: str) -> Optional[dict]:
        """
        Retorna um fato aleatório de um tema.

        Args:
            theme: Nome do tema

        Returns:
            Dicionário com fato aleatório ou None
        """
        import random

        if theme not in cls.FACTS or not cls.FACTS[theme]:
            return None

        identifier = random.choice(list(cls.FACTS[theme].keys()))
        return cls.FACTS[theme][identifier]
