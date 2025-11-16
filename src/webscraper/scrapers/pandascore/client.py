"""HTTP client for making authenticated requests to the PandaScore API with rate limiting."""
from base import BaseClient
class PandaScoreClient(BaseClient):
    BASE_URL: str = super.__init_()
    pandascore_auth_token: str = ""
    
    def __init__(self):
        pass
    
    # when scraping matches, what date range, params, live or historical?
    # If historical, use rest api, if not use websockets
    # take into account rate limits given

    def scrape_matches(self) -> Response:
        pass
    
    # have to figure out api response format to get the results
    
    def get_results(self) -> Response:
        pass

    def get_teams(self) -> Response:
        pass
    
    def get_team_rankings(self) -> Response:
        pass

    def get_tournaments(self) -> Response:
        pass
    

