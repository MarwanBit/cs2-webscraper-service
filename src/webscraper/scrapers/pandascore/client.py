"""HTTP client for making authenticated requests to the PandaScore API with rate limiting."""
from webscraper.scrapers.base import BaseClient
from webscraper.scrapers.pandascore.config import headers
from datetime import datetime, timedelta, timezone
from webscraper.scrapers.pandascore.utils import convert_datetime_to_string
import requests
from webscraper.modules.teams_service import get_all_teams

class PandaScoreClient(BaseClient):
    def __init__(self):
        self.base_url = "https://api.pandascore.co/csgo/"
        self.base_filter = "?filter[videogame_title]=cs-2"
        self.base_pagination = "&page=1&per_page=1"
    
    # when scraping matches, what date range, params, live or historical?
    # If historical, use rest api, if not use websockets
    # take into account rate limits given

    def scrape_matches(self):
        teams = get_all_teams()
        print(teams)
        # current_date = datetime.now(timezone.utc)
        # past_date = current_date - timedelta(hours=24)
        # url = self.base_url + 'matches' + self.base_filter + "&range[begin_at]=" + convert_datetime_to_string(past_date) + "," + convert_datetime_to_string(current_date) + self.base_pagination
        # response = requests.get(url, headers=headers)
        # # add matches to the the db
        # # add teams to the db
        # # add tournaments to the db
        # return response
    
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

