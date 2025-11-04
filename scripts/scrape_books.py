"""
Script para fazer scraping de livros.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time


def scrape_books(num_pages: int = 5) -> pd.DataFrame:
    """
    Faz scraping de livros do site Books to Scrape.
    
    Args:
        num_pages: Número de páginas para fazer scraping
        
    Returns:
        DataFrame com os dados dos livros
    """
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    books_data = []
    
    print(f"Iniciando scraping de {num_pages} páginas...")
    
    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        print(f"Processando página {page}...")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                # Título
                title = book.h3.a['title']
                
                # Preço
                price = book.find('p', class_='price_color').text
                price_value = float(price.replace('£', '').strip())
                
                # Rating
                rating_class = book.find('p', class_='star-rating')['class']
                rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
                rating = rating_map.get(rating_class[1], 0)
                
                # Disponibilidade
                availability = book.find('p', class_='instock availability').text.strip()
                
                # Link
                link = book.h3.a['href']
                
                books_data.append({
                    'title': title,
                    'price': price_value,
                    'rating': rating,
                    'availability': availability,
                    'link': f"http://books.toscrape.com/catalogue/{link}"
                })
            
            # Pequeno delay para não sobrecarregar o servidor
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Erro ao processar página {page}: {e}")
            continue
    
    print(f"Scraping concluído! Total de livros coletados: {len(books_data)}")
    
    return pd.DataFrame(books_data)


def save_books_to_csv(df: pd.DataFrame, filename: str = "books.csv"):
    """
    Salva os dados dos livros em um arquivo CSV.
    
    Args:
        df: DataFrame com os dados dos livros
        filename: Nome do arquivo CSV
    """
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    filepath = data_dir / filename
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"Dados salvos em: {filepath}")
    print(f"Total de registros: {len(df)}")


if __name__ == "__main__":
    # Fazer scraping de 5 páginas
    df = scrape_books(num_pages=5)
    
    # Salvar no CSV
    if not df.empty:
        save_books_to_csv(df)
        print("\n--- Amostra dos dados ---")
        print(df.head())
        print("\n--- Estatísticas ---")
        print(f"Preço médio: £{df['price'].mean():.2f}")
        print(f"Rating médio: {df['rating'].mean():.2f}")
    else:
        print("Nenhum dado foi coletado.")
