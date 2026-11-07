import os
import mysql.connector
from dotenv import load_dotenv

# Carga las variables del .env asegurando la ruta raíz
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)


def obtener_conexion():
    """
    Crea y devuelve una nueva conexión a MySQL usando las variables de entorno.
    Centralizada para que cualquier módulo del sistema la reutilice.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "proyecto_farmacia"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
    )


def ejecutar_lectura(sql, valores=None):
    """
    Ejecuta consultas de tipo SELECT.
    Siempre retorna cada fila como diccionario {columna: valor}.
    Abre la conexión, ejecuta la consulta, recupera los datos y cierra todo de forma segura.
    
    :param sql: Sentencia SQL a ejecutar.
    :param valores: Tupla con los parámetros para la sentencia preparada.
    :return: Lista de diccionarios con los registros obtenidos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(sql, valores or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()


def ejecutar_escritura(sql, valores=None):
    """
    Ejecuta consultas de tipo INSERT, UPDATE o DELETE individuales.
    Abre la conexión, ejecuta la consulta, hace commit y cierra todo de forma segura.
    
    :param sql: Sentencia SQL a ejecutar.
    :param valores: Tupla con los parámetros para la sentencia preparada.
    :return: Diccionario con 'ultimo_id' (para INSERT) y 'filas_afectadas' (para UPDATE/DELETE).
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(sql, valores or ())
        conexion.commit()
        return {
            "ultimo_id": cursor.lastrowid,
            "filas_afectadas": cursor.rowcount,
        }
    finally:
        cursor.close()
        conexion.close()


def ejecutar_transaccion(operaciones):
    """
    Ejecuta múltiples sentencias SQL en una ÚNICA transacción.
    Si alguna sentencia falla, realiza rollback automático garantizando la consistencia de datos.
    
    :param operaciones: Lista de tuplas (sentencia_sql, valores_tupla)
    :return: True si todas las sentencias se confirmaron con éxito.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        conexion.start_transaction()
        for sql, valores in operaciones:
            cursor.execute(sql, valores or ())
        conexion.commit()
        return True
    except Exception as err:
        conexion.rollback()
        raise err
    finally:
        cursor.close()
        conexion.close()
