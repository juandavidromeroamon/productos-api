# Created by Juan David Romero.

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.producto import (
    LONGITUD_MAXIMA_CATEGORIA,
    LONGITUD_MAXIMA_NOMBRE,
    PRECIO_MAXIMO,
    STOCK_MAXIMO,
    Producto,
)


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    categoria: str
    valor_en_inventario: float

    @classmethod
    def desde_entidad(cls, producto: Producto) -> "ProductoResponse":
        return cls(
            id=producto.id,
            nombre=producto.nombre,
            precio=producto.precio,
            stock=producto.stock,
            categoria=producto.categoria,
            valor_en_inventario=producto.valor_en_inventario(),
        )


class ListaProductosResponse(BaseModel):
    criterio: str
    total: int
    productos: list[ProductoResponse]

    @classmethod
    def desde_entidades(cls, criterio: str, productos: list[Producto]) -> "ListaProductosResponse":
        return cls(
            criterio=criterio,
            total=len(productos),
            productos=[ProductoResponse.desde_entidad(p) for p in productos],
        )


class ValorInventarioResponse(BaseModel):
    valor_total: float
    cantidad_productos: int
    unidades_totales: int
    moneda: str = "COP"


class ConteoPorCategoriaResponse(BaseModel):
    total_categorias: int
    conteo: dict[str, int]


class CrearProductoRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=1, max_length=LONGITUD_MAXIMA_NOMBRE)
    precio: float = Field(gt=0, le=PRECIO_MAXIMO)
    stock: int = Field(ge=0, le=STOCK_MAXIMO)
    categoria: str = Field(min_length=1, max_length=LONGITUD_MAXIMA_CATEGORIA)


class DetalleValidacion(BaseModel):
    campo: str
    mensaje: str


class ErrorResponse(BaseModel):
    detalle: str
    codigo: str
    errores: list[DetalleValidacion] | None = None
