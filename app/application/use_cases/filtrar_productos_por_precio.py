# Created by Juan David Romero.

from app.domain.entities.producto import Producto
from app.domain.repositories.producto_repository import ProductoRepository


class FiltrarProductosPorPrecioUseCase:

    PRECIO_POR_DEFECTO = 100000.0

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, precio_minimo: float = PRECIO_POR_DEFECTO) -> list[Producto]:
        return [p for p in self._repositorio.listar() if p.supera_precio(precio_minimo)]
