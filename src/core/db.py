import os
import mysql.connector
from dotenv import load_dotenv

# Carga las variables del .env
load_dotenv()


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


def ejecutar_lectura(sql, valores=None, como_dict=True):
    """
    Ejecuta consultas de tipo SELECT.
    Abre la conexión, ejecuta la consulta, recupera los datos y cierra todo de forma segura.
    
    :param sql: Sentencia SQL a ejecutar.
    :param valores: Tupla con los parámetros para la sentencia preparada.
    :param como_dict: Si es True, retorna cada fila como diccionario {columna: valor}.
    :return: Lista de registros obtenidos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=como_dict)
    try:
        cursor.execute(sql, valores or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()


def ejecutar_escritura(sql, valores=None):
    """
    Ejecuta consultas de tipo INSERT, UPDATE o DELETE.
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