import os
import csv

from src.core.db import obtener_conexion


TABLAS = [
    "medicamentos",
    "proveedores",
    "lotes",
    "movimientos_stock"
]

BASE_DATOS_DESTINO = "proyecto_farmacia_restaurada"


def restaurar_backup_csv(carpeta_backup):
    """Restaura la estructura y los datos desde archivos CSV."""

    if not os.path.isdir(carpeta_backup):
        raise FileNotFoundError(
            "No se encontró la carpeta del backup."
        )

    ruta_estructura = os.path.join(
        carpeta_backup, "estructura.csv"
    )

    if not os.path.isfile(ruta_estructura):
        raise FileNotFoundError(
            "No se encontró estructura.csv."
        )

    # Verificar que estén todos los archivos CSV
    for tabla in TABLAS:
        ruta = os.path.join(carpeta_backup, tabla + ".csv")

        if not os.path.isfile(ruta):
            raise FileNotFoundError(
                f"No se encontró el archivo {tabla}.csv"
            )

    # Leer las sentencias CREATE TABLE
    estructuras = {}

    with open(
        ruta_estructura,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:
            tabla = fila["tabla"]
            sentencia = fila["sentencia_create"]

            if tabla in TABLAS:
                estructuras[tabla] = sentencia

    if set(estructuras.keys()) != set(TABLAS):
        raise ValueError(
            "El archivo estructura.csv está incompleto."
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Crear y seleccionar la base de datos de destino
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{BASE_DATOS_DESTINO}`"
        )

        cursor.execute(
            f"USE `{BASE_DATOS_DESTINO}`"
        )

        # Desactivar temporalmente las claves foráneas
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Eliminar las tablas anteriores de la base de destino
        for tabla in reversed(TABLAS):
            cursor.execute(
                f"DROP TABLE IF EXISTS `{tabla}`"
            )

        # Crear nuevamente las tablas
        for tabla in TABLAS:
            cursor.execute(estructuras[tabla])

        # Restaurar los datos respetando las relaciones
        for tabla in TABLAS:

            ruta_csv = os.path.join(
                carpeta_backup, tabla + ".csv"
            )

            with open(
                ruta_csv,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:

                lector = csv.DictReader(archivo)
                columnas = lector.fieldnames

                if not columnas:
                    raise ValueError(
                        f"El archivo {tabla}.csv no tiene encabezados."
                    )

                nombres = ", ".join(
                    f"`{columna}`" for columna in columnas
                )

                marcadores = ", ".join(
                    ["%s"] * len(columnas)
                )

                sql = (
                    f"INSERT INTO `{tabla}` ({nombres}) "
                    f"VALUES ({marcadores})"
                )

                for fila in lector:
                    valores = []

                    for columna in columnas:
                        valor = fila[columna]

                        # El email es el único campo nullable
                        # en el esquema actual.
                        if columna == "email" and valor == "":
                            valor = None

                        valores.append(valor)

                    cursor.execute(sql, tuple(valores))

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conexion.commit()

        print("¡Restauración realizada correctamente!")
        print("Base de datos:", BASE_DATOS_DESTINO)

        return True

    except Exception:
        conexion.rollback()

        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        except Exception:
            pass

        raise

    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":

    print("RESTAURACIÓN DE FARMACIA BETTA")

    carpeta = input(
        "Ingrese la ruta de la carpeta del backup: "
    ).strip().strip('"')

    try:
        restaurar_backup_csv(carpeta)

    except Exception as error:
        print("Error durante la restauración:", error)
