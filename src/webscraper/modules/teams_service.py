from database.session_factory import SessionLocal
from database.models import Teams

def get_all_teams():
    with SessionLocal() as session:
        return session.query(Teams).all()