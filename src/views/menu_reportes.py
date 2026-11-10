import os
from src.reports.text_reports import generar_orden_compra
from src.reports.csv_reports import exportar_movimientos_csv
from src.reports.graphics import (
    generar_grafico_stock_vs_minimo,
    generar_grafico_estados_lotes,
    generar_grafico_ventas,
)
from src.views.ui_helpers import _separador, _pausar, _pedir_entero


def menu_reportes():
    """Submenú de generación de reportes documentales y gráficos estadísticos."""
    while True:
        _separador("REPORTES Y ANALÍTICA")
        print("  [1] Generar Orden de Compra y Reposición (TXT)")
        print("  [2] Exportar Auditoría Histórica de Movimientos (CSV con Pandas)")
        print("  [3] Gráfico Estadístico: Stock Disponible vs. Mínimo (PNG)")
        print("  [4] Gráfico Estadístico: Distribución de Lotes por Estado (PNG)")
        print("  [5] Gráfico Estadístico: Ranking de Medicamentos Más Vendidos (PNG)")
        print("  [6] Generar TODOS los reportes y gráficos juntos")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        try:
            if opcion == 1:
                ruta = generar_orden_compra()
                print(f"\n  ✅ Orden de compra generada exitosamente en:\n     {ruta}")
            elif opcion == 2:
                ruta = exportar_movimientos_csv()
                print(f"\n  ✅ Auditoría en CSV generada exitosamente en:\n     {ruta}")
            elif opcion == 3:
                ruta = generar_grafico_stock_vs_minimo()
                print(f"\n  ✅ Gráfico de stock vs mínimo generado en:\n     {ruta}")
            elif opcion == 4:
                ruta = generar_grafico_estados_lotes()
                print(f"\n  ✅ Gráfico circular de lotes generado en:\n     {ruta}")
            elif opcion == 5:
                ruta = generar_grafico_ventas()
                print(f"\n  ✅ Gráfico de ranking de ventas generado en:\n     {ruta}")
            elif opcion == 6:
                print("\n  Generando suite completa de reportes...")
                funciones = [
                    ("Orden de compra TXT", generar_orden_compra),
                    ("Auditoría CSV", exportar_movimientos_csv),
                    ("Gráfico Stock vs Mínimo PNG", generar_grafico_stock_vs_minimo),
                    ("Gráfico Estados de Lotes PNG", generar_grafico_estados_lotes),
                    ("Gráfico Ranking de Ventas PNG", generar_grafico_ventas),
                ]
                for nombre, fn in funciones:
                    ruta = fn()
                    print(f"  ✅ {nombre}: {os.path.basename(ruta)}")
                print("  Todos los reportes fueron guardados en la carpeta 'reports_output/'.")
            elif opcion == 0:
                break
        except Exception as e:
            print(f"\n  ❌ Error al generar el reporte solicitado: {e}")

        if opcion != 0:
            _pausar()

