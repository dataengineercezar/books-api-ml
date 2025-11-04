# Arquitetura da Books API

## Visão Geral

A Books API é uma aplicação REST desenvolvida em Python com FastAPI, destinada a fornecer acesso programático a informações de livros coletadas através de web scraping.

## Componentes Principais

### 1. API Layer (`api/`)

#### `main.py`
- **Framework**: FastAPI
- **Responsabilidades**:
  - Definição de endpoints REST
  - Validação de requisições (Pydantic)
  - Tratamento de erros e exceções
  - Documentação automática (OpenAPI/Swagger)
  - Serialização de respostas JSON

#### Endpoints:
```
GET  /              - Informações da API
GET  /health        - Health check
GET  /books         - Listar livros (com paginação)
GET  /books/{id}    - Obter livro por ID
GET  /books/search/ - Buscar livros por título/autor
```

### 2. Data Collection Layer (`scripts/`)

#### `scrape_books.py`
- **Bibliotecas**: BeautifulSoup4, Requests
- **Responsabilidades**:
  - Web scraping de dados de livros
  - Parsing de HTML
  - Extração de informações estruturadas
  - Salvamento em formato CSV
  
#### Dados Coletados:
- Título
- Preço
- Rating (1-5 estrelas)
- Disponibilidade
- URL/Link

### 3. Data Storage (`data/`)

#### `books.csv`
- **Formato**: CSV (Comma-Separated Values)
- **Encoding**: UTF-8
- **Schema**:
  ```
  title,price,rating,availability,link
  ```
- **Acesso**: Leitura via Pandas DataFrame

### 4. Testing Layer (`tests/`)

#### `test_api.py`
- **Framework**: pytest
- **Cliente**: FastAPI TestClient
- **Cobertura**:
  - Testes de endpoints
  - Validação de status codes
  - Verificação de schemas de resposta

## Fluxo de Dados

```mermaid
graph LR
    A[Web Source] -->|Scraping| B[scrape_books.py]
    B -->|Save| C[books.csv]
    C -->|Load| D[FastAPI App]
    D -->|Response| E[Client/User]
```

### 1. Coleta de Dados (Batch)
```
Web Source → BeautifulSoup → Parsing → DataFrame → CSV
```

### 2. Servir API (Runtime)
```
HTTP Request → FastAPI → Load CSV → Pandas → Filter/Query → JSON Response
```

## Decisões de Arquitetura

### Por que FastAPI?
- ⚡ Alta performance (baseado em Starlette e Pydantic)
- 📝 Documentação automática (OpenAPI)
- ✅ Validação automática de dados
- 🔄 Suporte nativo a async/await
- 🐍 Type hints do Python 3.11+

### Por que CSV?
- 📁 Simplicidade para volumes pequenos/médios
- 🔄 Fácil integração com Pandas
- 📊 Portabilidade e legibilidade
- 🚀 Suficiente para MVP/Prototipagem

**Evolução futura**: Migrar para banco de dados relacional (PostgreSQL) ou NoSQL (MongoDB) para:
- Consultas mais complexas
- Índices e otimização
- Concorrência e lock control
- Escalabilidade

### Por que Pandas?
- 📊 Manipulação eficiente de dados tabulares
- 🔍 Filtros e queries intuitivos
- 🔄 Conversão fácil para JSON/dict
- 📈 Análises e agregações

## Padrões de Projeto

### 1. Repository Pattern (Implícito)
```python
def load_books() -> pd.DataFrame:
    """Abstração para acesso aos dados"""
```

### 2. Dependency Injection
FastAPI gerencia dependências automaticamente através de seu sistema de DI.

### 3. Error Handling
```python
raise HTTPException(status_code=404, detail="Recurso não encontrado")
```

## Segurança

### Implementado:
- ✅ Input validation (Pydantic)
- ✅ HTTP exception handling
- ✅ CORS pode ser configurado

### A Implementar (Produção):
- 🔒 Autenticação (OAuth2/JWT)
- 🔑 Rate limiting
- 🛡️ HTTPS/TLS
- 📝 Logging e auditoria
- 🔐 Secrets management

## Performance

### Otimizações Atuais:
- Leitura em memória (Pandas DataFrame)
- Respostas JSON otimizadas
- Paginação para grandes volumes

### Otimizações Futuras:
- Cache (Redis)
- Compressão de respostas (gzip)
- CDN para conteúdo estático
- Load balancing
- Database indexing

## Escalabilidade

### Horizontal Scaling:
```
[Load Balancer]
     ↓
[API Instance 1] [API Instance 2] [API Instance N]
     ↓           ↓               ↓
[Shared Database / Storage]
```

### Container Orchestration:
- Docker para containerização
- Kubernetes para orquestração (futuro)
- CI/CD pipeline (futuro)

## Monitoramento e Observabilidade

### A Implementar:
- 📊 Prometheus + Grafana para métricas
- 📝 Structured logging (JSON)
- 🔍 Distributed tracing (OpenTelemetry)
- 🚨 Alerting (PagerDuty/Slack)
- 📈 APM (Application Performance Monitoring)

## Deploy

### Ambientes:

#### Development:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production (Docker):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Cloud Options:
- **AWS**: ECS, Lambda (Serverless), EC2
- **GCP**: Cloud Run, App Engine, GKE
- **Azure**: App Service, Container Instances, AKS
- **Heroku**: Simples e rápido para MVP

## Tecnologias e Stack

### Core:
- Python 3.11
- FastAPI 0.121+
- Uvicorn (ASGI server)
- Pydantic (validação)

### Data:
- Pandas 2.3+
- BeautifulSoup4
- Requests

### Testing:
- pytest
- TestClient (FastAPI)

### DevOps:
- Docker
- Git

## Próximos Passos

1. ✅ Implementar autenticação
2. ✅ Adicionar banco de dados
3. ✅ Implementar cache
4. ✅ CI/CD pipeline
5. ✅ Monitoramento e logging
6. ✅ Testes de carga
7. ✅ Documentação adicional
8. ✅ API versioning

## Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [12 Factor App](https://12factor.net/)
- [REST API Best Practices](https://restfulapi.net/)
