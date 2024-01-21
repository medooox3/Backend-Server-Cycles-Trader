from sqlmodel import SQLModel, create_engine
import os


def _get_db_name():
    name = os.environ.get("DB_NAME")
    if not name:
        return "database.db"
    return name


def _get_db_path():
    path = os.path.join(os.path.dirname(__file__), _get_db_name())
    if not path:
        return f"sqlite:///{_get_db_name()}"
    print(path)
    return f"sqlite:///{path}"


def _get_echo():
    echo = os.environ.get("DB_ECHO")
    return echo in ["1", "true", "True"]


sqlite_path = _get_db_path()

engine = create_engine(
    sqlite_path,
    echo=_get_echo(),
    connect_args={
        "check_same_thread": False,
    },
)


def create_tables():
    SQLModel.metadata.create_all(engine)
