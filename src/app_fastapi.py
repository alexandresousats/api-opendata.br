# -*- coding: utf-8 -*-
"""
Implementação FastAPI da API OpenData BR
Utiliza Pydantic e recursos assíncronos modernos com documentação Swagger automática.
"""
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.database import repo

app = FastAPI(
    title="API OpenData BR - Calendário Brasileiro 2026",
    description="API REST aberta para consulta de feriados nacionais, pontos facultativos, datas comemorativas, campanhas de saúde e fases da lua do Brasil (2026), baseada nos dados do Calendarr Brasil.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataItem(BaseModel):
    id: str = Field(..., description="Identificador único")
    ano: int = Field(2026, description="Ano de referência")
    mes: int = Field(..., description="Mês (1-12)")
    dia: int = Field(..., description="Dia do mês (1-31)")
    data: str = Field(..., description="Data no formato ISO YYYY-MM-DD")
    dia_semana: str = Field(..., description="Dia da semana por extenso")
    titulo: str = Field(..., description="Título do feriado ou celebração")
    tipo: str = Field(..., description="Tipo (feriado_nacional, ponto_facultativo, comemorativa, campanha)")
    categoria: str = Field(..., description="Categoria temática")
    fonte: str = Field(..., description="Link da fonte original")

class PaginacaoResponse(BaseModel):
    total: int
    pagina: int
    limite: int
    total_paginas: int
    tem_proxima: bool
    tem_anterior: bool
    dados: List[DataItem]

@app.get("/", tags=["Início"])
def raiz():
    return {
        "projeto": "API OpenData BR",
        "versao": "1.0.0",
        "descricao": "API REST do Calendário Brasileiro 2026 (Feriados, Datas Comemorativas e Fases da Lua)",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "endpoints": {
            "health": "/api/v1/health",
            "datas": "/api/v1/datas",
            "feriados": "/api/v1/feriados",
            "meses": "/api/v1/meses",
            "lua": "/api/v1/lua",
            "hoje": "/api/v1/hoje",
            "categorias": "/api/v1/categorias",
            "estatisticas": "/api/v1/estatisticas"
        }
    }

@app.get("/api/v1/health", tags=["Sistema"])
def health():
    return {
        "status": "healthy",
        "projeto": "API OpenData BR",
        "versao": "1.0.0",
        "total_registros": len(repo.datas)
    }

@app.get("/api/v1/datas", response_model=PaginacaoResponse, tags=["Datas"])
def listar_datas(
    mes: Optional[int] = Query(None, ge=1, le=12, description="Número do mês (1-12)"),
    dia: Optional[int] = Query(None, ge=1, le=31, description="Dia do mês (1-31)"),
    tipo: Optional[str] = Query(None, description="feriado_nacional, ponto_facultativo, comemorativa, campanha"),
    categoria: Optional[str] = Query(None, description="Ex: Saúde, Educação, Esportes, Profissões"),
    busca: Optional[str] = Query(None, description="Termo de busca no título ou categoria"),
    pagina: int = Query(1, ge=1, description="Número da página"),
    limite: int = Query(20, ge=1, le=100, description="Itens por página"),
    ordem: str = Query("asc", regex="^(asc|desc)$", description="Ordem cronológica: asc ou desc")
):
    return repo.listar_datas(
        mes=mes,
        dia=dia,
        tipo=tipo,
        categoria=categoria,
        busca=busca,
        pagina=pagina,
        limite=limite,
        ordem=ordem
    )

@app.get("/api/v1/datas/{item_id}", response_model=DataItem, tags=["Datas"])
def obter_data(item_id: str = Path(..., description="ID da data comemorativa")):
    item = repo.obter_por_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Data não encontrada")
    return item

@app.get("/api/v1/feriados", tags=["Feriados"])
def listar_feriados(
    apenas_nacionais: bool = Query(False, description="Filtrar somente feriados nacionais obrigatórios")
):
    lista = repo.listar_feriados(apenas_nacionais=apenas_nacionais)
    return {
        "total": len(lista),
        "apenas_nacionais": apenas_nacionais,
        "feriados": lista
    }

@app.get("/api/v1/meses", tags=["Meses"])
def listar_meses():
    return {
        "ano": 2026,
        "total_meses": len(repo.meses),
        "meses": repo.listar_meses()
    }

@app.get("/api/v1/meses/{mes_identificador}", tags=["Meses"])
def obter_mes(mes_identificador: str = Path(..., description="Número (1-12) ou nome do mês (ex: janeiro)")):
    resultado = repo.obter_mes(mes_identificador)
    if not resultado:
        raise HTTPException(status_code=404, detail="Mês não encontrado")
    return resultado

@app.get("/api/v1/lua", tags=["Astronomia"])
def fases_lua(
    mes: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mês (1-12)")
):
    return {
        "ano": 2026,
        "filtro_mes": mes,
        "total": len(repo.listar_lua(mes=mes)),
        "fases_lua": repo.listar_lua(mes=mes)
    }

@app.get("/api/v1/hoje", tags=["Hoje"])
def hoje(
    data: Optional[str] = Query(None, description="Data específica YYYY-MM-DD para consulta")
):
    try:
        return repo.obter_hoje(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data inválida. Use o formato YYYY-MM-DD. Detalhe: {str(e)}")

@app.get("/api/v1/categorias", tags=["Categorias"])
def categorias():
    cats = repo.listar_categorias()
    return {
        "total_categorias": len(cats),
        "categorias": cats
    }

@app.get("/api/v1/estatisticas", tags=["Estatísticas"])
def estatisticas():
    return repo.estatisticas()
