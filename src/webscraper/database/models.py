"""SQLAlchemy ORM models for matches, players, teams, and related entities."""

from sqlalchemy import Column, Integer, String, Float, DateTime
from .session import Base

class Teams(Base):
    __tablename__ = "teams"

    team_name = Column(String, primary_key=True)
    maps = Column(Integer)
    kd_diff = Column(Integer)
    kd = Column(Float)
    rating = Column(Float)
    updated_at = Column(DateTime)