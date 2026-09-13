from concurrent.futures import ThreadPoolExecutor

import pytest

from app.application.dtos.producto_dto import CrearProductoDTO
from app.application.use_cases.buscar_producto_por_id import BuscarProductoPorIdUseCase
from app.application.use_cases.calcular_valor_inventario import CalcularValorInventarioUseCase
from app.application.use_cases.contar_productos_por_categoria import ContarProductosPorCategoriaUseCase
from app.application.use_cases.crear_producto import CrearProductoUseCase
from app.application.use_cases.filtrar_productos_por_categoria import FiltrarProductosPorCategoriaUseCase
from app.application.use_cases.filtrar_productos_por_precio import FiltrarProductosPorPrecioUseCase
from app.application.use_cases.obtener_producto_mayor_stock import ObtenerProductoMayorStockUseCase
from app.domain.entities.producto import Producto
from app.domain.exceptions import InventarioVacioError, ProductoDuplicadoError, ProductoNoEncontradoError


def test_filtrar_por_precio_usa_100000_por_defecto(repositorio):
    assert len(FiltrarProductosPorPrecioUseCase(repositorio).ejecutar()) == 8


def test_filtrar_por_precio_con_valor_personalizado(repositorio):
    productos = FiltrarProductosPorPrecioUseCase(repositorio).ejecutar(1_000_000)
    assert [p.id for p in productos] == [1, 5]


def test_calcular_valor_inventario(repositorio):
    resumen = CalcularValorInventarioUseCase(repositorio).ejecutar()
    assert resumen.valor_total == 59_850_000
    assert resumen.cantidad_productos == 8
    assert resumen.unidades_totales == 91


def test_calcular_valor_inventario_vacio(repositorio_vacio):
    resumen = CalcularValorInventarioUseCase(repositorio_vacio).ejecutar()
    assert (resumen.valor_total, resumen.cantidad_productos, resumen.unidades_totales) == (0, 0, 0)


def test_obtener_producto_mayor_stock(repositorio):
    assert ObtenerProductoMayorStockUseCase(repositorio).ejecutar().id == 2


def test_obtener_producto_mayor_stock_con_inventario_vacio(repositorio_vacio):
    with pytest.raises(InventarioVacioError):
        ObtenerProductoMayorStockUseCase(repositorio_vacio).ejecutar()


def test_filtrar_por_categoria_sin_tildes_ni_mayusculas(repositorio):
    productos = FiltrarProductosPorCategoriaUseCase(repositorio).ejecutar("tecnologia")
    assert [p.id for p in productos] == [1, 2, 3, 8]


def test_buscar_producto_existente(repositorio):
    assert BuscarProductoPorIdUseCase(repositorio).ejecutar(4).nombre == "Silla Ergonómica"


def test_buscar_producto_inexistente(repositorio):
    with pytest.raises(ProductoNoEncontradoError):
        BuscarProductoPorIdUseCase(repositorio).ejecutar(99)


def test_contar_por_categoria(repositorio):
    conteo = ContarProductosPorCategoriaUseCase(repositorio).ejecutar().conteo
    assert conteo == {"Tecnología": 4, "Muebles": 2, "Audio": 2}


def test_contar_por_categoria_agrupa_igual_que_el_filtro(repositorio):
    CrearProductoUseCase(repositorio).ejecutar(
        CrearProductoDTO(nombre="Tablet", precio=900_000, stock=4, categoria="tecnologia")
    )
    conteo = ContarProductosPorCategoriaUseCase(repositorio).ejecutar().conteo
    filtrados = FiltrarProductosPorCategoriaUseCase(repositorio).ejecutar("Tecnología")
    assert conteo == {"Tecnología": 5, "Muebles": 2, "Audio": 2}
    assert len(filtrados) == 5


def test_crear_producto_asigna_id_y_normaliza(repositorio):
    creado = CrearProductoUseCase(repositorio).ejecutar(
        CrearProductoDTO(nombre="  Tablet ", precio=900_000, stock=4, categoria=" Tecnología ")
    )
    assert creado.id == 9
    assert creado.nombre == "Tablet"
    assert repositorio.obtener_por_id(9) == creado


def test_guardar_producto_con_id_repetido_falla(repositorio):
    with pytest.raises(ProductoDuplicadoError):
        repositorio.guardar(Producto(id=1, nombre="Otro", precio=1, stock=1, categoria="X"))


def test_crear_productos_en_paralelo_no_repite_ids(repositorio):
    caso_de_uso = CrearProductoUseCase(repositorio)
    datos = CrearProductoDTO(nombre="Cable", precio=10_000, stock=1, categoria="Tecnología")

    with ThreadPoolExecutor(max_workers=16) as ejecutor:
        creados = list(ejecutor.map(lambda _: caso_de_uso.ejecutar(datos), range(200)))

    ids = [p.id for p in creados]
    assert len(set(ids)) == 200
    assert len(repositorio.listar()) == 208
