CREATE DATABASE SoundVisualizerDB;

USE SoundVisualizerDB;

CREATE TABLE SoundShapes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    frequency FLOAT,
    amplitude FLOAT,
    shape VARCHAR(50)
);

select * from SoundShapes;