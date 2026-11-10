import os
import sys
import subprocess
from src.views.ui_helpers import _separador, _pausar, _pedir_entero


def menu_tests():
    """Submenú para ejecutar la suite de pruebas automatizadas."""
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    tests = {
        1: ("Test de Conectividad con MySQL", os.path.join(raiz, "tests", "test_conexion.py")),
        2: ("Test Integral de Controladores y Reglas de Negocio", os.path.join(raiz, "tests", "test_controllers.py")),
        3: ("Test del Módulo de Reportes y Gráficos", os.path.join(raiz, "tests", "test_reports.py")),
    }

    while True:
        _separador("EJECUCIÓN DE PRUEBAS AUTOMATIZADAS")
        for k, (nombre, _) in tests.items():
            print(f"  [{k}] {nombre}")
        print("  [4] Ejecutar TODAS las pruebas en secuencia")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        if opcion in tests:
            nombre, ruta_test = tests[opcion]
            print(f"\n  🚀 Ejecutando {nombre} ({os.path.basename(ruta_test)})...\n")
            subprocess.run([sys.executable, ruta_test])
            _pausar()
        elif opcion == 4:
            for k in sorted(tests.keys()):
                nombre, ruta_test = tests[k]
                print(f"\n  🚀 Ejecutando {nombre} ({os.path.basename(ruta_test)})...\n")
                subprocess.run([sys.executable, ruta_test])
            _pausar()
        elif opcion == 0:
            break

