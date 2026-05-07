CREATE DATABASE reservas_db;

USE reservas_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    privilegio VARCHAR(20) NOT NULL
);

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sala VARCHAR(50) NOT NULL,
    data_reserva DATE NOT NULL,
    horario VARCHAR(50) NOT NULL,
    usuario VARCHAR(100) NOT NULL
);

INSERT INTO usuarios (usuario, senha, privilegio)
VALUES
('admin', '123', 'admin'),
('joao', '123', 'comum');
