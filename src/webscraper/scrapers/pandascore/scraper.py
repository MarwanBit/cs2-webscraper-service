"""PandaScore scraper implementation for extracting match, team, and player data from PandaScore API."""
from scrapers.base import BaseScraper
from scrapers.pandascore.config import headers
import requests

class PandaScoreScraper(BaseScraper):
    
    def __init__(self):
        self.base_url = "https://api.pandascore.co/csgo/"
        self.filter = "?filter[videogame_title]=cs-2&page=1&per_page=1"
    
    def scrape_matches(self):
        url = self.base_url + 'matches' + self.filter
        response = requests.get(url, headers=headers)
        return response

    def get_results(self):
        pass

    def get_teams(self):
        pass
    
    def get_team_rankings(self):
        pass

    def get_tournaments(self):
        pass

# scraper = PandaScoreScraper()
# print(scraper.scrape_matches().text)