import json
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus

import feedparser
import requests
from bs4 import BeautifulSoup


# ==================================================
# 1. 현재 시간 조회
# ==================================================
def get_current_time(timezone: str = "Asia/Seoul") -> str:
    """입력한 시간대의 현재 시간을 반환합니다."""

    try:
        now = datetime.now(ZoneInfo(timezone))

        return (
            f"{timezone}의 현재 시간은 "
            f"{now.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}입니다."
        )

    except Exception:
        return "시간대를 확인할 수 없습니다. 예: Asia/Seoul, America/New_York"


# ==================================================
# 2. 날씨 조회
# ==================================================
def get_weather(location: str) -> str:
    """도시 또는 지역명을 입력받아 현재 날씨를 반환합니다."""

    try:
        # 1) 지역명 → 위도/경도 변환
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": location,
                "count": 1,
                "language": "ko",
                "format": "json",
            },
            timeout=10,
        )

        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"'{location}' 지역을 찾을 수 없습니다."

        place = geo_data["results"][0]

        latitude = place["latitude"]
        longitude = place["longitude"]
        place_name = place["name"]
        country = place.get("country", "")

        # 2) 현재 날씨 조회
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=10,
        )

        weather_data = weather_response.json()
        current = weather_data["current"]

        weather_code_map = {
            0: "맑음",
            1: "대체로 맑음",
            2: "부분적으로 흐림",
            3: "흐림",
            45: "안개",
            48: "서리 안개",
            51: "약한 이슬비",
            53: "이슬비",
            55: "강한 이슬비",
            61: "약한 비",
            63: "비",
            65: "강한 비",
            71: "약한 눈",
            73: "눈",
            75: "강한 눈",
            80: "소나기",
            81: "강한 소나기",
            95: "천둥번개",
        }

        weather_text = weather_code_map.get(
            current["weather_code"],
            "알 수 없음"
        )

        return (
            f"[{place_name}, {country}] 현재 날씨\n"
            f"- 상태: {weather_text}\n"
            f"- 기온: {current['temperature_2m']}°C\n"
            f"- 체감온도: {current['apparent_temperature']}°C\n"
            f"- 습도: {current['relative_humidity_2m']}%\n"
            f"- 풍속: {current['wind_speed_10m']} km/h\n"
            f"- 관측 시각: {current['time']}"
        )

    except Exception as e:
        return f"날씨 정보를 조회하는 중 오류가 발생했습니다: {str(e)}"


# ==================================================
# 3. 뉴스 검색
# ==================================================
def search_news(query: str) -> str:
    """Google News RSS를 이용하여 최신 뉴스 제목을 검색합니다."""

    try:
        encoded_query = quote_plus(query)

        rss_url = (
            "https://news.google.com/rss/search?"
            f"q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        )

        feed = feedparser.parse(rss_url)

        if not feed.entries:
            return f"'{query}' 관련 뉴스 결과를 찾을 수 없습니다."

        results = []

        for index, entry in enumerate(feed.entries[:5], start=1):
            title = entry.get("title", "제목 없음")
            link = entry.get("link", "")
            published = entry.get("published", "발행일 정보 없음")

            results.append(
                f"{index}. {title}\n"
                f"   - 발행: {published}\n"
                f"   - 링크: {link}"
            )

        return f"[{query}] 관련 최신 뉴스 검색 결과\n\n" + "\n\n".join(results)

    except Exception as e:
        return f"뉴스 검색 중 오류가 발생했습니다: {str(e)}"


# ==================================================
# 4. 웹 검색
# ==================================================
def search_web(query: str) -> str:
    """DuckDuckGo HTML 검색 결과에서 제목과 링크를 반환합니다."""

    try:
        search_url = "https://html.duckduckgo.com/html/"

        response = requests.post(
            search_url,
            data={"q": query},
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            },
            timeout=10,
        )

        soup = BeautifulSoup(response.text, "html.parser")

        result_items = soup.select(".result")

        if not result_items:
            return f"'{query}'에 대한 웹 검색 결과를 찾을 수 없습니다."

        results = []

        for index, item in enumerate(result_items[:5], start=1):
            title_tag = item.select_one(".result__a")
            snippet_tag = item.select_one(".result__snippet")

            if not title_tag:
                continue

            title = title_tag.get_text(" ", strip=True)
            link = title_tag.get("href", "")
            snippet = (
                snippet_tag.get_text(" ", strip=True)
                if snippet_tag
                else "설명 없음"
            )

            results.append(
                f"{index}. {title}\n"
                f"   - 설명: {snippet}\n"
                f"   - 링크: {link}"
            )

        if not results:
            return f"'{query}'에 대한 웹 검색 결과를 찾을 수 없습니다."

        return f"[{query}] 웹 검색 결과\n\n" + "\n\n".join(results)

    except Exception as e:
        return f"웹 검색 중 오류가 발생했습니다: {str(e)}"


# ==================================================
# OpenAI Tool Schema
# ==================================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "특정 시간대의 현재 날짜와 시간을 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": (
                            "IANA 시간대입니다. "
                            "예: Asia/Seoul, America/New_York, Europe/London"
                        ),
                    }
                },
                "required": ["timezone"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "특정 도시 또는 지역의 현재 날씨를 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": (
                            "날씨를 조회할 도시 또는 지역명입니다. "
                            "예: 서울, 부산, Tokyo, New York"
                        ),
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": "사용자의 검색어와 관련된 최신 뉴스 제목을 검색합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "뉴스 검색어입니다.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "인터넷 웹 검색을 수행하고 관련 페이지 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "웹 검색어입니다.",
                    }
                },
                "required": ["query"],
            },
        },
    },
]