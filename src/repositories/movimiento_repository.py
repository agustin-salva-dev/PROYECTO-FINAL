import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import ejecutar_lectura, ejecutar_escritura
from src.repositories.base_repository import BaseRepository


class MovimientoRepository(BaseRepository):
    """
    Repositorio para la entidad Movimientos de Stock.
    Registra ingresos, ventas y bajas por vencimiento vinculados a un lote específico.
    Hereda de BaseRepository: obtener_todos(), obtener_por_id(), eliminar(), contar_total().
    """

    def __init__(self):
        super().__init__(nombre_tabla="movimientos_stock", clave_primaria="id_movimiento")

    # ==========================================
    # C: CREATE
    # ==========================================
    def crear(self, tipo, cantidad, id_lote, fecha_hora=None):
        """
        Inserta un nuevo movimiento de stock.
        :param tipo: 'Ingreso', 'Venta' o 'Baja_vencimiento'.
        :param cantidad: Cantidad de unidades implicadas en el movimiento.
        :param id_lote: ID del lote al que afecta el movimiento.
        :param fecha_hora: Fecha y hora (opcional; si es None, MySQL usa NOW()).
        :return: ID del movimiento generado.
        """
        if fecha_hora:
            sql = """
                INSERT INTO movimientos_stock (tipo, cantidad, fecha_hora, id_lote)
                VALUES (%s, %s, %s, %s)
            """
            valores = (tipo, cantidad, fecha_hora, id_lote)
        else:
            sql = """
                INSERT INTO movimientos_stock (tipo, cantidad, fecha_hora, id_lote)
                VALUES (%s, %s, NOW(), %s)
            """
            valores = (tipo, cantidad, id_lote)

        resultado = ejecutar_escritura(sql, valores)
        nuevo_id = resultado["ultimo_id"]

        print(f"Movimiento '{tipo}' de {cantidad} un. registrado para el Lote ID {id_lote}. ID Asignado: {nuevo_id}")
        return nuevo_id

    # ==========================================
    # R: READ CON DETALLES (JOINs para auditoría)
    # ==========================================
    def obtener_detallados(self):
        """
        Retorna el historial de movimientos enriquecido con los datos del
        lote y del medicamento correspondiente (ideal para reportes y tablas UI).
        """
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

    def obtener_por_lote(self, id_lote):
        """Retorna todos los movimientos asociados a un lote específico."""
        sql = "SELECT * FROM movimientos_stock WHERE id_lote = %s ORDER BY fecha_hora DESC"
        return ejecutar_lectura(sql, (id_lote,))

    def obtener_por_tipo(self, tipo):
        """Retorna todos los movimientos filtrados por tipo ('Ingreso', 'Venta', 'Baja_vencimiento')."""
        sql = "SELECT * FROM movimientos_stock WHERE tipo = %s ORDER BY fecha_hora DESC"
        return ejecutar_lectura(sql, (tipo,))


# ==========================================
# EJEMPLO DE USO DE LA CLASE
# ==========================================
if __name__ == "__main__":
    repo = MovimientoRepository()

    print("--- 1. REGISTRAR MOVIMIENTO TEMPORAL ---")
    id_nuevo = repo.crear(tipo="Venta", cantidad=5, id_lote=1)

    print("\n--- 2. LEER HISTORIAL DETALLADO (JOIN Lotes y Medicamentos) ---")
    historial = repo.obtener_detallados()
    for mov in historial[:5]:  # Mostramos los últimos 5
        print(f"ID: {mov['id_movimiento']} | Fecha: {mov['fecha_hora']} | Tipo: {mov['tipo']:<16} | Cant: {mov['cantidad']} | Lote: {mov['num_lote']} | Med: {mov['medicamento']}")

    print("\n--- 3. ELIMINAR MOVIMIENTO TEMPORAL (Heredado de BaseRepository) ---")
    repo.eliminar(id_nuevo)

