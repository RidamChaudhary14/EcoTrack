import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_connection():
    # Explicitly load .env
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / ".env")
    
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("✗ Database connection failed: DATABASE_URL is not configured.")
        return

    # Mask password for printing
    masked_url = database_url
    if "@" in database_url and ":" in database_url:
        try:
            parts = database_url.split("@")
            user_pass = parts[0].split(":")
            if len(user_pass) >= 3:
                masked_url = f"{user_pass[0]}:{user_pass[1]}:****@{parts[1]}"
        except Exception:
            pass

    print(f"Testing connection to: {masked_url}")

    try:
        # Create an engine to test the connection
        engine = create_engine(database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            # Execute a simple query
            connection.execute(text("SELECT 1"))
            print("✓ Database connected successfully")
    except SQLAlchemyError as e:
        print(f"✗ Database connection failed: {e}")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_connection()
