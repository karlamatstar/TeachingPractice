# Fake Judge 자동화 실습

실제 OpenAI 또는 Anthropic API를 호출하지 않고 다음 기능을 검증합니다.

- Judge 함수 주입과 분기 로직
- 5개 평가기준
- PASS/FAIL 판정
- JSON, CSV, Markdown 보고서 생성
- pytest 자동 테스트

## 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
pytest -v
```

## 생성 파일

- `../_OUTPUT/fake_judge/v4/evaluation_result.json`
- `../_OUTPUT/fake_judge/v4/evaluation_result.csv`
- `../_OUTPUT/fake_judge/v4/evaluation_report.md`
