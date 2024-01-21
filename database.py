# import os
from sqlmodel import SQLModel, create_engine
from config import Settings


_settings = Settings()

sqlite_path = f"sqlite:///{_settings.db_name}"

engine = create_engine(
    sqlite_path,
    echo=_settings.db_echo,
    connect_args={
        "check_same_thread": False,
    },
)


def create_tables():
    SQLModel.metadata.create_all(engine)
