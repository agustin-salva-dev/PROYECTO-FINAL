import os

# ==========================================
# HELPERS DE INTERFAZ (privados)
# ==========================================

def _limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def _separador(titulo: str = "") -> None:
    print("\n" + "=" * 56)
    if titulo:
        print(f"  {titulo}")
        print("=" * 56)


def _pausar() -> None:
    input("\nPresioná ENTER para continuar...")


def _pedir_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(f"  {mensaje}: ").strip())
        except ValueError:
            print("  ⚠ Ingresá un número entero válido.")


def _pedir_texto(mensaje: str) -> str:
    while True:
        valor = input(f"  {mensaje}: ").strip()
        if valor:
            return valor
        print("  ⚠ El campo no puede estar vacío.")


def _pedir_confirmacion(mensaje: str) -> bool:
    respuesta = input(f"  {mensaje} (S/N): ").strip().upper()
    return respuesta == "S"


def _imprimir_tabla(datos: list) -> None:
    """Imprime una lista de diccionarios como tabla ASCII alineada."""
    if not datos:
        print("  (Sin registros para mostrar)")
        return

    columnas = list(datos[0].keys())
    anchos = {col: max(len(str(col)), max(len(str(fila.get(col, ""))) for fila in datos)) for col in columnas}

    def _linea(izq, sep, der, relleno):
        return izq + relleno.join(relleno * (anchos[c] + 2) for c in columnas) + der

    print(_linea("╔", "╦", "╗", "═"))
    encabezado = "║" + "║".join(f" {col:<{anchos[col]}} " for col in columnas) + "║"
    print(encabezado)
    print(_linea("╠", "╬", "╣", "═"))
    for fila in datos:
        print("║" + "║".join(f" {str(fila.get(col, '')):<{anchos[col]}} " for col in columnas) + "║")
    print(_linea("╚", "╩", "╝", "═"))
    print(f"  Total: {len(datos)} registro(s).")