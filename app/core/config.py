# Created by Juan David Romero.

import os
from dataclasses import dataclass, field


def _leer_lista_de_entorno(variable: str, por_defecto: str) -> list[str]:
    return [valor.strip() for valor in os.getenv(variable, por_defecto).split(",") if valor.strip()]


@dataclass(frozen=True)
class Settings:
    nombre_app: str = "Productos API"
    version: str = "1.1.0"
    descripcion: str = (
        "API REST de gestión de inventario de productos construida en Python con FastAPI, "
        "programación orientada a objetos y arquitectura por capas."
    )
    prefijo_api: str = "/api/v1"
    # Ejemplo: CORS_ORIGINS="https://mi-app.com,http://localhost:3000". Por defecto acepta cualquier origen.
    origenes_permitidos: list[str] = field(default_factory=lambda: _leer_lista_de_entorno("CORS_ORIGINS", "*"))


settings = Settings()
