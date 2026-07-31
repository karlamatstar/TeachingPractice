@echo off
cd /d "%~dp0.."

echo ========================================
echo Standalone Test Environment Setup
echo ========================================
echo.

IF NOT EXIST ".venv" (
    echo [INFO] .venv not found. Creating a new virtual environment...
    python -m venv .venv
    
    echo [INFO] Activating .venv and installing requirements...
    call .venv\Scripts\activate.bat
    pip install -r src\requirements.txt > nul
    echo [INFO] Installation complete!
) ELSE (
    echo [INFO] Activating existing .venv...
    call .venv\Scripts\activate.bat
)

echo.
echo ========================================
echo Running Tests...
echo ========================================
echo.
python src\run_tests.py

echo.
echo Test Execution Completed.
pause
