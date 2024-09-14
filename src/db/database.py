import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_HOST = os.environ.get("POSTGRES_HOST")

engine = create_engine(
    url=f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)


def create_tables():
    Base.metadata.create_all(engine)


def get_session():
    with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    pass
