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

## 🏗️ Arquitectura y Buenas Prácticas

El proyecto sigue una **Arquitectura en Capas (Layered Architecture)** y principios de **Clean Code**:

- **POO Avanzada:** Implementación de herencia y polimorfismo con una clase padre `BaseRepository` que centraliza operaciones CRUD y captura excepciones de integridad referencial (MySQL Error 1451).
- **Capa Core (`src/core`):** Conexión segura a MySQL con variables de entorno (`.env`) y gestión eficiente de recursos para prevenir fugas de conexión.
- **Capa de Persistencia (`src/repositories`):** Repositorios específicos (`Medicamento`, `Proveedor`, `Lote`, `Movimiento`) desacoplados de la lógica de interfaz.
- **Base de Datos Idempotente:** Script de automatización que permite desplegar la base de datos limpia con un solo comando.

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
