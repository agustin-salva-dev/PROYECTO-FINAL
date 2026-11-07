"""
Script para inicializar la base de datos de forma automática e idempotente.
Lee y ejecuta 'db/schema.sql' y 'db/seed.sql' en el servidor MySQL local.
Si las tablas ya existían, las reinicia limpiamente sin errores de integridad referencial.

Uso:
    python inicializar_db.py
"""

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def ejecutar_script_sql(cursor, ruta_archivo):
    """Lee un archivo .sql, filtra comentarios y ejecuta cada instrucción."""
    nombre_archivo = os.path.basename(ruta_archivo)
    print(f"-> Ejecutando '{nombre_archivo}'...")

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

    print(f"   [OK] {contador} instrucciones ejecutadas de '{nombre_archivo}'.")


def main():
    print("==================================================")
    print("  INICIALIZADOR DE BASE DE DATOS - PROYECTO FARMACIA")
    print("==================================================")

    host = os.getenv("DB_HOST", "127.0.0.1")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD")
    port = int(os.getenv("DB_PORT", "3306"))
    db_name = os.getenv("DB_NAME", "proyecto_farmacia")

    print(f"Destino: MySQL en {host}:{port} | Base de datos: '{db_name}'\n")

    try:
        # 1. Conexión a nivel de servidor (sin fijar base de datos para poder crearla si no existe)
        conexion = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
        )
        cursor = conexion.cursor()

        # 2. Asegurar que la base de datos exista y posicionarse en ella
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        cursor.execute(f"USE `{db_name}`;")
        conexion.commit()

        # 3. Ejecutar Schema (DDL: eliminación limpia y creación de tablas)
        ruta_schema = os.path.join(os.path.dirname(__file__), "db", "schema.sql")
        ejecutar_script_sql(cursor, ruta_schema)
        conexion.commit()
        print("✅ Tablas creadas y vinculadas con éxito.")

        # 4. Ejecutar Seed (DML: inserción de datos iniciales de prueba)
        ruta_seed = os.path.join(os.path.dirname(__file__), "db", "seed.sql")
        ejecutar_script_sql(cursor, ruta_seed)
        conexion.commit()
        print("Datos iniciales cargados con éxito.")

        cursor.close()
        conexion.close()

        print("\n¡Base de datos lista! Puedes ejecutar el script tantas veces como quieras sin errores.")
        print("==================================================")

    except mysql.connector.Error as err:
        print(f"\nError al inicializar la base de datos: {err}")
        print("Verifica que MySQL esté iniciado (sudo service mysql status en WSL) y tu contraseña en .env.")


if __name__ == "__main__":
    main()
