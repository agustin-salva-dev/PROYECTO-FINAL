import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import ejecutar_escritura
from src.models.base_model import BaseModel


class ProveedorModel(BaseModel):
    """
    Modelo para la entidad Proveedores.
    Hereda de BaseModel: obtener_todos(), obtener_por_id(), eliminar(), contar_total().
    """

    def __init__(self):
        super().__init__(nombre_tabla="proveedores", clave_primaria="id_proveedor")

    # ==========================================
    # C: CREATE 
    # ==========================================
    def crear(self, nombre: str, cuit: str, telefono: str, email: str) -> int:
        """Inserta un nuevo proveedor y retorna su ID asignado."""
        sql = """
            INSERT INTO proveedores (nombre, cuit, telefono, email)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nombre, cuit, telefono, email)
        resultado = ejecutar_escritura(sql, valores)
        nuevo_id = resultado["ultimo_id"]

        print(f"Proveedor '{nombre}' agregado con éxito. ID asignado: {nuevo_id}")
        return nuevo_id

    # ==========================================
    # U: UPDATE 
    # ==========================================
    def actualizar_contacto(self, id_prov: int, nuevo_telefono: str, nuevo_email: str = None) -> bool:
        """Actualiza el teléfono y opcionalmente el email de un proveedor."""
        if nuevo_email:
            sql = "UPDATE proveedores SET telefono = %s, email = %s WHERE id_proveedor = %s"
            valores = (nuevo_telefono, nuevo_email, id_prov)
        else:
            sql = "UPDATE proveedores SET telefono = %s WHERE id_proveedor = %s"
            valores = (nuevo_telefono, id_prov)

        resultado = ejecutar_escritura(sql, valores)
        if resultado["filas_afectadas"] > 0:
            print(f"Proveedor ID {id_prov} actualizado correctamente.")
            return True
        else:
            print(f"No se encontró el proveedor ID {id_prov}.")
            return False


# ==========================================
# EJEMPLO DE USO DEL MODELO
# ==========================================
if __name__ == "__main__":
    modelo = ProveedorModel()

    print("--- 1. CREAR PROVEEDOR TEMPORAL ---")
    id_nuevo = modelo.crear("Droguería Test", "30-99999999-9", "011-44445555", "test@drogueria.com")

    print("\n--- 2. LEER TODOS (Método heredado de BaseModel) ---")
    proveedores = modelo.obtener_todos()
    for prov in proveedores:
        print(f"ID: {prov['id_proveedor']} | {prov['nombre']} | CUIT: {prov['cuit']} | Tel: {prov['telefono']} | Email: {prov['email']}")

    print("\n--- 3. ACTUALIZAR CONTACTO ---")
    modelo.actualizar_contacto(id_nuevo, nuevo_telefono="011-88889999")

    print("\n--- 4. ELIMINAR PROVEEDOR TEMPORAL (Método heredado de BaseModel) ---")
    modelo.eliminar(id_nuevo)

