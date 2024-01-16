from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class User(SQLModel, table=True):
    """DB Model"""

    id: str = Field(primary_key=True)
    name: str
    password_hash: str


class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    id: str
    name: str


# ----------- Errors ------------
class UserNotFound(Exception):
    def __init__(self, msg: str = "User Not Found") -> None:
        self.msg = msg


class UserAlreadyExist(Exception):
    def __init__(self, msg: str = "User with the same name already exists") -> None:
        self.msg = msg
