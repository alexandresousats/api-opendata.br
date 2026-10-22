# 🇧🇷 OpenData BR — API e Dados Abertos do Calendário Brasileiro

[![Repository](https://img.shields.io/badge/GitHub-alexandresousats%2Fapi--opendata.br-181717?style=flat&logo=github)](https://github.com/alexandresousats/api-opendata.br.git)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-Stdlib%20Ready-brightgreen.svg)](#-como-executar)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](Dockerfile)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blueviolet.svg)](.github/workflows/ci.yml)

API RESTful pública, leve e de código aberto projetada para fornecer acesso centralizado, estruturado e padronizado a todas as informações do calendário brasileiro: **Feriados Nacionais**, **Pontos Facultativos**, **Datas Comemorativas**, **Campanhas de Conscientização da Saúde** e **Fases da Lua**.

🔗 **Repositório Oficial:** [https://github.com/alexandresousats/api-opendata.br.git](https://github.com/alexandresousats/api-opendata.br.git)

---

## 🎯 Propósito do Projeto

O calendário brasileiro é repleto de particularidades: marcos históricos e culturais, leis federais que instituem novos feriados nacionais, pontos facultativos da administração pública, campanhas cívicas e sanitárias mensais, além de centenas de datas comemorativas profissionais e sociais.

Historicamente, desenvolvedores de software, analistas de dados, plataformas de e-commerce, sistemas de RH/Departamento Pessoal e equipes de marketing enfrentam as mesmas dores recorrentes:
- Falta de dados públicos estruturados em formatos modernos (JSON, REST).
- Dispersão de informações em tabelas soltas, decretos governamentais em PDF ou calendários impressos.
- Dificuldade para calcular dias úteis, prever folgas bancárias e programar campanhas sazonais com precisão.
- Dependência de serviços proprietários, pagos ou que exigem chaves de API restritivas.

O **OpenData BR** foi criado com o propósito de ser uma **infraestrutura pública e aberta de dados temporais do Brasil**. Ele resolve essas barreiras entregando:
1. **Dados Confiáveis e Atualizados:** Feriados nacionais oficiais em estrita conformidade com as leis federais vigentes (Lei nº 662/1949, Lei nº 10.607/2002 e a recente Lei nº 14.759/2023, que consagrou o Dia Nacional de Zumbi e da Consciência Negra).
2. **Arquitetura Zero Dependências:** Um servidor HTTP nativo pronto para produção construído exclusivamente com a biblioteca padrão do Python (`http.server`), sem necessidade de `pip install`.
3. **Flexibilidade Moderna:** Suporte opcional imediato para **FastAPI**, documentação interativa **Swagger/OpenAPI**, Docker, Docker Compose e pipeline de CI/CD via GitHub Actions.
4. **Pronto para Integrações:** Respostas em JSON limpo com paginação, filtros por mês, dia, categoria e busca textual fonética/semântica.

---

## 📊 O que está incluído no Dataset

| Dimensão | Quantidade / Detalhes | Exemplos / Descrição |
| :--- | :--- | :--- |
| **Datas Comemorativas** | **+1.040 celebrações** | Profissionais, históricas, cívicas, ambientais e culturais |
| **Feriados Nacionais** | **11 feriados oficiais** | Confraternização Universal, Tiradentes, 7 de Setembro, Consciência Negra, Natal, etc. |
| **Pontos Facultativos** | **7 datas federais** | Carnaval, Quarta de Cinzas, Corpus Christi, Dia do Servidor Público, Vésperas |
| **Campanhas de Saúde** | **25 campanhas mensais** | Janeiro Branco/Roxo, Maio Amarelo, Setembro Amarelo, Outubro Rosa, Novembro Azul |
| **Ciclo Lunar Completo** | **49 fases astronômicas** | Datas exatas de Lua Nova, Quarto Crescente, Lua Cheia e Quarto Minguante |
| **Metadados dos 12 Meses** | **Dias totais e dias úteis** | Calendário de trabalho, contagem de feriados e estações climáticas |

---

## 📁 Estrutura do Repositório

```text
api-opendata/
├── .github/
│   └── workflows/
│       └── ci.yml                 # Pipeline automatizado de testes e linting
├── data/
│   ├── datas_brasil_2026.json     # Base estruturada com +1.040 celebrações brasileiras
│   ├── fases_lua_2026.json        # Calendário lunar completo com as 49 fases
│   └── meses_2026.json            # Metadados dos 12 meses (dias úteis, campanhas e estações)
├── scripts/
│   ├── extract_and_generate.py    # Script utilitário de processamento de dados
│   └── generate_full_database.py  # Construtor e normalizador dos arquivos JSON
├── src/
│   ├── __init__.py
│   ├── database.py                # Camada de persistência em memória, filtros e paginação
│   ├── server.py                  # Servidor REST HTTP nativo (Zero Dependencies) com Swagger
│   └── app_fastapi.py             # Aplicação alternativa de alto desempenho com FastAPI
├── tests/
│   ├── __init__.py
│   └── test_api.py                # Suíte de testes automatizados com cobertura completa
├── .gitignore                     # Filtro de arquivos e diretórios ignorados
├── Dockerfile                     # Construção de contêiner enxuta e segura
├── docker-compose.yml             # Orquestrador local de contêineres
├── LICENSE                        # Licença permissiva MIT
├── Makefile                       # Comandos simplificados de execução e teste
├── main.py                        # Entrypoint com seletor de runtime (--fastapi ou stdlib)
├── README.md                      # Documentação completa do projeto
└── requirements.txt               # Dependências opcionais (FastAPI e Uvicorn)
```

---

## 🚀 Como Executar

O projeto oferece três modos simples de execução:

### 1. Modo Nativo — Zero Dependências (Recomendado)
Não requer a instalação de pacotes externos. Funciona diretamente com qualquer instalação do Python 3.9+:

```bash
python3 main.py
```
> O servidor iniciará em **`http://localhost:8000`** com documentação interativa embutida em **`http://localhost:8000/docs`**.

---

### 2. Modo FastAPI + Uvicorn
Para ambientes que demandam servidores assíncronos ASGI de alta performance e validação estrita com Pydantic:

```bash
# 1. Instale as dependências opcionais
pip install -r requirements.txt

# 2. Inicie via main.py com o seletor --fastapi
python3 main.py --fastapi

# Ou diretamente com o Uvicorn
uvicorn src.app_fastapi:app --reload --port 8000
```

---

### 3. Modo Docker & Docker Compose
Para isolamento completo e deploy simplificado em servidores de homologação ou produção:

```bash
# Usando o Docker Compose
docker compose up -d

# Ou construindo a imagem manualmente
docker build -t api-opendata-br .
docker run -d -p 8000:8000 --name api-opendata-br api-opendata-br
```

---

## 📡 Rotas e Endpoints da API

Todas as rotas retornam respostas no padrão JSON codificadas em UTF-8.

| Método | Endpoint | Descrição | Parâmetros de Consulta (*Query Params*) |
| :---: | :--- | :--- | :--- |
| `GET` | `/` | Metadados do projeto, status e links úteis | — |
| `GET` | `/api/v1/health` | Verificação de integridade (*Health Check*) e uptime | — |
| `GET` | `/api/v1/datas` | Catálogo completo de datas com paginação e busca | `mes`, `dia`, `tipo`, `categoria`, `busca`, `pagina`, `limite`, `ordem` |
| `GET` | `/api/v1/datas/{id}` | Busca detalhada de uma celebração pelo ID único | — |
| `GET` | `/api/v1/feriados` | Lista feriados nacionais e pontos facultativos | `apenas_nacionais=true\|false` |
| `GET` | `/api/v1/meses` | Resumo dos 12 meses (dias úteis, campanhas e contagens) | — |
| `GET` | `/api/v1/meses/{mes}` | Detalhes de um mês por número (`1-12`) ou nome (`outubro`) | — |
| `GET` | `/api/v1/lua` | Fases da lua ao longo do ano | `mes=1..12` |
| `GET` | `/api/v1/hoje` | Comemorações do dia atual ou de data específica | `data=YYYY-MM-DD` (opcional) |
| `GET` | `/api/v1/categorias` | Relação de categorias temáticas com contagem | — |
| `GET` | `/api/v1/estatisticas` | Métricas consolidadas de feriados e eventos do ano | — |
| `GET` | `/docs` | Interface Swagger interativa com documentação visual | — |
| `GET` | `/openapi.json` | Especificação completa no padrão OpenAPI 3.0 | — |

---

## 💻 Exemplos de Consumo da API

### Consultar Feriados Nacionais Oficiais
```bash
curl -s -X GET "http://localhost:8000/api/v1/feriados?apenas_nacionais=true" | jq
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
      "categoria": "Nacional"
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
      "categoria": "Nacional"
    },
    {
      "id": "br-2026-11-20-dia-nacional-de-zumbi-e-da-co",
      "ano": 2026,
      "mes": 11,
      "dia": 20,
      "data": "2026-11-20",
      "dia_semana": "Sexta-feira",
      "titulo": "Dia Nacional de Zumbi e da Consciência Negra",
      "tipo": "feriado_nacional",
      "categoria": "Nacional"
    }
  ]
}
```

---

### Buscar Datas por Palavra-Chave (Ex: "professor")
```bash
curl -s -X GET "http://localhost:8000/api/v1/datas?busca=professor" | jq
```

---

### Consultar Dias Úteis e Campanhas de um Mês (Ex: Outubro)
```bash
curl -s -X GET "http://localhost:8000/api/v1/meses/10" | jq
```

**Exemplo de Resposta:**
```json
{
  "mes": 10,
  "nome": "Outubro",
  "dias_no_mes": 31,
  "dias_uteis": 21,
  "dias_fim_de_semana": 9,
  "feriados_nacionais_no_mes": 1,
  "campanhas_saude": [
    "Outubro Rosa (Conscientização e Prevenção do Câncer de Mama)"
  ],
  "estacao": "Primavera",
  "total_celebracoes": 114
}
```

---

### Exemplo em Python (urllib nativo — Zero Dependências)
```python
import urllib.request
import json

url = "http://localhost:8000/api/v1/hoje"

with urllib.request.urlopen(url) as response:
    dados = json.loads(response.read().decode("utf-8"))
    print(f"Data: {dados['data']} ({dados['dia_semana']})")
    for item in dados["celebracoes"]:
        print(f"- [{item['categoria']}] {item['titulo']}")
```

---

### Exemplo em JavaScript / Node.js
```javascript
const response = await fetch("http://localhost:8000/api/v1/feriados?apenas_nacionais=true");
const data = await response.json();

console.log(`Total de feriados: ${data.total}`);
data.feriados.forEach(f => {
  console.log(`${f.data} (${f.dia_semana}): ${f.titulo}`);
});
```

---

## 🧪 Testes Automatizados

O projeto inclui uma suíte completa de testes unitários e de integração utilizando o framework nativo `unittest`:

```bash
# Execução direta via Python
python3 tests/test_api.py

# Ou através do Makefile
make test
```

Os testes cobrem:
- Integridade e sintaxe de todos os arquivos JSON de dados.
- Respostas HTTP (status code, headers e payloads).
- Paginação, filtros de busca e ordenação.
- Validação das rotas `/feriados`, `/meses`, `/lua`, `/hoje`, `/categorias` e `/estatisticas`.

---

## 🛠️ Comandos Úteis (Makefile)

O repositório disponibiliza atalhos prontos para acelerar o desenvolvimento:

```bash
make run          # Inicia a API no modo nativo (Zero Dependências)
make run-fastapi  # Inicia a API com FastAPI e Uvicorn
make test         # Executa a suíte de testes automatizados
make docker-build # Constrói a imagem Docker local
make docker-run   # Executa o contêiner Docker na porta 8000
make clean        # Limpa caches temporários de Python (__pycache__)
```

---

## 🤝 Como Contribuir

Contribuições são muito bem-vindas! Se você deseja reportar um problema, sugerir novas funcionalidades ou submeter melhorias:

1. Faça um Fork do projeto: [https://github.com/alexandresousats/api-opendata.br](https://github.com/alexandresousats/api-opendata.br)
2. Crie uma branch para sua funcionalidade: `git checkout -b feature/minha-melhoria`
3. Faça commit de suas alterações: `git commit -m "feat: adiciona nova funcionalidade"`
4. Envie sua branch para o GitHub: `git push origin feature/minha-melhoria`
5. Abra um **Pull Request**.

---

## 📄 Licença

Este projeto é distribuído sob os termos da [Licença MIT](LICENSE). Você é livre para utilizar, modificar, distribuir e integrar em projetos comerciais e pessoais sem restrições.
