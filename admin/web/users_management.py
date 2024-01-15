from fastapi import APIRouter


router = APIRouter(tags=["Users Management"])


@router.post("")
async def add_user():
    """create a new user and store him in the DB"""
    pass


@router.delete("")
async def remove_users(users_id: list[int]):
    """remove user completely from the DB"""
    pass


@router.put("")
async def update_user():
    """update user info"""
    pass


@router.get("/{id}")
async def get_user(id):
    """return user using his id"""
    pass


@router.get("/users")
async def get_all_users():
    """return all users from the DB.
    results will be sent to the front-end to filer them"""
    pass
