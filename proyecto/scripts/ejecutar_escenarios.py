"""Tres escenarios reales de CI: Flask test client, logs y métricas MTTD/MTTR."""
import argparse
import csv
import shutil
import sqlite3
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import app
import detector
from crearDB import inicializar_bd
from werkzeug.security import check_password_hash


def verificar(condicion, mensaje):
    if not condicion:
        raise AssertionError(mensaje)


def ejecutar(destino):
    destino.mkdir(parents=True, exist_ok=True)
    mensajes = []
    inicio_ejecucion = datetime.now().astimezone().isoformat(timespec="seconds")

    with tempfile.TemporaryDirectory(prefix="esit-lab-") as tmp:
        carpeta = Path(tmp)
        bd = carpeta / "usuarios.db"
        eventos = carpeta / "eventos.log"
        respuestas = carpeta / "respuesta.log"
        resultados = carpeta / "resultados.csv"
        inicializar_bd(bd)
        app.app.config["TESTING"] = True

        with patch.object(app, "DB_PATH", bd), patch.object(app, "LOG_PATH", eventos):
            cliente = app.app.test_client()
            for ruta in ("/", "/registro", "/login"):
                verificar(cliente.get(ruta).status_code == 200, "Ruta web fallida: " + ruta)

            for numero in (1, 2):
                usuario = f"usuario_{numero:02d}"
                respuesta = cliente.post("/registro", data={
                    "usuario": usuario, "correo": f"prueba{numero}@example.com",
                    "password": "Prueba123!"
                })
                verificar(respuesta.status_code == 200, f"No pudo registrar {usuario}")

            invalidos = (
                ("abc", "correo@example.com", "Prueba123!"),
                ("usuario#01", "correo@example.com", "Prueba123!"),
                ("usuario normal", "correo@example.com", "Prueba123!"),
                ("usuario_03", "invalido", "Prueba123!"),
                ("usuario_03", "correo@example.com", "abc123"),
            )
            for usuario, correo, password in invalidos:
                respuesta = cliente.post("/registro", data={
                    "usuario": usuario, "correo": correo, "password": password
                })
                verificar(respuesta.status_code == 400, "No rechazo datos invalidos")

            duplicado = cliente.post("/registro", data={
                "usuario": "usuario_01", "correo": "prueba1@example.com",
                "password": "Prueba123!"
            })
            verificar(duplicado.status_code == 409, "No rechazo usuario duplicado")

            with sqlite3.connect(bd) as db:
                usuarios = db.execute("SELECT usuario, password FROM usuarios").fetchall()
            verificar(len(usuarios) == 2, "Se esperaban dos usuarios")
            verificar(all(hash_ != "Prueba123!" and check_password_hash(hash_, "Prueba123!")
                         for _usuario, hash_ in usuarios), "Hash invalido")

            # Cada escenario tiene tiempos distintos y tres fallos via /login.
            escenarios = (
                ("usuario_01", 0.10, 0.08),
                ("usuario_02", 0.17, 0.12),
                ("usuario_01", 0.24, 0.17),
            )
            for numero, (usuario, pausa, pausa_respuesta) in enumerate(escenarios, 1):
                correcto = cliente.post("/login", data={
                    "usuario": usuario, "password": "Prueba123!"
                })
                verificar(correcto.status_code == 200, "Login correcto fallido")
                for _ in range(3):
                    time.sleep(pausa)
                    fallo = cliente.post("/login", data={
                        "usuario": usuario, "password": "ClaveIncorrecta!"
                    })
                    verificar(fallo.status_code == 401, "Login fallido aceptado")

                mensajes.append(f"\n=== PRUEBA {numero}: {usuario} ===")
                def confirmar(_):
                    time.sleep(pausa_respuesta)

                filas = detector.analizar(
                    log_path=eventos, resultados_path=resultados,
                    respuestas_path=respuestas, confirmar=confirmar,
                    mostrar=mensajes.append
                )
                verificar(len(filas) == numero, "El detector omitio o duplico alertas")

            finales = detector.analizar(
                log_path=eventos, resultados_path=resultados, respuestas_path=respuestas,
                confirmar=lambda _: verificar(False, "Respuesta duplicada"),
                mostrar=mensajes.append
            )
            verificar(len(finales) == 3, "Se duplicaron incidentes")
            verificar(respuestas.read_text(encoding="utf-8").count("USUARIO_BLOQUEADO") == 3,
                     "No hay tres respuestas simuladas")
            verificar("Prueba123!" not in eventos.read_text(encoding="utf-8"),
                     "Se filtro una contrasena al log")

            for nombre in ("eventos.log", "respuesta.log", "resultados.csv"):
                shutil.copyfile(carpeta / nombre, destino / nombre)

            with resultados.open(encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
            verificar(len(filas) == 3, "Faltan tres escenarios")
            mttd = [float(r["mttd_segundos"]) for r in filas]
            mttr = [float(r["mttr_segundos"]) for r in filas]
            verificar(all(v > 0 for v in mttd + mttr), "Tiempo de medicion no positivo")

            reporte = [
                "# Resultados de las pruebas de seguridad",
                "",
                f"Fecha de la ejecucion automatizada: {inicio_ejecucion}",
                "",
                "**Entorno de prueba:** GitHub Actions (Linux, Python 3.13 y Flask).",
                "**Datos:** usuarios de ejemplo y mediciones tomadas durante la prueba;",
                "no se trata de una ejecucion en el equipo del estudiante.",
                "**Bloqueo:** SIMULADO; el usuario no se deshabilita realmente.",
                "",
                "| Prueba | Usuario | MTTD (s) | MTTR (s) |",
                "|---|---|---:|---:|",
            ]
            for n, fila in enumerate(filas, 1):
                reporte.append(f"| {n} | {fila['usuario']} | {fila['mttd_segundos']} | {fila['mttr_segundos']} |")
            reporte.append(
                f"| **Promedio** | — | **{sum(mttd)/3:.2f}** | **{sum(mttr)/3:.2f}** |"
            )
            reporte.extend([
                "",
                "**Verificado:** rutas Flask, 2 registros, validaciones, duplicados,",
                "hash de contrasenas, consultas SQL, 3 logins correctos, 9 logins",
                "fallidos, 3 alertas, 3 respuestas simuladas y no duplicacion.",
                "",
                "**Archivos:** eventos.log, respuesta.log, resultados.csv y salida_terminal.txt.",
                "",
                "**El README oficial ya se integro al repositorio. Falta entregar el enlace",
                "del repositorio por medio del Aula Virtual.**",
            ])
            (destino / "reporte.md").write_text("\n".join(reporte) + "\n", encoding="utf-8")
            (destino / "salida_terminal.txt").write_text("\n".join(mensajes) + "\n", encoding="utf-8")
            print("\n".join(reporte))
            return filas


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--salida", type=Path, default=Path("evidencias"))
    ejecutar(parser.parse_args().salida)
