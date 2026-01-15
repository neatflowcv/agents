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

다음 키워드가 포함된 질문은 반드시 get_datetime을 먼저 실행하세요:
- 오늘, 내일, 어제, 이번 주, 이번 달, 올해
- 최신, 최근, 새로운, 신곡, 신작
- 현재, 지금, 요즘

그 후 web_search로 검색할 때 날짜 정보를 포함하세요.

여러 도구가 필요하면 순차적으로 모두 사용하세요."""

    return create_react_agent(
        model=llm,
        tools=[search_tool, datetime_tool],
        prompt=system_prompt,
        debug=True,
    )
