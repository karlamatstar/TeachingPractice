@echo off
rem VOC Improve QA 런처 실행 (콘솔 창 없이 GUI만 표시)
cd /d "%~dp0.."
start "" ".venv\Scripts\pythonw.exe" "RUN\run_gui.py"

