# Created by Juan David Romero.

from app.domain.entities.producto import Producto
from app.domain.exceptions import InventarioVacioError
from app.domain.repositories.producto_repository import ProductoRepository


class ObtenerProductoMayorStockUseCase:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self) -> Producto:
        productos = self._repositorio.listar()
        if not productos:
            raise InventarioVacioError()
        # En caso de empate, max() conserva el primero (el de menor id).
        return max(productos, key=lambda p: p.stock)
