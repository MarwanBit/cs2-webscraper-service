"""PandaScore scraper implementation for extracting match, team, and player data from PandaScore API."""
from scrapers.base import BaseScraper
from scrapers.pandascore.config import headers
from datetime import datetime, timedelta, timezone
import requests
class PandaScoreScraper(BaseScraper):
    
    def __init__(self):
        self.base_url = "https://api.pandascore.co/csgo/"
        self.base_filter = "?filter[videogame_title]=cs-2"
        self.base_pagination = "&page=1&per_page=1"
    def scrape_matches(self):
        current_date = datetime.now(timezone.utc)
        past_date = current_date - timedelta(hours=24)
        url = self.base_url + 'matches' + self.base_filter + "&filter[begin_at][0]=" + past_date.isoformat() + "&filter[end_at][0]=" + current_date.isoformat() + self.base_pagination
        print(url)
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

# print((datetime.now(timezone.utc) - timedelta(hours=24)).isoformat())
# dt_str = datetime.now(timezone.utc) - timedelta(hours=24)
# print(datetime.now(timezone.utc).isoformat())
scraper = PandaScoreScraper()
print(scraper.scrape_matches().text)