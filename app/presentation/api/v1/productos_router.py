# Created by Juan David Romero.

from typing import Any

from fastapi import APIRouter, Depends, Path, Query, status

from app.application.dtos.producto_dto import CrearProductoDTO
from app.application.use_cases.filtrar_productos_por_precio import FiltrarProductosPorPrecioUseCase
from app.presentation.dependencies import Container, obtener_container
from app.presentation.schemas.producto_schema import (
    ConteoPorCategoriaResponse,
    CrearProductoRequest,
    ErrorResponse,
    ListaProductosResponse,
    ProductoResponse,
)

router = APIRouter(prefix="/productos", tags=["Productos"])

RESPUESTA_422: dict[int | str, dict[str, Any]] = {
    422: {"model": ErrorResponse, "description": "Datos de entrada inválidos"},
}


@router.get("", response_model=list[ProductoResponse], summary="Listar todos los productos")
def listar_productos(container: Container = Depends(obtener_container)) -> list[ProductoResponse]:
    productos = container.listar_productos().ejecutar()
    return [ProductoResponse.desde_entidad(p) for p in productos]


@router.get(
    "/precio-mayor",
    response_model=ListaProductosResponse,
    summary="Productos con precio mayor al valor indicado",
    responses=RESPUESTA_422,
)
def productos_precio_mayor(
    valor: float = Query(
        default=FiltrarProductosPorPrecioUseCase.PRECIO_POR_DEFECTO,
        gt=0,
        description="Precio mínimo excluyente",
    ),
    container: Container = Depends(obtener_container),
) -> ListaProductosResponse:
    productos = container.filtrar_por_precio().ejecutar(valor)
    return ListaProductosResponse.desde_entidades(f"precio > {valor:,.0f}", productos)


@router.get(
    "/mayor-stock",
    response_model=ProductoResponse,
    summary="Producto con mayor stock disponible",
    responses={409: {"model": ErrorResponse, "description": "El inventario está vacío"}},
)
def producto_mayor_stock(container: Container = Depends(obtener_container)) -> ProductoResponse:
    return ProductoResponse.desde_entidad(container.obtener_mayor_stock().ejecutar())


@router.get(
    "/categoria/{categoria}",
    response_model=ListaProductosResponse,
    summary="Productos de una categoría (no distingue mayúsculas ni tildes)",
    responses=RESPUESTA_422,
)
def productos_por_categoria(
    categoria: str = Path(description="Nombre de la categoría, por ejemplo Tecnología"),
    container: Container = Depends(obtener_container),
) -> ListaProductosResponse:
    productos = container.filtrar_por_categoria().ejecutar(categoria)
    return ListaProductosResponse.desde_entidades(f"categoria == {categoria}", productos)


@router.get(
    "/conteo-por-categoria",
    response_model=ConteoPorCategoriaResponse,
    summary="Cantidad de productos agrupados por categoría",
)
def conteo_por_categoria(container: Container = Depends(obtener_container)) -> ConteoPorCategoriaResponse:
    resumen = container.contar_por_categoria().ejecutar()
    return ConteoPorCategoriaResponse(total_categorias=len(resumen.conteo), conteo=resumen.conteo)


@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
    summary="Buscar un producto por su id",
    responses={404: {"model": ErrorResponse, "description": "Producto no encontrado"}, **RESPUESTA_422},
)
def buscar_producto(
    producto_id: int = Path(ge=1, description="Identificador del producto"),
    container: Container = Depends(obtener_container),
) -> ProductoResponse:
    producto = container.buscar_producto_por_id().ejecutar(producto_id)
    return ProductoResponse.desde_entidad(producto)


@router.post(
    "",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un producto",
    responses=RESPUESTA_422,
)
def crear_producto(
    peticion: CrearProductoRequest,
    container: Container = Depends(obtener_container),
) -> ProductoResponse:
    datos = CrearProductoDTO(
        nombre=peticion.nombre,
        precio=peticion.precio,
        stock=peticion.stock,
        categoria=peticion.categoria,
    )
    return ProductoResponse.desde_entidad(container.crear_producto().ejecutar(datos))
