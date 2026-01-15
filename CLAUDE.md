# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the application
uv run main.py
```

## Architecture

LangChain/LangGraph 기반 에이전트 애플리케이션으로, Gradio 웹 인터페이스를 통해 사용자와 상호작용합니다.

- `main.py` - 진입점, Gradio ChatInterface 실행
- `agent.py` - LangGraph의 `create_react_agent`로 에이전트 생성
- `config.py` - 환경변수 기반 설정 (dataclass)
- `tools/search.py` - Whoogle 검색 도구

## Code Style

- `__init__.py` 파일을 사용하지 않음. 명시적 import 경로 사용 (예: `from tools.search import search_tool`)

## Configuration

환경변수로 설정 가능:
- `WHOOGLE_HOST` - Whoogle 검색 서버 주소
- `LLM_BASE_URL` - LLM API 엔드포인트
- `LLM_API_KEY` - LLM API 키
- `LLM_TEMPERATURE` - LLM temperature 값
