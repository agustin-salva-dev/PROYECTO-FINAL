from src.models.proveedor_model import ProveedorModel
from src.views.ui_helpers import (
    _separador,
    _pausar,
    _pedir_entero,
    _pedir_texto,
    _pedir_confirmacion,
    _imprimir_tabla,
)


def menu_proveedores():
    """Submenú de gestión y CRUD para la entidad Proveedores."""
    modelo = ProveedorModel()
    while True:
        _separador("GESTIÓN DE PROVEEDORES (CRUD)")
        print("  [1] Listar todos los proveedores")
        print("  [2] Buscar proveedor por ID")
        print("  [3] Agregar nuevo proveedor")
        print("  [4] Actualizar datos de contacto de un proveedor")
        print("  [5] Eliminar proveedor")
        print("  [0] Volver al Menú Principal")
        opcion = _pedir_entero("Opción")

        if opcion == 1:
            _separador("LISTADO COMPLETO DE PROVEEDORES")
            _imprimir_tabla(modelo.obtener_todos())
            _pausar()

        elif opcion == 2:
            id_prov = _pedir_entero("ID del proveedor")
            resultado = modelo.obtener_por_id(id_prov)
            _separador(f"DETALLE DEL PROVEEDOR ID {id_prov}")
            _imprimir_tabla([resultado] if resultado else [])
            _pausar()

        elif opcion == 3:
            _separador("REGISTRO DE NUEVO PROVEEDOR")
            nombre = _pedir_texto("Nombre de la droguería / proveedor")
            cuit = _pedir_texto("CUIT (formato: 30-12345678-9)")
            telefono = _pedir_texto("Teléfono de contacto")
            email = input("  Email (opcional, presione ENTER para omitir): ").strip() or None
            try:
                nuevo_id = modelo.crear(nombre, cuit, telefono, email)
                print(f"\n  ✅ Proveedor registrado con éxito con ID asignado: {nuevo_id}")
            except Exception as e:
                print(f"  ❌ Error al registrar proveedor: {e}")
            _pausar()

        elif opcion == 4:
            id_prov = _pedir_entero("ID del proveedor a actualizar")
            nuevo_tel = _pedir_texto("Nuevo teléfono")
            nuevo_email = input("  Nuevo email (presione ENTER para no modificar): ").strip() or None
            if modelo.actualizar_contacto(id_prov, nuevo_tel, nuevo_email):
                print(f"\n  ✅ Datos de contacto actualizados correctamente para el ID {id_prov}.")
            else:
                print(f"\n  ❌ No se encontró el proveedor ID {id_prov}.")
            _pausar()

        elif opcion == 5:
            id_prov = _pedir_entero("ID del proveedor a eliminar")
            if _pedir_confirmacion(f"¿Está seguro de eliminar el proveedor ID {id_prov}?"):
                modelo.eliminar(id_prov)
            _pausar()

        elif opcion == 0:
            break

