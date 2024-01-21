from sqlmodel import SQLModel, Field
from typing import Optional


class AdminBase(SQLModel):
    name: str = Field(default="Admin", unique=True, primary_key=True)
    email: str = Field(unique=True)


class Admin(AdminBase, table=True):
    password_hash: str


class AdminCreate(AdminBase):
    password: str = Field(min_length=8)


class AdminRead(AdminBase):
    id: int
    name: str
