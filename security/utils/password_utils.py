'''
1. verify password (plain_password, hashed_password) -> bool
2. get_password_hash(password) -> return hashed password
'''
import logging as _logging
from passlib.context import CryptContext as _CryptContext


_logging.getLogger("passlib").setLevel(_logging.ERROR)
_password_context = _CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return _password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return _password_context.hash(password)
