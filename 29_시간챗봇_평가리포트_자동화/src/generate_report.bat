@echo off
cd /d "%~dp0.."
echo Activating .venv...
call .venv\Scripts\activate.bat
echo Generating Markdown Report...
python src\generate_report.py
pause
