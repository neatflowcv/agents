import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    whoogle_host: str = os.getenv("WHOOGLE_HOST", "http://127.0.0.1:5000")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost/v1")
    llm_api_key: str = os.getenv("LLM_API_KEY", "dummy")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
