-- phpMyAdmin SQL Dump
-- Compatible con Railway MySQL

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET NAMES utf8mb4 */;

-- =========================
-- TABLA: categorias
-- =========================
CREATE TABLE `categorias` (
`id` int(11) NOT NULL,
`nombre` varchar(100) NOT NULL,
`descripcion` text DEFAULT NULL,
`activo` tinyint(1) DEFAULT 1,
`created_at` timestamp NOT NULL DEFAULT current_timestamp(),
`updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `categorias` VALUES
(1,'Maderas','Maderas naturales y procesadas',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(2,'Triplay','Laminados y contrachapados',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(3,'MDF','Tableros de fibra de densidad media',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(4,'Herramientas Manuales','Herramientas de carpintería básica',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(5,'Herramientas Eléctricas','Sierras, taladros, routers',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(6,'Adhesivos','Pegamentos, resinas y colas',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(7,'Tornillería','Tornillos, clavos y fijaciones',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(8,'Barnices','Barnices, lacas y selladores',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(9,'Pinturas','Pinturas para madera',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(10,'Accesorios','Accesorios varios',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(11,'Protección','Equipo de protección personal',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(12,'Iluminación','Focos y lámparas',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(13,'Ferretería','Artículos generales de ferretería',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(14,'Selladores','Selladores para juntas y madera',1,'2025-11-27 15:47:37','2025-11-27 15:47:37'),
(15,'Especialidades','Productos especiales',1,'2025-11-27 15:47:37','2025-11-27 15:47:37');

ALTER TABLE `categorias`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `categorias`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

-- =========================
-- TABLA: proveedores
-- =========================
CREATE TABLE `proveedores` (
`id` int(11) NOT NULL,
`nombre` varchar(150) NOT NULL,
`contacto` varchar(100),
`telefono` varchar(20),
`email` varchar(100),
`direccion` text,
`activo` tinyint(1) DEFAULT 1,
`created_at` timestamp NOT NULL DEFAULT current_timestamp(),
`updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `proveedores`
ADD PRIMARY KEY (`id`);

ALTER TABLE `proveedores`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

-- =========================
-- TABLA: usuarios
-- =========================
CREATE TABLE `usuarios` (
`id` int(11) NOT NULL,
`nombre` varchar(100) NOT NULL,
`email` varchar(100) NOT NULL,
`password` varchar(255) NOT NULL,
`rol` enum('administrador','empleado') DEFAULT 'empleado',
`activo` tinyint(1) DEFAULT 1,
`created_at` timestamp NOT NULL DEFAULT current_timestamp(),
`updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `usuarios`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `usuarios`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

-- =========================
-- TABLA: productos
-- =========================
CREATE TABLE `productos` (
`id` int(11) NOT NULL,
`codigo` varchar(50) NOT NULL,
`nombre` varchar(200) NOT NULL,
`descripcion` text,
`categoria_id` int(11),
`proveedor_id` int(11),
`stock_actual` decimal(10,2) DEFAULT 0,
`stock_minimo` decimal(10,2) DEFAULT 0,
`stock_maximo` decimal(10,2),
`costo_unitario` decimal(10,2) DEFAULT 0,
`precio_venta` decimal(10,2) DEFAULT 0,
`activo` tinyint(1) DEFAULT 1,
`created_at` timestamp NOT NULL DEFAULT current_timestamp(),
`updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `productos`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `codigo` (`codigo`),
ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`) ON DELETE SET NULL,
ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`) ON DELETE SET NULL;

ALTER TABLE `productos`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

-- =========================
-- TABLA: movimientos
-- =========================
CREATE TABLE `movimientos` (
`id` int(11) NOT NULL,
`tipo` enum('entrada','salida') NOT NULL,
`producto_id` int(11) NOT NULL,
`cantidad` decimal(10,2) NOT NULL,
`costo_unitario` decimal(10,2),
`precio_unitario` decimal(10,2),
`usuario_id` int(11) NOT NULL,
`proveedor_id` int(11),
`fecha` datetime NOT NULL,
`notas` text,
`created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `movimientos`
ADD PRIMARY KEY (`id`),
ADD CONSTRAINT `movimientos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `movimientos_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `movimientos_ibfk_3` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`) ON DELETE SET NULL;

ALTER TABLE `movimientos`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

-- =========================
-- VISTAS (Railway compatible)
-- =========================
CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=CURRENT_USER SQL SECURITY DEFINER VIEW `vista_inventario_actual` AS
SELECT p.id, p.codigo, p.nombre, p.descripcion,
c.nombre AS categoria, pr.nombre AS proveedor,
p.stock_actual, p.stock_minimo, p.stock_maximo,
p.costo_unitario, p.precio_venta,
p.stock_actual * p.costo_unitario AS valor_inventario,
CASE
WHEN p.stock_actual = 0 THEN 'Sin Stock'
WHEN p.stock_actual <= p.stock_minimo THEN 'Stock Bajo'
ELSE 'Normal'
END AS estado_stock
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.id
LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
WHERE p.activo = 1;

CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=CURRENT_USER SQL SECURITY DEFINER VIEW `vista_productos_stock_bajo` AS
SELECT p.id, p.codigo, p.nombre,
c.nombre AS categoria,
p.stock_actual, p.stock_minimo,
p.stock_minimo - p.stock_actual AS cantidad_faltante
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.id
WHERE p.activo = 1 AND p.stock_actual <= p.stock_minimo
ORDER BY p.stock_actual ASC;

CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=CURRENT_USER SQL SECURITY DEFINER VIEW `vista_movimientos_detallados` AS
SELECT m.id, m.tipo, m.fecha,
p.codigo AS producto_codigo,
p.nombre AS producto_nombre,
m.cantidad, m.costo_unitario, m.precio_unitario,
m.cantidad * COALESCE(m.costo_unitario, m.precio_unitario, 0) AS total,
u.nombre AS usuario,
pr.nombre AS proveedor,
m.notas
FROM movimientos m
JOIN productos p ON m.producto_id = p.id
JOIN usuarios u ON m.usuario_id = u.id
LEFT JOIN proveedores pr ON m.proveedor_id = pr.id
ORDER BY m.fecha DESC;

COMMIT;
