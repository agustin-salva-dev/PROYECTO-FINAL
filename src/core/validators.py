"""
Funciones utilitarias de validación sanitaria y de negocio.
Centraliza todas las reglas para evitar repetición de código.
"""

from datetime import date
from src.core.exceptions import (
    StockInsuficienteError,
    LoteVencidoError,
    LoteAgotadoError,
    ValidacionError,
)


def _convertir_a_fecha(valor_fecha) -> date:
    """Convierte un valor a date si viene como string."""
    if isinstance(valor_fecha, date):
        return valor_fecha
    return date.fromisoformat(str(valor_fecha))


def validar_cantidad_positiva(cantidad: int) -> None:
    """Valida que la cantidad especificada sea un entero mayor a 0."""
    if cantidad <= 0:
        raise ValidacionError("La cantidad debe ser un número entero mayor a 0.")


def validar_lote_para_venta(lote: dict, cantidad: int) -> None:
    """
    Valida todas las reglas sanitarias y de stock para una venta:
      1. Que el lote no esté agotado.
      2. Que no esté vencido ni venza hoy.
      3. Que tenga suficiente stock para cubrir la cantidad solicitada.
    """
    num_lote = lote["num_lote"]
    cant_actual = lote["cant_actual"]
    estado = lote["estado"]
    fecha_venc = _convertir_a_fecha(lote["fecha_vencimiento"])

    if estado == "Agotado" or cant_actual == 0:
        raise LoteAgotadoError(num_lote)

    if estado == "Vencido" or fecha_venc <= date.today():
        raise LoteVencidoError(num_lote, str(fecha_venc))

    if cantidad > cant_actual:
        raise StockInsuficienteError(num_lote, cant_actual, cantidad)


def validar_lote_para_ingreso(lote: dict) -> None:
    """Valida que no se ingresen unidades a un lote que ya esté vencido."""
    fecha_venc = _convertir_a_fecha(lote["fecha_vencimiento"])
    if fecha_venc <= date.today():
        raise LoteVencidoError(lote["num_lote"], str(fecha_venc))


def validar_lote_para_baja(lote: dict) -> None:
    """Valida que el lote tenga unidades físicas para descartar."""
    if lote["cant_actual"] == 0:
        raise ValidacionError(f"El lote '{lote['num_lote']}' ya no tiene unidades físicas para descartar.")

