"""Main entry point for the webscraper service application."""

from webscraper.database.session import engine, Base
from webscraper.database import models

def main():
    print("Hello, this project is working")

def init_db():
    print("Creating tables")
    Base.metadata.create_all(bind=engine)
    print("database tables created")

if __name__ == '__main__':
    main()