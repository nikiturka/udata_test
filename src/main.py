import asyncio
from fastapi import FastAPI
from src.db.database import create_tables
from src.routers.items_router import items_router

app = FastAPI()
app.include_router(items_router)


@app.on_event("startup")
async def startup_event():
    create_tables()
