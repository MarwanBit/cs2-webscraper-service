"""Main entry point for the webscraper service application."""

from database.session_factory import engine, Base
from database import models

def main():
    print("Hello, this project is working")

def init_db():
    Base.metadata.create_all(bind=engine)
    print("database tables created")

if __name__ == '__main__':
    main()
    init_db()