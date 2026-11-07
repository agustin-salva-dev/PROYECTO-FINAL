"""
Pruebas automatizadas de los Controladores (Arquitectura MVC).
Valida las reglas de negocio, el control de excepciones y las transacciones.

Uso:
    python tests/test_controllers.py
"""

import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.controllers.inventario_controller import InventarioController
from src.controllers.movimiento_controller import MovimientoController
from src.models.lote_model import LoteModel
from src.core.db import ejecutar_escritura
from src.core.exceptions import (
    ValidacionError,
    StockInsuficienteError,
    LoteVencidoError,
    LoteAgotadoError,
    EntidadNoEncontradaError,
)


def ejecutar_pruebas():
    print("==================================================")
    print("  SUITE DE PRUEBAS DE CONTROLADORES (MVC)")
    print("==================================================")

    inventario_ctrl = InventarioController()
    movimiento_ctrl = MovimientoController()
    lote_model = LoteModel()

    errores = 0

    # ----------------------------------------------------
    # 1. PRUEBAS DE INVENTARIO CONTROLLER
    # ----------------------------------------------------
    print("\n--- 1. Probando InventarioController ---")

    try:
        alertas = inventario_ctrl.obtener_alertas_stock_critico()
        assert isinstance(alertas, list)
        if alertas:
            assert "unidades_a_reponer" in alertas[0]
            assert alertas[0]["unidades_a_reponer"] >= 0
        print(f"  [OK] obtener_alertas_stock_critico() -> {len(alertas)} medicamento(s) en alerta.")
    except Exception as e:
        print(f"  [FALLO] obtener_alertas_stock_critico(): {e}")
        errores += 1

    try:
        proximos = inventario_ctrl.obtener_lotes_proximos_a_vencer(dias=365)
        assert isinstance(proximos, list)
        print(f"  [OK] obtener_lotes_proximos_a_vencer() -> {len(proximos)} lote(s) en ventana.")
    except Exception as e:
        print(f"  [FALLO] obtener_lotes_proximos_a_vencer(): {e}")
        errores += 1

    try:
        disponibles = inventario_ctrl.obtener_lotes_disponibles_para_venta()
        assert isinstance(disponibles, list)
        print(f"  [OK] obtener_lotes_disponibles_para_venta() -> {len(disponibles)} lote(s) aptos.")
    except Exception as e:
        print(f"  [FALLO] obtener_lotes_disponibles_para_venta(): {e}")
        errores += 1

    # ----------------------------------------------------
    # 2. PRUEBAS DE VALIDACIONES EN MOVIMIENTO CONTROLLER
    # ----------------------------------------------------
    print("\n--- 2. Probando Validaciones de Negocio ---")

    # 2.1 Cantidad negativa o cero
    try:
        movimiento_ctrl.registrar_venta(id_lote=1, cantidad=-5)
        print("  [FALLO] No rechazó cantidad negativa.")
        errores += 1
    except ValidacionError:
        print("  [OK] ValidacionError capturado ante cantidad <= 0.")

    # 2.2 Lote inexistente
    try:
        movimiento_ctrl.registrar_venta(id_lote=999999, cantidad=1)
        print("  [FALLO] No detectó lote inexistente.")
        errores += 1
    except EntidadNoEncontradaError:
        print("  [OK] EntidadNoEncontradaError capturado ante ID inexistente.")

    # ----------------------------------------------------
    # 3. PRUEBAS TRANSACCIONALES CON LOTE TEMPORAL
    # ----------------------------------------------------
    print("\n--- 3. Probando Transacciones (Venta, Ingreso, Baja) ---")

    # Creamos un lote de prueba para no alterar los datos reales
    id_temp = lote_model.crear(
        num_lote="TEST-CTRL-01",
        fecha_vencimiento="2029-12-31",
        cant_inicial=50,
        cant_actual=50,
        id_medicamento=1,
        id_proveedor=1,
    )

    try:
        # 3.1 Venta válida (descuenta stock)
        res_v = movimiento_ctrl.registrar_venta(id_lote=id_temp, cantidad=20)
        assert res_v["stock_restante"] == 30
        assert res_v["estado"] == "Activo"
        print("  [OK] Venta: Descontó 20 unidades correctamente (quedan 30).")

        # 3.2 Venta excesiva (debe lanzar StockInsuficienteError y no alterar stock)
        try:
            movimiento_ctrl.registrar_venta(id_lote=id_temp, cantidad=100)
            print("  [FALLO] No detectó stock insuficiente.")
            errores += 1
        except StockInsuficienteError:
            print("  [OK] StockInsuficienteError capturado ante intento de venta excesiva.")

        # 3.3 Ingreso adicional (incrementa stock)
        res_i = movimiento_ctrl.registrar_ingreso(id_lote=id_temp, cantidad=10)
        assert res_i["stock_total"] == 40
        print("  [OK] Ingreso : Incrementó 10 unidades correctamente (total: 40).")

        # 3.4 Baja por vencimiento/descarte (vacía stock y cambia a 'Vencido')
        res_b = movimiento_ctrl.dar_de_baja_por_vencimiento(id_lote=id_temp)
        assert res_b["unidades_descartadas"] == 40
        assert res_b["estado"] == "Vencido"
        print("  [OK] Baja por descarte: Stock a 0 y estado cambiado a 'Vencido'.")

        # 3.5 Intentar vender de un lote vencido
        try:
            movimiento_ctrl.registrar_venta(id_lote=id_temp, cantidad=1)
            print("  [FALLO] Permitió vender de un lote vencido.")
            errores += 1
        except (LoteVencidoError, LoteAgotadoError):
            print("  [OK] Venta bloqueada por lote en estado Vencido/Agotado.")

    finally:
        # Limpieza del lote temporal y sus movimientos para dejar la BD limpia
        ejecutar_escritura("DELETE FROM movimientos_stock WHERE id_lote = %s", (id_temp,))
        ejecutar_escritura("DELETE FROM lotes WHERE id_lote = %s", (id_temp,))
        print("  [OK] Limpieza de lote temporal completada.")

    print("\n==================================================")
    if errores == 0:
        print("¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE! (0 errores)")
    else:
        print(f"Se detectaron {errores} error(es) en las pruebas.")
    print("==================================================")


if __name__ == "__main__":
    ejecutar_pruebas()
