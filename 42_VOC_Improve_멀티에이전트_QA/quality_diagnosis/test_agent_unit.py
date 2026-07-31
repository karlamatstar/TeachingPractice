# =============================================
# File: quality_diagnosis/test_agent_unit.py
# =============================================
# 에이전트별 단위 테스트
# interpreter부터 improver까지 6개 에이전트 파일의 존재·문법·기본 구조를 점검합니다.
# (서버 실행 없이 정적 검사만 수행하므로 언제든 실행 가능)
#
# 실행: pytest quality_diagnosis/test_agent_unit.py -v

import ast

import pytest
from qa_test_utils import AGENT_FILES, AGENT_PORTS, ROOT

AGENT_NAMES = list(AGENT_FILES.keys())


@pytest.mark.parametrize("agent", AGENT_NAMES)
def test_agent_file_exists(agent):
    """에이전트 소스 파일이 존재하는가."""
    rel_path, _ = AGENT_FILES[agent]
    assert (ROOT / rel_path).exists(), f"{rel_path} 파일이 없습니다"


@pytest.mark.parametrize("agent", AGENT_NAMES)
def test_agent_file_syntax(agent):
    """에이전트 소스 파일이 문법 오류 없이 파싱되는가."""
    rel_path, _ = AGENT_FILES[agent]
    source = (ROOT / rel_path).read_text(encoding="utf-8")
    ast.parse(source)  # SyntaxError 발생 시 테스트 실패


@pytest.mark.parametrize("agent", AGENT_NAMES)
def test_agent_required_symbols(agent):
    """에이전트 파일에 핵심 클래스와 serve 함수가 정의되어 있는가."""
    rel_path, symbols = AGENT_FILES[agent]
    source = (ROOT / rel_path).read_text(encoding="utf-8")
    tree = ast.parse(source)
    defined = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    }
    missing = [s for s in symbols if s not in defined]
    assert not missing, f"{rel_path}에 누락된 심볼: {missing}"


@pytest.mark.parametrize("agent", AGENT_NAMES)
def test_agent_has_main_entry(agent):
    """python -m agents.<name>으로 실행 가능한 진입점(__main__)이 있는가."""
    rel_path, _ = AGENT_FILES[agent]
    source = (ROOT / rel_path).read_text(encoding="utf-8")
    assert '__main__' in source, f"{rel_path}에 __main__ 진입점이 없습니다"


def test_agent_ports_are_unique():
    """6개 에이전트 포트(6001~6006)가 서로 겹치지 않는가."""
    ports = list(AGENT_PORTS.values())
    assert len(ports) == len(set(ports)) == 6
    assert sorted(ports) == [6001, 6002, 6003, 6004, 6005, 6006]


def test_voc_csv_exists_and_has_data():
    """voc.csv 데이터 파일이 존재하고 헤더+데이터가 있는가."""
    csv_path = ROOT / "voc.csv"
    assert csv_path.exists(), "voc.csv가 없습니다"
    lines = csv_path.read_text(encoding="utf-8-sig").strip().splitlines()
    assert len(lines) >= 2, "voc.csv에 데이터 행이 없습니다"
    assert "불만" in lines[0] or "고객" in lines[0], "voc.csv 헤더가 예상과 다릅니다"


def test_proto_file_defines_six_services():
    """voc.proto에 6개 서비스가 모두 정의되어 있는가."""
    proto = (ROOT / "voc.proto").read_text(encoding="utf-8")
    for svc in ["Interpreter", "Retriever", "Summarizer", "Evaluator", "Critic", "Improver"]:
        assert f"service {svc}" in proto, f"voc.proto에 service {svc}가 없습니다"


def test_recommended_cases_include_expected_results():
    """권장 TC-01~TC-10에 질문과 기대 결과가 함께 정의되어 있는가."""
    from qa_test_utils import load_test_cases

    cases = load_test_cases()[:10]
    assert [case["case_id"] for case in cases] == [f"TC-{number:02d}" for number in range(1, 11)]
    for case in cases:
        for field in ("question", "expected_intent", "expected_keywords", "required_output", "prohibited_output"):
            assert field in case, f"{case['case_id']}: {field} 누락"
        assert case["expected_intent"]
        assert case["required_output"]
