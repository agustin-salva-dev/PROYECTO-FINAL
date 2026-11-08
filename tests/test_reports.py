import os
import sys
import pandas as pd

# Asegura la raíz del proyecto en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.reports.text_reports import generar_orden_compra
from src.reports.csv_reports import exportar_movimientos_csv, COLUMNAS_ESPERADAS
from src.reports.graphics import (
    generar_grafico_stock_vs_minimo,
    generar_grafico_estados_lotes,
    generar_grafico_ventas,
)


def ejecutar_pruebas_reportes():
    print("==================================================")
    print("  SUITE DE PRUEBAS AUTOMATIZADAS: MÓDULO REPORTS  ")
    print("==================================================")

    # 1. Test Orden de Compra (TXT)
    print("\n[TEST 1] Generación de Orden de Compra en formato TXT...")
    ruta_txt = generar_orden_compra()
    assert os.path.exists(ruta_txt), f"El archivo TXT no fue creado en: {ruta_txt}"
    tamano_txt = os.path.getsize(ruta_txt)
    assert tamano_txt > 0, "El archivo TXT generado está vacío"

    with open(ruta_txt, "r", encoding="utf-8") as f:
        contenido = f.read()
    assert "FARMASTOCK" in contenido, "El encabezado no contiene el nombre institucional"
    assert "ORDEN DE COMPRA" in contenido, "El archivo no indica que es una orden de compra"
    print(f"  -> Archivo TXT verificado ({tamano_txt} bytes): {os.path.basename(ruta_txt)}")
    print("  [OK] Test 1 superado.")

    # 2. Test Auditoría de Movimientos (CSV con Pandas)
    print("\n[TEST 2] Exportación de Auditoría de Movimientos en CSV...")
    ruta_csv = exportar_movimientos_csv()
    assert os.path.exists(ruta_csv), f"El archivo CSV no fue creado en: {ruta_csv}"
    tamano_csv = os.path.getsize(ruta_csv)
    assert tamano_csv > 0, "El archivo CSV generado está vacío"

    df = pd.read_csv(ruta_csv, encoding="utf-8-sig")
    for col in COLUMNAS_ESPERADAS:
        assert col in df.columns, f"Falta la columna esperada '{col}' en el CSV exportado"
    print(f"  -> Archivo CSV verificado ({len(df)} filas, {len(df.columns)} columnas): {os.path.basename(ruta_csv)}")
    print("  [OK] Test 2 superado.")

    # 3. Test Gráfico Stock vs Mínimo (PNG)
    print("\n[TEST 3] Gráfico analítico: Stock Disponible vs Mínimo...")
    ruta_g1 = generar_grafico_stock_vs_minimo()
    assert os.path.exists(ruta_g1), f"El gráfico PNG no fue creado en: {ruta_g1}"
    assert os.path.getsize(ruta_g1) > 1000, "El archivo PNG generado es demasiado pequeño o inválido"
    print(f"  -> Gráfico 1 generado ({os.path.getsize(ruta_g1)} bytes): {os.path.basename(ruta_g1)}")
    print("  [OK] Test 3 superado.")

    # 4. Test Gráfico Estados de Lotes (PNG)
    print("\n[TEST 4] Gráfico analítico: Distribución de Estados de Lotes...")
    ruta_g2 = generar_grafico_estados_lotes()
    assert os.path.exists(ruta_g2), f"El gráfico circular no fue creado en: {ruta_g2}"
    assert os.path.getsize(ruta_g2) > 1000, "El gráfico circular generado es inválido"
    print(f"  -> Gráfico 2 generado ({os.path.getsize(ruta_g2)} bytes): {os.path.basename(ruta_g2)}")
    print("  [OK] Test 4 superado.")

    # 5. Test Gráfico Ranking de Ventas (PNG)
    print("\n[TEST 5] Gráfico analítico: Ranking de Medicamentos Más Vendidos...")
    ruta_g3 = generar_grafico_ventas()
    assert os.path.exists(ruta_g3), f"El gráfico de ventas no fue creado en: {ruta_g3}"
    assert os.path.getsize(ruta_g3) > 1000, "El gráfico de ventas generado es inválido"
    print(f"  -> Gráfico 3 generado ({os.path.getsize(ruta_g3)} bytes): {os.path.basename(ruta_g3)}")
    print("  [OK] Test 5 superado.")

    print("\n==================================================")
    print("  TODAS LAS PRUEBAS DE REPORTES PASARON EXITOSAMENTE ")
    print("==================================================")


if __name__ == "__main__":
    ejecutar_pruebas_reportes()
