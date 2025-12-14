from webscraper.database.session import SessionLocal
from webscraper.database.models import Teams

def get_all_teams():
    with SessionLocal() as session:
        return session.query(Teams).all()