from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    web_origin: str = "http://127.0.0.1:3000"
    openai_api_key: str = ""
    openai_model: str = "gpt-6.1-sol"
    pager_model: str = ""
    target_url: str = "http://127.0.0.1:8010"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
