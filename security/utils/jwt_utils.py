"""
1. create token
    1.1 local access token is valid for 1 year !!!!
    1.2 web access token is valid for 1 day
    1.3 refresh token is valid for 30 days
2. encode token
3. decode and (verify) token
"""


from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import timedelta, datetime

from di import get_settings
from ..model.token_model import TokenData, Token

# Contains secret key and algorithm
config = get_settings()


def create_access_token(token_data: TokenData, expires_delta: timedelta):
   pass