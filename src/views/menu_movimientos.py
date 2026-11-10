from src.controllers.movimiento_controller import MovimientoController
from src.models.movimiento_model import MovimientoModel
from src.core.exceptions import FarmaciaError
from src.views.ui_helpers import (
    _separador,
    _pausar,
    _pedir_entero,
    _pedir_confirmacion,
    _imprimir_tabla,
)


def menu_movimientos():
    """Submenú de transacciones de stock físico y auditoría."""
    controller = MovimientoController()
    modelo_mov = MovimientoModel()

    while True:
        _separador("MOVIMIENTOS DE STOCK Y AUDITORÍA")
        print("  [1] Ver historial completo de movimientos")
        print("  [2] Registrar venta (descuento atómico de stock)")
        print("  [3] Registrar ingreso de mercadería a lote")
        print("  [4] Dar de baja lote por vencimiento")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        if opcion == 1:
            _separador("HISTORIAL COMPLETO DE MOVIMIENTOS")
            _imprimir_tabla(modelo_mov.obtener_detallados())
            _pausar()

        elif opcion == 2:
            _separador("REGISTRAR VENTA")
            id_lote = _pedir_entero("ID del lote a vender")
            cantidad = _pedir_entero("Cantidad de unidades a vender")
            try:
                resultado = controller.registrar_venta(id_lote, cantidad)
                print(
                    f"\n  ✅ Venta registrada con éxito.\n"
                    f"     Stock restante: {resultado['stock_restante']} | Estado de lote: {resultado['estado']}"
                )
            except FarmaciaError as e:
                print(f"\n  ❌ {e}")
            except Exception as e:
                print(f"\n  ❌ Error inesperado: {e}")
            _pausar()

        elif opcion == 3:
            _separador("REGISTRAR INGRESO DE MERCADERÍA")
            id_lote = _pedir_entero("ID del lote a reponer")
            cantidad = _pedir_entero("Cantidad de unidades a ingresar")
            try:
                resultado = controller.registrar_ingreso(id_lote, cantidad)
                print(
                    f"\n  ✅ Ingreso registrado con éxito.\n"
                    f"     Stock total actualizado: {resultado['stock_total']} | Estado de lote: {resultado['estado']}"
                )
            except FarmaciaError as e:
                print(f"\n  ❌ {e}")
            except Exception as e:
                print(f"\n  ❌ Error inesperado: {e}")
            _pausar()

        elif opcion == 4:
            _separador("BAJA SANITARIA POR VENCIMIENTO")
            id_lote = _pedir_entero("ID del lote a dar de baja")
            if _pedir_confirmacion(f"¿Confirma la baja total por vencimiento del lote ID {id_lote}?"):
                try:
                    resultado = controller.dar_de_baja_por_vencimiento(id_lote)
                    print(
                        f"\n  ✅ Baja asentada correctamente.\n"
                        f"     Unidades descartadas: {resultado['unidades_descartadas']} | Estado: {resultado['estado']}"
                    )
                except FarmaciaError as e:
                    print(f"\n  ❌ {e}")
                except Exception as e:
                    print(f"\n  ❌ Error inesperado: {e}")
            _pausar()

        elif opcion == 0:
            break

