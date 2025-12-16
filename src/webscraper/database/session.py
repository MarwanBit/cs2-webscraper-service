"""Database session factory for creating and managing database connections and sessions."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(override=True) # change this when moving to production

DATABASE_URL = os.getenv("DATABASE_URL")
# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()