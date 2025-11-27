CREATE DATABASE IF NOT EXISTS gestion_drones_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE gestion_drones_db;

-- Tabla usuarios (con admin por defecto)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'operador', 'rescatista') NOT NULL DEFAULT 'rescatista',
    password VARCHAR(64)
);

-- Tabla drones
CREATE TABLE drones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(50) NOT NULL,
    bateria INT NOT NULL DEFAULT 100 CHECK (bateria BETWEEN 0 AND 100),
    ubicacion VARCHAR(100) DEFAULT 'Base central',
    sensores_activos TINYINT(1) DEFAULT 1,
    camara_activa TINYINT(1) DEFAULT 1,
    disponible TINYINT(1) DEFAULT 1
);

-- Tabla misiones
CREATE TABLE misiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    operador_id INT NOT NULL,
    estado ENUM('pendiente', 'en_curso', 'completada') DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (operador_id) REFERENCES usuarios(id)
);

-- Tabla reportes
CREATE TABLE reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mision_id INT NOT NULL,
    descripcion TEXT,
    victimas_localizadas INT DEFAULT 0,
    rutas_seguras TEXT,
    datos_extra JSON,
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE
);

-- admin
-- admin123
INSERT INTO usuarios (nombre, role, password) VALUES (
    'admin', 
    'admin', 
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
);