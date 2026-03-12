from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


# MySQL Database URL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Optional but recommended
)

# Session Local
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()