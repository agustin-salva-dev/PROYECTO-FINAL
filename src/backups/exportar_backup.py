import os
import csv
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import obtener_conexion

TABLAS = ["medicamentos", "proveedores", "lotes", "movimientos_stock"]

CARPETA_BACKUPS_DEFAULT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "backups_output")
)


def _exportar_estructura(cursor, carpeta_backup: str) -> None:
    """Guarda las sentencias CREATE TABLE de cada tabla en estructura.csv."""
    ruta = os.path.join(carpeta_backup, "estructura.csv")
    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["tabla", "sentencia_create"])
        for tabla in TABLAS:
            cursor.execute(f"SHOW CREATE TABLE `{tabla}`")
            resultado = cursor.fetchone()
            escritor.writerow([tabla, resultado["Create Table"]])


def _exportar_tabla(cursor, tabla: str, carpeta_backup: str) -> None:
    """Exporta todos los registros de una tabla a un archivo CSV."""
    cursor.execute(f"SELECT * FROM `{tabla}`")
    registros = cursor.fetchall()
    columnas = [col[0] for col in cursor.description]

    ruta = os.path.join(carpeta_backup, f"{tabla}.csv")
    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(registros)


def exportar_backup_csv() -> str:
    """
    Exporta la estructura y datos de las 4 tablas a una carpeta CSV con marca temporal.
    Retorna la ruta absoluta de la carpeta generada.
    """
    marca_temporal = datetime.now().strftime("%Y%m%d_%H%M%S")
    carpeta_backup = os.path.join(CARPETA_BACKUPS_DEFAULT, f"backup_{marca_temporal}")
    os.makedirs(carpeta_backup, exist_ok=True)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        _exportar_estructura(cursor, carpeta_backup)
        for tabla in TABLAS:
            _exportar_tabla(cursor, tabla, carpeta_backup)
        return carpeta_backup
    except Exception as error:
        raise RuntimeError(f"Error al crear el backup: {error}") from error
    finally:
        cursor.close()
        conexion.close()