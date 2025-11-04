# Books API

API REST para consulta e gerenciamento de informações de livros, desenvolvida com FastAPI e Python 3.11.

## 📋 Descrição

Este projeto consiste em uma API para gerenciar informações de livros obtidas através de web scraping. A aplicação permite consultar, buscar e filtrar livros através de endpoints REST.

## 🚀 Tecnologias

- **Python 3.11**
- **FastAPI** - Framework web moderno e rápido
- **Pandas** - Manipulação de dados
- **BeautifulSoup4** - Web scraping
- **Uvicorn** - Servidor ASGI
- **Docker** - Containerização

## 📁 Estrutura do Projeto

```
books-api-ml/
├── api/
│   ├── __init__.py
│   └── main.py              # Aplicação FastAPI principal
├── scripts/
│   └── scrape_books.py      # Script de web scraping
├── data/
│   └── books.csv            # Dados dos livros (gerado)
├── docs/
│   └── architecture.md      # Documentação da arquitetura
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Testes da API
├── requirements.txt         # Dependências
├── README.md
├── .gitignore
└── Dockerfile               # Container Docker
```

## 🔧 Instalação

### Pré-requisitos

- Python 3.11+
- pip ou conda

### Configuração do Ambiente

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd books-api-ml
```

2. Crie e ative um ambiente virtual (conda):
```bash
conda create -n py311 python=3.11
conda activate py311
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📊 Coleta de Dados

Execute o script de scraping para coletar dados de livros:

```bash
python scripts/scrape_books.py
```

Este script irá:
- Fazer scraping de livros do site Books to Scrape
- Salvar os dados em `data/books.csv`
- Coletar informações como título, preço, rating e disponibilidade

## 🏃 Executando a API

### Modo Desenvolvimento

```bash
cd api
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Usando Docker

```bash
docker build -t books-api .
docker run -p 8000:8000 books-api
```

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principais

#### `GET /`
Retorna informações sobre a API

#### `GET /health`
Verifica o status da API

#### `GET /books`
Lista todos os livros
- **Parâmetros**:
  - `skip` (int): Paginação - registros para pular
  - `limit` (int): Máximo de registros a retornar

#### `GET /books/{book_id}`
Retorna um livro específico por ID

#### `GET /books/search/`
Busca livros por título ou autor
- **Parâmetros**:
  - `title` (str): Busca parcial por título
  - `author` (str): Busca parcial por autor

### Exemplos de Uso

```bash
# Listar livros
curl http://localhost:8000/books

# Buscar por título
curl "http://localhost:8000/books/search/?title=Python"

# Obter livro específico
curl http://localhost:8000/books/0
```

## 🧪 Testes

Execute os testes com pytest:

```bash
pip install pytest pytest-cov
pytest tests/ -v
```

Com cobertura:
```bash
pytest tests/ --cov=api --cov-report=html
```

## 🐳 Docker

### Build da Imagem

```bash
docker build -t books-api:latest .
```

### Executar Container

```bash
docker run -d -p 8000:8000 --name books-api books-api:latest
```

## 📝 Desenvolvimento

### Adicionar Novas Dependências

```bash
pip install <pacote>
pip freeze > requirements.txt
```

### Estrutura de Código

- `api/main.py`: Definição da aplicação FastAPI e endpoints
- `scripts/scrape_books.py`: Lógica de web scraping
- `tests/`: Testes unitários e de integração

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

Tech Challenge - FIAP

## 📞 Suporte

Para dúvidas e suporte, abra uma issue no repositório.
