# Productos API — Backend Python (FastAPI)

API REST para la gestión de un inventario de productos. Implementa en el backend las seis
operaciones solicitadas en la actividad, usando **programación orientada a objetos** y una
**arquitectura por capas inspirada en Clean Architecture**.

- **Lenguaje:** Python 3.12
- **Framework:** FastAPI + Uvicorn
- **Documentación interactiva:** `/docs` (Swagger UI) y `/redoc`
- **CORS:** habilitado, lista para ser consumida desde una app móvil

---

## Operaciones solicitadas y su endpoint

| # | Operación de la actividad | Endpoint |
|---|---------------------------|----------|
| 1 | Productos con precio mayor a $100.000 | `GET /api/v1/productos/precio-mayor?valor=100000` |
| 2 | Valor total del inventario (precio × stock) | `GET /api/v1/inventario/valor-total` |
| 3 | Producto con mayor stock | `GET /api/v1/productos/mayor-stock` |
| 4 | Productos de la categoría "Tecnología" | `GET /api/v1/productos/categoria/Tecnología` |
| 5 | Buscar producto por id | `GET /api/v1/productos/{id}` |
| 6 | Cantidad de productos agrupados por categoría | `GET /api/v1/productos/conteo-por-categoria` |

Endpoints adicionales:

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Estado del servicio |
| `GET /health` | Health check para el proveedor de despliegue |
| `GET /api/v1/productos` | Lista completa de productos |
| `POST /api/v1/productos` | Registra un producto nuevo |

---

## Arquitectura

El proyecto separa responsabilidades en cuatro capas. La regla de dependencia apunta siempre
hacia adentro: la capa de presentación conoce la de aplicación, la de aplicación conoce el
dominio, y el dominio no conoce a nadie.

```
app/
├── domain/                         Capa de dominio (núcleo, sin dependencias externas)
│   ├── entities/producto.py        Entidad Producto con su comportamiento
│   ├── repositories/               Contrato abstracto ProductoRepository (ABC)
│   └── exceptions.py               Excepciones propias del negocio
│
├── application/                    Capa de aplicación (casos de uso)
│   ├── dtos/producto_dto.py        Objetos de transporte entre capas
│   └── use_cases/                  Una clase por caso de uso, con método ejecutar()
│       ├── listar_productos.py
│       ├── buscar_producto_por_id.py
│       ├── filtrar_productos_por_precio.py
│       ├── calcular_valor_inventario.py
│       ├── obtener_producto_mayor_stock.py
│       ├── filtrar_productos_por_categoria.py
│       ├── contar_productos_por_categoria.py
│       └── crear_producto.py
│
├── infrastructure/                 Capa de infraestructura (detalles técnicos)
│   ├── data/productos_seed.py      Datos iniciales del enunciado
│   └── repositories/               InMemoryProductoRepository, implementa el contrato
│
├── presentation/                   Capa de presentación (entrega HTTP)
│   ├── api/v1/                     Routers de FastAPI
│   ├── schemas/                    Modelos Pydantic de request y response
│   ├── dependencies.py             Container de inyección de dependencias
│   └── error_handlers.py           Traducción de errores de dominio a códigos HTTP
│
├── core/config.py                  Configuración de la aplicación
└── main.py                         Fábrica de la app (crear_app) y registro de routers

tests/                              Pruebas automatizadas (pytest)
├── test_producto.py                Reglas de la entidad
├── test_casos_de_uso.py            Casos de uso con el repositorio en memoria
└── test_api.py                     Endpoints de punta a punta con TestClient
```

**Por qué esta separación importa:** el repositorio hoy guarda los productos en memoria, pero
cambiarlo por PostgreSQL o MongoDB solo exige una clase nueva que herede de
`ProductoRepository` y una línea distinta en `dependencies.py`. Ningún caso de uso ni ningún
router se modifica.

### Principios aplicados

- **Inversión de dependencias:** los casos de uso reciben la abstracción `ProductoRepository`, nunca la implementación concreta.
- **Responsabilidad única:** cada caso de uso resuelve una sola operación del enunciado.
- **Encapsulamiento:** la entidad `Producto` expone su propio comportamiento (`valor_en_inventario()`, `supera_precio()`, `pertenece_a()`) en lugar de que los cálculos queden dispersos en los controladores.
- **Inyección de dependencias:** `Container` construye los casos de uso y FastAPI los inyecta con `Depends`.
- **Dominio que se protege a sí mismo:** `Producto` valida sus reglas al construirse (nombre y categoría no vacíos, precio mayor a 0, stock no negativo y límites máximos), sin importar desde qué capa se cree.
- **Seguridad en concurrencia:** el repositorio en memoria asigna los ids con un candado (`threading.Lock`), así que peticiones simultáneas nunca reciben el mismo id.

### Formato de errores

Todos los errores comparten la misma forma, incluidos los de validación:

```json
{ "detalle": "Los datos enviados no son válidos", "codigo": "DATOS_INVALIDOS",
  "errores": [{ "campo": "body.precio", "mensaje": "Input should be greater than 0" }] }
```

| Código HTTP | `codigo` | Cuándo |
|-------------|----------|--------|
| 404 | `PRODUCTO_NO_ENCONTRADO` | El id no existe |
| 409 | `INVENTARIO_VACIO` | Se pide el mayor stock sin productos |
| 409 | `PRODUCTO_DUPLICADO` | Se intenta guardar un id existente |
| 422 | `DATOS_INVALIDOS` | La petición no cumple las validaciones |
| 422 | `PRODUCTO_INVALIDO` | La entidad rechaza los datos |

La búsqueda y el conteo por categoría no distinguen mayúsculas ni tildes: `tecnologia` y `Tecnología` son la misma categoría.

---

## Ejecución local

```bash
git clone https://github.com/TU_USUARIO/productos-api.git
cd productos-api

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Servicio disponible en `http://127.0.0.1:8000` y documentación en `http://127.0.0.1:8000/docs`.

Para probarlo desde un emulador o un celular físico, levántalo escuchando en toda la red:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Emulador de Android: `http://10.0.2.2:8000`
- Celular físico en la misma red WiFi: `http://IP_DE_TU_PC:8000`

Con Docker:

```bash
docker build -t productos-api .
docker run -p 8000:8000 productos-api
```

---

## Despliegue

Cualquiera de estas opciones publica la API con una URL pública en pocos minutos.

**Render (recomendado, incluye `render.yaml`):**
1. Sube el repositorio a GitHub.
2. Entra a render.com → New → Web Service → conecta el repositorio.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Plan Free → Create Web Service.

Render entrega una URL del estilo `https://productos-api-xxxx.onrender.com`.

**Railway:** detecta el `Procfile` automáticamente; solo se conecta el repositorio y se genera el dominio público en Settings → Networking.

**Fly.io:** usa el `Dockerfile` incluido con `fly launch` y `fly deploy`.

> Nota sobre el plan gratuito de Render: el servicio se duerme tras un rato sin tráfico y la
> primera petición puede tardar unos 30 segundos. Conviene tenerlo en cuenta al grabar la
> evidencia o al probar desde la app móvil.

---

## Pruebas automatizadas

```bash
pip install -r requirements-dev.txt
pytest
```

Cada prueba usa un repositorio nuevo, así que no dependen del orden ni se afectan entre sí.

La variable de entorno `CORS_ORIGINS` (lista separada por comas) restringe los orígenes permitidos; si no se define, se acepta cualquiera.

## Pruebas funcionales

El repositorio incluye `docs/postman_collection.json`. En Postman: Import → File → seleccionar
ese archivo. La colección trae la variable `base_url`, que se cambia por la URL pública una vez
desplegado el servicio.

Los resultados esperados de cada caso están documentados en `docs/EVIDENCIA.md`, junto con la
respuesta real obtenida en cada endpoint.

---

## Consumo desde la app móvil

Ejemplos listos para Kotlin/Retrofit y .NET MAUI en `docs/CONSUMO_MOVIL.md`.
