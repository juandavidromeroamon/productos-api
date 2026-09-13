# Created by Juan David Romero.

from functools import lru_cache

from app.application.use_cases.buscar_producto_por_id import BuscarProductoPorIdUseCase
from app.application.use_cases.calcular_valor_inventario import CalcularValorInventarioUseCase
from app.application.use_cases.contar_productos_por_categoria import ContarProductosPorCategoriaUseCase
from app.application.use_cases.crear_producto import CrearProductoUseCase
from app.application.use_cases.filtrar_productos_por_categoria import FiltrarProductosPorCategoriaUseCase
from app.application.use_cases.filtrar_productos_por_precio import FiltrarProductosPorPrecioUseCase
from app.application.use_cases.listar_productos import ListarProductosUseCase
from app.application.use_cases.obtener_producto_mayor_stock import ObtenerProductoMayorStockUseCase
from app.domain.repositories.producto_repository import ProductoRepository
from app.infrastructure.repositories.in_memory_producto_repository import InMemoryProductoRepository


class Container:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def listar_productos(self) -> ListarProductosUseCase:
        return ListarProductosUseCase(self._repositorio)

    def buscar_producto_por_id(self) -> BuscarProductoPorIdUseCase:
        return BuscarProductoPorIdUseCase(self._repositorio)

    def filtrar_por_precio(self) -> FiltrarProductosPorPrecioUseCase:
        return FiltrarProductosPorPrecioUseCase(self._repositorio)

    def calcular_valor_inventario(self) -> CalcularValorInventarioUseCase:
        return CalcularValorInventarioUseCase(self._repositorio)

    def obtener_mayor_stock(self) -> ObtenerProductoMayorStockUseCase:
        return ObtenerProductoMayorStockUseCase(self._repositorio)

    def filtrar_por_categoria(self) -> FiltrarProductosPorCategoriaUseCase:
        return FiltrarProductosPorCategoriaUseCase(self._repositorio)

    def contar_por_categoria(self) -> ContarProductosPorCategoriaUseCase:
        return ContarProductosPorCategoriaUseCase(self._repositorio)

    def crear_producto(self) -> CrearProductoUseCase:
        return CrearProductoUseCase(self._repositorio)


@lru_cache
def obtener_container() -> Container:
    return Container(InMemoryProductoRepository())
