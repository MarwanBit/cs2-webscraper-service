"""Base scraper abstract class defining the interface that all scrapers must implement."""
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def scrape_matches(self) -> dict:
        pass

    # @abstractmethod
    # def get_results(self) -> dict:
    #     pass

    # @abstractmethod
    # def get_teams(self) -> dict:
    #     pass
    
    # @abstractmethod
    # def get_team_rankings(self) -> dict:
    #     pass

    # @abstractmethod
    # def get_tournaments(self) -> dict:
    #     pass
    
class BaseClient(ABC):
    BASE_URL: str = ""
    
    def request(self, method: str, endpoint: str, **kwargs):
        pass

    def get(self, endpoint: str, **kwargs):
        pass
    
    def scrape_matches(self):
        pass
    def get_results(self):
        pass

    def get_teams(self):
        pass
    
    def get_team_rankings(self):
        pass

    def get_tournaments(self):
        pass



