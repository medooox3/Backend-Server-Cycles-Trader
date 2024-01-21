from fastapi import FastAPI
from users_management import router as users_management_router
from admin import router as admin_router

app = FastAPI()
app.include_router(users_management_router, prefix="/users")
app.include_router(admin_router, prefix="/admin")


@app.on_event("startup")
async def on_startup():
    import bootstrap

    await bootstrap.on_startup()
