.PHONY: run run-fastapi test docker-build docker-run help

help:
	@echo "Comandos disponíveis:"
	@echo "  make run          - Inicia o servidor REST nativo (Zero dependências)"
	@echo "  make run-fastapi  - Inicia o servidor com FastAPI e Uvicorn"
	@echo "  make test         - Executa os testes automatizados"
	@echo "  make docker-build - Constrói a imagem Docker"
	@echo "  make docker-run   - Executa via Docker Compose"

run:
	python3 main.py

run-fastapi:
	python3 main.py --fastapi

test:
	python3 tests/test_api.py

docker-build:
	docker build -t api-opendata-br:latest .

docker-run:
	docker compose up -d
