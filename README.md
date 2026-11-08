# Laboratorio ESIT: Seguridad web, MTTD y MTTR

Práctica de **Unidad 3 — Código Seguro y Modelo OWASP** con Python, Flask y SQLite.

**Importante:** Descarga del Aula Virtual el README oficial y complétalo con tus datos académicos. Esta documentación técnica no sustituye el archivo o datos requeridos por la tutora.

## Funcionalidades

- Formulario de registro e inicio de sesión con SQLite.
- Validación del nombre de usuario (4-20 caracteres, letras, números y guion bajo), formato de correo y longitud mínima de contraseña (8).
- Comprobación de duplicados, sentencias SQL parametrizadas y hash de contraseñas con Werkzeug.
- Registro de eventos `LOGIN_CORRECTO` y `LOGIN_FALLIDO` sin almacenar contraseñas.
- Alerta al detectar tres intentos fallidos consecutivos de un mismo usuario.
- MTTD: detección menos primer intento fallido; MTTR: respuesta simulada menos detección.
- Tabla y promedios para tres escenarios; resultados persistidos en `resultados.csv` (excluido de Git).

## Windows 11 + VS Code

Abre una terminal PowerShell **en esta carpeta del proyecto**, y ejecuta:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe crearDB.py
.\venv\Scripts\python.exe app.py
```

Abre `http://127.0.0.1:5000/registro` para registrar un usuario ficticio y `http://127.0.0.1:5000/login` para iniciar sesión. En otra terminal:

```powershell
.\venv\Scripts\python.exe detector.py
```

## Pruebas del laboratorio

1. Registra dos usuarios de ejemplo con correos ficticios y contraseñas de 8+ caracteres.
2. Prueba usuario inválido, correo inválido, contraseña corta, usuario duplicado y login incorrecto.
3. Con `usuario_01`, inicia sesión correctamente, luego introduce **tres veces seguidas** una contraseña incorrecta.
4. Ejecuta `detector.py`. Se generará una alerta con MTTD, se pedirá presionar Enter para registrar el bloqueo **simulado**, y se mostrará MTTR.
5. Repite el paso anterior con dos grupos adicionales de tres intentos fallidos y ejecución de `detector.py` para registrar **tres escenarios** y observar promedios.
6. Revisa `eventos.log`, `respuesta.log`, `resultados.csv` (archivos generados localmente, no publicados).

| Prueba | MTTD (s) | MTTR (s) |
|---|---:|---:|
| 1 | Por medir | Por medir |
| 2 | Por medir | Por medir |
| 3 | Por medir | Por medir |
| Promedio | Por calcular | Por calcular |

**No inventar resultados:** las cifras salen de las ejecuciones reales.

## Pruebas automatizadas

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Seguridad y límites

La acción `USUARIO_BLOQUEADO_SIMULADO` registrada en `respuesta.log` **no bloquea realmente** la cuenta; así lo pide la práctica. El detector se ejecuta manualmente: no es un SIEM de tiempo real. Flask corre en desarrollo local con `debug=True` y **no debe exponerse a Internet**. El archivo `.gitignore` impide publicar bases de datos locales, logs y entornos virtuales.

Para entregar, pega únicamente el **enlace del repositorio público** en el Aula Virtual; no envíes ZIP.
