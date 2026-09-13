# Created by Juan David Romero.

import math
import unicodedata
from dataclasses import dataclass

from app.domain.exceptions import ProductoInvalidoError

PRECIO_MAXIMO = 1_000_000_000.0
STOCK_MAXIMO = 1_000_000
LONGITUD_MAXIMA_NOMBRE = 120
LONGITUD_MAXIMA_CATEGORIA = 60


def normalizar_texto(texto: str) -> str:
    """Quita tildes, espacios sobrantes y mayúsculas para comparar textos."""
    descompuesto = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join(c for c in descompuesto if not unicodedata.combining(c))
    return sin_tildes.strip().casefold()


@dataclass(frozen=True, kw_only=True)
class Producto:
    id: int | None = None
    nombre: str
    precio: float
    stock: int
    categoria: str

    def __post_init__(self) -> None:
        # La entidad está congelada; se usa object.__setattr__ solo para normalizar al construirla.
        object.__setattr__(self, "nombre", self.nombre.strip())
        object.__setattr__(self, "categoria", self.categoria.strip())
        self._validar()

    def _validar(self) -> None:
        if self.id is not None and self.id < 1:
            raise ProductoInvalidoError("el id debe ser mayor o igual a 1")
        if not 1 <= len(self.nombre) <= LONGITUD_MAXIMA_NOMBRE:
            raise ProductoInvalidoError(f"el nombre debe tener entre 1 y {LONGITUD_MAXIMA_NOMBRE} caracteres")
        if not 1 <= len(self.categoria) <= LONGITUD_MAXIMA_CATEGORIA:
            raise ProductoInvalidoError(
                f"la categoría debe tener entre 1 y {LONGITUD_MAXIMA_CATEGORIA} caracteres"
            )
        if not math.isfinite(self.precio) or not 0 < self.precio <= PRECIO_MAXIMO:
            raise ProductoInvalidoError(f"el precio debe ser mayor a 0 y menor o igual a {PRECIO_MAXIMO:,.0f}")
        if not 0 <= self.stock <= STOCK_MAXIMO:
            raise ProductoInvalidoError(f"el stock debe estar entre 0 y {STOCK_MAXIMO:,}")

    def valor_en_inventario(self) -> float:
        return self.precio * self.stock

    def supera_precio(self, valor: float) -> bool:
        return self.precio > valor

    def clave_categoria(self) -> str:
        return normalizar_texto(self.categoria)

    def pertenece_a(self, categoria: str) -> bool:
        return self.clave_categoria() == normalizar_texto(categoria)
