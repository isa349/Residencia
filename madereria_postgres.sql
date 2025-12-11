-- Dump convertido a PostgreSQL
BEGIN;

-- Tipos ENUM
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'movimiento_tipo') THEN
        CREATE TYPE movimiento_tipo AS ENUM ('entrada','salida');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_rol') THEN
        CREATE TYPE user_rol AS ENUM ('administrador','empleado');
    END IF;
END $$;

-- Tablas

CREATE TABLE categorias (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion TEXT,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE proveedores (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  contacto VARCHAR(100),
  telefono VARCHAR(20),
  email VARCHAR(100),
  direccion TEXT,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  rol user_rol DEFAULT 'empleado',
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  codigo VARCHAR(50) NOT NULL UNIQUE,
  nombre VARCHAR(200) NOT NULL,
  descripcion TEXT,
  categoria_id INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
  proveedor_id INTEGER REFERENCES proveedores(id) ON DELETE SET NULL,
  stock_actual NUMERIC(10,2) DEFAULT 0.00,
  stock_minimo NUMERIC(10,2) DEFAULT 0.00,
  stock_maximo NUMERIC(10,2),
  costo_unitario NUMERIC(10,2) DEFAULT 0.00,
  precio_venta NUMERIC(10,2) DEFAULT 0.00,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE movimientos (
  id SERIAL PRIMARY KEY,
  tipo movimiento_tipo NOT NULL,
  producto_id INTEGER NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
  cantidad NUMERIC(10,2) NOT NULL,
  costo_unitario NUMERIC(10,2),
  precio_unitario NUMERIC(10,2),
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  proveedor_id INTEGER REFERENCES proveedores(id) ON DELETE SET NULL,
  fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  notas TEXT,
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

-- Índices adicionales (equivalentes a MySQL)
CREATE INDEX idx_nombre_categorias ON categorias(nombre);
CREATE INDEX idx_proveedor_movimientos ON movimientos(proveedor_id);
CREATE INDEX idx_tipo_movimientos ON movimientos(tipo);
CREATE INDEX idx_producto_movimientos ON movimientos(producto_id);
CREATE INDEX idx_usuario_movimientos ON movimientos(usuario_id);
CREATE INDEX idx_fecha_movimientos ON movimientos(fecha);
CREATE INDEX idx_codigo_productos ON productos(codigo);
CREATE INDEX idx_nombre_productos ON productos(nombre);
CREATE INDEX idx_categoria_productos ON productos(categoria_id);
CREATE INDEX idx_proveedor_productos ON productos(proveedor_id);
CREATE INDEX idx_stock_productos ON productos(stock_actual);
CREATE INDEX idx_nombre_proveedores ON proveedores(nombre);
CREATE INDEX idx_email_usuarios ON usuarios(email);
CREATE INDEX idx_rol_usuarios ON usuarios(rol);

-- Inserts (datos)
-- NOTA: los booleanos se pasan como TRUE/FALSE; los tipos enum se asignan por texto.

INSERT INTO categorias (id, nombre, descripcion, activo, created_at, updated_at) VALUES
(1, 'Maderas', 'Maderas naturales y procesadas', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(2, 'Triplay', 'Laminados y contrachapados', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(3, 'MDF', 'Tableros de fibra de densidad media', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(4, 'Herramientas Manuales', 'Herramientas de carpintería básica', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(5, 'Herramientas Eléctricas', 'Sierras, taladros, routers', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(6, 'Adhesivos', 'Pegamentos, resinas y colas', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(7, 'Tornillería', 'Tornillos, clavos y fijaciones', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(8, 'Barnices', 'Barnices, lacas y selladores', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(9, 'Pinturas', 'Pinturas para madera', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(10, 'Accesorios', 'Accesorios varios', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(11, 'Protección', 'Equipo de protección personal', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(12, 'Iluminación', 'Focos y lámparas', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(13, 'Ferretería', 'Artículos generales de ferretería', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(14, 'Selladores', 'Selladores para juntas y madera', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(15, 'Especialidades', 'Productos especiales', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37');

INSERT INTO proveedores (id, nombre, contacto, telefono, email, direccion, activo, created_at, updated_at) VALUES
(1, 'La Forestal', 'Carlos Ruiz', '5512345678', 'ventas@laforestal.com', 'CDMX', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(2, 'Maderas del Norte', 'Luis Pérez', '5541239876', 'contacto@mdn.com', 'Monterrey', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(3, 'Distribuidora Hidalgo', 'Ana Torres', '5599988877', 'ventas@dhidalgo.com', 'Hidalgo', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(4, 'ToolsPro', 'Mario López', '5588876655', 'info@toolspro.com', 'Guadalajara', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(5, 'Carpintería MX', 'Ernesto Silva', '5577765544', 'contacto@cmpmx.com', 'CDMX', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(6, 'Tornimax', 'Jorge Díaz', '5511122233', 'ventas@tornimax.com', 'Querétaro', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(7, 'Pinturas Rivera', 'Claudia Mora', '5522233344', 'ventas@privera.com', 'CDMX', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(8, 'ProTooling', 'Raúl Ramos', '5556677788', 'info@protooling.com', 'Monterrey', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(9, 'Adhesivos Titan', 'Isabel Pérez', '5566554433', 'contacto@titan.com', 'Puebla', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(10, 'Maderas El Roble', 'Tomás Ríos', '5578991122', 'ventas@elroble.com', 'Toluca', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(11, 'MegaStock', 'Rosa Lima', '5512340000', 'info@megastock.com', 'CDMX', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(12, 'Herramex', 'Héctor Sandoval', '5533221100', 'ventas@herramex.com', 'León', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(13, 'IluminaPro', 'María Aguilar', '5599001122', 'contacto@iluminapro.com', 'CDMX', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(14, 'Selladores Plus', 'Pedro Campos', '5588662233', 'ventas@splus.com', 'Puebla', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(15, 'EspecialTec', 'Teresa Duarte', '5544221133', 'info@especialtec.com', 'Tijuana', TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37');

INSERT INTO usuarios (id, nombre, email, password, rol, activo, created_at, updated_at) VALUES
(1, 'Administrador General', 'admin@madereria.com', 'scrypt:32768:8:1$2Zi4oOMbHSg0bVRU$ca84285704f672ae6081805c644135249a6b91e499ed81dda72cbfda8866c9de11306495a43a0050f7d111c6ad14b217e25b47f177fa43b5561db86646d181ad', 'administrador'::user_rol, TRUE, '2025-11-27 15:45:16', '2025-11-27 16:26:12'),
(2, 'Empleado Caja', 'empleado@madereria.com', 'scrypt:32768:8:1$K7qUCO0uSayWbXkP$eab9eefcf97bffc86ed051f6f81c48b0dd6f80c0e39f1525d97a28a308e70af80bc2959d15b56355a2424190a892a27099edcba9a22bab60977a9351099c4186', 'empleado'::user_rol, TRUE, '2025-11-27 15:45:16', '2025-11-28 15:34:05');

INSERT INTO productos (id, codigo, nombre, descripcion, categoria_id, proveedor_id, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta, activo, created_at, updated_at) VALUES
(1, 'MAD001', 'Tablón Pino 1x12', 'Madera de pino de alta calidad', 1, 1, 50.00, 10.00, 200.00, 180.00, 250.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(2, 'MAD002', 'Viga Cedro 4x4', 'Viga para estructura', 1, 2, 20.00, 5.00, 80.00, 350.00, 500.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(3, 'TRI001', 'Triplay 12mm', 'Hoja 1.22 x 2.44 m', 2, 3, 35.00, 10.00, 100.00, 230.00, 330.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(4, 'MDF001', 'MDF 15mm', 'Tablero MDF estándar', 3, 1, 40.00, 8.00, 120.00, 210.00, 300.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(5, 'HER001', 'Martillo 16oz', 'Herramienta básica', 4, 4, 25.00, 5.00, 50.00, 90.00, 140.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(6, 'ELE001', 'Taladro 1/2"', 'Taladro industrial', 5, 4, 15.00, 3.00, 30.00, 800.00, 1100.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(7, 'ADH001', 'Resistol 850', 'Pegamento carpintero', 6, 9, 100.00, 20.00, 300.00, 60.00, 90.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(8, 'TOR001', 'Tornillo 2\" caja 100p', 'Para madera', 7, 6, 80.00, 20.00, 300.00, 40.00, 70.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(9, 'BAR001', 'Barniz brillante 1L', 'Acabado protector', 8, 7, 30.00, 10.00, 80.00, 120.00, 180.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(10, 'PIN001', 'Pintura blanca 1L', 'Acrílica', 9, 7, 50.00, 10.00, 100.00, 85.00, 130.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(11, 'ACC001', 'Bisagra reforzada', 'Bisagra metálica', 10, 6, 60.00, 10.00, 200.00, 25.00, 45.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(12, 'PRO001', 'Guantes protección', 'Guantes industriales', 11, 11, 80.00, 20.00, 150.00, 30.00, 55.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(13, 'ILU001', 'Foco LED 12W', 'Luz blanca fría', 12, 13, 120.00, 30.00, 300.00, 20.00, 35.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(14, 'FER001', 'Cinta métrica 5m', 'Herramienta de medición', 13, 12, 40.00, 10.00, 80.00, 50.00, 80.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37'),
(15, 'SEL001', 'Sellador Acrílico 300ml', 'Para juntas y grietas', 14, 14, 70.00, 15.00, 200.00, 45.00, 70.00, TRUE, '2025-11-27 15:47:37', '2025-11-27 15:47:37');

INSERT INTO movimientos (id, tipo, producto_id, cantidad, costo_unitario, precio_unitario, usuario_id, proveedor_id, fecha, notas, created_at) VALUES
(1, 'entrada'::movimiento_tipo, 1, 20.00, 180.00, NULL, 1, 1, '2025-11-27 09:47:37', 'Reposición de tablones', '2025-11-27 15:47:37'),
(2, 'entrada'::movimiento_tipo, 3, 15.00, 230.00, NULL, 1, 3, '2025-11-27 09:47:37', 'Llegada de triplay', '2025-11-27 15:47:37'),
(3, 'salida'::movimiento_tipo, 1, 5.00, NULL, 250.00, 1, NULL, '2025-11-27 09:47:37', 'Venta mostrador', '2025-11-27 15:47:37'),
(4, 'entrada'::movimiento_tipo, 4, 10.00, 210.00, NULL, 1, 1, '2025-11-27 09:47:37', 'Ingreso MDF', '2025-11-27 15:47:37'),
(5, 'salida'::movimiento_tipo, 4, 3.00, NULL, 300.00, 1, NULL, '2025-11-27 09:47:37', 'Venta', '2025-11-27 15:47:37'),
(6, 'entrada'::movimiento_tipo, 6, 5.00, 800.00, NULL, 1, 4, '2025-11-27 09:47:37', 'Compra taladros', '2025-11-27 15:47:37'),
(7, 'salida'::movimiento_tipo, 6, 1.00, NULL, 1100.00, 1, NULL, '2025-11-27 09:47:37', 'Venta', '2025-11-27 15:47:37'),
(8, 'entrada'::movimiento_tipo, 7, 50.00, 60.00, NULL, 1, 9, '2025-11-27 09:47:37', 'Ingreso pegamento', '2025-11-27 15:47:37'),
(9, 'salida'::movimiento_tipo, 7, 10.00, NULL, 90.00, 1, NULL, '2025-11-27 09:47:37', 'Salida para carpintería', '2025-11-27 15:47:37'),
(10, 'entrada'::movimiento_tipo, 8, 40.00, 40.00, NULL, 1, 6, '2025-11-27 09:47:37', 'Tornillos', '2025-11-27 15:47:37'),
(11, 'salida'::movimiento_tipo, 8, 15.00, NULL, 70.00, 1, NULL, '2025-11-27 09:47:37', 'Venta', '2025-11-27 15:47:37'),
(12, 'entrada'::movimiento_tipo, 10, 30.00, 85.00, NULL, 1, 7, '2025-11-27 09:47:37', 'Pintura blanca', '2025-11-27 15:47:37'),
(13, 'salida'::movimiento_tipo, 10, 8.00, NULL, 130.00, 1, NULL, '2025-11-27 09:47:37', 'Venta', '2025-11-27 15:47:37'),
(14, 'entrada'::movimiento_tipo, 12, 60.00, 30.00, NULL, 1, 11, '2025-11-27 09:47:37', 'Guantes', '2025-11-27 15:47:37'),
(15, 'salida'::movimiento_tipo, 12, 20.00, NULL, 55.00, 1, NULL, '2025-11-27 09:47:37', 'Salida taller', '2025-11-27 15:47:37');

-- Vistas (convertidas a Postgres)
DROP VIEW IF EXISTS vista_inventario_actual;
CREATE VIEW vista_inventario_actual AS
SELECT p.id AS id,
       p.codigo AS codigo,
       p.nombre AS nombre,
       p.descripcion AS descripcion,
       c.nombre AS categoria,
       pr.nombre AS proveedor,
       p.stock_actual AS stock_actual,
       p.stock_minimo AS stock_minimo,
       p.stock_maximo AS stock_maximo,
       p.costo_unitario AS costo_unitario,
       p.precio_venta AS precio_venta,
       (p.stock_actual * p.costo_unitario) AS valor_inventario,
       CASE
         WHEN p.stock_actual = 0 THEN 'Sin Stock'
         WHEN p.stock_actual <= p.stock_minimo THEN 'Stock Bajo'
         ELSE 'Normal'
       END AS estado_stock
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.id
LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
WHERE p.activo = TRUE;

DROP VIEW IF EXISTS vista_movimientos_detallados;
CREATE VIEW vista_movimientos_detallados AS
SELECT m.id AS id,
       m.tipo AS tipo,
       m.fecha AS fecha,
       p.codigo AS producto_codigo,
       p.nombre AS producto_nombre,
       m.cantidad AS cantidad,
       m.costo_unitario AS costo_unitario,
       m.precio_unitario AS precio_unitario,
       (m.cantidad * COALESCE(m.costo_unitario, m.precio_unitario, 0)) AS total,
       u.nombre AS usuario,
       pr.nombre AS proveedor,
       m.notas AS notas
FROM movimientos m
JOIN productos p ON m.producto_id = p.id
JOIN usuarios u ON m.usuario_id = u.id
LEFT JOIN proveedores pr ON m.proveedor_id = pr.id
-- ORDER BY m.fecha DESC;  -- ORDER BY en vista normalmente se ignora en Postgres, se puede aplicar al consultar
;

DROP VIEW IF EXISTS vista_productos_stock_bajo;
CREATE VIEW vista_productos_stock_bajo AS
SELECT p.id AS id,
       p.codigo AS codigo,
       p.nombre AS nombre,
       c.nombre AS categoria,
       p.stock_actual AS stock_actual,
       p.stock_minimo AS stock_minimo,
       (p.stock_minimo - p.stock_actual) AS cantidad_faltante
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.id
WHERE p.activo = TRUE
  AND p.stock_actual <= p.stock_minimo
ORDER BY p.stock_actual ASC;

-- Ajustar secuencias para respetar los id insertados
SELECT setval(pg_get_serial_sequence('categorias','id'), COALESCE((SELECT MAX(id) FROM categorias), 1));
SELECT setval(pg_get_serial_sequence('proveedores','id'), COALESCE((SELECT MAX(id) FROM proveedores), 1));
SELECT setval(pg_get_serial_sequence('usuarios','id'), COALESCE((SELECT MAX(id) FROM usuarios), 1));
SELECT setval(pg_get_serial_sequence('productos','id'), COALESCE((SELECT MAX(id) FROM productos), 1));
SELECT setval(pg_get_serial_sequence('movimientos','id'), COALESCE((SELECT MAX(id) FROM movimientos), 1));

COMMIT;
