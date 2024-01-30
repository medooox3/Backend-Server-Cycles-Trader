from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import Field, BaseModel
import secrets


class Settings(BaseModel):
    # --------- Secrets ---------
    secret_key: str = Field(
        default="477fd452c1709ff2e15d42bc4cf04156f662103f7859c9fd4647e1c3f70cb020"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 3  # 3 days
    refresh_token_expire_minutes: int = 60 * 24 * 15  # 15 days
    local_token_expire_minutes: int = 60 * 24 * 30 * 12 + 5  # 365 days
    # --------- Access session ---------
    # The time after which the user is considered offline =
    session_threshold: int = 5  # 5 minutes
    # --------- DB ---------
    db_path: str = "sqlite:///db.sqlite"
    db_echo: bool = False


# class Settings(BaseSettings):
#     # Secrets
#     secret_key: str = Field(default_factory=lambda: str(secrets.token_hex(32)))
#     algorithm: str = "HS256"
#     access_token_expire_minutes: int = 60 * 24 * 3  # 3 days
#     refresh_token_expire_minutes: int = 60 * 24 * 15  # 15 days
#     local_token_expire_minutes: int = 60 * 24 * 30 * 12 + 5  # 365 days
#     # DB
#     db_path: str = "sqlite:///db.sqlite"
#     db_echo: bool = False

#     model_config = SettingsConfigDict(env_file=".env", extra="allow")


# settings = Settings()

# if __name__ == "__main__":
#     print(settings)
