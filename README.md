# Laboratorio: Código Seguro y Modelo OWASP

## 1. Datos generales

- **Nombre completo:** Job José Benavides Pérez
- **Carné:** N/A
- **Correo institucional:** N/A
- **Asignatura:** Lenguajes de Programación con Aspectos de Seguridad
- **Fecha:** 08/11/2026

## 2. Descripción

En esta práctica se desarrolla una aplicación web sencilla con Python, Flask y SQLite. El objetivo es aprender a recibir y validar información, proteger las contraseñas y registrar lo que ocurre cuando un usuario intenta iniciar sesión.

También se incorpora un detector que identifica varios intentos fallidos de acceso. A partir de los registros se calculan dos medidas utilizadas en seguridad informática: **MTTD**, que indica cuánto se tarda en detectar un incidente, y **MTTR**, que indica cuánto se tarda en responder.

El bloqueo se representa mediante un registro de respuesta; no se desactiva realmente la cuenta, tal como establece la guía.

## 3. Estructura del proyecto

```text
laboratorio-esit-ciberseguridad-mttd-mttr/
├── README.md
├── RESULTADOS.md
├── INICIAR_LABORATORIO_WINDOWS.bat
└── proyecto/
    ├── app.py
    ├── crearDB.py
    ├── detector.py
    ├── requirements.txt
    ├── templates/
    │   ├── inicio.html
    │   ├── registro.html
    │   └── login.html
    ├── static/
    │   └── estilos.css
    ├── scripts/
    │   └── ejecutar_escenarios.py
    └── tests/
        └── test_laboratorio.py
```

**Archivos principales:** `app.py` recibe las solicitudes; `crearDB.py` prepara la base de datos; y `detector.py` revisa los eventos de autenticación y calcula los tiempos de detección y respuesta.

La base `usuarios.db` y los archivos `eventos.log`, `respuesta.log` y `resultados.csv` se crean al ejecutar la práctica. No se incluyen en el repositorio para evitar publicar información generada durante las pruebas.

## 4. Ejecución del proyecto

**Paso 1.** Clonar el repositorio:

```bash
git clone https://github.com/benavidesj61-lgtm/laboratorio-esit-ciberseguridad-mttd-mttr.git
```

**Paso 2.** Para Windows 11, abrir la carpeta clonada y hacer doble clic en `INICIAR_LABORATORIO_WINDOWS.bat`. El archivo prepara el entorno, instala Flask si hace falta y ejecuta la aplicación. **La ventana de la terminal debe quedar abierta** mientras se utiliza el navegador.

Como alternativa, desde una terminal de VS Code:

```powershell
cd laboratorio-esit-ciberseguridad-mttd-mttr/proyecto
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe crearDB.py
.\venv\Scripts\python.exe app.py
```

**Paso 3.** Abrir en el navegador:

- Inicio: http://127.0.0.1:5000/
- Registro: http://127.0.0.1:5000/registro
- Inicio de sesión: http://127.0.0.1:5000/login

**Paso 4.** Registrar dos usuarios de prueba. Comprobar que la aplicación rechace nombres inválidos, correos mal escritos, contraseñas cortas y usuarios duplicados. Después, iniciar sesión con una contraseña correcta y probar tres contraseñas incorrectas para un mismo usuario.

**Paso 5.** En una segunda terminal, dentro de `proyecto`, ejecutar:

```powershell
.\venv\Scripts\python.exe detector.py
```

El programa mostrará la alerta y el MTTD. Al presionar Enter, guardará la respuesta simulada y calculará el MTTR. Se puede repetir el procedimiento para completar tres escenarios.

## 5. Pruebas y resultados

Se verificaron el registro de usuarios, las validaciones de entrada, el uso de contraseñas con hash, los intentos de inicio de sesión, la detección de alertas y los cálculos de MTTD y MTTR.

| Prueba | MTTD | MTTR |
|---|---:|---:|
| 1 | 0.40 s | 0.08 s |
| 2 | 0.54 s | 0.12 s |
| 3 | 0.68 s | 0.17 s |
| **Promedio** | **0.54 s** | **0.12 s** |

Estos valores se obtuvieron en una **prueba automatizada de GitHub Actions**, usando usuarios de ejemplo y tres escenarios diferentes. Se pueden consultar los registros y el método de prueba en [Resultados y comprobaciones](RESULTADOS.md). Los tiempos pueden variar cuando se repita la actividad en otro equipo.

Para ejecutar las pruebas de código desde `proyecto`:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 6. Conclusión

La práctica permitió reunir en una misma aplicación varias medidas básicas de seguridad: validar los datos, guardar las contraseñas de forma protegida y registrar accesos correctos e incorrectos.

La parte de detección permitió observar cómo cambia el tiempo transcurrido entre el primer intento sospechoso, la alerta y la respuesta. Con ello fue posible calcular MTTD y MTTR y comprobar la importancia de contar con registros claros al analizar un incidente.

