from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from admin import admin_router
from security.web import token_router
from admin.features.users_management.web import users_management_router
from user.features.trading.web import trading_router
from user.features.profile.web import profile_router
from user.features.event import events_router

from security.service import admin_auth_service


app = FastAPI()

# ----------------- Admin -----------------
app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin Profile Management"],
    dependencies=[],
)

# ----------------- Token -----------------
app.include_router(
    token_router,
    prefix="/token",
)

app.include_router(
    users_management_router,
    prefix="/users",
    tags=["Admin Users Management"],
    dependencies=[
        Depends(admin_auth_service.get_admin),
    ],
)


# ----------------- Trading -----------------
app.include_router(
    trading_router,
    prefix="/cycles",
    tags=["User Trading Management"],
)


# ----------------- User Profile -----------------
app.include_router(
    profile_router,
    prefix="/me",
    tags=["User Profile"],
)

# ----------------- User Events -----------------
app.include_router(
    events_router,
    prefix="/events",
    tags=["User Events"],
)

# ----------------- Middleware -----------------
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
