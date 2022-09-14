import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", default='postgres')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default='postgres')
DB_HOST = os.getenv("DB_HOST", default='db')
DB_NAME = os.getenv("DB_NAME", default='postgres')
DB_PORT = os.getenv("DB_PORT", default='5432')

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:" \
         f"{DB_PORT}/{DB_NAME}"


engine = create_engine(DB_URL, connect_args={"options": "-c timezone=utc"})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
