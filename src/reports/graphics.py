import os
import sys
from datetime import date
import pandas as pd
import matplotlib

# Configurar backend no interactivo antes de pyplot para evitar ventanas emergentes
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Asegura la raíz del proyecto en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.models.medicamento_model import MedicamentoModel
from src.models.lote_model import LoteModel
from src.models.movimiento_model import MovimientoModel

CARPETA_SALIDA_DEFAULT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "reports_output")
)


# ==========================================
# FUNCIONES AUXILIARES PRIVADAS
# ==========================================

def _asegurar_directorio(directorio: str = None) -> str:
    """Garantiza la existencia del directorio destino y retorna su ruta."""
    carpeta = directorio or CARPETA_SALIDA_DEFAULT
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


def _guardar_figura(fig, nombre_archivo: str, directorio: str = None) -> str:
    """Encapsula el ciclo de vida del guardado físico de la figura y libera memoria."""
    carpeta = _asegurar_directorio(directorio)
    ruta = os.path.join(carpeta, nombre_archivo)
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close(fig)
    return ruta


# ==========================================
# FUNCIONES PÚBLICAS DE REPORTES GRÁFICOS
# ==========================================

def generar_grafico_stock_vs_minimo(directorio_salida: str = None) -> str:
    """
    Genera un gráfico de barras comparativas entre el Stock Disponible
    y el Stock Mínimo por medicamento, resaltando visualmente los déficits.
    """
    medicamentos = MedicamentoModel().obtener_todos()
    lotes = LoteModel().obtener_todos()
    hoy = date.today()

    datos = []
    for med in medicamentos:
        id_med = med["id_medicamento"]
        stock_disp = sum(
            l["cant_actual"]
            for l in lotes
            if l["id_medicamento"] == id_med
            and l["estado"] == "Activo"
            and (l["fecha_vencimiento"] if isinstance(l["fecha_vencimiento"], date) else date.fromisoformat(str(l["fecha_vencimiento"]))) > hoy
        )
        datos.append({
            "medicamento": f"{med['nombre_comercial']}\n({med['presentacion']})",
            "stock_disponible": stock_disp,
            "stock_minimo": med["stock_minimo"],
            "en_deficit": stock_disp <= med["stock_minimo"],
        })

    fig, ax = plt.subplots(figsize=(10, 6))

    if not datos:
        ax.text(0.5, 0.5, "Sin datos de medicamentos", ha="center", va="center")
    else:
        df = pd.DataFrame(datos)
        x = range(len(df))
        ancho = 0.38
        colores_disp = ["#e74c3c" if d else "#3498db" for d in df["en_deficit"]]

        ax.bar([i - ancho / 2 for i in x], df["stock_disponible"], width=ancho, label="Stock Disponible", color=colores_disp)
        ax.bar([i + ancho / 2 for i in x], df["stock_minimo"], width=ancho, label="Stock Mínimo (Umbral)", color="#95a5a6", alpha=0.7, edgecolor="#7f8c8d", linestyle="--")

        ax.set_xticks(list(x))
        ax.set_xticklabels(df["medicamento"], fontsize=9)
        ax.set_ylabel("Cantidad de Unidades (físicas)", fontsize=11)
        ax.set_title("Nivel de Stock Disponible vs. Stock Mínimo por Medicamento", fontsize=13, fontweight="bold")
        ax.grid(axis="y", linestyle=":", alpha=0.6)
        ax.legend(loc="upper right")

    return _guardar_figura(fig, "grafico_stock_vs_minimo.png", directorio_salida)


def generar_grafico_estados_lotes(directorio_salida: str = None) -> str:
    """
    Genera un gráfico circular mostrando la distribución de lotes
    según su estado físico ('Activo', 'Agotado', 'Vencido').
    """
    lotes = LoteModel().obtener_todos()
    fig, ax = plt.subplots(figsize=(7, 6))

    if not lotes:
        ax.text(0.5, 0.5, "Sin registros de lotes", ha="center", va="center")
    else:
        df = pd.DataFrame(lotes)
        conteo = df["estado"].value_counts()
        colores_map = {"Activo": "#2ecc71", "Agotado": "#f39c12", "Vencido": "#e74c3c"}
        colores = [colores_map.get(e, "#bdc3c7") for e in conteo.index]

        def _formato_valor(pct):
            val = int(round(pct * sum(conteo) / 100.0))
            return f"{pct:.1f}%\n({val} lotes)"

        _, _, autotextos = ax.pie(
            conteo,
            labels=conteo.index,
            autopct=_formato_valor,
            startangle=140,
            colors=colores,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
        )
        for t in autotextos:
            t.set_color("white")
            t.set_fontweight("bold")

        ax.set_title("Distribución de Lotes por Estado Físico", fontsize=13, fontweight="bold")

    return _guardar_figura(fig, "grafico_estados_lotes.png", directorio_salida)


def generar_grafico_ventas(directorio_salida: str = None) -> str:
    """
    Genera un gráfico de barras horizontales con el ranking de los
    medicamentos con mayor volumen histórico de ventas.
    """
    movimientos = MovimientoModel().obtener_detallados()
    fig, ax = plt.subplots(figsize=(9, 5))

    ventas = [m for m in movimientos if m.get("tipo") == "Venta"]

    if not ventas:
        ax.text(0.5, 0.5, "No se registran movimientos de venta", ha="center", va="center")
    else:
        df = pd.DataFrame(ventas)
        ventas_med = df.groupby("medicamento")["cantidad"].sum().sort_values(ascending=True)

        barras = ax.barh(ventas_med.index, ventas_med.values, color="#16a085", edgecolor="#0e6655", height=0.55)

        for barra in barras:
            ancho = barra.get_width()
            ax.annotate(
                f"{int(ancho)} u.",
                xy=(ancho, barra.get_y() + barra.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=9,
                fontweight="bold",
            )

        ax.set_xlabel("Unidades Vendidas (Histórico acumulado)", fontsize=11)
        ax.set_title("Ranking de Medicamentos Más Vendidos", fontsize=13, fontweight="bold")
        ax.grid(axis="x", linestyle=":", alpha=0.6)

    return _guardar_figura(fig, "grafico_ventas.png", directorio_salida)
