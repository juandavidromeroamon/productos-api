# Created by Juan David Romero.

from fastapi import APIRouter, Depends

from app.presentation.dependencies import Container, obtener_container
from app.presentation.schemas.producto_schema import ValorInventarioResponse

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get(
    "/valor-total",
    response_model=ValorInventarioResponse,
    summary="Valor total del inventario (precio x stock)",
)
def valor_total_inventario(container: Container = Depends(obtener_container)) -> ValorInventarioResponse:
    resumen = container.calcular_valor_inventario().ejecutar()
    return ValorInventarioResponse(
        valor_total=resumen.valor_total,
        cantidad_productos=resumen.cantidad_productos,
        unidades_totales=resumen.unidades_totales,
    )
