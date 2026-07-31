"""LangChain 에이전트가 사용할 도구 모음"""

import ast
import operator
from typing import Any

import requests
from langchain.tools import tool

from config import settings


@tool
def get_weather(location: str) -> str:
    """특정 지역의 예시 날씨 정보를 조회합니다."""

    return f"{location}의 날씨는 맑고 28도입니다."


@tool
def get_schedule(date: str) -> str:
    """특정 날짜의 예시 일정을 조회합니다. 날짜는 YYYY-MM-DD 형식을 권장합니다."""

    return f"{date} 일정: 10시 팀 회의, 14시 고객사 미팅 예정입니다."


@tool
def send_email(content: str) -> str:
    """이메일 발송을 흉내 내는 예시 도구입니다. 실제 이메일은 발송하지 않습니다."""

    return f"이메일 전송 완료로 가정합니다.\n---\n{content}"


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval_node(node: ast.AST) -> int | float:
    """허용된 숫자 연산만 계산합니다."""

    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("허용되지 않은 연산자입니다.")
        left = _safe_eval_node(node.left)
        right = _safe_eval_node(node.right)
        return _ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("허용되지 않은 단항 연산자입니다.")
        operand = _safe_eval_node(node.operand)
        return _ALLOWED_OPERATORS[operator_type](operand)

    raise ValueError("숫자, 괄호, 사칙연산, 거듭제곱만 사용할 수 있습니다.")


@tool
def calculate(expression: str) -> str:
    """숫자 수식을 안전하게 계산합니다. 예: 3 * (4 + 2), 2 ** 8"""

    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval_node(tree)
        return f"{expression} = {result}"
    except Exception as exc:
        return f"계산 오류: {exc}"


@tool
def search_serper(query: str) -> str:
    """Serper.dev API를 사용하여 Google 검색 결과 상위 3개를 가져옵니다."""

    if not settings.serper_api_key:
        return "SERPER_API_KEY가 설정되지 않아 검색을 실행할 수 없습니다. .env 파일을 확인하세요."

    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "gl": "kr",
        "hl": "ko",
    }
    headers = {
        "X-API-KEY": settings.serper_api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        results: dict[str, Any] = response.json()
        organic = results.get("organic", [])[:3]

        if not organic:
            return "검색 결과가 없습니다."

        lines = []
        for index, item in enumerate(organic, start=1):
            title = item.get("title", "제목 없음")
            link = item.get("link", "링크 없음")
            snippet = item.get("snippet", "")
            line = f"{index}. {title}\n   {link}"
            if snippet:
                line += f"\n   요약: {snippet}"
            lines.append(line)

        return "\n".join(lines)
    except Exception as exc:
        return f"검색 중 오류 발생: {exc}"


ALL_TOOLS = [
    get_weather,
    get_schedule,
    send_email,
    calculate,
    search_serper,
]
