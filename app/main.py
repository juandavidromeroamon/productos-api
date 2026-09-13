# Created by Juan David Romero.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.presentation.api.v1 import inventario_router, productos_router
from app.presentation.error_handlers import registrar_manejadores


def crear_app() -> FastAPI:
    app = FastAPI(
        title=settings.nombre_app,
        version=settings.version,
        description=settings.descripcion,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origenes_permitidos,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    registrar_manejadores(app)
    app.include_router(productos_router.router, prefix=settings.prefijo_api)
    app.include_router(inventario_router.router, prefix=settings.prefijo_api)

    @app.get("/", tags=["Salud"], summary="Estado del servicio")
    def estado():
        return {
            "servicio": settings.nombre_app,
            "version": settings.version,
            "estado": "activo",
            "documentacion": "/docs",
        }

    @app.get("/health", tags=["Salud"], summary="Health check")
    def health():
        return {"status": "ok"}

    return app


app = crear_app()
