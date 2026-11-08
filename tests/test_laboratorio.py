"""Pruebas del laboratorio sin modificar la base de datos real."""
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import app
import detector
from crearDB import inicializar_bd

class TestAplicacion(unittest.TestCase):
    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        raiz = Path(self.directorio.name)
        self.bd = raiz / "usuarios.db"
        self.log = raiz / "eventos.log"
        inicializar_bd(self.bd)
        self.parches = [patch.object(app, "DB_PATH", self.bd), patch.object(app, "LOG_PATH", self.log)]
        for parche in self.parches:
            parche.start()
        app.app.config["TESTING"] = True
        self.cliente = app.app.test_client()

    def tearDown(self):
        for parche in self.parches:
            parche.stop()
        self.directorio.cleanup()

    def registrar(self, usuario="usuario_01", correo="prueba@example.com", password="Prueba123!"):
        return self.cliente.post("/registro", data={
            "usuario": usuario, "correo": correo, "password": password
        })

    def test_registro_hash_y_login(self):
        respuesta = self.registrar()
        self.assertEqual(respuesta.status_code, 200)
        with sqlite3.connect(self.bd) as conexion:
            guardado = conexion.execute("SELECT password FROM usuarios").fetchone()[0]
        self.assertNotEqual(guardado, "Prueba123!")
        self.assertTrue(guardado)
        self.assertEqual(self.cliente.post("/login", data={"usuario": "usuario_01", "password": "Prueba123!"}).status_code, 200)
        self.assertEqual(self.cliente.post("/login", data={"usuario": "usuario_01", "password": "incorrecta"}).status_code, 401)
        self.assertIn("LOGIN_CORRECTO", self.log.read_text(encoding="utf-8"))
        self.assertIn("LOGIN_FALLIDO", self.log.read_text(encoding="utf-8"))

    def test_validaciones_y_duplicados(self):
        self.assertEqual(self.registrar(usuario="abc").status_code, 400)
        self.assertEqual(self.registrar(usuario="usuario#01").status_code, 400)
        self.assertEqual(self.registrar(correo="correo-invalido").status_code, 400)
        self.assertEqual(self.registrar(password="abc123").status_code, 400)
        self.assertEqual(self.registrar().status_code, 200)
        self.assertEqual(self.registrar().status_code, 409)
        self.assertEqual(self.registrar(usuario="usuario_02").status_code, 409)
        self.assertEqual(self.registrar(usuario="usuario_02", correo="prueba02@example.com").status_code, 200)

class TestDetector(unittest.TestCase):
    def test_tres_fallos_consecutivos_y_reinicio(self):
        t = datetime(2026, 11, 2, 12, 0, 0)
        eventos = [
            (1, t, "LOGIN_FALLIDO", "usuario_01"),
            (2, t, "LOGIN_CORRECTO", "usuario_01"),
            (3, t, "LOGIN_FALLIDO", "usuario_01"),
            (4, t, "LOGIN_FALLIDO", "usuario_01"),
            (5, t, "LOGIN_FALLIDO", "usuario_01"),
            (6, t, "LOGIN_FALLIDO", "usuario_01"),
        ]
        alertas = detector.detectar_grupos(eventos)
        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["id"], "usuario_01:5")

    def test_mttd_mttr_y_sin_duplicar(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            eventos = raiz / "eventos.log"
            resultados = raiz / "resultados.csv"
            respuestas = raiz / "respuesta.log"
            inicio = datetime(2026, 11, 2, 12, 0, 0)
            entradas = [
                f"{(inicio + timedelta(seconds=i)).strftime(detector.FORMATO)},LOGIN_FALLIDO,usuario_01\n"
                for i in range(3)
            ]
            eventos.write_text("".join(entradas), encoding="utf-8")
            tiempos = iter([inicio + timedelta(seconds=13), inicio + timedelta(seconds=20)])
            registros = detector.analizar(eventos, resultados, respuestas, confirmar=lambda _: None,
                                         ahora=lambda: next(tiempos), mostrar=lambda _: None)
            self.assertEqual(len(registros), 1)
            self.assertEqual(registros[0]["mttd_segundos"], "13.00")
            self.assertEqual(registros[0]["mttr_segundos"], "7.00")
            self.assertIn("USUARIO_BLOQUEADO_SIMULADO", respuestas.read_text(encoding="utf-8"))
            registros2 = detector.analizar(eventos, resultados, respuestas, confirmar=lambda _: None,
                                          mostrar=lambda _: None)
            self.assertEqual(len(registros2), 1)

if __name__ == "__main__":
    unittest.main()
