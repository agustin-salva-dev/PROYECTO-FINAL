from src.backups.exportar_backup import exportar_backup_csv
from src.backups.restaurar_backup import restaurar_backup_csv
from db.inicializar_db import inicializar_base_de_datos
from src.views.ui_helpers import (
    _separador,
    _pausar,
    _pedir_entero,
    _pedir_texto,
    _pedir_confirmacion,
)


def menu_backup():
    """Submenú de seguridad, respaldo, restauración e inicialización de la base de datos."""
    while True:
        _separador("BACKUP, RESTAURACIÓN E INICIALIZACIÓN DE BASE DE DATOS")
        print("  [1] Crear backup completo (Exportar tablas a CSV)")
        print("  [2] Restaurar base de datos desde una carpeta de backup")
        print("  [3] Inicializar Base de Datos (Estructura DDL y Datos de Prueba Iniciales)")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        if opcion == 1:
            try:
                carpeta = exportar_backup_csv()
                print(f"\n  ✅ Backup generado exitosamente en:\n     {carpeta}")
            except Exception as e:
                print(f"\n  ❌ Error al generar backup: {e}")
            _pausar()

        elif opcion == 2:
            carpeta = _pedir_texto("Ruta completa de la carpeta de backup a restaurar")
            if _pedir_confirmacion("⚠️ ADVERTENCIA: Esta acción sobreescribirá los datos actuales de la base. ¿Continuar?"):
                try:
                    restaurar_backup_csv(carpeta)
                    print("\n  ✅ Base de datos restaurada correctamente a partir del backup.")
                except Exception as e:
                    print(f"\n  ❌ Error durante la restauración: {e}")
            else:
                print("\n  Operación de restauración cancelada por el usuario.")
            _pausar()

        elif opcion == 3:
            _separador("INICIALIZACIÓN AUTOMÁTICA DE LA BASE DE DATOS")
            print("  Esta operación:")
            print("   1. Creará la base de datos 'proyecto_farmacia' si no existe.")
            print("   2. Construirá todas las tablas con sus claves foráneas (schema.sql).")
            print("   3. Cargará el set completo de datos iniciales de prueba (seed.sql).")
            print("  (Si ya existían tablas previas, se reiniciarán limpiamente).")
            print("-" * 56)
            if _pedir_confirmacion("¿Desea inicializar/restablecer la base de datos ahora?"):
                try:
                    inicializar_base_de_datos()
                    print("\n  ✅ ¡Base de datos inicializada y cargada con éxito!")
                except Exception as e:
                    print(f"\n  ❌ Error al inicializar la base de datos: {e}")
                    print("     Verifique que el servicio MySQL esté activo y su contraseña en '.env'.")
            else:
                print("\n  Operación cancelada.")
            _pausar()

        elif opcion == 0:
            break
