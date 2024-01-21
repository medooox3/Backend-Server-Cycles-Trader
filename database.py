# import os
from sqlmodel import SQLModel, create_engine
from config import Settings


# def _get_db_name():
#     return _settings.db_name


# def _get_db_path():
#     path = os.path.join(os.path.dirname(__file__), _get_db_name())
#     if not path:
#         return f"sqlite:///{_get_db_name()}"
#     print(path)
#     return f"sqlite:///{path}"

# sqlite_path = _get_db_path()


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
