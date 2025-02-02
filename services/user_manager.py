# services/user_manager.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models.user_model import Base, User

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "newsletterai")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "yourpassword")
DB_NAME = os.getenv("POSTGRES_DB", "newsletterai")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")

# SQLAlchemy setup
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize tables (run once)
Base.metadata.create_all(bind=engine)