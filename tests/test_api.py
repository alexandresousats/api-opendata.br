# -*- coding: utf-8 -*-
"""
Testes automatizados da API OpenData BR
Testa o repositório de dados e os handlers do servidor REST sem necessidade de binding de socket de rede.
"""
import unittest
import io
import json
import sys
import os

# Adicionar pasta raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import OpenDataRepository
from src.server import OpenDataHTTPHandler

class MockSocket:
    def __init__(self, data=b""):
        self.data = data
        self.output = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if "r" in mode:
            return io.BytesIO(self.data)
        elif "w" in mode or "b" in mode:
            return self.output

class MockRequest(OpenDataHTTPHandler):
    def __init__(self, method="GET", path="/"):
        self.rfile = io.BytesIO(f"{method} {path} HTTP/1.1\r\nHost: localhost\r\n\r\n".encode("utf-8"))
        self.wfile = io.BytesIO()
        self.raw_requestline = self.rfile.readline()
        self.parse_request()
        if method == "GET":
            self.do_GET()

    def get_response(self):
        self.wfile.seek(0)
        lines = self.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        header_text = lines[0]
        body_text = lines[1] if len(lines) > 1 else ""
        status_line = header_text.splitlines()[0]
        status_code = int(status_line.split()[1])
        try:
            body_json = json.loads(body_text)
        except Exception:
            body_json = body_text
        return status_code, body_json

class TestOpenDataRepository(unittest.TestCase):
    def setUp(self):
        self.repo = OpenDataRepository()

    def test_dados_carregados(self):
        self.assertGreater(len(self.repo.datas), 1000)
        self.assertEqual(len(self.repo.meses), 12)
        self.assertGreater(len(self.repo.fases_lua), 40)

    def test_feriados_nacionais(self):
        feriados = self.repo.listar_feriados(apenas_nacionais=True)
        self.assertEqual(len(feriados), 11)
        titulos = [f["titulo"] for f in feriados]
        self.assertTrue(any("Confraternização Universal" in t for t in titulos))
        self.assertTrue(any("Tiradentes" in t for t in titulos))
        self.assertTrue(any("Trabalho" in t for t in titulos))
        self.assertTrue(any("Independência" in t for t in titulos))
        self.assertTrue(any("Aparecida" in t for t in titulos))
        self.assertTrue(any("Finados" in t for t in titulos))
        self.assertTrue(any("República" in t for t in titulos))
        self.assertTrue(any("Zumbi" in t or "Consciência Negra" in t for t in titulos))
        self.assertTrue(any("Natal" in t for t in titulos))

    def test_pontos_facultativos(self):
        todos = self.repo.listar_feriados(apenas_nacionais=False)
        pontos = [f for f in todos if f["tipo"] == "ponto_facultativo"]
        self.assertGreaterEqual(len(pontos), 7)
        titulos = [p["titulo"] for p in pontos]
        self.assertTrue(any("Carnaval" in t for t in titulos))
        self.assertTrue(any("Cinzas" in t for t in titulos))
        self.assertTrue(any("Corpus Christi" in t for t in titulos))

    def test_filtro_por_mes_e_dia(self):
        # 12 de Outubro (Nossa Senhora Aparecida / Dia das Crianças)
        res = self.repo.listar_datas(mes=10, dia=12)
        self.assertGreater(res["total"], 0)
        titulos = [d["titulo"] for d in res["dados"]]
        self.assertTrue(any("Aparecida" in t for t in titulos))
        self.assertTrue(any("Crianças" in t for t in titulos))

    def test_filtro_busca_textual(self):
        res = self.repo.listar_datas(busca="tiradentes")
        self.assertGreater(res["total"], 0)
        self.assertEqual(res["dados"][0]["dia"], 21)
        self.assertEqual(res["dados"][0]["mes"], 4)

    def test_paginacao(self):
        res = self.repo.listar_datas(pagina=1, limite=10)
        self.assertEqual(len(res["dados"]), 10)
        self.assertEqual(res["pagina"], 1)
        self.assertEqual(res["limite"], 10)
        self.assertTrue(res["tem_proxima"])
        self.assertFalse(res["tem_anterior"])

    def test_fases_lua_ano_e_mes(self):
        todas = self.repo.listar_lua()
        self.assertGreater(len(todas), 40)
        maio = self.repo.listar_lua(mes=5)
        self.assertGreaterEqual(len(maio), 4)

    def test_obter_mes_detalhes(self):
        # Por número
        mes1 = self.repo.obter_mes(1)
        self.assertIsNotNone(mes1)
        self.assertEqual(mes1["informacoes"]["nome"], "Janeiro")
        self.assertEqual(mes1["informacoes"]["dias_uteis"], 21)

        # Por nome
        mes10 = self.repo.obter_mes("outubro")
        self.assertIsNotNone(mes10)
        self.assertEqual(mes10["informacoes"]["numero"], 10)

    def test_estatisticas(self):
        stats = self.repo.estatisticas()
        self.assertEqual(stats["ano"], 2026)
        self.assertGreater(stats["total_eventos_cadastrados"], 1000)
        self.assertEqual(stats["total_meses"], 12)
        self.assertGreater(stats["total_dias_uteis_ano"], 200)

class TestServerEndpoints(unittest.TestCase):
    def test_endpoint_raiz(self):
        req = MockRequest("GET", "/")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertEqual(data["projeto"], "API OpenData BR")
        self.assertIn("endpoints_principais", data)

    def test_endpoint_health(self):
        req = MockRequest("GET", "/api/v1/health")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "healthy")
        self.assertGreater(data["total_registros"], 1000)

    def test_endpoint_datas_com_filtro(self):
        req = MockRequest("GET", "/api/v1/datas?mes=12&dia=25")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertGreaterEqual(data["total"], 1)
        titulos = [item["titulo"] for item in data["dados"]]
        self.assertTrue(any("Natal" in t for t in titulos))

    def test_endpoint_feriados(self):
        req = MockRequest("GET", "/api/v1/feriados?apenas_nacionais=true")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertEqual(data["total"], 11)

    def test_endpoint_meses(self):
        req = MockRequest("GET", "/api/v1/meses")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertEqual(data["total_meses"], 12)

    def test_endpoint_lua(self):
        req = MockRequest("GET", "/api/v1/lua?mes=10")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertEqual(len(data["fases_lua"]), 4)

    def test_endpoint_estatisticas(self):
        req = MockRequest("GET", "/api/v1/estatisticas")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertEqual(data["ano"], 2026)

    def test_endpoint_categorias(self):
        req = MockRequest("GET", "/api/v1/categorias")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertGreater(data["total_categorias"], 10)

    def test_endpoint_hoje(self):
        req = MockRequest("GET", "/api/v1/hoje?data=2026-10-21")
        status, data = req.get_response()
        self.assertEqual(status, 200)
        self.assertEqual(data["dia"], 21)
        self.assertEqual(data["mes"], 10)
        self.assertGreater(data["total_celebracoes"], 0)

if __name__ == "__main__":
    unittest.main()
