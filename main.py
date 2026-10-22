# -*- coding: utf-8 -*-
"""
Ponto de Entrada Principal da API OpenData BR
Permite iniciar o servidor usando a biblioteca padrão do Python (Zero dependências)
ou via FastAPI/Uvicorn se especificado.
"""
import sys
import argparse
import os

# Adicionar pasta raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="API OpenData BR - Servidor REST")
    parser.add_argument("--port", type=int, default=8000, help="Porta do servidor (padrão: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host do servidor (padrão: 0.0.0.0)")
    parser.add_argument("--fastapi", action="store_true", help="Executar usando FastAPI e Uvicorn")
    args = parser.parse_args()

    if args.fastapi:
        try:
            import uvicorn
            print("Iniciando via FastAPI / Uvicorn...")
            uvicorn.run("src.app_fastapi:app", host=args.host, port=args.port, reload=True)
        except ImportError:
            print("FastAPI ou Uvicorn não estão instalados. Executando servidor padrão nativo (Zero Dependências)...")
            from src.server import run_server
            server = run_server(port=args.port, host=args.host)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\nServidor finalizado.")
    else:
        from src.server import run_server
        server = run_server(port=args.port, host=args.host)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor finalizado.")

if __name__ == "__main__":
    main()
