# -*- coding: utf-8 -*-
"""
Camada de dados e busca da API OpenData BR
Carrega e indexa os dados extraídos de Calendarr Brasil (2026).
"""
import json
import os
import unicodedata
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.lower().strip()

class OpenDataRepository:
    def __init__(self):
        self.datas = []
        self.fases_lua = []
        self.meses = []
        self.datas_por_id = {}
        self.load_data()

    def load_data(self):
        datas_file = os.path.join(DATA_DIR, "datas_brasil_2026.json")
        fases_file = os.path.join(DATA_DIR, "fases_lua_2026.json")
        meses_file = os.path.join(DATA_DIR, "meses_2026.json")

        if os.path.exists(datas_file):
            with open(datas_file, "r", encoding="utf-8") as f:
                self.datas = json.load(f)
                self.datas_por_id = {d["id"]: d for d in self.datas}

        if os.path.exists(fases_file):
            with open(fases_file, "r", encoding="utf-8") as f:
                self.fases_lua = json.load(f)

        if os.path.exists(meses_file):
            with open(meses_file, "r", encoding="utf-8") as f:
                self.meses = json.load(f)

    def listar_datas(self, mes=None, dia=None, tipo=None, categoria=None, busca=None, pagina=1, limite=20, ordem="asc"):
        resultado = list(self.datas)

        if mes is not None:
            try:
                mes_int = int(mes)
                resultado = [d for d in resultado if d["mes"] == mes_int]
            except ValueError:
                pass

        if dia is not None:
            try:
                dia_int = int(dia)
                resultado = [d for d in resultado if d["dia"] == dia_int]
            except ValueError:
                pass

        if tipo:
            t_norm = tipo.lower()
            resultado = [d for d in resultado if d["tipo"].lower() == t_norm]

        if categoria:
            c_norm = normalize_text(categoria)
            resultado = [d for d in resultado if c_norm in normalize_text(d["categoria"])]

        if busca:
            b_norm = normalize_text(busca)
            resultado = [
                d for d in resultado
                if b_norm in normalize_text(d["titulo"]) or b_norm in normalize_text(d["categoria"]) or b_norm in normalize_text(d.get("descricao", ""))
            ]

        # Ordenação
        reverse = (ordem.lower() == "desc")
        resultado.sort(key=lambda x: (x["mes"], x["dia"]), reverse=reverse)

        # Paginação
        total = len(resultado)
        pagina = max(1, int(pagina))
        limite = max(1, min(100, int(limite)))
        total_paginas = (total + limite - 1) // limite if total > 0 else 1
        inicio = (pagina - 1) * limite
        fim = inicio + limite
        itens = resultado[inicio:fim]

        return {
            "total": total,
            "pagina": pagina,
            "limite": limite,
            "total_paginas": total_paginas,
            "tem_proxima": pagina < total_paginas,
            "tem_anterior": pagina > 1,
            "dados": itens
        }

    def obter_por_id(self, item_id: str):
        return self.datas_por_id.get(item_id)

    def listar_feriados(self, apenas_nacionais=False):
        if apenas_nacionais:
            return [d for d in self.datas if d["tipo"] == "feriado_nacional"]
        return [d for d in self.datas if d["tipo"] in ("feriado_nacional", "ponto_facultativo")]

    def listar_meses(self):
        resumo = []
        for m in self.meses:
            num = m["numero"]
            datas_mes = [d for d in self.datas if d["mes"] == num]
            feriados = [d for d in datas_mes if d["tipo"] == "feriado_nacional"]
            pontos = [d for d in datas_mes if d["tipo"] == "ponto_facultativo"]
            comemorativas = [d for d in datas_mes if d["tipo"] == "comemorativa"]
            lua_mes = [f for f in self.fases_lua if f["mes"] == num]

            resumo.append({
                "numero": num,
                "nome": m["nome"],
                "dias_totais": m["dias_totais"],
                "dias_uteis": m["dias_uteis"],
                "total_eventos": len(datas_mes),
                "feriados_nacionais_qtd": len(feriados),
                "pontos_facultativos_qtd": len(pontos),
                "datas_comemorativas_qtd": len(comemorativas),
                "campanhas_saude": m.get("campanhas_saude", []),
                "fases_lua": lua_mes,
                "estacao": m.get("estacao")
            })
        return resumo

    def obter_mes(self, mes_id):
        try:
            if isinstance(mes_id, str) and not mes_id.isdigit():
                mes_norm = normalize_text(mes_id)
                mes_info = next((m for m in self.meses if normalize_text(m["nome"]) == mes_norm), None)
            else:
                m_num = int(mes_id)
                mes_info = next((m for m in self.meses if m["numero"] == m_num), None)

            if not mes_info:
                return None

            num = mes_info["numero"]
            datas_mes = [d for d in self.datas if d["mes"] == num]
            lua_mes = [f for f in self.fases_lua if f["mes"] == num]

            return {
                "informacoes": mes_info,
                "fases_lua": lua_mes,
                "total_eventos": len(datas_mes),
                "datas": datas_mes
            }
        except Exception:
            return None

    def listar_lua(self, mes=None):
        if mes is not None:
            try:
                mes_int = int(mes)
                return [f for f in self.fases_lua if f["mes"] == mes_int]
            except ValueError:
                pass
        return self.fases_lua

    def obter_hoje(self, data_ref=None):
        if data_ref is None:
            data_ref = date.today()
        elif isinstance(data_ref, str):
            data_ref = datetime.strptime(data_ref, "%Y-%m-%d").date()

        mes = data_ref.month
        dia = data_ref.day
        datas_hoje = [d for d in self.datas if d["mes"] == mes and d["dia"] == dia]
        lua_hoje = next((f for f in self.fases_lua if f["mes"] == mes and f["dia"] == dia), None)

        return {
            "data_consulta": data_ref.strftime("%Y-%m-%d"),
            "dia": dia,
            "mes": mes,
            "fase_lua": lua_hoje["fase"] if lua_hoje else "Consulte calendário lunar",
            "total_celebracoes": len(datas_hoje),
            "celebracoes": datas_hoje
        }

    def listar_categorias(self):
        contagem = {}
        for d in self.datas:
            cat = d["categoria"]
            contagem[cat] = contagem.get(cat, 0) + 1
        return [{"categoria": k, "total": v} for k, v in sorted(contagem.items(), key=lambda x: -x[1])]

    def estatisticas(self):
        tipos = {}
        for d in self.datas:
            t = d["tipo"]
            tipos[t] = tipos.get(t, 0) + 1

        total_dias_uteis = sum(m["dias_uteis"] for m in self.meses)
        return {
            "ano": 2026,
            "fonte": "Calendarr Brasil (https://www.calendarr.com/brasil/)",
            "total_eventos_cadastrados": len(self.datas),
            "distribuicao_por_tipo": tipos,
            "total_fases_lunares_registradas": len(self.fases_lua),
            "total_meses": len(self.meses),
            "total_dias_uteis_ano": total_dias_uteis,
            "categorias_cadastradas": len(self.listar_categorias())
        }

repo = OpenDataRepository()
