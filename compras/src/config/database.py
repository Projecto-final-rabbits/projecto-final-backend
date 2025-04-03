import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv("src/.env")

if os.getenv("TESTING") == "true" or os.getenv("PYTEST_CURRENT_TEST"):
    database_url = "sqlite:///./test.db"
    connect_args = {"check_same_thread": False}
else:
    database_url = os.getenv("DATABASE_URL")
    connect_args = {}

if not database_url:
    raise ValueError("DATABASE_URL compras no está definido")

engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
