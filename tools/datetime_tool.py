from datetime import datetime

from langchain_core.tools import Tool


def get_current_datetime(_: str = "") -> str:
    """현재 날짜와 시간을 반환합니다."""
    now = datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")


datetime_tool = Tool(
    name="get_datetime",
    description="현재 날짜와 시간을 알고 싶을 때 사용한다",
    func=get_current_datetime,
)
