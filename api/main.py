"""
API FastAPI para gerenciamento de livros.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from pathlib import Path
from typing import List, Optional

app = FastAPI(
    title="Books API",
    description="API para consulta e gerenciamento de informações de livros",
    version="1.0.0"
)

# Caminho para o arquivo CSV
DATA_PATH = Path(__file__).parent.parent / "data" / "books.csv"


def load_books() -> pd.DataFrame:
    """Carrega os dados dos livros do CSV."""
    if not DATA_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)


@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {
        "message": "Books API",
        "version": "1.0.0",
        "endpoints": {
            "books": "/books",
            "book_by_id": "/books/{book_id}",
            "search": "/books/search?title=..."
        }
    }


@app.get("/health")
async def health_check():
    """Verifica o status da API."""
    return {"status": "healthy"}


@app.get("/books")
async def get_books(skip: int = 0, limit: int = 100):
    """
    Retorna a lista de livros.
    
    - **skip**: Número de registros para pular (paginação)
    - **limit**: Número máximo de registros a retornar
    """
    df = load_books()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    
    total = len(df)
    books = df.iloc[skip:skip + limit].to_dict(orient="records")
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "books": books
    }


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    """
    Retorna um livro específico pelo ID.
    
    - **book_id**: ID do livro
    """
    df = load_books()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    
    if book_id >= len(df) or book_id < 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    book = df.iloc[book_id].to_dict()
    return book


@app.get("/books/search/")
async def search_books(title: Optional[str] = None, author: Optional[str] = None):
    """
    Busca livros por título ou autor.
    
    - **title**: Título do livro (busca parcial)
    - **author**: Autor do livro (busca parcial)
    """
    df = load_books()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    
    # Aplicar filtros
    if title:
        df = df[df['title'].str.contains(title, case=False, na=False)]
    
    if author:
        df = df[df['author'].str.contains(author, case=False, na=False)]
    
    if df.empty:
        return {"total": 0, "books": []}
    
    books = df.to_dict(orient="records")
    
    return {
        "total": len(books),
        "books": books
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
