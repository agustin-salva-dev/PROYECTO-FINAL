import os
import sys
from datetime import datetime
import pandas as pd

# Asegura la raíz del proyecto en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.models.movimiento_model import MovimientoModel

CARPETA_SALIDA_DEFAULT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "reports_output")
)

COLUMNAS_ESPERADAS = [
    "id_movimiento",
    "tipo",
    "cantidad",
    "fecha_hora",
    "num_lote",
    "medicamento",
    "presentacion",
]


def exportar_movimientos_csv(directorio_salida: str = None) -> str:
    """
    Exporta el historial completo y detallado de auditoría de movimientos
    de stock (Ingresos, Ventas, Bajas por vencimiento) a un archivo CSV estructurado.

    Utiliza Pandas para la manipulación y exportación de datos tabulares.

    :param directorio_salida: Ruta personalizada donde guardar el archivo (opcional).
    :return: Ruta absoluta del archivo .csv generado.
    """
    carpeta_destino = directorio_salida or CARPETA_SALIDA_DEFAULT
    os.makedirs(carpeta_destino, exist_ok=True)

    modelo_mov = MovimientoModel()
    movimientos = modelo_mov.obtener_detallados()

    if movimientos:
        df = pd.DataFrame(movimientos)
        # Asegurar orden consistente de columnas si existen
        columnas_presentes = [c for c in COLUMNAS_ESPERADAS if c in df.columns]
        df = df[columnas_presentes]
    else:
        df = pd.DataFrame(columns=COLUMNAS_ESPERADAS)

    fecha_hoy = datetime.now()
    nombre_archivo = f"movimientos_{fecha_hoy.strftime('%Y%m%d')}.csv"
    ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)

    # utf-8-sig garantiza visualización correcta de tildes y caracteres especiales en Excel
    df.to_csv(ruta_archivo, index=False, encoding="utf-8-sig")

    return ruta_archivo
