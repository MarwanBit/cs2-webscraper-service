"""HTTP client for making authenticated requests to the PandaScore API with rate limiting."""
import os
import django
import sys
# insert absolute path, only for debugging
PROJECT_ROOT = "/app/src/cs2_webscraper_service/cs2_webscraper_django_app"
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs2_webscraper_django_app.cs2_webscraper_django_app.settings")
# print(sys.path) for debugging path issues
# print(sys.executable) ^
django.setup()
from cs2_webscraper_service.cs2_webscraper_django_app.scrapers.base import BaseClient
from cs2_webscraper_service.cs2_webscraper_django_app.scrapers.pandascore.config import headers
from datetime import datetime, timedelta, timezone
from cs2_webscraper_service.cs2_webscraper_django_app.scrapers.pandascore.utils import convert_datetime_to_string
import requests
# from cs2_webscraper_service.cs2_webscraper_django_app.modules.teams_service import get_all_teams
from cs2_webscraper_service.cs2_webscraper_django_app.core.models import Team
class PandaScoreClient(BaseClient):
    def __init__(self):
        self.base_url = "https://api.pandascore.co/csgo/"
        self.base_filter = "?filter[videogame_title]=cs-2"
        self.base_pagination = "&page=1&per_page=1"
    
    # when scraping matches, what date range, params, live or historical?
    # If historical, use rest api, if not use websockets
    # take into account rate limits given

    def scrape_matches(self):
        teams = Team.objects.all()
        current_date = datetime.now(timezone.utc)
        past_date = current_date - timedelta(hours=24)
        # for testing
        # current_date = "2026-01-12T22:44:15.508742Z"
        # past_date = "2026-01-11T22:44:15.508742Z"
        for t in teams:
            # for testing
            # url = self.base_url + 'matches' + self.base_filter + "&filter[opponent_id]=" + t.name.lower() + "&range[begin_at]=" + past_date + "," + current_date + self.base_pagination
            url = self.base_url + 'matches' + self.base_filter + "&filter[opponent_id]=" + t.name.lower() + "&range[begin_at]=" + convert_datetime_to_string(past_date) + "," + convert_datetime_to_string(current_date) + self.base_pagination
            print(url)
            response = requests.get(url, headers=headers)
            print(response.text)
        # add matches to the the db
        # add teams to the db
        # add tournaments to the db
        return ""
    
    # have to figure out api response format to get the results
    
    def get_results(self):
        # fetch leftover matches from db
        matches = ["123", "456", "789"]
        for match_id in matches:
            url = self.base_url + "matches/" + match_id
            response = requests.get(url, headers=headers)
            # insert to results table in db


    def get_teams(self):
        pass
    
    def get_team_rankings(self):
        pass

    def get_tournaments(self):
        pass

# print(datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))
# print((datetime.now(timezone.utc) - timedelta(hours=24)).isoformat().replace('+00:00', 'Z'))
# dt_str = datetime.now(timezone.utc) - timedelta(hours=24)
# print(datetime.now(timezone.utc).isoformat())
client = PandaScoreClient()
print(client.scrape_matches())

