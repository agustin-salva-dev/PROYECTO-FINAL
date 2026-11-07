import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import ejecutar_lectura, ejecutar_escritura
from src.models.base_model import BaseModel


class LoteModel(BaseModel):
    """
    Modelo para la entidad Lotes.
    Hereda de BaseModel: obtener_todos(), obtener_por_id(), eliminar(), contar_total().
    Concentra todas las consultas SQL relacionales vinculadas a stock y lotes físicos.
    """

    def __init__(self):
        super().__init__(nombre_tabla="lotes", clave_primaria="id_lote")

    # ==========================================
    # C: CREATE
    # ==========================================
    def crear(self, num_lote: str, fecha_vencimiento: str, cant_inicial: int, cant_actual: int, id_medicamento: int, id_proveedor: int) -> int:
        """Inserta un nuevo lote y retorna su ID asignado."""
        sql = """
            INSERT INTO lotes (num_lote, fecha_vencimiento, estado, cant_inicial, cant_actual, id_medicamento, id_proveedor)
            VALUES (%s, %s, 'Activo', %s, %s, %s, %s)
        """
        valores = (num_lote, fecha_vencimiento, cant_inicial, cant_actual, id_medicamento, id_proveedor)
        resultado = ejecutar_escritura(sql, valores)
        nuevo_id = resultado["ultimo_id"]

        print(f"Lote '{num_lote}' agregado con éxito. ID asignado: {nuevo_id}")
        return nuevo_id

    # ==========================================
    # R: READ CON DETALLES (JOINs)
    # ==========================================
    def obtener_detallados(self) -> list:
        """Retorna los lotes junto con los nombres del medicamento y proveedor asociados."""
        sql = """
            SELECT 
                l.id_lote, 
                l.num_lote, 
                l.fecha_vencimiento, 
                l.estado,
                l.cant_actual,
                l.cant_inicial, 
                m.nombre_comercial AS medicamento, 
                p.nombre AS proveedor
            FROM lotes l
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            JOIN proveedores p ON l.id_proveedor = p.id_proveedor
            ORDER BY l.fecha_vencimiento ASC
        """
        return ejecutar_lectura(sql)

    def obtener_alertas_stock_critico(self) -> list:
        """
        Consulta relacional con agregación (JOIN, GROUP BY, SUM, HAVING):
        Identifica medicamentos con stock consolidado activo menor o igual al stock mínimo.
        """
        sql = """
            SELECT 
                m.id_medicamento, 
                m.nombre_comercial, 
                m.presentacion, 
                m.dosis_valor, 
                m.dosis_unidad, 
                m.stock_minimo,
                IFNULL(SUM(l.cant_actual), 0) AS stock_total_disponible
            FROM medicamentos m
            LEFT JOIN lotes l ON m.id_medicamento = l.id_medicamento 
                             AND l.estado = 'Activo' 
                             AND l.fecha_vencimiento > CURDATE()
            GROUP BY 
                m.id_medicamento, 
                m.nombre_comercial, 
                m.presentacion, 
                m.dosis_valor, 
                m.dosis_unidad, 
                m.stock_minimo
            HAVING stock_total_disponible <= m.stock_minimo
            ORDER BY stock_total_disponible ASC;
        """
        return ejecutar_lectura(sql)

    def obtener_proximos_a_vencer(self, dias: int = 180) -> list:
        """Consulta relacional: lotes activos con vencimiento próximo."""
        sql = """
            SELECT 
                l.id_lote,
                l.num_lote,
                l.fecha_vencimiento,
                l.cant_actual,
                DATEDIFF(l.fecha_vencimiento, CURDATE()) AS dias_para_vencer,
                m.nombre_comercial AS medicamento,
                m.presentacion,
                p.nombre AS proveedor
            FROM lotes l
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            JOIN proveedores p ON l.id_proveedor = p.id_proveedor
            WHERE l.estado = 'Activo' 
              AND l.cant_actual > 0
              AND l.fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
            ORDER BY l.fecha_vencimiento ASC;
        """
        return ejecutar_lectura(sql, (dias,))

    def obtener_disponibles_venta(self) -> list:
        """Retorna lotes aptos para la venta (activos, con stock y vencimiento futuro)."""
        sql = """
            SELECT 
                l.id_lote,
                l.num_lote,
                l.fecha_vencimiento,
                l.cant_actual,
                m.nombre_comercial AS medicamento,
                m.presentacion,
                CONCAT(m.dosis_valor, m.dosis_unidad) AS dosis
            FROM lotes l
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            WHERE l.estado = 'Activo' 
              AND l.cant_actual > 0 
              AND l.fecha_vencimiento > CURDATE()
            ORDER BY l.fecha_vencimiento ASC;
        """
        return ejecutar_lectura(sql)

    # ==========================================
    # U: UPDATE
    # ==========================================
    def actualizar_stock_y_estado(self, id_lote: int, nueva_cant_actual: int, nuevo_estado: str = None) -> bool:
        """Actualiza la cantidad actual y opcionalmente el estado del lote."""
        if nuevo_estado:
            sql = "UPDATE lotes SET cant_actual = %s, estado = %s WHERE id_lote = %s"
            valores = (nueva_cant_actual, nuevo_estado, id_lote)
        else:
            sql = "UPDATE lotes SET cant_actual = %s WHERE id_lote = %s"
            valores = (nueva_cant_actual, id_lote)

        resultado = ejecutar_escritura(sql, valores)
        return resultado["filas_afectadas"] > 0

