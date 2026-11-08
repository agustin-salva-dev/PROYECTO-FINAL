import os
import sys
from datetime import datetime

# Asegura la raíz del proyecto en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.controllers.inventario_controller import InventarioController

CARPETA_SALIDA_DEFAULT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "reports_output")
)


def generar_orden_compra(directorio_salida: str = None) -> str:
    """
    Genera un archivo de texto formal (.txt) con la orden de compra y reposición
    para todos los medicamentos cuyo stock actual esté por debajo del stock mínimo.

    Consume la lógica de negocio de InventarioController (patrón MVC).

    :param directorio_salida: Ruta personalizada donde guardar el archivo (opcional).
    :return: Ruta absoluta del archivo .txt generado.
    """
    carpeta_destino = directorio_salida or CARPETA_SALIDA_DEFAULT
    os.makedirs(carpeta_destino, exist_ok=True)

    controller = InventarioController()
    alertas = controller.obtener_alertas_stock_critico()

    fecha_hoy = datetime.now()
    fecha_formateada = fecha_hoy.strftime("%d/%m/%Y %H:%M")
    nombre_archivo = f"orden_compra_{fecha_hoy.strftime('%Y%m%d')}.txt"
    ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)

    lineas = [
        "=" * 82,
        "                     FARMASTOCK - ORDEN DE COMPRA Y REPOSICIÓN",
        "=" * 82,
        f"Fecha de emisión: {fecha_formateada}",
        f"Criterio        : Medicamentos con stock disponible <= stock mínimo de seguridad",
        "-" * 82,
        f"{'MEDICAMENTO':<22} {'PRESENTACIÓN':<15} {'DOSIS':<10} {'ACTUAL':>8} {'MÍNIMO':>8} {'A REPONER':>11}",
        "-" * 82,
    ]

    total_unidades = 0

    if not alertas:
        lineas.append("  Actualmente no existen medicamentos en estado de stock crítico.")
        lineas.append("  Todos los productos cuentan con niveles de stock dentro de los márgenes.")
    else:
        for item in alertas:
            nombre = str(item.get("nombre_comercial", ""))[:21]
            pres = str(item.get("presentacion", ""))[:14]
            dosis = f"{item.get('dosis_valor', '')}{item.get('dosis_unidad', '')}"[:9]
            actual = int(item.get("stock_total_disponible", 0))
            minimo = int(item.get("stock_minimo", 0))
            reponer = int(item.get("unidades_a_reponer", 0))

            total_unidades += reponer

            lineas.append(
                f"{nombre:<22} {pres:<15} {dosis:<10} {actual:>8} {minimo:>8} {reponer:>11}"
            )

    lineas.append("-" * 82)
    lineas.append(f"TOTAL DE PRODUCTOS A REPONER: {len(alertas):>5}")
    lineas.append(f"TOTAL DE UNIDADES A SOLICITAR: {total_unidades:>5}")
    lineas.append("=" * 82)
    lineas.append("Documento generado automáticamente por el Sistema FarmaStock.")
    lineas.append("Firma Responsable de Farmacia: _______________________________")
    lineas.append("")

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    return ruta_archivo
