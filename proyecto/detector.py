"""Detecta tres fallos consecutivos y mide MTTD / MTTR (respuesta simulada)."""
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EVENTOS = BASE_DIR / "eventos.log"
RESPUESTAS = BASE_DIR / "respuesta.log"
RESULTADOS = BASE_DIR / "resultados.csv"
FORMATO = "%Y-%m-%d %H:%M:%S.%f"
COLUMNAS = ["incidente", "usuario", "mttd_segundos", "mttr_segundos"]

def leer_eventos(ruta=EVENTOS):
    if not ruta.exists():
        return []
    eventos = []
    with ruta.open(encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, 1):
            partes = linea.strip().split(",", 2)
            if len(partes) != 3:
                continue
            fecha_texto, tipo, usuario = partes
            try:
                fecha = datetime.strptime(fecha_texto, FORMATO)
            except ValueError:
                try:
                    fecha = datetime.strptime(fecha_texto, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
            if tipo in ("LOGIN_CORRECTO", "LOGIN_FALLIDO"):
                eventos.append((numero, fecha, tipo, usuario))
    return eventos

def detectar_grupos(eventos):
    """Cada tercer fallo consecutivo de un usuario origina una alerta."""
    pendientes = defaultdict(list)
    alertas = []
    for numero, fecha, tipo, usuario in eventos:
        if tipo == "LOGIN_CORRECTO":
            pendientes[usuario].clear()
        elif tipo == "LOGIN_FALLIDO":
            pendientes[usuario].append((numero, fecha))
            if len(pendientes[usuario]) == 3:
                primeras = pendientes[usuario]
                alertas.append({
                    "id": f"{usuario}:{numero}",
                    "usuario": usuario,
                    "cantidad": 3,
                    "primer_intento": primeras[0][1],
                })
                pendientes[usuario] = []
    return alertas

def leer_resultados(ruta=RESULTADOS):
    if not ruta.exists():
        return []
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))

def guardar_resultado(fila, ruta=RESULTADOS):
    nuevo = not ruta.exists() or ruta.stat().st_size == 0
    with ruta.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        if nuevo:
            escritor.writeheader()
        escritor.writerow(fila)

def registrar_respuesta(usuario, fecha, ruta=RESPUESTAS):
    """Registra un bloqueo SIMULADO; no modifica la cuenta."""
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha.strftime(FORMATO)},USUARIO_BLOQUEADO,{usuario}\n")

def analizar(log_path=EVENTOS, resultados_path=RESULTADOS, respuestas_path=RESPUESTAS,
             confirmar=input, ahora=datetime.now, mostrar=print):
    eventos = leer_eventos(log_path)
    previos = leer_resultados(resultados_path)
    ids = {r["incidente"] for r in previos}
    nuevas = [a for a in detectar_grupos(eventos) if a["id"] not in ids]
    if not nuevas:
        mostrar("No hay alertas nuevas. Genera tres intentos fallidos en /login.")
    for alerta in nuevas:
        deteccion = ahora()
        mttd = max(0.0, (deteccion - alerta["primer_intento"]).total_seconds())
        mostrar("\nALERTA DE SEGURIDAD")
        mostrar(f"Usuario: {alerta['usuario']}")
        mostrar("Intentos fallidos: 3")
        mostrar(f"Primer intento: {alerta['primer_intento']}")
        mostrar(f"Detección: {deteccion}")
        mostrar(f"MTTD: {mttd:.2f} segundos")
        confirmar("Presiona Enter para registrar el bloqueo SIMULADO del usuario...")
        respuesta = ahora()
        registrar_respuesta(alerta["usuario"], respuesta, respuestas_path)
        mttr = max(0.0, (respuesta - deteccion).total_seconds())
        mostrar("Acción aplicada: bloqueo SIMULADO (no se deshabilita la cuenta)")
        mostrar(f"Respuesta: {respuesta}")
        mostrar(f"MTTR: {mttr:.2f} segundos")
        fila = {
            "incidente": alerta["id"], "usuario": alerta["usuario"],
            "mttd_segundos": f"{mttd:.2f}", "mttr_segundos": f"{mttr:.2f}",
        }
        guardar_resultado(fila, resultados_path)
        previos.append(fila)
    if previos:
        mostrar("\nRESULTADOS DEL LABORATORIO")
        for i, fila in enumerate(previos, 1):
            mostrar(f"Prueba {i}: MTTD={fila['mttd_segundos']} s | MTTR={fila['mttr_segundos']} s")
        promedio_mttd = sum(float(f["mttd_segundos"]) for f in previos) / len(previos)
        promedio_mttr = sum(float(f["mttr_segundos"]) for f in previos) / len(previos)
        mostrar(f"MTTD promedio ({len(previos)} pruebas): {promedio_mttd:.2f} s")
        mostrar(f"MTTR promedio ({len(previos)} pruebas): {promedio_mttr:.2f} s")
        if len(previos) < 3:
            mostrar(f"Faltan {3 - len(previos)} pruebas para completar las tres de la guía.")
    return previos

if __name__ == "__main__":
    analizar()
