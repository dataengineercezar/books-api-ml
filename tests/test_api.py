"""
Testes para os endpoints da API.
"""
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app

client = TestClient(app)


def test_root():
    """Testa o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Books API"


def test_health_check():
    """Testa o endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_books():
    """Testa o endpoint de listagem de livros."""
    response = client.get("/books")
    # Pode retornar 404 se não houver dados ainda
    assert response.status_code in [200, 404]


def test_search_books():
    """Testa o endpoint de busca de livros."""
    response = client.get("/books/search/?title=test")
    # Pode retornar 404 se não houver dados ainda
    assert response.status_code in [200, 404]
