import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import ejecutar_escritura
from src.repositories.base_repository import BaseRepository


class MedicamentoRepository(BaseRepository):
    """
    Repositorio para la entidad Medicamentos.
    Hereda de BaseRepository las operaciones comunes: obtener_todos(), obtener_por_id(), eliminar().
    """

    def __init__(self):
        super().__init__(nombre_tabla="medicamentos", clave_primaria="id_medicamento")

    # ==========================================
    # C: CREATE
    # ==========================================
    def crear(self, nombre, presentacion, dosis_valor, dosis_unidad, stock_minimo):
        """Inserta un nuevo medicamento y retorna el ID autoincremental generado."""
        sql = """
            INSERT INTO medicamentos (nombre_comercial, presentacion, dosis_valor, dosis_unidad, stock_minimo)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, presentacion, dosis_valor, dosis_unidad, stock_minimo)
        resultado = ejecutar_escritura(sql, valores)
        nuevo_id = resultado["ultimo_id"]

        print(f"Medicamento '{nombre}' agregado con éxito. ID asignado: {nuevo_id}")
        return nuevo_id

    # ==========================================
    # U: UPDATE
    # ==========================================
    def actualizar_stock_minimo(self, id_med, nuevo_stock_minimo):
        """Actualiza el stock mínimo de un medicamento."""
        sql = "UPDATE medicamentos SET stock_minimo = %s WHERE id_medicamento = %s"
        valores = (nuevo_stock_minimo, id_med)
        resultado = ejecutar_escritura(sql, valores)

        if resultado["filas_afectadas"] > 0:
            print(f"Medicamento ID {id_med} actualizado con nuevo stock mínimo: {nuevo_stock_minimo}")
            return True
        else:
            print(f"No se encontró el medicamento ID {id_med} para actualizar.")
            return False


# ==========================================
# EJEMPLO DE USO DE LA CLASE
# ==========================================
if __name__ == "__main__":
    repo = MedicamentoRepository()

    print("--- 1. CREAR REGISTRO ---")
    id_nuevo = repo.crear("Medicamento Temporal", "Jarabe", 100, "ml", 5)

    print("\n--- 2. LEER TODOS (Método heredado de BaseRepository) ---")
    medicamentos = repo.obtener_todos()
    for med in medicamentos:
        print(f"ID: {med['id_medicamento']} | {med['nombre_comercial']} ({med['presentacion']}) | Dosis: {med['dosis_valor']}{med['dosis_unidad']} | Stock Mín: {med['stock_minimo']}")

    print("\n--- 3. LEER UNO POR ID (Método heredado de BaseRepository) ---")
    med_encontrado = repo.obtener_por_id(id_nuevo)
    print("Detalle del nuevo:", med_encontrado)

    print("\n--- 4. ACTUALIZAR ---")
    repo.actualizar_stock_minimo(id_med=id_nuevo, nuevo_stock_minimo=25)

    print("\n--- 5. ELIMINAR (Método heredado de BaseRepository) ---")
    repo.eliminar(id_nuevo)

    print("\n--- 6. VERIFICAR TOTAL RESTANTE ---")
    print(f"Total de medicamentos en la base de datos: {repo.contar_total()}")
