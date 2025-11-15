"""Base scraper abstract class defining the interface that all scrapers must implement."""
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def scrape_matches(self) -> JSON:
        pass

    @abstractmethod
    def get_results(self) -> JSON:
        pass

    @abstractmethod
    def get_teams(self) -> JSON:
        pass
    
    @abstractmethod
    def get_team_rankings(self) -> JSON:
        pass

    @abstractmethod
    def get_tournaments(self) -> JSON:
        pass
    
class BaseClient(ABC):
    BASE_URL: str = ""
    
    def request(self, method: str, endpoint: str, **kwargs) -> Response:
        pass

    def get(self, endpoint: str, **kwargs) -> Response:
        pass
    
    def scrape_matches(self) -> Response:
        pass

    def get_results(self) -> Response:
        pass

    def get_teams(self) -> Response:
        pass
    
    def get_team_rankings(self) -> Response:
        pass

    def get_tournaments(self) -> Response:
        pass


