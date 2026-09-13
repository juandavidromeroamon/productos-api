# Created by Juan David Romero.

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DominioError,
    InventarioVacioError,
    ProductoDuplicadoError,
    ProductoInvalidoError,
    ProductoNoEncontradoError,
)
from app.presentation.schemas.producto_schema import DetalleValidacion, ErrorResponse

ERRORES_DE_DOMINIO: dict[type[DominioError], tuple[int, str]] = {
    ProductoNoEncontradoError: (status.HTTP_404_NOT_FOUND, "PRODUCTO_NO_ENCONTRADO"),
    ProductoDuplicadoError: (status.HTTP_409_CONFLICT, "PRODUCTO_DUPLICADO"),
    InventarioVacioError: (status.HTTP_409_CONFLICT, "INVENTARIO_VACIO"),
    ProductoInvalidoError: (status.HTTP_422_UNPROCESSABLE_ENTITY, "PRODUCTO_INVALIDO"),
}
ERROR_DE_DOMINIO_GENERICO = (status.HTTP_400_BAD_REQUEST, "ERROR_DE_DOMINIO")


def _responder(status_code: int, error: ErrorResponse) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=error.model_dump(exclude_none=True))


def registrar_manejadores(app: FastAPI) -> None:

    # Starlette busca el manejador recorriendo la jerarquía de la excepción, así que este
    # cubre cualquier subclase de DominioError, incluidas las que se agreguen en el futuro.
    @app.exception_handler(DominioError)
    async def error_de_dominio(_: Request, exc: DominioError) -> JSONResponse:
        status_code, codigo = ERRORES_DE_DOMINIO.get(type(exc), ERROR_DE_DOMINIO_GENERICO)
        return _responder(status_code, ErrorResponse(detalle=str(exc), codigo=codigo))

    # Reemplaza el 422 por defecto de FastAPI ({"detail": [...]}) para que todos los errores
    # de la API compartan el mismo formato.
    @app.exception_handler(RequestValidationError)
    async def error_de_validacion(_: Request, exc: RequestValidationError) -> JSONResponse:
        errores = [
            DetalleValidacion(campo=".".join(str(parte) for parte in error["loc"]), mensaje=error["msg"])
            for error in exc.errors()
        ]
        return _responder(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            ErrorResponse(detalle="Los datos enviados no son válidos", codigo="DATOS_INVALIDOS", errores=errores),
        )
