# Created by Juan David Romero.

from app.domain.entities.producto import Producto
from app.domain.repositories.producto_repository import ProductoRepository


class ListarProductosUseCase:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self) -> list[Producto]:
        return self._repositorio.listar()
