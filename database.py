from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL Database URL
DATABASE_URL = "mysql+pymysql://root:Atp%404466@localhost:3306/portfolio_d"
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