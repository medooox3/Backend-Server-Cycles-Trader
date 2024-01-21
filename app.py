from fastapi import FastAPI
from users_management import router as users_management_router

app = FastAPI()
app.include_router(users_management_router, prefix="/users")

@app.on_event("startup")
async def on_startup():
    import bootstrap

    await bootstrap.on_startup()
