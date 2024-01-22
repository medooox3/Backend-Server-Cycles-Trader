from pydantic import BaseModel
from di import get_settings


config = get_settings()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str
    admin: bool = False
