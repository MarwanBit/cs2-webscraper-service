"""PandaScore scraper implementation for extracting match, team, and player data from PandaScore API."""
from scrapers.base import BaseScraper
from scrapers.pandascore.config import headers
from datetime import datetime, timedelta, timezone
from scrapers.pandascore.utils import convert_datetime_to_string
import requests
from webscraper.modules.teams_service import get_all_teams

class PandaScoreScraper(BaseScraper):
    
    def __init__(self):
        self.base_url = "https://api.pandascore.co/csgo/"
        self.base_filter = "?filter[videogame_title]=cs-2"
        self.base_pagination = "&page=1&per_page=1"

    def scrape_matches(self):
        pass

    def get_results(self):
        # need to run sql query for this one
        pass

    def get_teams(self):
        pass
    
    def get_team_rankings(self):
        pass

    def get_tournaments(self):
        pass
