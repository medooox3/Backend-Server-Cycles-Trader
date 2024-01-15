from fastapi import APIRouter


router = APIRouter(tags=["Keys Management"])


# ---- keys Management -------
@router.get("")
async def create_api_key():
    """generate an api key for a user local client and store it in the DB"""
    pass


@router.delete("")
async def remove_api_key(user_id):
    """delete the local client key , must provide the user id"""
    pass


@router.put("")
async def update_api_key():
    """remove old key and generate new one"""
    pass
