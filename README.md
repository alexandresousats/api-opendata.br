# 🇧🇷 API OpenData BR — Calendário Brasileiro

[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-Stdlib%20Ready-brightgreen.svg)](#como-executar)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](Dockerfile)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blueviolet.svg)](.github/workflows/ci.yml)

API RESTful pública e de código aberto contendo todas as informações sobre as datas do calendário brasileiro de 2026: **Feriados Nacionais**, **Pontos Facultativos**, **Datas Comemorativas**, **Campanhas Mensais de Saúde** e **Fases da Lua**, extraídas e estruturadas a partir do [Calendarr Brasil](https://www.calendarr.com/brasil/).

---

## 📋 Sumário
- [Recursos e Estatísticas](#-recursos-e-estatísticas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Executar](#-como-executar)
  - [Opção 1: Zero Dependências (Biblioteca Padrão)](#opção-1-zero-dependências-recomendado-para-início-rápido)
  - [Opção 2: FastAPI + Uvicorn](#opção-2-fastapi--uvicorn)
  - [Opção 3: Docker & Docker Compose](#opção-3-docker--docker-compose)
- [Rotas e Endpoints da API](#-rotas-e-endpoints-da-api)
- [Exemplos de Uso com cURL](#-exemplos-de-uso-com-curl)
- [Documentação Swagger / OpenAPI](#-documentação-swagger--openapi)
- [Testes Automatizados](#-testes-automatizados)
- [Fonte dos Dados](#-fonte-dos-dados)
- [Licença](#-licença)

---

## 📊 Recursos e Estatísticas

- **+1.040 celebrações registradas** cobrindo todos os 12 meses do ano.
- **11 Feriados Nacionais Oficiais** (Confraternização Universal, Carnaval, Paixão de Cristo, Tiradentes, Dia do Trabalho, Independência do Brasil, Nossa Senhora Aparecida, Finados, Proclamação da República, Dia da Consciência Negra, Natal).
- **7 Pontos Facultativos** regulamentares (Segunda de Carnaval, Quarta-feira de Cinzas até 14h, Corpus Christi, pós-Corpus Christi, Dia do Servidor Público, Vésperas de Natal e Ano-Novo).
- **Fases da Lua (Lua Nova, Crescente, Cheia e Minguante)** detalhadas mês a mês.
- **Metadados dos Meses**: Dias totais, contagem de dias úteis, estações do ano e campanhas de saúde (Janeiro Branco, Fevereiro Roxo/Laranja, Março Azul, Abril Azul/Verde, Maio Amarelo, Junho Vermelho, Julho Amarelo, Agosto Dourado, Setembro Amarelo, Outubro Rosa, Novembro Azul, Dezembro Vermelho).

---

## 📁 Estrutura do Projeto

```text
api-opendata/
├── .github/
│   └── workflows/
│       └── ci.yml                 # Integração contínua (CI)
├── data/
│   ├── datas_brasil_2026.json     # Base completa com +1.040 datas estruturadas
│   ├── fases_lua_2026.json        # Ciclo lunar completo de 2026
│   └── meses_2026.json            # Metadados e dias úteis dos 12 meses
├── scripts/
│   ├── extract_and_generate.py    # Script de extração e mapeamento base
│   └── generate_full_database.py  # Gerador dos datasets em JSON
├── src/
│   ├── __init__.py
│   ├── database.py                # Camada de consulta, paginação e filtros
│   ├── server.py                  # Servidor REST HTTP nativo com Swagger embutido
│   └── app_fastapi.py             # Aplicação alternativa moderna com FastAPI
├── tests/
│   ├── __init__.py
│   └── test_api.py                # Suíte de testes automatizados unitários e de integração
├── .gitignore
├── Dockerfile                     # Imagem Docker otimizada
├── docker-compose.yml             # Orquestração de contêineres
├── LICENSE                        # Licença MIT
├── Makefile                       # Atalhos úteis de desenvolvimento
├── main.py                        # Ponto de entrada unificado
├── README.md                      # Documentação completa
└── requirements.txt               # Dependências opcionais (FastAPI / Uvicorn)
```

---

## 🚀 Como Executar

### Opção 1: Zero Dependências (Recomendado para início rápido)
Não necessita instalar nenhuma biblioteca via `pip`. O projeto roda diretamente com o Python 3.9+:

```bash
python3 main.py
```
O servidor estará disponível em: **`http://localhost:8000`**

### Opção 2: FastAPI + Uvicorn
Para quem prefere a experiência assíncrona com validação Pydantic:

```bash
pip install -r requirements.txt
python3 main.py --fastapi
```
Ou diretamente com o Uvicorn:
```bash
uvicorn src.app_fastapi:app --reload --port 8000
```

### Opção 3: Docker & Docker Compose
```bash
# Com Docker Compose
docker compose up -d

# Ou construindo a imagem manualmente
docker build -t api-opendata-br .
docker run -p 8000:8000 api-opendata-br
```

---

## 📡 Rotas e Endpoints da API

| Método | Endpoint | Descrição | Parâmetros de Query |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Informações gerais, versão e links rápidos | — |
| `GET` | `/api/v1/health` | Status de saúde do serviço e tempo ativo | — |
| `GET` | `/api/v1/datas` | Lista todas as datas com paginação e filtros | `mes`, `dia`, `tipo`, `categoria`, `busca`, `pagina`, `limite`, `ordem` |
| `GET` | `/api/v1/datas/{id}` | Busca os dados completos de uma data específica pelo ID | — |
| `GET` | `/api/v1/feriados` | Lista feriados nacionais e pontos facultativos | `apenas_nacionais=true\|false` |
| `GET` | `/api/v1/meses` | Lista os 12 meses com dias úteis, campanhas e contagens | — |
| `GET` | `/api/v1/meses/{mes}` | Detalhes de um mês (por número `1-12` ou nome `outubro`) | — |
| `GET` | `/api/v1/lua` | Fases da lua ao longo do ano | `mes=1..12` |
| `GET` | `/api/v1/hoje` | Retorna o que se comemora no dia atual | `data=YYYY-MM-DD` (opcional) |
| `GET` | `/api/v1/categorias` | Relação de categorias temáticas e contagem de eventos | — |
| `GET` | `/api/v1/estatisticas` | Métricas consolidadas do calendário brasileiro | — |
| `GET` | `/docs` | Interface gráfica interativa (Swagger UI) | — |
| `GET` | `/openapi.json` | Especificação completa no padrão OpenAPI 3.0 | — |

---

## 💻 Exemplos de Uso com cURL

### 1. Consultar todos os feriados nacionais oficiais
```bash
curl -X GET "http://localhost:8000/api/v1/feriados?apenas_nacionais=true"
```
**Exemplo de Resposta:**
```json
{
  "total": 11,
  "apenas_nacionais": true,
  "feriados": [
    {
      "id": "br-2026-01-01-dia-da-confraternizacao-unive",
      "ano": 2026,
      "mes": 1,
      "dia": 1,
      "data": "2026-01-01",
      "dia_semana": "Quinta-feira",
      "titulo": "Dia da Confraternização Universal (1º de janeiro)",
      "tipo": "feriado_nacional",
      "categoria": "Nacional",
      "fonte": "https://www.calendarr.com/brasil/"
    },
    {
      "id": "br-2026-04-21-dia-de-tiradentes",
      "ano": 2026,
      "mes": 4,
      "dia": 21,
      "data": "2026-04-21",
      "dia_semana": "Terça-feira",
      "titulo": "Dia de Tiradentes",
      "tipo": "feriado_nacional",
      "categoria": "Nacional",
      "fonte": "https://www.calendarr.com/brasil/"
    }
  ]
}
```

### 2. Buscar por palavra-chave (Ex: "professor")
```bash
curl -X GET "http://localhost:8000/api/v1/datas?busca=professor"
```

### 3. Consultar as fases da lua de Outubro
```bash
curl -X GET "http://localhost:8000/api/v1/lua?mes=10"
```

### 4. Consultar o que se comemora hoje
```bash
curl -X GET "http://localhost:8000/api/v1/hoje"
```

### 5. Consultar estatísticas e dias úteis de um mês
```bash
curl -X GET "http://localhost:8000/api/v1/meses/10"
```

---

## 📖 Documentação Swagger / OpenAPI

A API conta com documentação interativa embutida acessível diretamente pelo navegador:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **OpenAPI Schema:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 🧪 Testes Automatizados

Para executar os testes com a biblioteca padrão:
```bash
python3 tests/test_api.py
```
Ou usando o `Makefile`:
```bash
make test
```

---

## 🔗 Fonte dos Dados

Os dados foram extraídos e normalizados a partir do portal **[Calendarr Brasil](https://www.calendarr.com/brasil/)**, cobrindo o calendário de 2026:
- [Feriados Nacionais 2026](https://www.calendarr.com/brasil/feriados-2026/)
- [Datas Comemorativas 2026](https://www.calendarr.com/brasil/datas-comemorativas-2026/)
- [Calendário Lunar 2026](https://www.calendarr.com/brasil/calendario-lunar-2026/)

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE). Sinta-se livre para usar, estudar, modificar e distribuir.
