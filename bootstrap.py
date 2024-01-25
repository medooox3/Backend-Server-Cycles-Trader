def load_dotenv():
    import dotenv

    dotenv.load_dotenv()


def init_db():
    # ! Must import all SqlModel tables before running this function
    from database import create_tables
    from admin.data.admin import Admin
    from users_management.data import User, License
    from user.cycles.data.cycle import Cycle

    create_tables()


async def on_startup():
    # load_dotenv()
    init_db()
