from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    model_config = ConfigDict(env_file=".env")

    APP_NAME: str

    MONGO_URL: str
    DATABASE_NAME: str

    REDIS_URL: str

    QUEUE_NAME: str = "document_queue"
    CACHE_TTL: int = 360
    MAX_ACTIVE_JOBS: int = 3


settings = Settings()