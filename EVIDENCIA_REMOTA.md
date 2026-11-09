# Evidencia verificada — laboratorio ESIT (ejecución remota)

**Origen:** ejecución real de [GitHub Actions #2](https://github.com/benavidesj61-lgtm/laboratorio-esit-ciberseguridad-mttd-mttr/actions/runs/42557324420), sobre el commit `81a9aae3c3cb3934860c13cb586eba00f59ac5c9`, el 9 de noviembre de 2026 a las 03:36 UTC (8 de noviembre, horario de El Salvador).

**Entorno:** Python 3.13 en Linux GitHub Actions; pruebas HTTP con el cliente de pruebas de Flask. No constituye evidencia de ejecución en el ordenador del estudiante.

## Tres pruebas exigidas por la página 32 de la guía

En cada prueba se inició sesión correctamente y luego se generaron **tres intentos fallidos** mediante `POST /login`, con diferentes intervalos. Se ejecutó `detector.analizar` y se registró la respuesta **simulada**.

| Prueba | Usuario ficticio | MTTD (s) | MTTR (s) |
|---|---|---:|---:|
| 1 | usuario_01 | 0.40 | 0.08 |
| 2 | usuario_02 | 0.54 | 0.12 |
| 3 | usuario_01 | 0.68 | 0.17 |
| **Promedio** | — | **0.54** | **0.12** |

Estas cifras fueron **medidas por el programa durante esa ejecución de CI** y verificadas contra los logs del trabajo. No son resultados inventados ni deben presentarse como mediciones manuales en Windows.

## Evidencia disponible

- [Ver ejecución verde y registro de la consola](https://github.com/benavidesj61-lgtm/laboratorio-esit-ciberseguridad-mttd-mttr/actions/runs/42557324420).
- En la parte inferior de la ejecución, en **Artifacts**, está `evidencia-esit-mttd-mttr`, con cinco archivos: `reporte.md`, `resultados.csv`, `eventos.log`, `respuesta.log` y `salida_terminal.txt` (retención de 30 días).
- Código reproducible de los tres escenarios: [scripts/ejecutar_escenarios.py](https://github.com/benavidesj61-lgtm/laboratorio-esit-ciberseguridad-mttd-mttr/blob/main/scripts/ejecutar_escenarios.py).

## Cobertura de la rúbrica, página 33

1. Aplicación Flask y estructura: `app.py`, `templates/`.
2. SQLite, tabla usuarios: `crearDB.py`.
3. Registro y almacenamiento: ruta `/registro`.
4. Usuario/correo/contraseña: validaciones en `app.py`.
5. Normalización y duplicados: `strip()` y verificación SQL.
6. Hash y consultas parametrizadas: `werkzeug.security`, SQL con `?`.
7. Logs de acceso correcto/fallido: `eventos.log`.
8. Alertas tras tres fallos: `detector.py`.
9. MTTD medido: tiempo desde el primer fallo hasta detección.
10. MTTR y respuesta simulada: `respuesta.log`, tiempo hasta el registro de respuesta.

**Límites:** no se bloquean cuentas de verdad (como indica la guía); no se ha accedido al Aula Virtual, no se ha incorporado su archivo README oficial con datos académicos, ni se ha enviado la tarea en esa plataforma. La entrega solicitada es únicamente el enlace público de este repositorio.
