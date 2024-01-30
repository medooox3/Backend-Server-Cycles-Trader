"""
1. create token
    1.1 local access token is valid for 1 year !!!!
    1.2 web access token is valid for 1 day
    1.3 refresh token is valid for 30 days
2. encode token
3. decode and (verify) token
"""


from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException, status

from dependencies import get_settings
from ..model.token_model import TokenData
from ..model.exceptions import TokenCredentialsException

# Contains secret key and algorithm
config = get_settings()


def create_access_token(token_data: TokenData, expires_delta: timedelta | None = None):
    payload = token_data.model_dump()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.access_token_expire_minutes
        )
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, config.secret_key, algorithm=config.algorithm)

    return encoded_jwt


def verify_token_access(token: str):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])

        sub = payload.get("sub")
        access_session = payload.get("session")

        if sub is None:
            raise TokenCredentialsException

        token_data = TokenData(sub=sub, session=access_session)

        return token_data

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Couldn't verify credentials, {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
