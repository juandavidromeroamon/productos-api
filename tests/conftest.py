import pytest
from fastapi.testclient import TestClient

from app.infrastructure.repositories.in_memory_producto_repository import InMemoryProductoRepository
from app.main import crear_app
from app.presentation.dependencies import Container, obtener_container


def construir_cliente(repositorio: InMemoryProductoRepository) -> TestClient:
    app = crear_app()
    app.dependency_overrides[obtener_container] = lambda: Container(repositorio)
    return TestClient(app)


@pytest.fixture
def repositorio() -> InMemoryProductoRepository:
    # Repositorio nuevo en cada prueba para que ninguna dependa del estado que dejó otra.
    return InMemoryProductoRepository()


@pytest.fixture
def repositorio_vacio() -> InMemoryProductoRepository:
    return InMemoryProductoRepository(productos_iniciales=[])


@pytest.fixture
def cliente(repositorio: InMemoryProductoRepository) -> TestClient:
    return construir_cliente(repositorio)


@pytest.fixture
def cliente_vacio(repositorio_vacio: InMemoryProductoRepository) -> TestClient:
    return construir_cliente(repositorio_vacio)
