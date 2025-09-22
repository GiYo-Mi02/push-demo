@echo off
setlocal

REM Try Python on PATH first
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python -m pip install -r requirements.txt
  exit /b %ERRORLEVEL%
)

REM Fallback to per-user install path (winget default)
set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%PY_EXE%" (
  "%PY_EXE%" -m pip install -r requirements.txt
  exit /b %ERRORLEVEL%
)

echo Could not find Python. Install Python 3.8+ and re-run this script.
exit /b 1
