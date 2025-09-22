@echo off
setlocal

REM Try Python on PATH first
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python main.py
  exit /b %ERRORLEVEL%
)

REM Fallback to per-user install path (winget default)
set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%PY_EXE%" (
  "%PY_EXE%" main.py
  exit /b %ERRORLEVEL%
)

echo Could not find Python. Install it or edit run.bat to point to your Python.
exit /b 1
