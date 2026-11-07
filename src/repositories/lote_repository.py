import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import ejecutar_lectura, ejecutar_escritura
from src.repositories.base_repository import BaseRepository

class LoteRepository(BaseRepository):
    """
    Repositorio para la entidad Lotes.
    Hereda de BaseRepository: obtener_todos(), obtener_por_id(), eliminar(), contar_total().
    """

    def __init__(self):
        super().__init__(nombre_tabla="lotes", clave_primaria="id_lote")

    # ==========================================
    # C: CREATE
    # ==========================================
    def crear(self, num_lote, fecha_vencimiento, cant_inicial, cant_actual, id_medicamento, id_proveedor):
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
    # R: READ CON DETALLES
    # ==========================================
    def obtener_detallados(self):
        """
        Consulta avanzada específica de Lotes:
        Retorna los lotes junto con los nombres del medicamento y proveedor asociados.
        """
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

    # ==========================================
    # U: UPDATE
    # ==========================================
    def actualizar_stock_y_estado(self, id_lote, nueva_cant_actual, nuevo_estado=None):
        """Actualiza la cantidad actual y opcionalmente el estado del lote."""
        if nuevo_estado:
            sql = "UPDATE lotes SET cant_actual = %s, estado = %s WHERE id_lote = %s"
            valores = (nueva_cant_actual, nuevo_estado, id_lote)
        else:
            sql = "UPDATE lotes SET cant_actual = %s WHERE id_lote = %s"
            valores = (nueva_cant_actual, id_lote)

        resultado = ejecutar_escritura(sql, valores)
        if resultado["filas_afectadas"] > 0:
            print(f"Lote ID {id_lote} actualizado: Stock={nueva_cant_actual}" + (f", Estado={nuevo_estado}" if nuevo_estado else ""))
            return True
        else:
            print(f"No se encontró el lote ID {id_lote}.")
            return False


# ==========================================
# EJEMPLO DE USO DE LA CLASE
# ==========================================
if __name__ == "__main__":
    repo = LoteRepository()

    print("--- 1. CREAR LOTE TEMPORAL ---")
    id_nuevo = repo.crear("LOTE-TEST-01", "2028-12-31", 100, 100, id_medicamento=1, id_proveedor=1)

    print("\n--- 2. LEER LOTES CON JOIN (Detalles de medicamento y proveedor) ---")
    lotes = repo.obtener_detallados()
    for l in lotes:
        print(f"Lote: {l['num_lote']} | Vence: {l['fecha_vencimiento']} | Estado: {l['estado']} | Stock: {l['cant_actual']} | Med: {l['medicamento']} | Prov: {l['proveedor']}")

    print("\n--- 3. ACTUALIZAR STOCK Y ESTADO ---")
    repo.actualizar_stock_y_estado(id_nuevo, nueva_cant_actual=0, nuevo_estado="Agotado")

    print("\n--- 4. ELIMINAR LOTE TEMPORAL (Heredado de BaseRepository) ---")
    repo.eliminar(id_nuevo)
