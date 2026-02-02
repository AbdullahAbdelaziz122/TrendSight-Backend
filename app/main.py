from typing import Union
from functools import lru_cache
from .configs import configs
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

