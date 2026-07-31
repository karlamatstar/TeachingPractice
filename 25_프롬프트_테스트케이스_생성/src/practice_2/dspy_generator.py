import dspy
import os
from pathlib import Path
from dotenv import load_dotenv

# 최상단 경로에 있는 .env 파일에서 환경 변수(API 키) 로드
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# 1. 언어 모델 설정 (OpenAI GPT-4o-mini 사용)
llm = dspy.LM('openai/gpt-4o-mini', api_key=os.environ.get("OPENAI_API_KEY"))
dspy.configure(lm=llm)

# 2. DSPy Signature 정의 (입력 변수와 출력 변수를 선언)
class GenerateQATestCases(dspy.Signature):
    """QA 전문가로서, 주어진 설정값에 맞춰 검색 엔진 평가용 테스트 케이스를 생성합니다."""
    
    domain = dspy.InputField(desc="테스트할 기능 도메인 (예: 영화 검색, 쇼핑몰 검색)")
    quality_metric = dspy.InputField(desc="평가할 품질 지표 (예: 이해도, 안전성, 정확성)")
    search_type = dspy.InputField(desc="사용할 검색 형태 (예: 자연어 질문형, 복합 조건 검색)")
    tc_type = dspy.InputField(desc="테스트 케이스 유형 (Happy, Edge, Negative)")
    difficulty = dspy.InputField(desc="난이도 (Low, Medium, High)")
    count = dspy.InputField(desc="생성할 테스트 케이스의 개수")
    
    test_cases = dspy.OutputField(desc="생성된 테스트 케이스 목록. 각 케이스는 [질문, 기대 결과, 답변 주의 요소]를 반드시 포함해야 합니다.")

# 3. DSPy Module 정의
class QAGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        # ChainOfThought를 사용하면 모델이 중간에 논리적 추론(이유)을 거친 후 결과를 출력하여 품질이 높아집니다.
        self.generate = dspy.ChainOfThought(GenerateQATestCases)
        
    def forward(self, domain, quality_metric, search_type, tc_type, difficulty, count):
        result = self.generate(
            domain=domain,
            quality_metric=quality_metric,
            search_type=search_type,
            tc_type=tc_type,
            difficulty=difficulty,
            count=count
        )
        return result

# 4. 실행 예시 (대화형 입력 방식)
if __name__ == "__main__":
    generator = QAGenerator()
    
    print("=== [DSPy 기반 테스트 케이스 생성 시작] ===")
    print("테스트 케이스 생성을 위한 변수들을 입력해주세요.")
    print("(입력하지 않고 엔터를 누르면 기본값이 사용됩니다.)\n")
    
    domain_input = input("1. 도메인 (기본값: 배달 앱 메뉴 검색): ") or "배달 앱 메뉴 검색"
    quality_input = input("2. 품질지표 (기본값: 일관성): ") or "일관성"
    search_input = input("3. 검색형태 (기본값: 비교/선택 검색): ") or "비교/선택 검색"
    tc_type_input = input("4. 유형 (기본값: Edge): ") or "Edge"
    diff_input = input("5. 난이도 (기본값: Medium): ") or "Medium"
    count_input = input("6. 개수 (기본값: 3): ") or "3"
    
    print("\nAI가 프롬프트를 바탕으로 추론 중입니다. 잠시만 기다려주세요...\n")
    
    response = generator(
        domain=domain_input,
        quality_metric=quality_input,
        search_type=search_input,
        tc_type=tc_type_input,
        difficulty=diff_input,
        count=count_input
    )
    
    print("=== [생성 완료] ===")
    print(response.test_cases)
