import os
import mysql.connector
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

print("Intentando conectar a MySQL...")
print(f"  Host:     {os.getenv('DB_HOST')}")
print(f"  Puerto:   {os.getenv('DB_PORT')}")
print(f"  Base:     {os.getenv('DB_NAME')}")
print(f"  Usuario:  {os.getenv('DB_USER')}")
print()

try:
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cursor = conexion.cursor()
    cursor.execute("SHOW TABLES;")
    tablas = cursor.fetchall()

    print("Conexion exitosa!")
    print(f"Tablas encontradas en '{os.getenv('DB_NAME')}':")
    for tabla in tablas:
        print(f"     - {tabla[0]}")

    cursor.close()
    conexion.close()

except mysql.connector.Error as e:
    print(f"Error de conexion: {e}")
    print()
    print("Verificá que:")
    print("  1. MySQL está corriendo  →  sudo service mysql start")
    print("  2. Las credenciales en .env son correctas")
    print("  3. El nombre de la base de datos existe")

