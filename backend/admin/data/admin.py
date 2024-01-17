from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Admin(SQLModel, table=True):
    id: str = Field( primary_key=True)
    name: str
    password_hash: str

class AdminOut(BaseModel):
    id: str
    name: str

class AdminIn(BaseModel):
    name: str
    password: str

# ------ Exceptions -------
class AdminNotCreated(Exception):
    def __init__(self, msg: str = "Admin Not Created") -> None:
        self.msg = msg

class AdminAlreadyExist(Exception):
    def __init__(self, msg: str = "Admin with the same name already exists") -> None:
        self.msg = msg