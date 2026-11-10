from src.controllers.inventario_controller import InventarioController
from src.views.ui_helpers import _separador, _pausar, _pedir_entero, _imprimir_tabla


def menu_inventario():
    """Submenú de consultas analíticas y alertas de stock e inventario."""
    controller = InventarioController()

    while True:
        _separador("INVENTARIO Y ALERTAS")
        print("  [1] Ver alertas de stock crítico (con unidades a reponer)")
        print("  [2] Ver lotes próximos a vencer (ventana preventiva de 180 días)")
        print("  [3] Ver lotes disponibles para venta (activos y vigentes)")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        if opcion == 1:
            _separador("ALERTAS DE STOCK CRÍTICO")
            alertas = controller.obtener_alertas_stock_critico()
            _imprimir_tabla(alertas)
            _pausar()

        elif opcion == 2:
            _separador("LOTES PRÓXIMOS A VENCER (RIESGO SANITARIO)")
            proximos = controller.obtener_lotes_proximos_a_vencer()
            _imprimir_tabla(proximos)
            _pausar()

        elif opcion == 3:
            _separador("LOTES DISPONIBLES PARA VENTA INMEDIATA")
            disponibles = controller.obtener_lotes_disponibles_para_venta()
            _imprimir_tabla(disponibles)
            _pausar()

        elif opcion == 0:
            break

