from pydantic import HttpUrl
from pydantic_settings import BaseSettings,SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )
    host: str
    email_user: str 
    api_key: str 