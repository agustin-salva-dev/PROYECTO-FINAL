import os
import csv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.db import obtener_conexion

TABLAS = ["medicamentos", "proveedores", "lotes", "movimientos_stock"]


def _a_none_si_vacio(valor: str):
    """Convierte strings vacíos a None para respetar campos NULL en la base de datos."""
    return None if valor == "" else valor


def _verificar_archivos(carpeta_backup: str) -> None:
    """Valida que la carpeta contenga todos los archivos CSV necesarios."""
    if not os.path.isdir(carpeta_backup):
        raise FileNotFoundError(f"No se encontró la carpeta: {carpeta_backup}")

    for nombre in ["estructura.csv"] + [f"{t}.csv" for t in TABLAS]:
        ruta = os.path.join(carpeta_backup, nombre)
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"Archivo faltante en el backup: {nombre}")


def _leer_estructuras(carpeta_backup: str) -> dict:
    """Lee las sentencias CREATE TABLE desde estructura.csv."""
    estructuras = {}
    ruta = os.path.join(carpeta_backup, "estructura.csv")
    with open(ruta, "r", newline="", encoding="utf-8-sig") as archivo:
        for fila in csv.DictReader(archivo):
            if fila["tabla"] in TABLAS:
                estructuras[fila["tabla"]] = fila["sentencia_create"]

    if set(estructuras.keys()) != set(TABLAS):
        raise ValueError("El archivo estructura.csv está incompleto.")
    return estructuras


def restaurar_backup_csv(carpeta_backup: str) -> bool:
    """
    Restaura las 4 tablas sobre la base de datos activa (definida en .env)
    a partir de una carpeta de backup CSV.
    Retorna True si la restauración fue exitosa.
    """
    _verificar_archivos(carpeta_backup)
    estructuras = _leer_estructuras(carpeta_backup)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Eliminar y recrear tablas en orden inverso para respetar FKs
        for tabla in reversed(TABLAS):
            cursor.execute(f"DROP TABLE IF EXISTS `{tabla}`")
        for tabla in TABLAS:
            cursor.execute(estructuras[tabla])

        # Insertar datos respetando el orden de FKs
        for tabla in TABLAS:
            ruta_csv = os.path.join(carpeta_backup, f"{tabla}.csv")
            with open(ruta_csv, "r", newline="", encoding="utf-8-sig") as archivo:
                lector = csv.DictReader(archivo)
                columnas = lector.fieldnames
                if not columnas:
                    raise ValueError(f"El archivo {tabla}.csv no tiene encabezados.")

                nombres = ", ".join(f"`{c}`" for c in columnas)
                marcadores = ", ".join(["%s"] * len(columnas))
                sql = f"INSERT INTO `{tabla}` ({nombres}) VALUES ({marcadores})"

                for fila in lector:
                    valores = tuple(_a_none_si_vacio(fila[c]) for c in columnas)
                    cursor.execute(sql, valores)

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conexion.commit()
        return True

    except Exception:
        conexion.rollback()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        raise
    finally:
        cursor.close()
        conexion.close()