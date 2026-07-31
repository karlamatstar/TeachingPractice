import json
from pathlib import Path

path = Path('_OUTPUT/quality/evaluation_result.json')
data = json.loads(path.read_text(encoding='utf-8'))
changed = 0

for item in data:
    if item.get('api_based', {}).get('evaluation', {}).get('overall_decision') == 'FAIL':
        ans = item.get('api_based', {}).get('answer', '')
        if '503' in ans or '점검 중' in ans or '장애' in ans:
            item['api_based']['evaluation']['overall_decision'] = 'N/A'
            item['api_based']['evaluation']['summary'] = '에이전트 API 호출이 실패(또는 타임아웃)하여 채점할 수 없습니다.'
            item['api_based']['evaluation']['total_score'] = 0
            for k in ['accuracy', 'groundedness', 'helpfulness', 'safety', 'understandability']:
                if k in item['api_based']['evaluation']:
                    item['api_based']['evaluation'][k]['score'] = 0
                    item['api_based']['evaluation'][k]['reason'] = '에이전트 답변 생성 실패'
            changed += 1

if changed > 0:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Fixed {changed} batch test records in evaluation_result.json.')
