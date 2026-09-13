# Productos API

API REST para gestionar un inventario de productos, construida con **Python 3.12** y **FastAPI**
sobre una arquitectura por capas (dominio, aplicación, infraestructura y presentación).

## Ejecución

```bash
python -m venv .venv
.venv\Scripts\activate           # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentación interactiva en `http://127.0.0.1:8000/docs`.

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/productos` | Lista todos los productos |
| GET | `/api/v1/productos/precio-mayor?valor=100000` | Productos con precio mayor al valor |
| GET | `/api/v1/inventario/valor-total` | Valor total del inventario (precio × stock) |
| GET | `/api/v1/productos/mayor-stock` | Producto con mayor stock |
| GET | `/api/v1/productos/categoria/{categoria}` | Productos de una categoría |
| GET | `/api/v1/productos/{id}` | Busca un producto por id |
| GET | `/api/v1/productos/conteo-por-categoria` | Cantidad de productos por categoría |
| POST | `/api/v1/productos` | Registra un producto |
| GET | `/health` | Estado del servicio |

La colección de Postman está en `docs/postman_collection.json`.

## Arquitectura

```
app/
├── domain/           Entidad Producto, contrato del repositorio y excepciones de negocio
├── application/      Casos de uso y DTOs
├── infrastructure/   Repositorio en memoria y datos iniciales
├── presentation/     Routers, schemas, inyección de dependencias y manejo de errores
├── core/             Configuración
└── main.py           Creación de la aplicación
tests/                Pruebas de la entidad, los casos de uso y los endpoints
```
