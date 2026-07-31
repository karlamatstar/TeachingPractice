@echo off
echo =========================================
echo 챗봇 답변 품질 일일 결함 보고서 (Word) 생성기
echo =========================================
echo.

REM 현재 디렉토리 기준으로 상위의 가상환경 python.exe 경로 탐색
set PYTHON_EXE=..\..\..\..\.venv\Scripts\python.exe
if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python
)

"%PYTHON_EXE%" generate_word_report.py

echo.
pause
