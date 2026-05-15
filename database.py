from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# ======================
# LOAD ENV
# ======================
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not found")

# ======================
# ENGINE
# ======================
engine = create_engine(
    DATABASE_URL,

    echo=True,

    # Prevent stale/disconnected connections
    pool_pre_ping=True,
    pool_recycle=3600,

    # Connection pool settings
    pool_size=5,
    max_overflow=10,

    # Neon/PostgreSQL SSL
    connect_args={
        "sslmode": "require"
    }
)

# ======================
# SESSION
# ======================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ======================
# BASE
# ======================
Base = declarative_base()

# ======================
# DB DEPENDENCY
# ======================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()