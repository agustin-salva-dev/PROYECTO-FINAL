CREATE DATABASE IF NOT EXISTS proyecto_farmacia;
USE proyecto_farmacia;

-- Eliminar tablas previas en orden inverso a sus claves foráneas para permitir reinicialización limpia
DROP TABLE IF EXISTS movimientos_stock;
DROP TABLE IF EXISTS lotes;
DROP TABLE IF EXISTS medicamentos;
DROP TABLE IF EXISTS proveedores;

-- ==========================================
-- 1. TABLA: MEDICAMENTOS
-- ==========================================
CREATE TABLE medicamentos (
    id_medicamento INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_comercial VARCHAR(20) NOT NULL,
    presentacion VARCHAR(20) NOT NULL,
    dosis_valor INT UNSIGNED NOT NULL,
    dosis_unidad ENUM ('ml', 'g', 'mg') NOT NULL,
    stock_minimo INT UNSIGNED NOT NULL
);

-- ==========================================
-- 2. TABLA: PROVEEDORES
-- ==========================================
CREATE TABLE proveedores (
    id_proveedor INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    cuit CHAR(13) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(50)
);

-- ==========================================
-- 3. TABLA: LOTES (Entidad intermedia inventario)
-- ==========================================
CREATE TABLE lotes (
    id_lote INT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,
    num_lote VARCHAR(15) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estado ENUM ('Activo', 'Agotado', 'Vencido') NOT NULL DEFAULT 'Activo',
    cant_inicial INT UNSIGNED NOT NULL,
    cant_actual INT UNSIGNED NOT NULL,
    id_medicamento INT UNSIGNED NOT NULL,
    id_proveedor INT UNSIGNED NOT NULL,
    CONSTRAINT fk_lote_medicamento FOREIGN KEY (id_medicamento)
        REFERENCES medicamentos (id_medicamento),
    CONSTRAINT fk_lote_proveedor FOREIGN KEY (id_proveedor)
        REFERENCES proveedores (id_proveedor)
);

-- ==========================================
-- 4. TABLA: MOVIMIENTOS DE STOCK (Historial/Auditoría)
-- ==========================================
CREATE TABLE movimientos_stock (
    id_movimiento INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM ('Ingreso', 'Venta', 'Baja_vencimiento') NOT NULL,
    cantidad INT UNSIGNED NOT NULL,
    fecha_hora DATETIME NOT NULL,
    id_lote INT UNSIGNED NOT NULL,
    CONSTRAINT fk_movimiento_lote FOREIGN KEY (id_lote)
        REFERENCES lotes (id_lote)
);
