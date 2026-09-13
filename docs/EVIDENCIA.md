# Evidencia de funcionamiento

Ejecución real del servicio (`uvicorn app.main:app`) y respuesta obtenida en cada endpoint.
Los comandos usan `curl`; la misma batería está disponible en `postman_collection.json`.

Base local: `http://127.0.0.1:8000`

---

## Caso 1 — Productos con precio mayor a $100.000

```
GET /api/v1/productos/precio-mayor?valor=100000
```

```json
{
  "criterio": "precio > 100,000",
  "total": 8,
  "productos": [
    { "id": 1, "nombre": "Laptop Lenovo", "precio": 2800000.0, "stock": 8, "categoria": "Tecnología", "valor_en_inventario": 22400000.0 },
    { "id": 2, "nombre": "Mouse Logitech", "precio": 120000.0, "stock": 25, "categoria": "Tecnología", "valor_en_inventario": 3000000.0 },
    { "id": 3, "nombre": "Teclado Mecánico", "precio": 350000.0, "stock": 12, "categoria": "Tecnología", "valor_en_inventario": 4200000.0 }
  ]
}
```

*(respuesta recortada: los 8 productos del inventario superan los $100.000)*

**HTTP 200** — Resultado correcto: ningún producto del set inicial está por debajo de $100.000.

---

## Caso 2 — Valor total del inventario

```
GET /api/v1/inventario/valor-total
```

```json
{
  "valor_total": 59850000.0,
  "cantidad_productos": 8,
  "unidades_totales": 91,
  "moneda": "COP"
}
```

**HTTP 200** — Verificación manual: 22.400.000 + 3.000.000 + 4.200.000 + 4.250.000 + 8.400.000 + 8.100.000 + 3.800.000 + 5.700.000 = **59.850.000**

---

## Caso 3 — Producto con mayor stock

```
GET /api/v1/productos/mayor-stock
```

```json
{
  "id": 2,
  "nombre": "Mouse Logitech",
  "precio": 120000.0,
  "stock": 25,
  "categoria": "Tecnología",
  "valor_en_inventario": 3000000.0
}
```

**HTTP 200** — Correcto: 25 unidades es el stock más alto del inventario.

---

## Caso 4 — Productos de la categoría Tecnología

```
GET /api/v1/productos/categoria/Tecnología
```

```json
{
  "criterio": "categoria == Tecnología",
  "total": 4,
  "productos": [
    { "id": 1, "nombre": "Laptop Lenovo", "...": "..." },
    { "id": 2, "nombre": "Mouse Logitech", "...": "..." },
    { "id": 3, "nombre": "Teclado Mecánico", "...": "..." },
    { "id": 8, "nombre": "Monitor Samsung", "...": "..." }
  ]
}
```

**HTTP 200** — Correcto: 4 productos. La comparación ignora mayúsculas y espacios, por lo que
`tecnologia` y `Tecnología` devuelven el mismo resultado.

---

## Caso 5 — Buscar producto por id

```
GET /api/v1/productos/3
```

```json
{
  "id": 3,
  "nombre": "Teclado Mecánico",
  "precio": 350000.0,
  "stock": 12,
  "categoria": "Tecnología",
  "valor_en_inventario": 4200000.0
}
```

**HTTP 200** — Correcto.

---

## Caso 6 — Cantidad de productos por categoría

```
GET /api/v1/productos/conteo-por-categoria
```

```json
{
  "total_categorias": 3,
  "conteo": {
    "Tecnología": 4,
    "Muebles": 2,
    "Audio": 2
  }
}
```

**HTTP 200** — Correcto: 4 + 2 + 2 = 8 productos.

---

## Caso 7 — Producto inexistente (caso negativo)

```
GET /api/v1/productos/99
```

```json
{
  "detalle": "No existe un producto con id 99",
  "codigo": "PRODUCTO_NO_ENCONTRADO"
}
```

**HTTP 404** — Correcto: el error de dominio `ProductoNoEncontradoError` se traduce a un 404
con un cuerpo estructurado, lo que permite manejarlo limpiamente desde la app móvil.

---

## Caso 8 — Registrar un producto

```
POST /api/v1/productos
Content-Type: application/json

{ "nombre": "Webcam Logitech", "precio": 290000, "stock": 14, "categoria": "Tecnología" }
```

```json
{
  "id": 9,
  "nombre": "Webcam Logitech",
  "precio": 290000.0,
  "stock": 14,
  "categoria": "Tecnología",
  "valor_en_inventario": 4060000.0
}
```

**HTTP 201** — Correcto: el id se asigna automáticamente y el valor en inventario se calcula en
la entidad.

---

## Matriz de pruebas funcionales

| # | Caso | Entrada | Resultado esperado | HTTP | Estado |
|---|------|---------|--------------------|------|--------|
| 1 | Health check | — | `{"status":"ok"}` | 200 | OK |
| 2 | Listar productos | — | 8 productos | 200 | OK |
| 3 | Precio mayor a 100.000 | `valor=100000` | 8 productos | 200 | OK |
| 4 | Precio mayor a 500.000 | `valor=500000` | 4 productos | 200 | OK |
| 5 | Valor total inventario | — | 59.850.000 | 200 | OK |
| 6 | Mayor stock | — | Mouse Logitech (25) | 200 | OK |
| 7 | Categoría Tecnología | `Tecnología` | 4 productos | 200 | OK |
| 8 | Categoría inexistente | `Ropa` | lista vacía, total 0 | 200 | OK |
| 9 | Buscar por id válido | `3` | Teclado Mecánico | 200 | OK |
| 10 | Buscar por id inexistente | `99` | PRODUCTO_NO_ENCONTRADO | 404 | OK |
| 11 | Buscar por id inválido | `abc` | error de validación | 422 | OK |
| 12 | Conteo por categoría | — | Tecnología 4, Muebles 2, Audio 2 | 200 | OK |
| 13 | Crear producto válido | JSON completo | producto con id 9 | 201 | OK |
| 14 | Crear producto con precio 0 | `precio: 0` | error de validación | 422 | OK |

---

## Evidencia adicional sugerida para la entrega

1. Captura de Swagger UI (`/docs`) mostrando todos los endpoints.
2. Captura de Postman con la colección importada y las respuestas.
3. Captura de la consola del despliegue (Render/Railway) con el servicio en verde.
4. Captura o video de la app móvil consumiendo la URL pública, más el APK generado.
