"""
Script para inicializar la base de datos de forma automática e idempotente.
Lee y ejecuta 'db/schema.sql' y 'db/seed.sql' en el servidor MySQL local.
Si las tablas ya existían, las reinicia limpiamente sin errores de integridad referencial.
"""

import os
import mysql.connector
from dotenv import load_dotenv

# Carga las variables del archivo .env ubicado en la raíz del proyecto
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path, override=True)


def ejecutar_script_sql(cursor, ruta_archivo):
    """Lee un archivo .sql, filtra comentarios y ejecuta cada instrucción."""
    nombre_archivo = os.path.basename(ruta_archivo)
    print(f"  -> Ejecutando '{nombre_archivo}'...")

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        lineas = []
        for linea in f:
            linea_limpia = linea.strip()
            # Ignora comentarios de línea
            if linea_limpia.startswith("--"):
                continue
            lineas.append(linea)
        contenido = "".join(lineas)

    # Divide las instrucciones por punto y coma (;)
    instrucciones = contenido.split(";")
    contador = 0
    for instruccion in instrucciones:
        comando = instruccion.strip()
        if comando:
            cursor.execute(comando)
            contador += 1

    print(f"     [OK] {contador} instrucciones ejecutadas de '{nombre_archivo}'.")


def inicializar_base_de_datos() -> bool:
    """
    Crea la base de datos 'proyecto_farmacia', ejecuta el schema (DDL)
    y carga los datos iniciales de prueba (seed) de forma idempotente.
    Retorna True si la operación fue exitosa.
    """
    # Asegura lectura actualizada del .env
    load_dotenv(dotenv_path, override=True)

    host = os.getenv("DB_HOST", "127.0.0.1")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD")
    port = int(os.getenv("DB_PORT", "3306"))
    db_name = os.getenv("DB_NAME", "proyecto_farmacia")

    print(f"  Conectando a MySQL en {host}:{port}...")

    # 1. Conexión a nivel de servidor (sin fijar base de datos para poder crearla)
    conexion = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    cursor = conexion.cursor()

    try:
        # 2. Asegurar que la base de datos exista y posicionarse en ella
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        cursor.execute(f"USE `{db_name}`;")
        conexion.commit()

        # 3. Ejecutar Schema (DDL: eliminación limpia y creación de tablas)
        dir_db = os.path.dirname(__file__)
        ruta_schema = os.path.join(dir_db, "schema.sql")
        ejecutar_script_sql(cursor, ruta_schema)
        conexion.commit()
        print("  ✅ Estructura de tablas y claves foráneas creada exitosamente.")

        # 4. Ejecutar Seed (DML: inserción de datos iniciales de prueba)
        ruta_seed = os.path.join(dir_db, "seed.sql")
        ejecutar_script_sql(cursor, ruta_seed)
        conexion.commit()
        print("  ✅ Datos de prueba iniciales cargados exitosamente.")

        return True

    finally:
        cursor.close()
        conexion.close()


def main():
    print("==================================================")
    print("  INICIALIZADOR DE BASE DE DATOS - PROYECTO FARMACIA")
    print("==================================================")
    try:
        inicializar_base_de_datos()
        print("\n¡Base de datos lista! Puedes re-ejecutar tantas veces como desees sin errores.")
        print("==================================================")
    except mysql.connector.Error as err:
        print(f"\n❌ Error al inicializar la base de datos: {err}")
        print("Verifica que MySQL esté iniciado y tus credenciales en el archivo .env.")


if __name__ == "__main__":
    main()
