import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import ejecutar_lectura, ejecutar_escritura
import mysql.connector


class BaseModel:
    """
    Clase base para todos los modelos del sistema .
    Contiene la lógica común de las operaciones CRUD para evitar repetir código.
    """

    def __init__(self, nombre_tabla: str, clave_primaria: str):
        self.tabla = nombre_tabla
        self.pk = clave_primaria

    def obtener_todos(self) -> list:
        """Retorna todos los registros de la tabla."""
        sql = f"SELECT * FROM {self.tabla}"
        return ejecutar_lectura(sql)

    def obtener_por_id(self, id_registro: int) -> dict | None:
        """Retorna un único registro según su clave primaria."""
        sql = f"SELECT * FROM {self.tabla} WHERE {self.pk} = %s"
        resultados = ejecutar_lectura(sql, (id_registro,))
        return resultados[0] if resultados else None

    def eliminar(self, id_registro: int) -> bool:
        """
        Elimina un registro según su clave primaria.
        Controla errores de clave foránea (integridad referencial).
        """
        sql = f"DELETE FROM {self.tabla} WHERE {self.pk} = %s"
        try:
            res = ejecutar_escritura(sql, (id_registro,))
            if res["filas_afectadas"] > 0:
                print(f"Registro con {self.pk}={id_registro} eliminado de '{self.tabla}'.")
                return True
            else:
                print(f"No se encontró registro con {self.pk}={id_registro} en '{self.tabla}'.")
                return False

        except mysql.connector.Error as err:
            if err.errno == 1451:
                print(
                    f"No se puede eliminar el registro con {self.pk}={id_registro} de '{self.tabla}': "
                    f"Tiene registros asociados en otras tablas (integridad referencial)."
                )
            else:
                print(f"Error al eliminar en '{self.tabla}': {err}")
            return False

    def contar_total(self) -> int:
        """Retorna la cantidad total de registros en la tabla."""
        sql = f"SELECT COUNT(*) AS total FROM {self.tabla}"
        res = ejecutar_lectura(sql)
        return res[0]["total"] if res else 0

