# Imagem base com Python 3.11
FROM python:3.11-slim

# Metadados
LABEL maintainer="Tech Challenge FIAP"
LABEL description="Books API - REST API para consulta de livros"

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copiar arquivo de dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY api/ ./api/
COPY data/ ./data/
COPY scripts/ ./scripts/
COPY run.py .

# Criar diretório para dados (caso não exista)
RUN mkdir -p /app/data

# Expor porta da aplicação
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
