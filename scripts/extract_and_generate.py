# -*- coding: utf-8 -*-
"""
Script de estruturação dos dados extraídos de Calendarr Brasil (2026)
Gera os arquivos JSON do OpenData BR.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Meses e metadados gerais de 2026 no Brasil
MESES_2026 = [
    {
        "numero": 1,
        "nome": "Janeiro",
        "dias_totais": 31,
        "dias_uteis": 21,
        "campanhas_saude": [
            {"nome": "Janeiro Branco", "tema": "Saúde Mental", "periodo": "1 a 31 de janeiro"},
            {"nome": "Janeiro Roxo", "tema": "Conscientização sobre a Hanseníase", "periodo": "1 a 31 de janeiro"}
        ],
        "feriados_nacionais": ["Dia da Confraternização Universal (1º de janeiro)"]
    },
    {
        "numero": 2,
        "nome": "Fevereiro",
        "dias_totais": 28,
        "dias_uteis": 20,
        "campanhas_saude": [
            {"nome": "Fevereiro Roxo", "tema": "Lúpus, Alzheimer e Fibromialgia", "periodo": "1 a 28 de fevereiro"},
            {"nome": "Fevereiro Laranja", "tema": "Combate à Leucemia", "periodo": "1 a 28 de fevereiro"}
        ],
        "feriados_nacionais": ["Carnaval (terça-feira)"],
        "pontos_facultativos": ["Segunda-feira de Carnaval", "Quarta-feira de Cinzas (até 14h)"]
    },
    {
        "numero": 3,
        "nome": "Março",
        "dias_totais": 31,
        "dias_uteis": 22,
        "campanhas_saude": [
            {"nome": "Março Azul-Marinho", "tema": "Prevenção ao Câncer Colorretal", "periodo": "1 a 31 de março"},
            {"nome": "Março Vermelho", "tema": "Conscientização do Câncer Renal", "periodo": "1 a 31 de março"}
        ],
        "estacao": "Início do Outono (20 de março)"
    },
    {
        "numero": 4,
        "nome": "Abril",
        "dias_totais": 30,
        "dias_uteis": 20,
        "campanhas_saude": [
            {"nome": "Abril Azul", "tema": "Conscientização sobre o Autismo", "periodo": "1 a 30 de abril"},
            {"nome": "Abril Verde", "tema": "Saúde e Segurança no Trabalho", "periodo": "1 a 30 de abril"}
        ],
        "feriados_nacionais": ["Sexta-feira Santa (Paixão de Cristo)", "Dia de Tiradentes (21 de abril)"]
    },
    {
        "numero": 5,
        "nome": "Maio",
        "dias_totais": 31,
        "dias_uteis": 20,
        "campanhas_saude": [
            {"nome": "Maio Amarelo", "tema": "Segurança e Conscientização no Trânsito", "periodo": "1 a 31 de maio"},
            {"nome": "Maio Cinza", "tema": "Combate ao Câncer Cerebral", "periodo": "1 a 31 de maio"},
            {"nome": "Maio Laranja", "tema": "Combate ao Abuso e Exploração Sexual Infantil", "periodo": "1 a 31 de maio"},
            {"nome": "Maio Roxo", "tema": "Doenças Inflamatórias Intestinais", "periodo": "1 a 31 de maio"}
        ],
        "feriados_nacionais": ["Dia do Trabalho (1º de maio)"]
    },
    {
        "numero": 6,
        "nome": "Junho",
        "dias_totais": 30,
        "dias_uteis": 22,
        "campanhas_saude": [
            {"nome": "Junho Vermelho", "tema": "Incentivo à Doação de Sangue", "periodo": "1 a 30 de junho"},
            {"nome": "Junho Verde", "tema": "Proteção do Meio Ambiente", "periodo": "1 a 30 de junho"}
        ],
        "pontos_facultativos": ["Corpus Christi (4 de junho)", "Ponto Facultativo após Corpus Christi (5 de junho)"],
        "estacao": "Início do Inverno (21 de junho)"
    },
    {
        "numero": 7,
        "nome": "Julho",
        "dias_totais": 31,
        "dias_uteis": 23,
        "campanhas_saude": [
            {"nome": "Julho Amarelo", "tema": "Luta contra as Hepatites Virais", "periodo": "1 a 31 de julho"},
            {"nome": "Julho Verde", "tema": "Prevenção do Câncer de Cabeça e Pescoço", "periodo": "1 a 31 de julho"}
        ]
    },
    {
        "numero": 8,
        "nome": "Agosto",
        "dias_totais": 31,
        "dias_uteis": 21,
        "campanhas_saude": [
            {"nome": "Agosto Dourado", "tema": "Incentivo ao Aleitamento Materno", "periodo": "1 a 31 de agosto"},
            {"nome": "Agosto Verde-Claro", "tema": "Combate ao Linfoma", "periodo": "1 a 31 de agosto"}
        ]
    },
    {
        "numero": 9,
        "nome": "Setembro",
        "dias_totais": 30,
        "dias_uteis": 21,
        "campanhas_saude": [
            {"nome": "Setembro Amarelo", "tema": "Prevenção do Suicídio e Saúde Mental", "periodo": "1 a 30 de setembro"},
            {"nome": "Setembro Verde", "tema": "Incentivo à Doação de Órgãos", "periodo": "1 a 30 de setembro"}
        ],
        "feriados_nacionais": ["Dia da Independência do Brasil (7 de setembro)"],
        "estacao": "Início da Primavera (22 de setembro)"
    },
    {
        "numero": 10,
        "nome": "Outubro",
        "dias_totais": 31,
        "dias_uteis": 21,
        "campanhas_saude": [
            {"nome": "Outubro Rosa", "tema": "Prevenção e Diagnóstico Precoce do Câncer de Mama", "periodo": "1 a 31 de outubro"}
        ],
        "feriados_nacionais": ["Dia de Nossa Senhora Aparecida (12 de outubro)"],
        "pontos_facultativos": ["Dia do Servidor Público (28 de outubro)"]
    },
    {
        "numero": 11,
        "nome": "Novembro",
        "dias_totais": 30,
        "dias_uteis": 19,
        "campanhas_saude": [
            {"nome": "Novembro Azul", "tema": "Conscientização sobre Câncer de Próstata e Diabetes", "periodo": "1 a 30 de novembro"},
            {"nome": "Novembro Roxo", "tema": "Sensibilização para a Prematuridade", "periodo": "1 a 30 de novembro"}
        ],
        "feriados_nacionais": [
            "Finados (2 de novembro)",
            "Proclamação da República (15 de novembro)",
            "Dia Nacional de Zumbi e da Consciência Negra (20 de novembro)"
        ]
    },
    {
        "numero": 12,
        "nome": "Dezembro",
        "dias_totais": 31,
        "dias_uteis": 22,
        "campanhas_saude": [
            {"nome": "Dezembro Vermelho", "tema": "Prevenção e Luta contra o HIV/AIDS", "periodo": "1 a 31 de dezembro"},
            {"nome": "Dezembro Laranja", "tema": "Combate e Prevenção ao Câncer de Pele", "periodo": "1 a 31 de dezembro"}
        ],
        "feriados_nacionais": ["Natal (25 de dezembro)"],
        "pontos_facultativos": [
            "Véspera de Natal (24 de dezembro, após 13h)",
            "Véspera de Ano-Novo (31 de dezembro, após 13h)"
        ],
        "estacao": "Início do Verão (21 de dezembro)"
    }
]

# 2. Fases da Lua 2026 no Brasil (Calendarr)
FASES_LUA_2026 = [
    {"mes": 1, "mes_nome": "Janeiro", "dia": 3, "data": "2026-01-03", "fase": "Lua Cheia"},
    {"mes": 1, "mes_nome": "Janeiro", "dia": 10, "data": "2026-01-10", "fase": "Lua Minguante"},
    {"mes": 1, "mes_nome": "Janeiro", "dia": 18, "data": "2026-01-18", "fase": "Lua Nova"},
    {"mes": 1, "mes_nome": "Janeiro", "dia": 26, "data": "2026-01-26", "fase": "Lua Crescente"},

    {"mes": 2, "mes_nome": "Fevereiro", "dia": 1, "data": "2026-02-01", "fase": "Lua Cheia"},
    {"mes": 2, "mes_nome": "Fevereiro", "dia": 9, "data": "2026-02-09", "fase": "Lua Minguante"},
    {"mes": 2, "mes_nome": "Fevereiro", "dia": 17, "data": "2026-02-17", "fase": "Lua Nova"},
    {"mes": 2, "mes_nome": "Fevereiro", "dia": 24, "data": "2026-02-24", "fase": "Lua Crescente"},

    {"mes": 3, "mes_nome": "Março", "dia": 3, "data": "2026-03-03", "fase": "Lua Cheia"},
    {"mes": 3, "mes_nome": "Março", "dia": 11, "data": "2026-03-11", "fase": "Lua Minguante"},
    {"mes": 3, "mes_nome": "Março", "dia": 18, "data": "2026-03-18", "fase": "Lua Nova"},
    {"mes": 3, "mes_nome": "Março", "dia": 25, "data": "2026-03-25", "fase": "Lua Crescente"},

    {"mes": 4, "mes_nome": "Abril", "dia": 1, "data": "2026-04-01", "fase": "Lua Cheia"},
    {"mes": 4, "mes_nome": "Abril", "dia": 10, "data": "2026-04-10", "fase": "Lua Minguante"},
    {"mes": 4, "mes_nome": "Abril", "dia": 17, "data": "2026-04-17", "fase": "Lua Nova"},
    {"mes": 4, "mes_nome": "Abril", "dia": 23, "data": "2026-04-23", "fase": "Lua Crescente"},

    {"mes": 5, "mes_nome": "Maio", "dia": 1, "data": "2026-05-01", "fase": "Lua Cheia"},
    {"mes": 5, "mes_nome": "Maio", "dia": 9, "data": "2026-05-09", "fase": "Lua Minguante"},
    {"mes": 5, "mes_nome": "Maio", "dia": 16, "data": "2026-05-16", "fase": "Lua Nova"},
    {"mes": 5, "mes_nome": "Maio", "dia": 23, "data": "2026-05-23", "fase": "Lua Crescente"},
    {"mes": 5, "mes_nome": "Maio", "dia": 31, "data": "2026-05-31", "fase": "Lua Cheia"},

    {"mes": 6, "mes_nome": "Junho", "dia": 8, "data": "2026-06-08", "fase": "Lua Minguante"},
    {"mes": 6, "mes_nome": "Junho", "dia": 14, "data": "2026-06-14", "fase": "Lua Nova"},
    {"mes": 6, "mes_nome": "Junho", "dia": 21, "data": "2026-06-21", "fase": "Lua Crescente"},
    {"mes": 6, "mes_nome": "Junho", "dia": 29, "data": "2026-06-29", "fase": "Lua Cheia"},

    {"mes": 7, "mes_nome": "Julho", "dia": 7, "data": "2026-07-07", "fase": "Lua Minguante"},
    {"mes": 7, "mes_nome": "Julho", "dia": 14, "data": "2026-07-14", "fase": "Lua Nova"},
    {"mes": 7, "mes_nome": "Julho", "dia": 21, "data": "2026-07-21", "fase": "Lua Crescente"},
    {"mes": 7, "mes_nome": "Julho", "dia": 29, "data": "2026-07-29", "fase": "Lua Cheia"},

    {"mes": 8, "mes_nome": "Agosto", "dia": 5, "data": "2026-08-05", "fase": "Lua Minguante"},
    {"mes": 8, "mes_nome": "Agosto", "dia": 12, "data": "2026-08-12", "fase": "Lua Nova"},
    {"mes": 8, "mes_nome": "Agosto", "dia": 19, "data": "2026-08-19", "fase": "Lua Crescente"},
    {"mes": 8, "mes_nome": "Agosto", "dia": 28, "data": "2026-08-28", "fase": "Lua Cheia"},

    {"mes": 9, "mes_nome": "Setembro", "dia": 4, "data": "2026-09-04", "fase": "Lua Minguante"},
    {"mes": 9, "mes_nome": "Setembro", "dia": 11, "data": "2026-09-11", "fase": "Lua Nova"},
    {"mes": 9, "mes_nome": "Setembro", "dia": 18, "data": "2026-09-18", "fase": "Lua Crescente"},
    {"mes": 9, "mes_nome": "Setembro", "dia": 26, "data": "2026-09-26", "fase": "Lua Cheia"},

    {"mes": 10, "mes_nome": "Outubro", "dia": 3, "data": "2026-10-03", "fase": "Lua Minguante"},
    {"mes": 10, "mes_nome": "Outubro", "dia": 10, "data": "2026-10-10", "fase": "Lua Nova"},
    {"mes": 10, "mes_nome": "Outubro", "dia": 18, "data": "2026-10-18", "fase": "Lua Crescente"},
    {"mes": 10, "mes_nome": "Outubro", "dia": 26, "data": "2026-10-26", "fase": "Lua Cheia"},

    {"mes": 11, "mes_nome": "Novembro", "dia": 1, "data": "2026-11-01", "fase": "Lua Minguante"},
    {"mes": 11, "mes_nome": "Novembro", "dia": 9, "data": "2026-11-09", "fase": "Lua Nova"},
    {"mes": 11, "mes_nome": "Novembro", "dia": 17, "data": "2026-11-17", "fase": "Lua Crescente"},
    {"mes": 11, "mes_nome": "Novembro", "dia": 24, "data": "2026-11-24", "fase": "Lua Cheia"},

    {"mes": 12, "mes_nome": "Dezembro", "dia": 1, "data": "2026-12-01", "fase": "Lua Minguante"},
    {"mes": 12, "mes_nome": "Dezembro", "dia": 8, "data": "2026-12-08", "fase": "Lua Nova"},
    {"mes": 12, "mes_nome": "Dezembro", "dia": 17, "data": "2026-12-17", "fase": "Lua Crescente"},
    {"mes": 12, "mes_nome": "Dezembro", "dia": 23, "data": "2026-12-23", "fase": "Lua Cheia"},
    {"mes": 12, "mes_nome": "Dezembro", "dia": 30, "data": "2026-12-30", "fase": "Lua Minguante"}
]

print("Script base preparado.")
