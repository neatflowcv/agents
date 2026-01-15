from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from config import Config
from tools.search import search_tool


def create_agent():
    """에이전트를 생성하고 반환합니다."""
    config = Config()
    llm = ChatOpenAI(
        base_url=config.llm_base_url,
        api_key=config.llm_api_key,
        temperature=config.llm_temperature,
    )

    return create_react_agent(
        model=llm,
        tools=[search_tool],
    )
