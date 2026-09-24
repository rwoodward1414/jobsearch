import os
from typing import Iterator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pass")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "jobsearch")

DATABASE_URL = (
  f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
  f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)


def init_db():
  SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
  with Session(engine) as session:
    yield session
