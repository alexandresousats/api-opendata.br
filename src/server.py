# -*- coding: utf-8 -*-
"""
Servidor REST HTTP nativo da API OpenData BR
Desenvolvido com a biblioteca padrão do Python (Zero dependências externas).
Suporta roteamento REST, paginação, filtros, CORS e documentação Swagger UI integrada.
"""
import http.server
import json
import time
import urllib.parse
from datetime import datetime
from src.database import repo

START_TIME = time.time()

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "API OpenData BR - Calendário Brasileiro 2026",
        "description": "API REST pública para consulta de feriados nacionais, pontos facultativos, datas comemorativas, campanhas sazonais de saúde e fases da lua do Brasil (2026). Dados extraídos e estruturados de Calendarr Brasil.",
        "version": "1.0.0",
        "contact": {
            "name": "OpenData BR",
            "url": "https://github.com/alexandresouds/api-opendata"
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "servers": [
        {"url": "http://localhost:8000", "description": "Servidor Local"}
    ],
    "paths": {
        "/api/v1/health": {
            "get": {
                "summary": "Health Check da API",
                "responses": {"200": {"description": "Status operacional da API"}}
            }
        },
        "/api/v1/datas": {
            "get": {
                "summary": "Listar datas com filtros e paginação",
                "parameters": [
                    {"name": "mes", "in": "query", "schema": {"type": "integer"}, "description": "Filtrar por mês (1-12)"},
                    {"name": "dia", "in": "query", "schema": {"type": "integer"}, "description": "Filtrar por dia (1-31)"},
                    {"name": "tipo", "in": "query", "schema": {"type": "string"}, "description": "feriado_nacional, ponto_facultativo, comemorativa, campanha"},
                    {"name": "categoria", "in": "query", "schema": {"type": "string"}, "description": "Ex: Saúde, Educação, Esportes, etc."},
                    {"name": "busca", "in": "query", "schema": {"type": "string"}, "description": "Termo de busca no título ou categoria"},
                    {"name": "pagina", "in": "query", "schema": {"type": "integer", "default": 1}},
                    {"name": "limite", "in": "query", "schema": {"type": "integer", "default": 20}},
                    {"name": "ordem", "in": "query", "schema": {"type": "string", "enum": ["asc", "desc"]}}
                ],
                "responses": {"200": {"description": "Lista paginada de datas comemorativas e feriados"}}
            }
        },
        "/api/v1/datas/{id}": {
            "get": {
                "summary": "Obter detalhes de uma data por ID",
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}],
                "responses": {"200": {"description": "Data encontrada"}, "404": {"description": "Data não encontrada"}}
            }
        },
        "/api/v1/feriados": {
            "get": {
                "summary": "Listar Feriados Nacionais e Pontos Facultativos",
                "parameters": [
                    {"name": "apenas_nacionais", "in": "query", "schema": {"type": "boolean"}, "description": "Filtrar apenas feriados oficiais"}
                ],
                "responses": {"200": {"description": "Lista de feriados"}}
            }
        },
        "/api/v1/meses": {
            "get": {
                "summary": "Listar todos os 12 meses com estatísticas",
                "responses": {"200": {"description": "Resumo dos meses do ano"}}
            }
        },
        "/api/v1/meses/{mes}": {
            "get": {
                "summary": "Obter detalhes de um mês específico",
                "parameters": [{"name": "mes", "in": "path", "required": True, "schema": {"type": "string"}, "description": "Número do mês (1-12) ou nome"}],
                "responses": {"200": {"description": "Detalhes do mês com datas e fases lunares"}}
            }
        },
        "/api/v1/lua": {
            "get": {
                "summary": "Consultar o calendário lunar (fases da lua)",
                "parameters": [{"name": "mes", "in": "query", "schema": {"type": "integer"}}],
                "responses": {"200": {"description": "Fases da lua"}}
            }
        },
        "/api/v1/hoje": {
            "get": {
                "summary": "O que se comemora hoje no Brasil",
                "parameters": [{"name": "data", "in": "query", "schema": {"type": "string"}, "description": "Formato YYYY-MM-DD (opcional)"}],
                "responses": {"200": {"description": "Datas comemorativas do dia"}}
            }
        },
        "/api/v1/categorias": {
            "get": {
                "summary": "Listar todas as categorias e contagens",
                "responses": {"200": {"description": "Lista de categorias"}}
            }
        },
        "/api/v1/estatisticas": {
            "get": {
                "summary": "Estatísticas gerais do calendário brasileiro",
                "responses": {"200": {"description": "Métricas agregadas"}}
            }
        }
    }
}

SWAGGER_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>API OpenData BR - Documentação Swagger</title>
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
  <style>
    body { margin: 0; background: #fafafa; }
    .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
"""

class OpenDataHTTPHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Log mais limpo no terminal
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]} - {args[1]} {args[2]}")

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, status_code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, status_code: int, html: str):
        body = html.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path.rstrip("/") or "/"
        query = urllib.parse.parse_qs(parsed_url.query)

        # Helper para pegar parâmetro único
        def q(param, default=None):
            return query.get(param, [default])[0]

        # 1. Rota raiz
        if path == "" or path == "/":
            welcome = {
                "projeto": "API OpenData BR",
                "descricao": "API REST aberta do Calendário Brasileiro 2026 (Feriados, Pontos Facultativos, Datas Comemorativas e Fases da Lua).",
                "versao": "1.0.0",
                "fonte": "Calendarr Brasil (https://www.calendarr.com/brasil/)",
                "documentacao_interativa": "/docs",
                "especificacao_openapi": "/openapi.json",
                "endpoints_principais": {
                    "health": "/api/v1/health",
                    "todas_datas": "/api/v1/datas",
                    "feriados": "/api/v1/feriados",
                    "meses": "/api/v1/meses",
                    "detalhe_mes": "/api/v1/meses/1",
                    "fases_lua": "/api/v1/lua",
                    "hoje": "/api/v1/hoje",
                    "categorias": "/api/v1/categorias",
                    "estatisticas": "/api/v1/estatisticas"
                }
            }
            return self.send_json(200, welcome)

        # 2. Documentação Swagger UI e OpenAPI spec
        if path == "/docs":
            return self.send_html(200, SWAGGER_HTML)

        if path == "/openapi.json":
            return self.send_json(200, OPENAPI_SPEC)

        # 3. Health check
        if path == "/api/v1/health":
            uptime = round(time.time() - START_TIME, 2)
            return self.send_json(200, {
                "status": "healthy",
                "projeto": "API OpenData BR",
                "versao": "1.0.0",
                "uptime_segundos": uptime,
                "total_registros": len(repo.datas),
                "timestamp": datetime.now().isoformat()
            })

        # 4. Listar todas as datas com filtros
        if path == "/api/v1/datas":
            res = repo.listar_datas(
                mes=q("mes"),
                dia=q("dia"),
                tipo=q("tipo"),
                categoria=q("categoria"),
                busca=q("busca") or q("q"),
                pagina=int(q("pagina", 1)),
                limite=int(q("limite", 20)),
                ordem=q("ordem", "asc")
            )
            return self.send_json(200, res)

        # 5. Obter data por ID
        if path.startswith("/api/v1/datas/"):
            item_id = path.replace("/api/v1/datas/", "").strip()
            item = repo.obter_por_id(item_id)
            if item:
                return self.send_json(200, item)
            return self.send_json(404, {"erro": "Data não encontrada", "id": item_id})

        # 6. Listar feriados
        if path == "/api/v1/feriados":
            apenas_nacionais = q("apenas_nacionais", "false").lower() in ("true", "1", "s", "sim")
            lista = repo.listar_feriados(apenas_nacionais=apenas_nacionais)
            return self.send_json(200, {
                "total": len(lista),
                "apenas_nacionais": apenas_nacionais,
                "feriados": lista
            })

        # 7. Listar meses
        if path == "/api/v1/meses":
            meses = repo.listar_meses()
            return self.send_json(200, {
                "ano": 2026,
                "total_meses": len(meses),
                "meses": meses
            })

        # 8. Obter mês específico
        if path.startswith("/api/v1/meses/"):
            mes_id = path.replace("/api/v1/meses/", "").strip()
            mes_detalhe = repo.obter_mes(mes_id)
            if mes_detalhe:
                return self.send_json(200, mes_detalhe)
            return self.send_json(404, {"erro": "Mês não encontrado", "parametro": mes_id})

        # 9. Fases da Lua
        if path == "/api/v1/lua":
            mes = q("mes")
            fases = repo.listar_lua(mes=mes)
            return self.send_json(200, {
                "ano": 2026,
                "filtro_mes": mes,
                "total": len(fases),
                "fases_lua": fases
            })

        # 10. O que se comemora hoje
        if path == "/api/v1/hoje":
            data_ref = q("data")
            hoje_info = repo.obter_hoje(data_ref)
            return self.send_json(200, hoje_info)

        # 11. Categorias
        if path == "/api/v1/categorias":
            cats = repo.listar_categorias()
            return self.send_json(200, {
                "total_categorias": len(cats),
                "categorias": cats
            })

        # 12. Estatísticas
        if path == "/api/v1/estatisticas":
            return self.send_json(200, repo.estatisticas())

        # Rota não encontrada
        return self.send_json(404, {
            "erro": "Endpoint não encontrado",
            "caminho": path,
            "documentacao": "/docs",
            "rotas_disponiveis": "/"
        })

def run_server(port=8000, host="0.0.0.0"):
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, OpenDataHTTPHandler)
    print(f"==================================================")
    print(f"  API OpenData BR - Servidor REST em Execução")
    print(f"  URL: http://localhost:{port}")
    print(f"  Swagger UI: http://localhost:{port}/docs")
    print(f"  OpenAPI Spec: http://localhost:{port}/openapi.json")
    print(f"==================================================")
    return httpd

if __name__ == "__main__":
    server = run_server()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado pelo usuário.")
