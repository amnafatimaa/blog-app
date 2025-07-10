from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

database_url = os.getenv("DATABASE_URL")

# Create engine with optimized PostgreSQL settings
engine = create_engine(
    database_url,
    pool_size=5,              # Limit connection pool size
    max_overflow=10,          # Allow overflow connections
    pool_timeout=30,          # Timeout for getting a connection
    pool_pre_ping=True,       # Check connection health
    echo=False                # Disable SQL logging for production
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
