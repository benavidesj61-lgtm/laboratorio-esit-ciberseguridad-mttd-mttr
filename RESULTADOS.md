# Resultados de las pruebas y comprobaciones

## Desarrollo de la práctica

La aplicación se preparó con Python, Flask y SQLite. Primero se comprobó el registro de usuarios, incluyendo el rechazo de datos que no cumplen los requisitos del formulario. Después se verificó el inicio de sesión con contraseñas correctas e incorrectas y se revisó la creación de los eventos de autenticación.

El detector está programado para identificar tres intentos fallidos consecutivos de un mismo usuario. Cuando encuentra ese patrón, muestra una alerta, mide el tiempo transcurrido desde el primer intento y permite registrar una respuesta **simulada**.

## Pruebas de MTTD y MTTR

Se ejecutaron tres escenarios con usuarios ficticios y diferentes intervalos entre intentos. En cada escenario se realizó un inicio de sesión correcto, seguido de tres intentos fallidos.

| Escenario | Usuario de prueba | MTTD (segundos) | MTTR (segundos) |
|---|---|---:|---:|
| 1 | usuario_01 | 0.40 | 0.08 |
| 2 | usuario_02 | 0.54 | 0.12 |
| 3 | usuario_01 | 0.68 | 0.17 |
| **Promedio** | — | **0.54** | **0.12** |

**MTTD:** tiempo entre el primer intento fallido y la detección.  
**MTTR:** tiempo entre la detección y el registro de la respuesta.

Los números de la tabla corresponden a una ejecución automatizada realizada el **8 de noviembre de 2026, hora de El Salvador**, mediante GitHub Actions. No se presentan como mediciones tomadas manualmente en una computadora personal.

## Qué se comprobó

- Se registraron dos usuarios ficticios y se verificó que sus contraseñas no se guardaran en texto plano.
- Se probaron nombres de usuario y correos inválidos, contraseñas cortas y registros duplicados.
- Se realizaron tres inicios de sesión válidos y nueve intentos fallidos.
- Se generaron tres alertas y tres respuestas registradas.
- Se comprobó que una alerta procesada no se volviera a contar al ejecutar el detector otra vez.

## Registros y código de prueba

Las pruebas automáticas se pueden revisar en [GitHub Actions](https://github.com/benavidesj61-lgtm/laboratorio-esit-ciberseguridad-mttd-mttr/actions/runs/42557324420). En esa ejecución se generaron `eventos.log`, `respuesta.log`, `resultados.csv`, `salida_terminal.txt` y `reporte.md`. Los archivos están disponibles como artefacto de la ejecución durante el período de retención establecido por GitHub.

El procedimiento para repetir las mediciones está en [`proyecto/scripts/ejecutar_escenarios.py`](proyecto/scripts/ejecutar_escenarios.py). Además, el repositorio incluye pruebas automáticas de las funciones principales en `proyecto/tests/`.

## Observaciones finales

Los valores de MTTD y MTTR dependen del intervalo entre los intentos y de cuánto se tarda en registrar la respuesta. En este ejercicio el bloqueo se simula mediante una anotación en `respuesta.log`; no modifica el acceso del usuario. La finalidad del laboratorio es comprender la detección, el registro de incidentes y el cálculo de ambas métricas.
