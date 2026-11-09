@echo off
setlocal
chcp 65001 >nul
title Laboratorio de ciberseguridad
cd /d "%~dp0proyecto"
if not exist "venv\Scripts\python.exe" (
  echo Preparando entorno de Python...
  where py >nul 2>&1
  if not errorlevel 1 (
    py -3 -m venv venv
  ) else (
    python -m venv venv
  )
)
if not exist "venv\Scripts\python.exe" (
  echo No se pudo crear el entorno virtual. Comprueba que Python este instalado.
  pause
  exit /b 1
)
echo Instalando o comprobando Flask...
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo No se pudieron instalar las dependencias.
  pause
  exit /b 1
)
"venv\Scripts\python.exe" crearDB.py
if errorlevel 1 (
  echo No se pudo preparar la base de datos.
  pause
  exit /b 1
)
echo.
echo Abriendo http://127.0.0.1:5000
echo No cierres esta ventana mientras uses la aplicacion.
start "" cmd /c "timeout /t 2 >nul & start http://127.0.0.1:5000"
"venv\Scripts\python.exe" app.py
echo.
echo El servidor se ha detenido.
pause
