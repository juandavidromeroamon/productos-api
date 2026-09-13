import math

import pytest

from app.domain.entities.producto import PRECIO_MAXIMO, STOCK_MAXIMO, Producto
from app.domain.exceptions import ProductoInvalidoError

DATOS_VALIDOS = {"id": 1, "nombre": "Laptop", "precio": 1000.0, "stock": 3, "categoria": "Tecnología"}


def test_calcula_valor_en_inventario():
    assert Producto(**DATOS_VALIDOS).valor_en_inventario() == 3000.0


def test_quita_espacios_de_nombre_y_categoria():
    producto = Producto(**{**DATOS_VALIDOS, "nombre": "  Laptop  ", "categoria": " Tecnología "})
    assert producto.nombre == "Laptop"
    assert producto.categoria == "Tecnología"


def test_permite_crear_producto_sin_id():
    assert Producto(**{**DATOS_VALIDOS, "id": None}).id is None


@pytest.mark.parametrize("categoria", ["Tecnología", "tecnologia", "  TECNOLOGÍA ", "Tecnologia"])
def test_pertenece_a_ignora_mayusculas_tildes_y_espacios(categoria):
    assert Producto(**DATOS_VALIDOS).pertenece_a(categoria)


def test_no_pertenece_a_otra_categoria():
    assert not Producto(**DATOS_VALIDOS).pertenece_a("Muebles")


def test_supera_precio_es_excluyente():
    producto = Producto(**DATOS_VALIDOS)
    assert producto.supera_precio(999.0)
    assert not producto.supera_precio(1000.0)


@pytest.mark.parametrize(
    "cambios",
    [
        {"id": 0},
        {"nombre": "   "},
        {"nombre": "x" * 121},
        {"categoria": ""},
        {"precio": 0},
        {"precio": -1},
        {"precio": math.inf},
        {"precio": math.nan},
        {"precio": PRECIO_MAXIMO + 1},
        {"stock": -1},
        {"stock": STOCK_MAXIMO + 1},
    ],
)
def test_rechaza_datos_invalidos(cambios):
    with pytest.raises(ProductoInvalidoError):
        Producto(**{**DATOS_VALIDOS, **cambios})
