@echo off
rem AI Agent quality platform client (double-click to open)
rem Runs on a colleague's computer - only needs Python installed (no packages).
cd /d "%~dp0"

where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "client.py"
) else (
    start "" python "client.py"
)
