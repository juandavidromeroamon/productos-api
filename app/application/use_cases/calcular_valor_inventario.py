# Created by Juan David Romero.

from app.application.dtos.producto_dto import ValorInventarioDTO
from app.domain.repositories.producto_repository import ProductoRepository


class CalcularValorInventarioUseCase:

    def __init__(self, repositorio: ProductoRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self) -> ValorInventarioDTO:
        productos = self._repositorio.listar()
        return ValorInventarioDTO(
            valor_total=sum(p.valor_en_inventario() for p in productos),
            cantidad_productos=len(productos),
            unidades_totales=sum(p.stock for p in productos),
        )
