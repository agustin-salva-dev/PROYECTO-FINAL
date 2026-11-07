# 💊 FarmaStock - Sistema de Control de Stock Farmacéutico

Proyecto final para la materia **Programación 2**.  
Es una aplicación de escritorio diseñada para la administración integral de inventario, trazabilidad de lotes y auditoría de movimientos de stock en el ámbito farmacéutico.

---

## 🎯 ¿Qué hace el sistema?

El sistema resuelve la problemática de control de inventario y pérdidas por vencimiento en farmacias mediante:

1. **Gestión de Catálogo (CRUD):** Administración de medicamentos y proveedores de droguería.
2. **Trazabilidad de Lotes Físicos:** Control de stock real por lote con seguimiento de fechas de vencimiento y estados (`Activo`, `Agotado`, `Vencido`).
3. **Registro de Movimientos:** Auditoría histórica de transacciones (`Ingreso`, `Venta`, `Baja por Vencimiento`).
4. **Alertas de Reposición:** Detección automática de medicamentos cuyo stock consolidado es menor al stock mínimo admitido.
5. **Análisis y Reportes:** Generación de métricas visuales con **Pandas** y **Matplotlib**, exportación de órdenes de compra a **TXT** y auditorías a **CSV**.
6. **Seguridad y Respaldo:** Módulo de Backup y Restauración completa de la base de datos a partir de archivos CSV.

---

## 🏗️ Arquitectura del Sistema (MVC)

El proyecto implementa la arquitectura **MVC (Modelo - Vista - Controlador)** combinada con principios de **Clean Code** y Programación Orientada a Objetos:

```text
PROYECTO FINAL/
├── db/                         # Scripts SQL y automatizador de inicialización
│   ├── inicializar_db.py       # Despliegue automático e idempotente
│   ├── schema.sql              # Estructura DDL (Tablas, Claves, Checks)
│   └── seed.sql                # Datos iniciales realistas de prueba
├── src/
│   ├── core/                   # Infraestructura transversal
│   │   ├── db.py               # Pool de conexiones, lectura, escritura y transacciones
│   │   ├── exceptions.py       # Excepciones de dominio personalizadas
│   │   └── validators.py       # Reglas de validación de negocio puras
│   ├── models/                 # MODELO (M): Persistencia y entidades de datos
│   │   ├── base_model.py       # Clase padre abstracta con CRUD genérico y manejo de FK
│   │   ├── medicamento_model.py# Consultas y operaciones sobre medicamentos
│   │   ├── proveedor_model.py  # Consultas y operaciones sobre proveedores
│   │   ├── lote_model.py       # Gestión relacional de lotes y stock físico
│   │   └── movimiento_model.py # Auditoría histórica y transacciones atómicas
│   ├── controllers/            # CONTROLADOR (C): Orquestación y lógica de aplicación
│   │   ├── inventario_controller.py # Alertas, reposición y filtros de lotes
│   │   └── movimiento_controller.py # Ventas, ingresos y bajas transaccionales
│   └── views/                  # VISTA (V): Interfaz gráfica de usuario (Tkinter)
├── tests/                      # Suite de pruebas automatizadas
│   ├── test_conexion.py        # Comprobación de enlace con MySQL
│   └── test_controllers.py     # Pruebas integrales de reglas de negocio y transacciones
├── .env.example                # Plantilla de variables de entorno
└── README.md                   # Documentación principal del proyecto
```

### Componentes de la Arquitectura:

- **Modelo (`src/models`):**
  - **POO Avanzada:** Herencia a partir de `BaseModel`, centralizando operaciones CRUD (`obtener_todos`, `obtener_por_id`, `eliminar`, `contar_total`) y captura controlada de errores de integridad referencial (MySQL Error 1451).
  - Modelos especializados (`MedicamentoModel`, `ProveedorModel`, `LoteModel`, `MovimientoModel`) que encapsulan sentencias SQL parametrizadas para prevenir inyecciones SQL.
- **Controlador (`src/controllers`):**
  - Conecta la Vista con los Modelos correspondientes.
  - Ejecuta validaciones previas mediante `src/core/validators` antes de persistir cambios.
  - Asegura transacciones atómicas (por ejemplo, actualizando simultáneamente el stock del lote y registrando la fila de auditoría en `movimientos_stock`).
- **Vista (`src/views`):**
  - Formularios y pantallas interactivas desarrolladas en **Tkinter**, desacopladas de la persistencia directa.
- **Capa Core (`src/core`):**
  - Conexión segura a MySQL con variables de entorno (`.env`) y gestión robusta de conexiones para prevenir fugas de recursos.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Motor de Base de Datos:** MySQL 8.0+
- **Conector:** `mysql-connector-python`
- **Análisis de Datos:** `pandas`, `matplotlib`
- **Interfaz de Usuario:** `tkinter`
- **Entorno y Seguridad:** `python-dotenv`

---

## 🚀 Puesta en Marcha Rápida

PROXIMO
