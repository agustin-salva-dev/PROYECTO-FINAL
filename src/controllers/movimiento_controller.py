import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.exceptions import EntidadNoEncontradaError
from src.core.validators import (
    validar_cantidad_positiva,
    validar_lote_para_venta,
    validar_lote_para_ingreso,
    validar_lote_para_baja,
)
from src.models.lote_model import LoteModel
from src.models.movimiento_model import MovimientoModel


class MovimientoController:
    """
    Controlador para transacciones de stock físico (Patrón MVC).
    Aplica las reglas de negocio y orquesta los modelos del sistema.
    """

    def __init__(self):
        self.lote_model = LoteModel()
        self.movimiento_model = MovimientoModel()

    # ==========================================
    # MÉTODO AUXILIAR PRIVADO
    # ==========================================
    def _obtener_lote(self, id_lote: int) -> dict:
        lote = self.lote_model.obtener_por_id(id_lote)
        if not lote:
            raise EntidadNoEncontradaError("Lote", id_lote)
        return lote

    # ==========================================
    # ACCIONES DEL CONTROLADOR
    # ==========================================
    def registrar_venta(self, id_lote: int, cantidad: int) -> dict:
        """Registra la venta descontando stock y asentando el movimiento mediante el modelo."""
        validar_cantidad_positiva(cantidad)
        lote = self._obtener_lote(id_lote)
        validar_lote_para_venta(lote, cantidad)

        nueva_cant = lote["cant_actual"] - cantidad
        nuevo_estado = "Agotado" if nueva_cant == 0 else "Activo"

        self.movimiento_model.registrar_movimiento_y_actualizar_lote(
            id_lote=id_lote,
            tipo="Venta",
            cantidad=cantidad,
            nueva_cant=nueva_cant,
            nuevo_estado=nuevo_estado,
        )
        return {"id_lote": id_lote, "cantidad": cantidad, "stock_restante": nueva_cant, "estado": nuevo_estado}

    def registrar_ingreso(self, id_lote: int, cantidad: int) -> dict:
        """Registra el ingreso reactivando el lote si estaba agotado."""
        validar_cantidad_positiva(cantidad)
        lote = self._obtener_lote(id_lote)
        validar_lote_para_ingreso(lote)

        nueva_cant = lote["cant_actual"] + cantidad
        self.movimiento_model.registrar_movimiento_y_actualizar_lote(
            id_lote=id_lote,
            tipo="Ingreso",
            cantidad=cantidad,
            nueva_cant=nueva_cant,
            nuevo_estado="Activo",
        )
        return {"id_lote": id_lote, "cantidad": cantidad, "stock_total": nueva_cant, "estado": "Activo"}

    def dar_de_baja_por_vencimiento(self, id_lote: int) -> dict:
        """Descarta las unidades físicas de un lote y cambia su estado a 'Vencido'."""
        lote = self._obtener_lote(id_lote)
        validar_lote_para_baja(lote)

        cant_descarte = lote["cant_actual"]
        self.movimiento_model.registrar_movimiento_y_actualizar_lote(
            id_lote=id_lote,
            tipo="Baja_vencimiento",
            cantidad=cant_descarte,
            nueva_cant=0,
            nuevo_estado="Vencido",
        )
        return {"id_lote": id_lote, "unidades_descartadas": cant_descarte, "estado": "Vencido"}
