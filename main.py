from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

# Explicitly load backend/.env
BASE_DIR = Path(__file__).resolve().parent / "backend"
load_dotenv(BASE_DIR / ".env")

# Fetch DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")
