# import os
from sqlmodel import SQLModel, create_engine
from config import Settings


_settings = Settings()


engine = create_engine(
    _settings.db_path,
    echo=_settings.db_echo,
    connect_args={
        "check_same_thread": False,
    },
)


def create_tables():
    SQLModel.metadata.create_all(engine)
