from typing import Any, Dict, List, Optional

from pydantic import AnyUrl, BaseSettings, Field, validator, HttpUrl


class CelerySettings(BaseSettings):
    rabbit_user: str = Field(..., env="RABBITMQ_DEFAULT_USER")
    rabbit_pw: str = Field(..., env="RABBITMQ_DEFAULT_PASS")
    rabbit_url: str = Field(..., env="RABBITMQ_URL")
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: List[str] = ["json"]
    enable_utc: bool = True
    broker_url: Optional[AnyUrl] = None
    # timezone: str = 'Asia/Tokyo'

    @validator("broker_url", pre=True)
    def concat_broker_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        user = values.get("rabbit_user")
        pw = values.get("rabbit_pw")
        url = values.get("rabbit_url")
        return f"pyamqp://{user}:{pw}@{url}/"


class SpiderSettings(BaseSettings):
    SCRAPY_URL: HttpUrl = Field(..., env="SCRAPY_URL")
