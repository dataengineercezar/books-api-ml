#!/bin/bash

# Executar o script de scraping para coletar dados (opcional)
# python scripts/scrape_books.py

# Iniciar o servidor uvicorn
uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
