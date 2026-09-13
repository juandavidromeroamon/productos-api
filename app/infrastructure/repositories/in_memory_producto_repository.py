# Created by Juan David Romero.

import threading
from collections.abc import Iterable
from dataclasses import replace
from typing import Any

from app.domain.entities.producto import Producto
from app.domain.exceptions import ProductoDuplicadoError
from app.domain.repositories.producto_repository import ProductoRepository
from app.infrastructure.data.productos_seed import PRODUCTOS_INICIALES


class InMemoryProductoRepository(ProductoRepository):

    def __init__(self, productos_iniciales: Iterable[dict[str, Any]] = PRODUCTOS_INICIALES) -> None:
        self._productos: dict[int, Producto] = {}
        # FastAPI ejecuta los endpoints síncronos en varios hilos: el candado evita ids repetidos
        # y lecturas mientras otro hilo modifica el diccionario.
        self._candado = threading.Lock()
        for registro in productos_iniciales:
            self.guardar(Producto(**registro))

    def listar(self) -> list[Producto]:
        with self._candado:
            return [self._productos[producto_id] for producto_id in sorted(self._productos)]

    def obtener_por_id(self, producto_id: int) -> Producto | None:
        with self._candado:
            return self._productos.get(producto_id)

    def guardar(self, producto: Producto) -> Producto:
        with self._candado:
            if producto.id is None:
                producto = replace(producto, id=max(self._productos, default=0) + 1)
            elif producto.id in self._productos:
                raise ProductoDuplicadoError(producto.id)
            self._productos[producto.id] = producto
            return producto
