from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # DB
    db_name: str = "database.sqlite"
    db_echo: bool = False
    # Secrets
    secret_key: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

if __name__ == '__main__':
    print(settings)