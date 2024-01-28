from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from admin.features.users_management.web import users_management_router
from admin import admin_router
from security.service import auth_service
from user.features.trading.web import trading as user_trading_api
from user.features.profile.web import profile as user_profile


app = FastAPI()

app.include_router(
    users_management_router,
    prefix="/users",
    tags=["Admin Users Management"],
    dependencies=[
        Depends(auth_service.get_admin),
    ],
)
app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin Profile Management"],
    dependencies=[],
)
app.include_router(auth_service.router, prefix="/token")

app.include_router(
    user_trading_api.router,
    prefix="/cycles",
    tags=["User Trading Management"],
)

app.include_router(user_profile.router, prefix="/me", tags=["User Profile"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    import bootstrap

    await bootstrap.on_startup()
