USE proyecto_farmacia;

INSERT INTO proveedores (nombre, cuit, telefono, email) VALUES
('Droguería del Sur S.A.', '30-12345678-9', '011-45678910', 'contacto@drogueriasur.com'),
('Farmaco Argentina', '30-87654321-2', '011-55551234', 'ventas@farmacosa.com'),
('Distribuidora Médica', '30-11223344-5', '0351-4223344', 'info@distmedica.com.ar'),
('Laboratorios Globales', '30-99887766-1', '0221-4889900', 'pedidos@labglobal.com');

INSERT INTO medicamentos (nombre_comercial, presentacion, dosis_valor, dosis_unidad, stock_minimo) VALUES
('Ibuprofeno', 'Comprimidos', 400, 'mg', 50),
('Paracetamol', 'Jarabe', 2, 'g', 40),
('Amoxicilina', 'Suspensión', 250, 'ml', 30),
('Clonazepam', 'Gotas', 2, 'mg', 15),
('Salbutamol', 'Spray', 100, 'mg', 20),
('Omeprazol', 'Cápsulas', 20, 'mg', 25);

INSERT INTO lotes (num_lote, fecha_vencimiento, cant_inicial, cant_actual, estado, id_medicamento, id_proveedor) VALUES
('LOT-IBU-01', '2027-12-31', 200, 180, 'Activo', 1, 1),
('LOT-PAR-02', '2027-06-30', 150, 150, 'Activo', 2, 2),
('LOT-AMO-03', '2025-01-15', 100, 0, 'Vencido', 3, 1),
('LOT-CLO-04', '2028-01-20', 50, 50, 'Activo', 4, 3),
('LOT-SAL-05', '2027-04-10', 80, 65, 'Activo', 5, 4),
('LOT-OME-06', '2027-09-01', 120, 110, 'Activo', 6, 2);

INSERT INTO movimientos_stock (tipo, cantidad, fecha_hora, id_lote) VALUES
('Ingreso', 200, '2026-01-10 08:00:00', 1),
('Venta', 20, '2026-02-15 10:30:00', 1),
('Ingreso', 150, '2026-01-12 09:15:00', 2),
('Ingreso', 100, '2025-01-02 08:00:00', 3),
('Baja_vencimiento', 10, '2025-01-16 11:00:00', 3),
('Ingreso', 50, '2026-01-20 16:45:00', 4),
('Ingreso', 80, '2026-01-22 08:30:00', 5),
('Venta', 15, '2026-03-10 12:00:00', 5),
('Ingreso', 120, '2026-01-25 09:00:00', 6),
('Venta', 10, '2026-03-12 15:10:00', 6);