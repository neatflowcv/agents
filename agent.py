from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from config import Config
from tools.datetime_tool import datetime_tool
from tools.search import search_tool


def create_agent():
    """에이전트를 생성하고 반환합니다."""
    config = Config()
    llm = ChatOpenAI(
        base_url=config.llm_base_url,
        api_key=config.llm_api_key,
        temperature=config.llm_temperature,
    )

    system_prompt = """당신은 도움이 되는 AI 어시스턴트입니다.

질문에 답하기 위해 필요한 모든 도구를 사용하세요.
- 날짜/시간 관련 질문: 먼저 get_datetime으로 현재 날짜를 확인하세요.
- 검색이 필요한 질문: web_search로 최신 정보를 검색하세요.
- "오늘의 날씨" 같은 질문: get_datetime으로 오늘 날짜를 확인한 후, 그 날짜와 함께 web_search를 사용하세요.

여러 도구가 필요하면 순차적으로 모두 사용하세요."""

    return create_react_agent(
        model=llm,
        tools=[search_tool, datetime_tool],
        prompt=system_prompt,
        debug=True,
    )
