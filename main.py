from langchain_core.tools import Tool
import requests
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import gradio as gr

WHOOGLE_HOST = "http://127.0.0.1:5000"


def search_whoogle(query: str) -> str:
    """Whoogle 검색 API를 호출하고 결과를 문자열로 반환합니다."""
    try:
        response = requests.get(
            f"{WHOOGLE_HOST}/search", params={"q": query, "format": "json"}, timeout=10
        )
        response.raise_for_status()
        results = response.json()

        # JSON 결과를 읽기 쉬운 문자열로 변환
        if "results" in results:
            formatted_results = []
            for item in results["results"][:5]:  # 상위 5개 결과만
                title = item.get("title", "")
                url = item.get("url", "")
                content = item.get("content", "")
                formatted_results.append(
                    f"제목: {title}\nURL: {url}\n내용: {content}\n"
                )
            return "\n".join(formatted_results)
        else:
            return str(results)
    except requests.exceptions.RequestException as e:
        return f"Whoogle 검색 실패: {str(e)}"


def main():
    print("Hello from agents!")

    search_tool = Tool(
        name="web_search",
        description="웹에서 최신 정보를 검색할 때 사용한다",
        func=search_whoogle,
    )

    llm = ChatOpenAI(
        base_url="http://localhost:8080/v1",
        api_key="dummy",
        temperature=0.2,
    )

    agent = create_agent(
        model=llm,
        tools=[search_tool],
        debug=True,  # ★ 중요: 추론 과정 확인
    )

    def chat(msg, history):
        """Gradio ChatInterface용 chat 함수"""
        try:
            result = agent.invoke({"messages": [("user", msg)]})
            # agent 응답에서 메시지 추출
            if "messages" in result and len(result["messages"]) > 0:
                last_message = result["messages"][-1]
                if hasattr(last_message, "content"):
                    return last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    return last_message["content"]
                else:
                    return str(last_message)
            else:
                return str(result)
        except Exception as e:
            return f"오류 발생: {str(e)}"

    gr.ChatInterface(chat).launch()


if __name__ == "__main__":
    main()
