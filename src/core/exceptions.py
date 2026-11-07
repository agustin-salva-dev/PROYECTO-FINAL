"""
Excepciones personalizadas de la farmacia.
Permiten a la capa de servicios comunicar errores de negocio claros y controlados.
"""


class FarmaciaError(Exception):
    """Excepción base para todos los errores del sistema de farmacia."""
    pass


class StockInsuficienteError(FarmaciaError):
    """Se lanza cuando se intenta vender o descontar más stock del disponible en un lote."""
    def __init__(self, num_lote: str, disponible: int, solicitado: int):
        self.num_lote = num_lote
        self.disponible = disponible
        self.solicitado = solicitado
        super().__init__(
            f"Stock insuficiente en lote '{num_lote}'. "
            f"Disponible: {disponible} | Solicitado: {solicitado}."
        )


class LoteVencidoError(FarmaciaError):
    """Se lanza cuando se intenta operar comercialmente con un lote vencido o que vence hoy."""
    def __init__(self, num_lote: str, fecha_vencimiento):
        self.num_lote = num_lote
        self.fecha_vencimiento = fecha_vencimiento
        super().__init__(
            f"El lote '{num_lote}' no es apto para la venta por fecha de vencimiento ({fecha_vencimiento}). "
            f"Operación bloqueada por seguridad sanitaria preventiva."
        )


class LoteAgotadoError(FarmaciaError):
    """Se lanza cuando se intenta operar con un lote sin unidades disponibles (stock = 0)."""
    def __init__(self, num_lote: str):
        self.num_lote = num_lote
        super().__init__(f"El lote '{num_lote}' se encuentra agotado (stock = 0).")


class EntidadNoEncontradaError(FarmaciaError):
    """Se lanza cuando un registro solicitado por ID no existe en la base de datos."""
    def __init__(self, entidad: str, id_registro):
        self.entidad = entidad
        self.id_registro = id_registro
        super().__init__(f"No se encontró {entidad} con ID {id_registro}.")


class ValidacionError(FarmaciaError):
    """Se lanza cuando algún dato de entrada no cumple las reglas básicas de validación."""
    pass

