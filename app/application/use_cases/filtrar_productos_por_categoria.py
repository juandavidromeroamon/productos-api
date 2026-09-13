# Created by Juan David Romero.

from app.domain.entities.producto import Producto
from app.domain.repositories.producto_repository import ProductoRepository


class FiltrarProductosPorCategoriaUseCase:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, categoria: str) -> list[Producto]:
        return [p for p in self._repositorio.listar() if p.pertenece_a(categoria)]
