"""Aplicación web Flask para el laboratorio MTTD/MTTR de ESIT (uso local)."""
import re
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "usuarios.db"
LOG_PATH = BASE_DIR / "eventos.log"
app = Flask(__name__)

def validar_usuario(usuario):
    return re.fullmatch(r"[A-Za-z0-9_]{4,20}", usuario) is not None

def validar_correo(correo):
    return re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", correo) is not None

def registrar_evento(tipo, usuario):
    """Registra un evento de autenticación sin contraseñas ni datos sensibles."""
    marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    nombre = usuario if validar_usuario(usuario) else "usuario_invalido"
    with LOG_PATH.open("a", encoding="utf-8") as archivo:
        archivo.write(f"{marca},{tipo},{nombre}\n")

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")

        if not validar_usuario(usuario):
            return "Usuario inválido (4-20 caracteres: letras, números o _)", 400
        if not validar_correo(correo):
            return "Correo electrónico inválido", 400
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres", 400

        try:
            with sqlite3.connect(DB_PATH) as conexion:
                existente = conexion.execute(
                    "SELECT id FROM usuarios WHERE usuario = ? OR correo = ?",
                    (usuario, correo),
                ).fetchone()
                if existente:
                    return "El usuario o correo ya está registrado", 409
                conexion.execute(
                    "INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)",
                    (usuario, correo, generate_password_hash(password)),
                )
        except sqlite3.IntegrityError:
            return "El usuario o correo ya está registrado", 409
        return "Usuario registrado"
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        resultado = None
        if validar_usuario(usuario):
            with sqlite3.connect(DB_PATH) as conexion:
                resultado = conexion.execute(
                    "SELECT password FROM usuarios WHERE usuario = ?", (usuario,)
                ).fetchone()

        if resultado and check_password_hash(resultado[0], password):
            registrar_evento("LOGIN_CORRECTO", usuario)
            return "Inicio de sesión correcto"
        registrar_evento("LOGIN_FALLIDO", usuario)
        return "Credenciales incorrectas", 401
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
