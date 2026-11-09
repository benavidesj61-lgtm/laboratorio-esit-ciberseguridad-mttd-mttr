"""Inicializa SQLite para el laboratorio de ESIT."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "usuarios.db"

def inicializar_bd(ruta=DB_PATH):
    with sqlite3.connect(ruta) as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                correo TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

if __name__ == "__main__":
    inicializar_bd()
    print("Base de datos y tabla creadas correctamente.")
