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
│   ├── reports/                # REPORTES Y ANALÍTICA: Exportadores y visualización
│   │   ├── text_reports.py     # Generador de Orden de Compra formal en TXT
│   │   ├── csv_reports.py      # Exportación de auditoría histórica con Pandas
│   │   └── graphics.py         # Gráficos estadísticos con Matplotlib (PNG)
│   ├── backups/                # BACKUPS: Respaldo y restauración relacional
│   │   ├── exportar_backup.py  # Exportación completa a CSV con marcas temporales
│   │   └── restaurar_backup.py # Restauración íntegra respetando integridad referencial
│   └── views/                  # VISTA (V): Interfaz interactiva de consola (CLI)
│       ├── ui_helpers.py       # Utilidades visuales (tablas ASCII, inputs, separadores)
│       ├── menu_medicamentos.py# Submenú CRUD Medicamentos
│       ├── menu_proveedores.py # Submenú CRUD Proveedores
│       ├── menu_lotes.py       # Submenú CRUD Lotes
│       ├── menu_movimientos.py # Submenú Transacciones de Stock y Auditoría
│       ├── menu_inventario.py  # Submenú Alertas Sanitarias y Stock Crítico
│       ├── menu_reportes.py    # Submenú Generación de Reportes y Gráficos
│       ├── menu_backup.py      # Submenú Backup y Restauración
│       └── menu_tests.py       # Submenú Suite de Pruebas
├── tests/                      # Suite de pruebas automatizadas
│   ├── test_conexion.py        # Comprobación de enlace con MySQL
│   ├── test_controllers.py     # Pruebas integrales de reglas de negocio y transacciones
│   └── test_reports.py         # Validación de exportación TXT, CSV y gráficos PNG
├── main.py                     # Punto de entrada unificado del sistema
├── requirements.txt            # Dependencias del proyecto (pip)
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
- **Módulo de Reportes y Analítica (`src/reports`):**
  - Funciones independientes y desacopladas (stateless) para generar reportes sin depender de la UI.
  - Generación de Órdenes de Compra en texto plano (`text_reports.py`).
  - Auditoría histórica exportable a CSV mediante `pandas` (`csv_reports.py`).
  - Gráficos analíticos renderizados en PNG con `matplotlib` (`graphics.py`), configurados con backend no interactivo (`Agg`) para integración fluida con la UI.
- **Módulo de Backups (`src/backups`):**
  - Exportación de estructura DDL y datos relacionales a CSV con marcas de tiempo (`exportar_backup.py`).
  - Restauración atómica con control temporal de claves foráneas (`restaurar_backup.py`) para evitar conflictos de integridad referencial.
- **Vista (`src/views`):**
  - Interfaz de consola interactiva (CLI) desacoplada en submenús modulares independientes por entidad y responsabilidad (`menu_*.py`).
  - Utilidades visuales reutilizables (`ui_helpers.py`) para renderizado dinámico de tablas ASCII con autoajuste de columnas y sanitización de entradas por teclado.
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

## ⚙️ Cómo Levantar el Sistema (Paso a Paso)

Sigue estos pasos para desplegar y ejecutar el proyecto localmente desde cero:

### 1. Requisitos Previos

Asegúrate de contar con el siguiente software instalado y en ejecución en tu sistema:

- **Python 3.10 o superior:** [python.org/downloads](https://www.python.org/downloads/)
- **MySQL Server 8.0 o superior:** Debe estar activo en el puerto `3306` (puerto por defecto de MySQL, o el puerto que definas en tu archivo `.env`).
  - _Si usas Linux / WSL (Ubuntu):_ Verifica el estado con `sudo service mysql status` o inícialo con `sudo service mysql start`.
  - _Si usas Windows nativo:_ Verifica que el servicio de MySQL esté iniciado en el Administrador de Servicios.

---

### 2. Clonar el Repositorio

Abre una terminal y clona este repositorio en tu máquina local:

```bash
git clone https://github.com/agustin-salva-dev/PROYECTO-FINAL.git
cd "PROYECTO FINAL"
```

---

### 3. Crear y Activar un Entorno Virtual (RECOMENDADO)

Se recomienda aislar las dependencias del proyecto utilizando el módulo estándar `venv`:

- **En Windows (PowerShell):**

  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```

  _(Nota: Si PowerShell arroja un error de directiva de ejecución `ExecutionPolicy`, puedes ejecutar antes `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` o bien usar el Símbolo del sistema CMD ejecutando `venv\Scripts\activate.bat`)._

- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### 4. Instalar Dependencias

Instala los paquetes requeridos especificados en `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 5. Configurar Variables de Entorno (`.env`)

Crea tu archivo de configuración local a partir de la plantilla `.env.example`:

- **En Windows:**
  ```powershell
  copy .env.example .env
  ```
- **En Linux / macOS:**
  ```bash
  cp .env.example .env
  ```

Abre el archivo `.env` recién creado con tu editor y coloca tus credenciales reales de MySQL:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=proyecto_farmacia
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
```

---

### 6. Inicializar la Base de Datos Automáticamente

El proyecto cuenta con un script de automatización **idempotente** que crea la base de datos `proyecto_farmacia`, construye todas las tablas con sus claves foráneas (`db/schema.sql`) y carga un set de datos de prueba realistas (`db/seed.sql`):

```bash
python db/inicializar_db.py
```

> **Nota:** Puedes re-ejecutar este script tantas veces como desees para restablecer la base de datos a su estado original limpio sin errores de claves foráneas.

---

### 7. Comprobar el Funcionamiento (Suite de Pruebas)

Antes de iniciar la interfaz, puedes verificar que la conexión y las reglas de negocio estén operativas ejecutando los tests automatizados:

1. **Test de Conectividad con MySQL:**
   ```bash
   python tests/test_conexion.py
   ```
2. **Test Integral de Controladores y Reglas de Negocio:**
   ```bash
   python tests/test_controllers.py
   ```
   *(Valida transacciones de venta, compras, alertas sanitarias y manejo de excepciones).*
3. **Test de Generación de Reportes y Gráficos:**
   ```bash
   python tests/test_reports.py
   ```
   *(Valida la generación física de la orden de compra TXT, auditoría CSV y los 3 gráficos analíticos PNG).*

---

### 8. Ejecutar la Aplicación

Una vez completados los pasos anteriores, inicia el sistema ejecutando:

```bash
python main.py
```
