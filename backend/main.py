from fastapi import FastAPI

from backend.api.routes.protected.users import router as users_router
from backend.api.routes.public.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="")
app.include_router(users_router, prefix="")


@app.get("/")
async def root():
    return {"status": "Welcome to the API, no need to login to see this"}
