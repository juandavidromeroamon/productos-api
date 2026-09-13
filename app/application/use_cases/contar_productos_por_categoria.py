# Created by Juan David Romero.

from collections import Counter

from app.application.dtos.producto_dto import ResumenCategoriasDTO
from app.domain.repositories.producto_repository import ProductoRepository


class ContarProductosPorCategoriaUseCase:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self) -> ResumenCategoriasDTO:
        # Agrupa con la misma regla que el filtro ("tecnologia" y "Tecnología" son la misma
        # categoría) y muestra el nombre con el que apareció por primera vez.
        nombres: dict[str, str] = {}
        conteo: Counter[str] = Counter()
        for producto in self._repositorio.listar():
            clave = producto.clave_categoria()
            nombres.setdefault(clave, producto.categoria)
            conteo[clave] += 1
        return ResumenCategoriasDTO(conteo={nombres[clave]: n for clave, n in conteo.items()})
