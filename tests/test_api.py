import pytest

API = "/api/v1"
PRODUCTO_NUEVO = {"nombre": "Tablet", "precio": 900000, "stock": 4, "categoria": "Tecnología"}


def test_health(cliente):
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}


def test_listar_productos(cliente):
    respuesta = cliente.get(f"{API}/productos")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 8
    assert respuesta.json()[0]["valor_en_inventario"] == 22_400_000


def test_precio_mayor_por_defecto(cliente):
    cuerpo = cliente.get(f"{API}/productos/precio-mayor").json()
    assert cuerpo["criterio"] == "precio > 100,000"
    assert cuerpo["total"] == 8


def test_precio_mayor_con_valor(cliente):
    cuerpo = cliente.get(f"{API}/productos/precio-mayor", params={"valor": 1_000_000}).json()
    assert cuerpo["total"] == 2
    assert [p["id"] for p in cuerpo["productos"]] == [1, 5]


def test_precio_mayor_rechaza_valor_no_positivo(cliente):
    respuesta = cliente.get(f"{API}/productos/precio-mayor", params={"valor": 0})
    assert respuesta.status_code == 422
    assert respuesta.json()["codigo"] == "DATOS_INVALIDOS"


def test_valor_total_inventario(cliente):
    cuerpo = cliente.get(f"{API}/inventario/valor-total").json()
    assert cuerpo == {
        "valor_total": 59_850_000,
        "cantidad_productos": 8,
        "unidades_totales": 91,
        "moneda": "COP",
    }


def test_mayor_stock(cliente):
    cuerpo = cliente.get(f"{API}/productos/mayor-stock").json()
    assert cuerpo["id"] == 2
    assert cuerpo["stock"] == 25


def test_mayor_stock_con_inventario_vacio(cliente_vacio):
    respuesta = cliente_vacio.get(f"{API}/productos/mayor-stock")
    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "INVENTARIO_VACIO"


@pytest.mark.parametrize("categoria", ["Tecnología", "tecnologia"])
def test_productos_por_categoria(cliente, categoria):
    cuerpo = cliente.get(f"{API}/productos/categoria/{categoria}").json()
    assert cuerpo["criterio"] == f"categoria == {categoria}"
    assert cuerpo["total"] == 4


def test_conteo_por_categoria(cliente):
    cuerpo = cliente.get(f"{API}/productos/conteo-por-categoria").json()
    assert cuerpo == {"total_categorias": 3, "conteo": {"Tecnología": 4, "Muebles": 2, "Audio": 2}}


def test_buscar_producto_por_id(cliente):
    respuesta = cliente.get(f"{API}/productos/1")
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Laptop Lenovo"


def test_buscar_producto_inexistente(cliente):
    respuesta = cliente.get(f"{API}/productos/99")
    assert respuesta.status_code == 404
    assert respuesta.json() == {"detalle": "No existe un producto con id 99", "codigo": "PRODUCTO_NO_ENCONTRADO"}


def test_buscar_producto_con_id_no_numerico(cliente):
    respuesta = cliente.get(f"{API}/productos/abc")
    cuerpo = respuesta.json()
    assert respuesta.status_code == 422
    assert cuerpo["codigo"] == "DATOS_INVALIDOS"
    assert cuerpo["errores"][0]["campo"] == "path.producto_id"


def test_crear_producto(cliente):
    respuesta = cliente.post(f"{API}/productos", json=PRODUCTO_NUEVO)
    assert respuesta.status_code == 201
    assert respuesta.json()["id"] == 9
    assert cliente.get(f"{API}/productos/9").status_code == 200


@pytest.mark.parametrize(
    "cambios",
    [
        {"nombre": "   "},
        {"categoria": ""},
        {"precio": 0},
        {"precio": 1e308},
        {"stock": -1},
        {"stock": 10_000_000},
    ],
)
def test_crear_producto_con_datos_invalidos(cliente, cambios):
    respuesta = cliente.post(f"{API}/productos", json={**PRODUCTO_NUEVO, **cambios})
    assert respuesta.status_code == 422
    assert respuesta.json()["codigo"] == "DATOS_INVALIDOS"
    assert len(cliente.get(f"{API}/productos").json()) == 8
