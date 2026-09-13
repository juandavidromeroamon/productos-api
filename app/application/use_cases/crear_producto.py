# Created by Juan David Romero.

from app.application.dtos.producto_dto import CrearProductoDTO
from app.domain.entities.producto import Producto
from app.domain.repositories.producto_repository import ProductoRepository


class CrearProductoUseCase:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, datos: CrearProductoDTO) -> Producto:
        producto = Producto(
            nombre=datos.nombre,
            precio=datos.precio,
            stock=datos.stock,
            categoria=datos.categoria,
        )
        return self._repositorio.guardar(producto)
