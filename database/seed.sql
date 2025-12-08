USE madereria_almacen;

-- Agregando más datos realistas de maderería

-- Insertar usuarios
INSERT INTO usuarios (nombre, email, password, rol) VALUES
('José Ramírez', 'admin@madereria.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxnT8F3hC', 'administrador'),
('Carlos Méndez', 'carlos@madereria.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxnT8F3hC', 'empleado'),
('María González', 'maria@madereria.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxnT8F3hC', 'empleado');

-- Insertar categorías de maderería
INSERT INTO categorias (nombre, descripcion) VALUES
('Madera Maciza', 'Tablas y tablones de madera natural'),
('Tableros', 'MDF, aglomerado, triplay y melamina'),
('Herramientas Eléctricas', 'Sierras, taladros, lijadoras y más'),
('Herramientas Manuales', 'Martillos, serruchos, formones y cinceles'),
('Acabados', 'Barnices, lacas, selladores y tintes'),
('Pinturas', 'Pinturas para madera y superficies'),
('Ferretería', 'Tornillos, clavos, bisagras y cerraduras'),
('Adhesivos', 'Pegamentos y colas para madera'),
('Abrasivos', 'Lijas, discos y esponjas'),
('Decoración', 'Molduras, zócalos y cornisas');

-- Insertar proveedores
INSERT INTO proveedores (nombre, contacto, telefono, email, direccion) VALUES
('Maderas del Pacífico S.A.', 'Roberto Vargas', '2234-5678', 'ventas@maderaspacifico.com', 'Zona Industrial La Lima, Cartago'),
('Distribuidora Ferretera Central', 'Ana Solís', '2245-8901', 'info@ferreteracentral.cr', 'Avenida Central, San José'),
('Importadora de Herramientas ProTools', 'Luis Mora', '2256-7890', 'contacto@protools.cr', 'Heredia Centro'),
('Acabados y Pinturas Premium', 'Carmen Rojas', '2267-3456', 'ventas@acabadospremium.com', 'Alajuela, Zona Franca'),
('Tableros Nacionales S.A.', 'Miguel Ángel Castro', '2278-9012', 'pedidos@tablerosna.cr', 'Cartago, Zona Industrial');

-- Insertar productos de madera maciza
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('MAD-001', 'Tabla Pino 1x4x8 pies', 'Tabla de pino nacional, 1x4 pulgadas, 8 pies de largo', 1, 1, 120, 30, 200, 2800, 4200),
('MAD-002', 'Tabla Pino 1x6x10 pies', 'Tabla de pino nacional, 1x6 pulgadas, 10 pies de largo', 1, 1, 85, 25, 150, 4500, 6800),
('MAD-003', 'Tabla Cedro 1x6x8 pies', 'Tabla de cedro amargo, 1x6 pulgadas, 8 pies', 1, 1, 45, 15, 80, 8500, 12500),
('MAD-004', 'Tabla Laurel 1x8x10 pies', 'Tabla de laurel, 1x8 pulgadas, 10 pies de largo', 1, 1, 35, 10, 60, 11000, 16500),
('MAD-005', 'Regla Pino 2x2x8 pies', 'Regla cuadrada de pino, 2x2 pulgadas, 8 pies', 1, 1, 200, 50, 300, 1800, 2700),
('MAD-006', 'Regla Pino 2x4x8 pies', 'Regla de pino para construcción, 2x4 pulgadas, 8 pies', 1, 1, 150, 40, 250, 3200, 4800),
('MAD-007', 'Tabla Melina 1x6x8 pies', 'Tabla de melina, 1x6 pulgadas, 8 pies de largo', 1, 1, 90, 25, 150, 3500, 5200),
('MAD-008', 'Viga Pino 4x4x10 pies', 'Viga de pino, 4x4 pulgadas, 10 pies de largo', 1, 1, 40, 15, 70, 12000, 18000);

-- Insertar tableros
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('TAB-001', 'MDF 3mm 1.22x2.44m', 'Tablero MDF de 3mm, medida estándar', 2, 5, 45, 15, 80, 4500, 6800),
('TAB-002', 'MDF 6mm 1.22x2.44m', 'Tablero MDF de 6mm, medida estándar', 2, 5, 38, 12, 70, 6200, 9300),
('TAB-003', 'MDF 9mm 1.22x2.44m', 'Tablero MDF de 9mm, medida estándar', 2, 5, 32, 10, 60, 7800, 11700),
('TAB-004', 'MDF 15mm 1.22x2.44m', 'Tablero MDF de 15mm, medida estándar', 2, 5, 28, 10, 50, 11500, 17200),
('TAB-005', 'MDF 18mm 1.22x2.44m', 'Tablero MDF de 18mm, medida estándar', 2, 5, 25, 8, 45, 13800, 20700),
('TAB-006', 'Triplay 6mm 1.22x2.44m', 'Tablero de triplay de 6mm', 2, 5, 30, 10, 55, 8500, 12800),
('TAB-007', 'Triplay 9mm 1.22x2.44m', 'Tablero de triplay de 9mm', 2, 5, 25, 8, 45, 11200, 16800),
('TAB-008', 'Triplay 12mm 1.22x2.44m', 'Tablero de triplay de 12mm', 2, 5, 20, 8, 40, 14500, 21800),
('TAB-009', 'Melamina Blanca 18mm', 'Tablero melamínico blanco 18mm, 1.22x2.44m', 2, 5, 18, 6, 35, 18500, 27800),
('TAB-010', 'Melamina Nogal 18mm', 'Tablero melamínico color nogal 18mm, 1.22x2.44m', 2, 5, 15, 5, 30, 19200, 28800);

-- Insertar herramientas eléctricas
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('HER-001', 'Sierra Circular 7-1/4"', 'Sierra circular eléctrica 1400W, disco 7-1/4"', 3, 3, 8, 3, 15, 45000, 68000),
('HER-002', 'Taladro Inalámbrico 18V', 'Taladro percutor inalámbrico 18V con 2 baterías', 3, 3, 12, 4, 20, 38000, 57000),
('HER-003', 'Lijadora Orbital', 'Lijadora orbital eléctrica 300W', 3, 3, 6, 2, 12, 28000, 42000),
('HER-004', 'Caladora Eléctrica', 'Caladora eléctrica 650W con guía láser', 3, 3, 7, 3, 15, 32000, 48000),
('HER-005', 'Esmeril Angular 4-1/2"', 'Esmeril angular 900W, disco 4-1/2"', 3, 3, 10, 4, 18, 25000, 37500),
('HER-006', 'Router Eléctrico', 'Router eléctrico 1200W con accesorios', 3, 3, 5, 2, 10, 52000, 78000);

-- Insertar herramientas manuales
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('HEM-001', 'Martillo Carpintero 16oz', 'Martillo de carpintero con mango de fibra de vidrio', 4, 2, 25, 10, 40, 4500, 6800),
('HEM-002', 'Serrucho Carpintero 20"', 'Serrucho para madera 20 pulgadas', 4, 2, 18, 8, 35, 5200, 7800),
('HEM-003', 'Juego Formones 6 piezas', 'Juego de formones profesionales 6 piezas', 4, 2, 12, 5, 25, 18500, 27800),
('HEM-004', 'Escuadra Carpintero 12"', 'Escuadra de aluminio 12 pulgadas', 4, 2, 20, 8, 35, 3800, 5700),
('HEM-005', 'Nivel Torpedo 9"', 'Nivel torpedo magnético 9 pulgadas', 4, 2, 15, 6, 30, 4200, 6300),
('HEM-006', 'Cinta Métrica 5m', 'Cinta métrica profesional 5 metros', 4, 2, 30, 12, 50, 2800, 4200),
('HEM-007', 'Prensa Carpintero 24"', 'Prensa tipo C para carpintería 24 pulgadas', 4, 2, 10, 4, 20, 8500, 12800);

-- Insertar acabados
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('ACA-001', 'Barniz Marino 1 Litro', 'Barniz marino transparente brillante 1L', 5, 4, 35, 12, 60, 8500, 12800),
('ACA-002', 'Barniz Mate 1 Litro', 'Barniz transparente acabado mate 1L', 5, 4, 28, 10, 50, 7800, 11700),
('ACA-003', 'Sellador Madera 1 Litro', 'Sellador base agua para madera 1L', 5, 4, 42, 15, 70, 5200, 7800),
('ACA-004', 'Laca Nitrocelulosa 1L', 'Laca nitrocelulosa transparente 1L', 5, 4, 25, 10, 45, 9200, 13800),
('ACA-005', 'Tinte Nogal 250ml', 'Tinte para madera color nogal 250ml', 5, 4, 30, 12, 55, 3500, 5200),
('ACA-006', 'Tinte Caoba 250ml', 'Tinte para madera color caoba 250ml', 5, 4, 28, 10, 50, 3500, 5200),
('ACA-007', 'Aceite Teka 500ml', 'Aceite protector para madera teka 500ml', 5, 4, 20, 8, 40, 6800, 10200);

-- Insertar pinturas
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('PIN-001', 'Pintura Látex Blanco 1 Galón', 'Pintura látex blanco mate interior 1 galón', 6, 4, 45, 15, 80, 8500, 12800),
('PIN-002', 'Esmalte Blanco 1 Litro', 'Esmalte sintético blanco brillante 1L', 6, 4, 32, 12, 60, 7200, 10800),
('PIN-003', 'Pintura Anticorrosiva Gris', 'Pintura anticorrosiva gris 1 galón', 6, 4, 18, 8, 35, 11500, 17200);

-- Insertar ferretería
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('FER-001', 'Tornillos Madera 1" x100', 'Caja 100 tornillos para madera 1 pulgada', 7, 2, 85, 25, 150, 1800, 2700),
('FER-002', 'Tornillos Madera 1-1/2" x100', 'Caja 100 tornillos para madera 1-1/2 pulgadas', 7, 2, 75, 20, 130, 2200, 3300),
('FER-003', 'Tornillos Madera 2" x100', 'Caja 100 tornillos para madera 2 pulgadas', 7, 2, 68, 20, 120, 2800, 4200),
('FER-004', 'Clavos 2" Caja 1kg', 'Caja de clavos de 2 pulgadas, 1 kilogramo', 7, 2, 95, 30, 160, 1500, 2200),
('FER-005', 'Clavos 3" Caja 1kg', 'Caja de clavos de 3 pulgadas, 1 kilogramo', 7, 2, 82, 25, 140, 1800, 2700),
('FER-006', 'Bisagra Piano 1.5m', 'Bisagra continua tipo piano 1.5 metros', 7, 2, 35, 12, 60, 3500, 5200),
('FER-007', 'Bisagra Cazoleta 35mm', 'Bisagra de cazoleta 35mm con tornillos', 7, 2, 120, 40, 200, 850, 1300),
('FER-008', 'Cerradura Pomo Dorado', 'Cerradura de pomo acabado dorado', 7, 2, 15, 6, 30, 8500, 12800),
('FER-009', 'Corredera Telescópica 18"', 'Corredera telescópica para cajón 18 pulgadas', 7, 2, 45, 15, 80, 2800, 4200);

-- Insertar adhesivos
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('ADH-001', 'Cola Blanca 1 Litro', 'Cola blanca para madera 1 litro', 8, 4, 55, 20, 90, 3200, 4800),
('ADH-002', 'Cola Amarilla 500ml', 'Cola amarilla profesional 500ml', 8, 4, 38, 15, 65, 4500, 6800),
('ADH-003', 'Pegamento Contacto 1L', 'Pegamento de contacto 1 litro', 8, 4, 28, 10, 50, 5800, 8700),
('ADH-004', 'Silicón Transparente', 'Silicón transparente cartucho 300ml', 8, 4, 65, 25, 110, 1800, 2700);

-- Insertar abrasivos
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('ABR-001', 'Lija Madera Grano 80', 'Pliego de lija para madera grano 80', 9, 2, 150, 50, 250, 350, 520),
('ABR-002', 'Lija Madera Grano 120', 'Pliego de lija para madera grano 120', 9, 2, 140, 45, 230, 350, 520),
('ABR-003', 'Lija Madera Grano 180', 'Pliego de lija para madera grano 180', 9, 2, 130, 40, 220, 350, 520),
('ABR-004', 'Lija Madera Grano 220', 'Pliego de lija para madera grano 220', 9, 2, 120, 40, 200, 350, 520),
('ABR-005', 'Disco Lija 7" Grano 80', 'Disco de lija 7 pulgadas grano 80 para lijadora', 9, 2, 85, 30, 150, 580, 870),
('ABR-006', 'Esponja Abrasiva Media', 'Esponja abrasiva grano medio', 9, 2, 95, 35, 160, 420, 630);

-- Insertar decoración
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta) VALUES
('DEC-001', 'Moldura Colonial 2"x8pies', 'Moldura colonial de pino 2 pulgadas, 8 pies', 10, 1, 45, 15, 80, 2800, 4200),
('DEC-002', 'Zócalo MDF 3"x8pies', 'Zócalo de MDF 3 pulgadas, 8 pies', 10, 5, 55, 20, 90, 3500, 5200),
('DEC-003', 'Cornisa Colonial 3"x8pies', 'Cornisa colonial de pino 3 pulgadas, 8 pies', 10, 1, 35, 12, 60, 4200, 6300);

-- Insertar movimientos de ejemplo (historial realista)
INSERT INTO movimientos (tipo, producto_id, cantidad, costo_unitario, precio_unitario, usuario_id, proveedor_id, fecha, notas) VALUES
-- Entradas iniciales de inventario (hace 60 días)
('entrada', 1, 120, 2800, NULL, 1, 1, DATE_SUB(NOW(), INTERVAL 60 DAY), 'Compra inicial de inventario'),
('entrada', 2, 85, 4500, NULL, 1, 1, DATE_SUB(NOW(), INTERVAL 60 DAY), 'Compra inicial de inventario'),
('entrada', 3, 45, 8500, NULL, 1, 1, DATE_SUB(NOW(), INTERVAL 60 DAY), 'Compra inicial de inventario'),
('entrada', 9, 18, 18500, NULL, 1, 5, DATE_SUB(NOW(), INTERVAL 58 DAY), 'Compra de tableros melamínicos'),
('entrada', 11, 8, 45000, NULL, 1, 3, DATE_SUB(NOW(), INTERVAL 55 DAY), 'Compra de herramientas eléctricas'),

-- Salidas (ventas a clientes)
('salida', 1, 15, NULL, 4200, 2, NULL, DATE_SUB(NOW(), INTERVAL 50 DAY), 'Venta a cliente - Proyecto residencial'),
('salida', 2, 10, NULL, 6800, 2, NULL, DATE_SUB(NOW(), INTERVAL 48 DAY), 'Venta a cliente - Muebles'),
('salida', 5, 25, NULL, 2700, 3, NULL, DATE_SUB(NOW(), INTERVAL 45 DAY), 'Venta a constructor'),

-- Más entradas (reabastecimiento)
('entrada', 21, 35, 8500, NULL, 1, 4, DATE_SUB(NOW(), INTERVAL 40 DAY), 'Reabastecimiento de acabados'),
('entrada', 31, 85, 1800, NULL, 1, 2, DATE_SUB(NOW(), INTERVAL 38 DAY), 'Compra de ferretería'),
('entrada', 41, 55, 3200, NULL, 1, 4, DATE_SUB(NOW(), INTERVAL 35 DAY), 'Compra de adhesivos'),

-- Más salidas
('salida', 9, 3, NULL, 27800, 2, NULL, DATE_SUB(NOW(), INTERVAL 30 DAY), 'Venta - Proyecto cocina integral'),
('salida', 11, 1, NULL, 68000, 2, NULL, DATE_SUB(NOW(), INTERVAL 28 DAY), 'Venta de herramienta'),
('salida', 21, 8, NULL, 12800, 3, NULL, DATE_SUB(NOW(), INTERVAL 25 DAY), 'Venta de barniz'),

-- Entradas recientes
('entrada', 1, 50, 2800, NULL, 1, 1, DATE_SUB(NOW(), INTERVAL 20 DAY), 'Reabastecimiento de tablas de pino'),
('entrada', 45, 150, 350, NULL, 1, 2, DATE_SUB(NOW(), INTERVAL 18 DAY), 'Compra de lijas'),

-- Salidas recientes
('salida', 3, 5, NULL, 12500, 2, NULL, DATE_SUB(NOW(), INTERVAL 15 DAY), 'Venta - Proyecto muebles finos'),
('salida', 31, 20, NULL, 2700, 3, NULL, DATE_SUB(NOW(), INTERVAL 12 DAY), 'Venta de tornillos'),
('salida', 45, 35, NULL, 520, 2, NULL, DATE_SUB(NOW(), INTERVAL 10 DAY), 'Venta de lijas'),

-- Movimientos de esta semana
('entrada', 5, 100, 1800, NULL, 1, 1, DATE_SUB(NOW(), INTERVAL 5 DAY), 'Compra de reglas de pino'),
('salida', 5, 30, NULL, 2700, 2, NULL, DATE_SUB(NOW(), INTERVAL 3 DAY), 'Venta a constructor'),
('salida', 21, 5, NULL, 12800, 3, NULL, DATE_SUB(NOW(), INTERVAL 2 DAY), 'Venta de barniz marino'),
('entrada', 11, 4, 45000, NULL, 1, 3, DATE_SUB(NOW(), INTERVAL 1 DAY), 'Reabastecimiento de sierras circulares'),
('salida', 1, 8, NULL, 4200, 2, NULL, NOW(), 'Venta del día - Cliente regular');
