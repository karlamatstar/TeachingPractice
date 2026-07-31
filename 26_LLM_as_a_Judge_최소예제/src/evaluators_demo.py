import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_classic.evaluation import load_evaluator
from langchain_openai import ChatOpenAI

# 0. 공통 설정
# 최상위 경로에 있는 .env 파일에서 환경 변수(OPENAI_API_KEY 등)를 불러옵니다.
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# 평가를 수행할 LLM 모델 설정 (주로 GPT-4 수준의 똑똑한 모델을 평가자로 사용합니다)
eval_llm = ChatOpenAI(model="gpt-4o", temperature=0)

def run_qa_evaluator():
    print("=== 1. Question-Answer Evaluator (qa) ===")
    # 단순 맞춤/틀림을 판단하는 평가자
    evaluator = load_evaluator("qa", llm=eval_llm)
    
    result = evaluator.evaluate_strings(
        input="한국의 수도는 어디인가요?",
        prediction="한국의 수도는 부산입니다.",
        reference="한국의 수도는 서울입니다."
    )
    print("평가 결과:", result)
    print()


def run_context_qa_evaluator():
    print("=== 2. Context 기반 답변 Evaluator (context_qa) ===")
    # 정답 대신 제공된 Context를 바탕으로 판단
    evaluator = load_evaluator("context_qa", llm=eval_llm)
    
    result = evaluator.evaluate_strings(
        input="주인공의 이름은 무엇인가요?",
        prediction="주인공의 이름은 앨리스입니다.",
        reference="어느 날 토끼 굴로 떨어져 신비한 나라로 가게 된 앨리스는..." # Context
    )
    print("평가 결과:", result)
    print()


def run_cot_qa_evaluator():
    print("=== 3. Chain-of-Thought Context 기반 Evaluator (cot_qa) ===")
    # Context를 바탕으로 판단하되, 추론(Chain of Thought) 과정을 거침
    evaluator = load_evaluator("cot_qa", llm=eval_llm)
    
    result = evaluator.evaluate_strings(
        input="주인공의 이름은 무엇인가요?",
        prediction="주인공의 이름은 앨리스입니다.",
        reference="어느 날 토끼 굴로 떨어져 신비한 나라로 가게 된 앨리스는..." # Context
    )
    print("평가 결과:", result)
    print()


def run_labeled_criteria_evaluator():
    print("=== 4. Labeled Criteria Evaluator (labeled_criteria) ===")
    # 정답(reference)과 비교하여 특정 기준(예: 정확성)을 만족하는지 평가
    evaluator = load_evaluator("labeled_criteria", criteria="correctness", llm=eval_llm)
    
    result = evaluator.evaluate_strings(
        input="태양계의 3번째 행성은 무엇인가요?",
        prediction="태양계의 세 번째 행성은 화성입니다.",
        reference="지구"
    )
    print("평가 결과:", result)
    print()


def run_labeled_score_string_evaluator():
    print("=== 5. 사용자 정의 점수 Evaluator (labeled_score_string) ===")
    # 1점부터 10점까지 점수를 매기도록 커스텀된 평가자
    evaluator = load_evaluator("labeled_score_string", llm=eval_llm)
    
    result = evaluator.evaluate_strings(
        input="양자역학에 대해 간단히 설명해주세요.",
        prediction="양자역학은 아주 작은 물질들의 상태를 다루는 물리학입니다.",
        reference="양자역학은 원자나 아원자 입자와 같은 미시 세계의 물리적 현상을 연구하는 학문으로, 불확정성 원리와 파동-입자 이중성이 특징입니다."
    )
    print("평가 결과:", result)
    print()


if __name__ == "__main__":
    print("LLM-as-Judge 실습 예제 실행 시작\n" + "-"*40)
    run_qa_evaluator()
    run_context_qa_evaluator()
    run_cot_qa_evaluator()
    run_labeled_criteria_evaluator()
    run_labeled_score_string_evaluator()
    print("모든 평가자 테스트가 완료되었습니다.")
