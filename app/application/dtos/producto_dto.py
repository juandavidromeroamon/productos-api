# Created by Juan David Romero.

from dataclasses import dataclass


@dataclass(frozen=True)
class CrearProductoDTO:
    nombre: str
    precio: float
    stock: int
    categoria: str


@dataclass(frozen=True)
class ValorInventarioDTO:
    valor_total: float
    cantidad_productos: int
    unidades_totales: int


@dataclass(frozen=True)
class ResumenCategoriasDTO:
    conteo: dict[str, int]
