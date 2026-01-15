import requests
from langchain_core.tools import Tool

from config import Config


def search_whoogle(query: str) -> str:
    """Whoogle 검색 API를 호출하고 결과를 문자열로 반환합니다."""
    config = Config()
    try:
        response = requests.get(
            f"{config.whoogle_host}/search",
            params={"q": query, "format": "json"},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json()

        if "results" in results:
            formatted_results = []
            for item in results["results"][:5]:
                title = item.get("title", "")
                url = item.get("url", "")
                content = item.get("content", "")
                formatted_results.append(
                    f"제목: {title}\nURL: {url}\n내용: {content}\n"
                )
            return "\n".join(formatted_results)
        return str(results)
    except requests.exceptions.RequestException as e:
        return f"Whoogle 검색 실패: {e}"


search_tool = Tool(
    name="web_search",
    description="웹에서 최신 정보를 검색할 때 사용한다",
    func=search_whoogle,
)
