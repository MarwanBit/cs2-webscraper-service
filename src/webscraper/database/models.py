"""SQLAlchemy ORM models for matches, players, teams, and related entities."""

from sqlalchemy import Column, Integer, String, Float, DateTime, UUID
from .session import Base

class Teams(Base):
    __tablename__ = "teams"

    team_id = Column(UUID, primary_key=True)
    team_name = Column(String)
    country = Column(String)
    maps = Column(Integer)
    kd_diff = Column(Integer)
    kd = Column(Float)
    rating = Column(Float)
    updated_at = Column(DateTime)

class Matches(Base):
    __tablename__ = "matches"

    match_id = Column(UUID, primary_key=True)
    team1_id = Column(UUID)
    team2_id = Column(UUID)
    match_date = Column(DateTime)
    tournament_id = Column(UUID)
    winner = Column(UUID)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)