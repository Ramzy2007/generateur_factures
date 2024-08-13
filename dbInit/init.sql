CREATE DATABASE IF NOT EXISTS generateur_db;
USE generateur_db;

-- Importer le contenu initial
SOURCE /docker-entrypoint-initdb.d/generateur_db.sql;