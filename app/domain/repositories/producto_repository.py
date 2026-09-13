# Created by Juan David Romero.

from abc import ABC, abstractmethod

from app.domain.entities.producto import Producto


class ProductoRepository(ABC):

    @abstractmethod
    def listar(self) -> list[Producto]:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, producto_id: int) -> Producto | None:
        raise NotImplementedError

    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        """Persiste el producto. Si no trae id, el repositorio le asigna uno y lo devuelve con él."""
        raise NotImplementedError
