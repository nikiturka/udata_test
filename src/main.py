import asyncio

from fastapi import FastAPI
from src.db.database import create_tables
from src.services.scraper_service import ScraperService

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    create_tables()
