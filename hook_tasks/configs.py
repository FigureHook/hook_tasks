import os
import pathlib
import tempfile
from typing import Any, Dict, List, Optional

from pydantic import AnyUrl, BaseSettings, Field, HttpUrl, validator


def get_celery_settings():
    if os.getenv("ENV") == "test":
        results_dir = pathlib.Path(tempfile.gettempdir()).joinpath(
            "celery_test_results"
        )
        results_dir.mkdir(exist_ok=True)
        return TestCelerySettings(result_backend=results_dir.as_uri())  # type: ignore
    return CelerySettings()  # type: ignore


class CelerySettings(BaseSettings):
    rabbit_user: str = Field(..., env="RABBITMQ_DEFAULT_USER")
    rabbit_pw: str = Field(..., env="RABBITMQ_DEFAULT_PASS")
    rabbit_url: str = Field(..., env="RABBITMQ_URL")
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: List[str] = ["json"]
    enable_utc: bool = True
    broker_url: Optional[AnyUrl] = None

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


class TestCelerySettings(CelerySettings):
    result_backend: str


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
    host: str = Field(..., env="REDIS_HOST")
    port: int = Field(..., env="REDIS_PORT")
    username: str = Field(..., env="REDIS_USERNAME")
    password: str = Field(..., env="REDIS_PASSWORD")

    class Config:
        env_file = ".env"
