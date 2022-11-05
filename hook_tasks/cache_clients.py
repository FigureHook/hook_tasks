import redis

from .configs import RedisSettings

redis_settings = RedisSettings()  # type: ignore
redis_client = redis.Redis(
    username=redis_settings.username,
    password=redis_settings.password,
    host=redis_settings.host,
    port=redis_settings.port,
)
