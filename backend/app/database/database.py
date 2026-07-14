import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# Read from environment, raise exception if not configured
SQL_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQL_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured. Please create backend/.env.")

# Configure engine with connection pooling settings
engine = create_engine(
    SQL_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
