class Observer:
    """Interface para observadores de eventos."""
    def actualizar(self, evento: str) -> None:
        raise NotImplementedError("Método actualizar debe implementarse por subclases.")