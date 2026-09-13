# Created by Juan David Romero.

from app.domain.entities.producto import Producto
from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.repositories.producto_repository import ProductoRepository


class BuscarProductoPorIdUseCase:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, producto_id: int) -> Producto:
        producto = self._repositorio.obtener_por_id(producto_id)
        if producto is None:
            raise ProductoNoEncontradoError(producto_id)
        return producto
