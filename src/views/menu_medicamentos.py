from src.models.medicamento_model import MedicamentoModel
from src.views.ui_helpers import (
    _separador,
    _pausar,
    _pedir_entero,
    _pedir_texto,
    _pedir_confirmacion,
    _imprimir_tabla,
)


def menu_medicamentos():
    """Submenú de gestión y CRUD para la entidad Medicamentos."""
    modelo = MedicamentoModel()
    while True:
        _separador("GESTIÓN DE MEDICAMENTOS (CRUD)")
        print("  [1] Listar todos los medicamentos")
        print("  [2] Buscar medicamento por ID")
        print("  [3] Agregar nuevo medicamento")
        print("  [4] Actualizar stock mínimo de un medicamento")
        print("  [5] Eliminar medicamento")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        if opcion == 1:
            _separador("LISTADO COMPLETO DE MEDICAMENTOS")
            _imprimir_tabla(modelo.obtener_todos())
            _pausar()

        elif opcion == 2:
            id_med = _pedir_entero("ID del medicamento")
            resultado = modelo.obtener_por_id(id_med)
            _separador(f"DETALLE DEL MEDICAMENTO ID {id_med}")
            _imprimir_tabla([resultado] if resultado else [])
            _pausar()

        elif opcion == 3:
            _separador("REGISTRO DE NUEVO MEDICAMENTO")
            nombre = _pedir_texto("Nombre comercial")
            presentacion = _pedir_texto("Presentación (ej: Comprimido, Jarabe)")
            dosis_valor = _pedir_entero("Dosis valor (ej: 500)")
            print("  Unidades de dosis admitidas: mg / g / ml")
            dosis_unidad = _pedir_texto("Dosis unidad")
            stock_min = _pedir_entero("Stock mínimo de seguridad")
            try:
                nuevo_id = modelo.crear(nombre, presentacion, dosis_valor, dosis_unidad, stock_min)
                print(f"\n  ✅ Medicamento creado con éxito con ID asignado: {nuevo_id}")
            except Exception as e:
                print(f"  ❌ Error al registrar medicamento: {e}")
            _pausar()

        elif opcion == 4:
            id_med = _pedir_entero("ID del medicamento a actualizar")
            nuevo_min = _pedir_entero("Nuevo stock mínimo")
            if modelo.actualizar_stock_minimo(id_med, nuevo_min):
                print(f"\n  ✅ Stock mínimo actualizado correctamente para el ID {id_med}.")
            else:
                print(f"\n  ❌ No se pudo actualizar el medicamento ID {id_med}.")
            _pausar()

        elif opcion == 5:
            id_med = _pedir_entero("ID del medicamento a eliminar")
            if _pedir_confirmacion(f"¿Está seguro de eliminar el medicamento ID {id_med}?"):
                modelo.eliminar(id_med)
            _pausar()

        elif opcion == 0:
            break

