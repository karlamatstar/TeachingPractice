import csv
import re
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "_OUTPUT"

def generate_markdown_table(csv_path: str) -> str:
    rows = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
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
            
            rows.append(f"| {i} | {case_id} | {question} | {ai_ans} | {eval_result} |")
            
    header = [
        "| 번호 | 케이스ID | 질문 | AI 답변 | 평가 결과 |",
        "|---|---|---|---|---|"
    ]
    return "\n".join(header + rows) + "\n\n"

def update_test_report_md(
    md_path: str = OUTPUT_DIR / "reports" / "test_report.md",
    csv_path: str = OUTPUT_DIR / "test_results" / "test_results.csv",
    section_num_bug: str = "6",
    section_title: str = "### 5.1 테스트 케이스별 상세 평가 결과"
):
    md_file = Path(md_path)
    if not md_file.exists():
        logging.warning(f"보고서 파일이 없습니다: {md_path}")
        return

    content = md_file.read_text(encoding='utf-8')
    
    # Remove existing section if it exists
    pattern_remove = rf'{re.escape(section_title)}.*?(?=\n---\s*\n+## {section_num_bug}\. 결함 보고서)'
    content = re.sub(pattern_remove, '', content, flags=re.DOTALL)
    
    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    table_md = generate_markdown_table(csv_path)
    new_section = f"{section_title}\n\n{table_md}"
    
    pattern_insert = rf'\n---\s*\n+## {section_num_bug}\. 결함 보고서'
    match = re.search(pattern_insert, content)
    if match:
        idx = match.start()
        new_content = content[:idx] + "\n\n" + new_section + content[idx:]
        md_file.write_text(new_content, encoding='utf-8')
        logging.info(f"마크다운 보고서({md_path})의 표가 자동으로 업데이트 되었습니다.")
    else:
        logging.warning(f"마크다운 업데이트 실패: 삽입 위치(## {section_num_bug}. 결함 보고서)를 찾지 못했습니다.")

if __name__ == "__main__":
    update_test_report_md()
