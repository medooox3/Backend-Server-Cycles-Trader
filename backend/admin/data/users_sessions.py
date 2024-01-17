from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class UserSession(SQLModel, table=True):
    id:str = Field(primary_key=True)
    user_id: str

class UserSessionModel(BaseModel):
    id: str
    user_id: str
    

# ------ Exceptions ------
class SessionNotFound(Exception):
    def __init__(self, msg:str = "Session Not Found") -> None:
        self.msg = msg
