# Created by Juan David Romero.


class DominioError(Exception):
    pass


class ProductoInvalidoError(DominioError):
    def __init__(self, motivo: str) -> None:
        self.motivo = motivo
        super().__init__(f"Producto inválido: {motivo}")


class ProductoNoEncontradoError(DominioError):
    def __init__(self, producto_id: int) -> None:
        self.producto_id = producto_id
        super().__init__(f"No existe un producto con id {producto_id}")


class InventarioVacioError(DominioError):
    def __init__(self) -> None:
        super().__init__("El inventario no contiene productos")


class ProductoDuplicadoError(DominioError):
    def __init__(self, producto_id: int) -> None:
        self.producto_id = producto_id
        super().__init__(f"Ya existe un producto con id {producto_id}")
