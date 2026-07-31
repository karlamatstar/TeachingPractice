# AI 서비스 품질관리 3시간 실습

## 설치

```powershell
cd C:\AI_Service_Quality_Lab
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Streamlit 실행

```powershell
streamlit run app.py
```

## pytest 실행

```powershell
pytest -v
```

정상 기준은 `5 passed`입니다.

## JupyterLab 실행

```powershell
jupyter lab
```

## 평가 기준

- 관련성
- 구체성
- 실행가능성
- 측정가능성
- 안전성

실제 API를 호출하지 않으므로 비용이 발생하지 않습니다.
