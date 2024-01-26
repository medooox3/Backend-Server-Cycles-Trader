from pydantic import BaseModel
from di import get_settings


config = get_settings()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    # user name or admin email
    sub: str
    # session uuid
    session: str
    # whether this user is admin or normal user
    admin: bool = False
