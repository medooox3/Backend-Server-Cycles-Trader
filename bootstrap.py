def load_dotenv():
    import dotenv

    dotenv.load_dotenv()


def init_db():
    # ! Must import all SqlModel tables before running this function
    from database import create_tables

    create_tables()


async def on_startup():
    load_dotenv()
    init_db()
