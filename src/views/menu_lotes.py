from src.models.lote_model import LoteModel
from src.models.medicamento_model import MedicamentoModel
from src.models.proveedor_model import ProveedorModel
from src.views.ui_helpers import (
    _separador,
    _pausar,
    _pedir_entero,
    _pedir_texto,
    _pedir_confirmacion,
    _imprimir_tabla,
)


def menu_lotes():
    """Submenú de gestión y CRUD para la entidad Lotes."""
    modelo_lote = LoteModel()
    modelo_med = MedicamentoModel()
    modelo_prov = ProveedorModel()

    while True:
        _separador("GESTIÓN DE LOTES (CRUD)")
        print("  [1] Listar todos los lotes (con medicamento y proveedor)")
        print("  [2] Buscar lote por ID")
        print("  [3] Agregar nuevo lote físico")
        print("  [4] Eliminar lote")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        if opcion == 1:
            _separador("LISTADO DETALLADO DE LOTES")
            _imprimir_tabla(modelo_lote.obtener_detallados())
            _pausar()

        elif opcion == 2:
            id_lote = _pedir_entero("ID del lote")
            resultado = modelo_lote.obtener_por_id(id_lote)
            _separador(f"DETALLE DEL LOTE ID {id_lote}")
            _imprimir_tabla([resultado] if resultado else [])
            _pausar()

        elif opcion == 3:
            _separador("REGISTRO DE NUEVO LOTE FÍSICO")
            print("  --- Medicamentos registrados ---")
            _imprimir_tabla(modelo_med.obtener_todos())
            id_med = _pedir_entero("ID del medicamento")

            print("\n  --- Proveedores registrados ---")
            _imprimir_tabla(modelo_prov.obtener_todos())
            id_prov = _pedir_entero("ID del proveedor")

            num_lote = _pedir_texto("Número / código de lote (ej: L-2024-001)")
            fecha_venc = _pedir_texto("Fecha de vencimiento (formato: YYYY-MM-DD)")
            cantidad = _pedir_entero("Cantidad inicial de unidades")

            try:
                nuevo_id = modelo_lote.crear(
                    num_lote=num_lote,
                    fecha_vencimiento=fecha_venc,
                    cant_inicial=cantidad,
                    cant_actual=cantidad,
                    id_medicamento=id_med,
                    id_proveedor=id_prov,
                )
                print(f"\n  ✅ Lote registrado con éxito con ID asignado: {nuevo_id}")
            except Exception as e:
                print(f"  ❌ Error al registrar lote: {e}")
            _pausar()

        elif opcion == 4:
            id_lote = _pedir_entero("ID del lote a eliminar")
            if _pedir_confirmacion(f"¿Está seguro de eliminar el lote ID {id_lote}?"):
                modelo_lote.eliminar(id_lote)
            _pausar()

        elif opcion == 0:
            break

