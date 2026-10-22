FROM python:3.11-slim

WORKDIR /app

# Copiar arquivos do projeto
COPY requirements.txt .
COPY main.py .
COPY src/ ./src/
COPY data/ ./data/

# Instalação opcional das dependências FastAPI/Uvicorn
RUN pip install --no-cache-dir -r requirements.txt || true

EXPOSE 8000

# Executa o servidor nativo leve (ou com FastAPI se instalado)
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8000"]
