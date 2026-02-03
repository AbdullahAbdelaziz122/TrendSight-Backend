from fastapi import FastAPI
from . import models
from .routers import user, auth
from .database import engine

app = FastAPI()

# FIX: Use a startup event to run the sync function safely
@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        # run_sync bridges the async engine to the sync create_all method
        await conn.run_sync(models.Base.metadata.create_all)

app.include_router(user.router)
app.include_router(auth.router)