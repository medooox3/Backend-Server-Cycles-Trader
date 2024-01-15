from fastapi.routing import APIRouter
from .strategy import router as strategy_router
from .users_management import router as users_router
from .keys import router as keys_router

router = APIRouter()
router.include_router(users_router, prefix="/users")
router.include_router(strategy_router, prefix="/strategy")
router.include_router(keys_router, prefix="/key")


@router.get("/login")
async def login():
    """login and redirect the user to the dashboard"""
    pass


@router.get("/logout")
async def logout():
    """logout and redirect the user to the login route"""
    pass


# ! Todo: is this realy necessary in case of using react ?
@router.get("/dashboard")
async def dashboard():
    """show the dashboard"""
    pass



