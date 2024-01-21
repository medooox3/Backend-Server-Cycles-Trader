from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DB
    db_name: str = "database.sqlite"
    db_echo: bool = False
    # Secrets
    secret_key: str = "9fe7a24fb495c8a665b58568de6437480fcefb432dcc7f4148af44b92269a753"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
