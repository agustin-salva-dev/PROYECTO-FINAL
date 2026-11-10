import sys
import os

# Asegura que la raíz del proyecto esté en el path de importaciones
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.views.menu_medicamentos import menu_medicamentos
from src.views.menu_proveedores import menu_proveedores
from src.views.menu_lotes import menu_lotes
from src.views.menu_movimientos import menu_movimientos
from src.views.menu_inventario import menu_inventario
from src.views.menu_reportes import menu_reportes
from src.views.menu_backup import menu_backup
from src.views.menu_tests import menu_tests
from src.views.ui_helpers import _limpiar, _separador, _pedir_entero, _pausar


def menu_principal():
    """Menú principal interactivo de la aplicación FarmaStock (CLI)."""
    acciones = {
        1: menu_medicamentos,
        2: menu_proveedores,
        3: menu_lotes,
        4: menu_movimientos,
        5: menu_inventario,
        6: menu_reportes,
        7: menu_backup,
        8: menu_tests,
    }

    while True:
        _limpiar()
        _separador("FARMASTOCK - SISTEMA DE CONTROL DE STOCK FARMACÉUTICO")
        print("  [1] Medicamentos (CRUD)")
        print("  [2] Proveedores (CRUD)")
        print("  [3] Lotes de Stock (CRUD)")
        print("  [4] Movimientos de Stock y Transacciones")
        print("  [5] Inventario y Alertas Sanitarias")
        print("  [6] Reportes y Analítica (TXT, CSV, PNG)")
        print("  [7] Backup y Restauración de Base de Datos")
        print("  [8] Ejecutar Tests Automatizados")
        print("  [0] Salir del Sistema")
        print("=" * 56)
        opcion = _pedir_entero("Seleccione una opción")

        if opcion == 0:
            print("\n  ¡Gracias por utilizar FarmaStock! Sistema finalizado con éxito.\n")
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            print("  ⚠️ Opción no válida. Por favor, seleccione un número del menú.")
            _pausar()


if __name__ == "__main__":
    menu_principal()

