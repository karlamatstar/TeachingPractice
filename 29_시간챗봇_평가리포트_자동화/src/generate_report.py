import csv
import re
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "_OUTPUT"

def get_next_version(reports_dir: Path) -> int:
    existing_files = list(reports_dir.glob("test_report_v*.md"))
    max_v = 0
    for f in existing_files:
        match = re.search(r'test_report_v(\d+)\.md', f.name)
        if match:
            v = int(match.group(1))
            if v > max_v:
                max_v = v
    return max_v + 1

def generate_markdown_report(
    csv_path: str = OUTPUT_DIR / "test_results" / "test_results.csv",
    reports_dir_str: str = OUTPUT_DIR / "reports"
):
    csv_file = Path(csv_path)
    if not csv_file.exists():
        logging.warning(f"CSV 파일이 없습니다: {csv_path}")
        return
        
    reports_dir = Path(reports_dir_str)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    version = get_next_version(reports_dir)
    output_path = reports_dir / f"test_report_v{version}.md"
    
    rows = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            
    total = len(rows)
    if total == 0:
        logging.warning("CSV 파일에 데이터가 없습니다.")
        return
        
    passed = sum(1 for r in rows if r['pass_fail'] == 'PASS')
    failed = total - passed
    pass_rate = round((passed / total) * 100, 1)
    
    valid_times = [float(r['response_time_sec']) for r in rows if r.get('response_time_sec')]
    avg_time = round(sum(valid_times) / len(valid_times), 2) if valid_times else 0
    
    type_stats = {}
    for r in rows:
        t = r['type']
        if t not in type_stats:
            type_stats[t] = {'total': 0, 'pass': 0, 'fail': 0}
        type_stats[t]['total'] += 1
        if r['pass_fail'] == 'PASS':
            type_stats[t]['pass'] += 1
        else:
            type_stats[t]['fail'] += 1
            
    type_table = []
    for t, stat in type_stats.items():
        prate = round((stat['pass'] / stat['total']) * 100, 1)
        type_table.append(f"| {t} | {stat['total']} | {stat['pass']} | {stat['fail']} | {prate}% |")
        
    type_table_str = "\n".join(type_table)
    
    md = [
        f"# 테스트 결과 보고서 (v{version})",
        "",
        "## 1. 전체 결과 요약",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        f"| 총 테스트 케이스 | {total} |",
        f"| PASS | {passed} |",
        f"| FAIL | {failed} |",
        f"| PASS율 | {pass_rate}% |",
        f"| 평균 응답 시간 | 약 {avg_time}초 |",
        "",
        "## 2. 유형별(Happy/Edge/Negative) 결과",
        "",
        "| 유형 | 총 케이스 | PASS | FAIL | PASS율 |",
        "|---|---|---|---|---|",
        type_table_str,
        "",
        "*(유형별 결과 분석을 작성하세요)*",
        "",
        "## 3. 결함위치(Defect Location) 분포",
        "",
        "*(결함위치 분석을 작성하세요)*",
        "",
        "## 4. 발견된 주요 문제 패턴",
        "",
        "*(주요 문제 패턴을 작성하세요)*",
        "",
        "## 5. 테스트 케이스별 상세 평가 결과",
        "",
        "| 번호 | 케이스ID | 질문 | AI 답변 | 평가 결과 |",
        "|---|---|---|---|---|"
    ]
    
    for i, row in enumerate(rows, start=1):
        case_id = row['case_id']
        question = row['user_question'].replace('\n', '<br>').replace('|', '&#124;')
        ai_ans = row['ai_answer'].replace('\n', '<br>').replace('|', '&#124;')
        
        acc = row['accuracy_score']
        use = row['usefulness_score']
        saf = row['safety_score']
        rel = row['reliability_score']
        tool = row['tool_score']
        reason = row['reason'].replace('\n', '<br>').replace('|', '&#124;')
        
        eval_result = f"**정확성**: {acc}점<br>**유용성**: {use}점<br>**안전성**: {saf}점<br>**신뢰성**: {rel}점<br>**Tool Calling**: {tool}점<br><br>**사유**: {reason}"
        
        md.append(f"| {i} | {case_id} | {question} | {ai_ans} | {eval_result} |")
        
    md.extend([
        "",
        "## 6. 결함 보고서 (Bug Report)",
        "",
        "*(버그 리포트를 작성하세요)*",
        "",
        "## 7. 결론 및 권고",
        "",
        "*(결론 및 권고 사항을 작성하세요)*",
        ""
    ])
    
    output_path.write_text("\n".join(md), encoding='utf-8')
    logging.info(f"새 마크다운 보고서가 생성되었습니다: {output_path}")

if __name__ == "__main__":
    generate_markdown_report()
