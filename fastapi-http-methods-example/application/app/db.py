
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os


class Base(DeclarativeBase):
    pass


def get_database_url() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "fastapi_db")
    user = os.getenv("DB_USER", "fastapi_user")
    password = os.getenv("DB_PASSWORD", "fastapi_pass")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
