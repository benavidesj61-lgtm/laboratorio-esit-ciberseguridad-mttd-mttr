# Laboratorio: Código Seguro y Modelo OWASP

## 1. Datos generales

- **Nombre completo:** Job José Benavides Pérez
- **Carné:** N/A
- **Correo institucional:** N/A
- **Asignatura:** LENGUAJES DE PROGRAMACIÓN CON ASPECTOS DE SEGURIDAD
- **Fecha:** 08/11/2026

> Carné y correo institucional: N/A (no asignados por ESIT).

## 2. Descripción

Este laboratorio consiste en desarrollar una aplicación web utilizando Python, implementando controles básicos de seguridad basados en buenas prácticas y el modelo OWASP. Se aplican mecanismos de validación de entradas, consultas parametrizadas, protección de contraseñas, registro de eventos de autenticación y detección de incidentes, incluyendo el cálculo de las métricas MTTD y MTTR.

## 3. Estructura del proyecto

~~~text
laboratorio-esit-ciberseguridad-mttd-mttr/
├── proyecto/
│   ├── app.py
│   ├── crearDB.py
│   ├── detector.py
│   ├── requirements.txt
│   ├── templates/
│   │   ├── registro.html
│   │   └── login.html
│   ├── scripts/
│   │   └── ejecutar_escenarios.py
│   └── tests/
│       └── test_laboratorio.py
├── README.md
├── EVIDENCIA_REMOTA.md
├── .gitignore
└── .github/workflows/tests.yml
~~~

La base de datos SQLite y los archivos de registro se generan al ejecutar el proyecto; no se publican datos sensibles.

## 4. Ejecución del proyecto

**Paso 1.** Clonar el repositorio.

~~~bash
git clone https://github.com/benavidesj61-lgtm/laboratorio-esit-ciberseguridad-mttd-mttr.git
~~~

**Paso 2.** Ingresar al proyecto.

~~~bash
cd laboratorio-esit-ciberseguridad-mttd-mttr/proyecto
~~~

**Paso 3.** Instalar las dependencias. Se recomienda un entorno virtual:

~~~bash
python -m venv venv
~~~

En Windows PowerShell, sin activar el entorno:

~~~powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
~~~

**Paso 4.** Crear la base de datos y ejecutar la aplicación:

~~~powershell
.\venv\Scripts\python.exe crearDB.py
.\venv\Scripts\python.exe app.py
~~~

Abrir **http://127.0.0.1:5000/registro** para registrar dos usuarios ficticios y **http://127.0.0.1:5000/login** para iniciar sesión y realizar tres intentos fallidos.

**Paso 5.** En otra terminal, ejecutar el detector:

~~~powershell
.\venv\Scripts\python.exe detector.py
~~~

Tras la alerta, presionar Enter para registrar la respuesta de bloqueo **simulado**. Repetir con tres escenarios diferentes para obtener los promedios de MTTD y MTTR.

## 5. Evidencias de pruebas y cálculos

- Se verifican automáticamente la validación de datos, los registros, el hash de contraseñas, los eventos y las métricas mediante GitHub Actions.
- En [EVIDENCIA_REMOTA.md](EVIDENCIA_REMOTA.md) se documentan tres escenarios ejecutados en GitHub Actions, con una tabla de MTTD y MTTR basada en sus tiempos reales y el enlace a los registros.
- Para ejecutar las pruebas unitarias desde la carpeta del proyecto: \`python -m unittest discover -s tests -v\`.
- El bloqueo de usuarios se **simula y registra**, no se deshabilita realmente ninguna cuenta.

Los resultados de GitHub Actions corresponden a una ejecución automatizada en Linux y no representan pruebas realizadas en el equipo personal del estudiante.
