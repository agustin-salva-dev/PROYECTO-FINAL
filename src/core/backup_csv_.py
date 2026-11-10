import os
import csv
from datetime import datetime

from src.core.db import obtener_conexion


# Tablas de la base de datos
TABLAS = [
    "medicamentos",
    "proveedores",
    "lotes",
    "movimientos_stock"
]


def crear_backup_csv():
    """Exporta la estructura y los datos de la base de datos a CSV."""

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Carpeta donde se guardarán los backups
    raiz = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    carpeta_backup = os.path.join(
        raiz, "backups", f"backup_{fecha}"
    )

    os.makedirs(carpeta_backup, exist_ok=True)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        # --------------------------------
        # 1. EXPORTAR ESTRUCTURA
        # --------------------------------

        ruta_estructura = os.path.join(
            carpeta_backup, "estructura.csv"
        )

        with open(
            ruta_estructura,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:

            escritor = csv.writer(archivo)

            escritor.writerow(["tabla", "sentencia_create"])

            for tabla in TABLAS:
                cursor.execute(f"SHOW CREATE TABLE `{tabla}`")
                resultado = cursor.fetchone()

                sentencia = resultado["Create Table"]

                escritor.writerow([tabla, sentencia])

        # --------------------------------
        # 2. EXPORTAR DATOS DE CADA TABLA
        # --------------------------------

        for tabla in TABLAS:

            cursor.execute(f"SELECT * FROM `{tabla}`")
            registros = cursor.fetchall()

            ruta_csv = os.path.join(
                carpeta_backup, f"{tabla}.csv"
            )

            # Obtener nombres de columnas
            columnas = [columna[0] for columna in cursor.description]

            with open(
                ruta_csv,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:

                escritor = csv.DictWriter(
                    archivo,
                    fieldnames=columnas
                )

                escritor.writeheader()
                escritor.writerows(registros)

        print("Backup creado correctamente.")
        print("Ubicación:", carpeta_backup)

        return carpeta_backup

    except Exception as error:
        print("Error al crear el backup:", error)
        raise

    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    crear_backup_csv()
