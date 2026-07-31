@echo off
rem AI Agent Performance Test launcher (double-click to open the GUI)
rem Prefers the project venv (.venv); falls back to system Python.
cd /d "%~dp0.."

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "RUN\test_launcher.py"
    goto :eof
)
if exist ".venv\Scripts\python.exe" (
    start "" ".venv\Scripts\python.exe" "RUN\test_launcher.py"
    goto :eof
)

where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "RUN\test_launcher.py"
) else (
    start "" python "RUN\test_launcher.py"
)
