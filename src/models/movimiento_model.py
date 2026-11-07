import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import ejecutar_lectura, ejecutar_escritura, ejecutar_transaccion
from src.models.base_model import BaseModel


class MovimientoModel(BaseModel):
    """
    Modelo para la entidad Movimientos de Stock.
    Concentra todas las sentencias SQL de persistencia para movimientos e historial.
    Hereda de BaseModel: obtener_todos(), obtener_por_id(), eliminar(), contar_total().
    """

    def __init__(self):
        super().__init__(nombre_tabla="movimientos_stock", clave_primaria="id_movimiento")

    # ==========================================
    # C: CREATE INDIVIDUAL
    # ==========================================
    def crear(self, tipo: str, cantidad: int, id_lote: int, fecha_hora: str = None) -> int:
        """Inserta un movimiento de stock individual."""
        if fecha_hora:
            sql = "INSERT INTO movimientos_stock (tipo, cantidad, fecha_hora, id_lote) VALUES (%s, %s, %s, %s)"
            valores = (tipo, cantidad, fecha_hora, id_lote)
        else:
            sql = "INSERT INTO movimientos_stock (tipo, cantidad, fecha_hora, id_lote) VALUES (%s, %s, NOW(), %s)"
            valores = (tipo, cantidad, id_lote)

        resultado = ejecutar_escritura(sql, valores)
        return resultado["ultimo_id"]

    # ==========================================
    # TRANSACCIÓN DE STOCK
    # ==========================================
    def registrar_movimiento_y_actualizar_lote(
        self, id_lote: int, tipo: str, cantidad: int, nueva_cant: int, nuevo_estado: str
    ) -> bool:
        """
        Ejecuta en una sola transacción SQL:
          1. El cambio de stock y estado en la tabla 'lotes'.
          2. La inserción del registro histórico en 'movimientos_stock'.
        """
        operaciones = [
            (
                "UPDATE lotes SET cant_actual = %s, estado = %s WHERE id_lote = %s",
                (nueva_cant, nuevo_estado, id_lote),
            ),
            (
                "INSERT INTO movimientos_stock (tipo, cantidad, fecha_hora, id_lote) VALUES (%s, %s, NOW(), %s)",
                (tipo, cantidad, id_lote),
            ),
        ]
        return ejecutar_transaccion(operaciones)

    # ==========================================
    # R: READ CON DETALLES (JOINs para auditoría)
    # ==========================================
    def obtener_detallados(self) -> list:
        """Retorna el historial de movimientos enriquecido con datos del lote y medicamento."""
        sql = """
            SELECT 
                ms.id_movimiento,
                ms.tipo,
                ms.cantidad,
                ms.fecha_hora,
                l.num_lote,
                med.nombre_comercial AS medicamento,
                med.presentacion
            FROM movimientos_stock ms
            JOIN lotes l ON ms.id_lote = l.id_lote
            JOIN medicamentos med ON l.id_medicamento = med.id_medicamento
            ORDER BY ms.fecha_hora DESC
        """
        return ejecutar_lectura(sql)

    def obtener_por_lote(self, id_lote: int) -> list:
        """Retorna todos los movimientos asociados a un lote específico."""
        sql = "SELECT * FROM movimientos_stock WHERE id_lote = %s ORDER BY fecha_hora DESC"
        return ejecutar_lectura(sql, (id_lote,))

    def obtener_por_tipo(self, tipo: str) -> list:
        """Retorna todos los movimientos filtrados por tipo ('Ingreso', 'Venta', 'Baja_vencimiento')."""
        sql = "SELECT * FROM movimientos_stock WHERE tipo = %s ORDER BY fecha_hora DESC"
        return ejecutar_lectura(sql, (tipo,))

