@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

REM Disable system proxy for this process only
set HTTP_PROXY=
set HTTPS_PROXY=
set ALL_PROXY=
set NO_PROXY=*

set "VENV=%~dp0.venv"
set "VENV_PY=%VENV%\Scripts\python.exe"
set "PY="

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found on PATH. Install Python 3.10+ and try again.
    pause
    exit /b 1
)

REM 1. Use system Python if Django is already installed there
python -c "import django" >nul 2>&1
if not errorlevel 1 (
    set "PY=python"
    echo [setup] Using system Python ^(Django already installed^)
    goto :ready
)

REM 2. Use existing virtualenv if it has Django
if exist "%VENV_PY%" (
    "%VENV_PY%" -c "import django" >nul 2>&1
    if not errorlevel 1 (
        set "PY=%VENV_PY%"
        echo [setup] Using existing virtualenv at .venv
        goto :ready
    )
)

REM 3. Otherwise create venv and install Django via pip
if not exist "%VENV_PY%" (
    echo [setup] Creating virtual environment in .venv ...
    python -m venv "%VENV%" || goto :err_venv
)

echo [setup] Installing dependencies via pip ...
"%VENV_PY%" -m pip install --quiet --disable-pip-version-check -r "%~dp0requirements.txt" || goto :err_pip

set "PY=%VENV_PY%"

:ready

set FIRST_RUN=0
if not exist "db.sqlite3" set FIRST_RUN=1

echo [setup] Applying migrations ...
"%PY%" manage.py migrate --no-input || goto :err

if "%FIRST_RUN%"=="1" (
    echo [setup] Seeding demo data ...
    "%PY%" seed_data.py || goto :err
)

echo.
echo Demo accounts:  roman / demo1234   ^|   admin / admin1234
echo Server:         http://127.0.0.1:8000/
echo Admin panel:    http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server.
echo.

"%PY%" manage.py runserver

goto :eof

:err_venv
echo.
echo [ERROR] Could not create virtualenv. Make sure Python 3.10+ is installed.
pause
exit /b 1

:err_pip
echo.
echo [ERROR] pip could not install Django. Possible causes:
echo         - No internet access
echo         - Try installing manually:  pip install Django
echo.
echo If Django is already installed somewhere ^(e.g. globally^), this script
echo will use it on the next run.
pause
exit /b 1

:err
echo.
echo [ERROR] Setup failed. Check messages above.
pause
exit /b 1
