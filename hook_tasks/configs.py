from typing import Any, Dict, List, Optional

from pydantic import AnyUrl, BaseSettings, Field, HttpUrl, validator


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

    class Config:
        env_file = ".env"


class SpiderSettings(BaseSettings):
    SCRAPY_URL: HttpUrl = Field(..., env="SCRAPY_URL")

    class Config:
        env_file = ".env"


class HookApiSettings(BaseSettings):
    URL: HttpUrl = Field(..., env="HOOK_API_URL")
    TOKEN: str = Field(..., env="HOOK_API_TOKEN")

    class Config:
        env_file = ".env"


class PlurkApiSettings(BaseSettings):
    app_key: str = Field(..., env="PLURK_APP_KEY")
    app_secret: str = Field(..., env="PLURK_APP_SECRET")
    access_token: str = Field(..., env="PLURK_USER_TOKEN")
    access_token_secret: str = Field(..., env="PLURK_USER_SECRET")

    class Config:
        env_file = ".env"


class RedisSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str

    class Config:
        env_file = ".env"