import json, time
from datetime import date, datetime, timedelta
from datetime import datetime
from http.client import HTTPResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
# from .client import HLTVClient
from zenrows import ZenRowsClient
import cloudscraper

class HLTVCrawler:

    def __init__(self):
        # noting
        self.scraper = cloudscraper.create_scraper(debug=True)
        pass

    def crawl_matches(self, start_date: date, end_date: date) -> list[str]:
        # Need to verify that the matches are at the current day or after (matches must occur in the future)
        pass

    def crawl_results(self, start_date: date, end_date: date) -> list[str]:
        # must verify that the results are within a range that is before or during the current day (results must be in the past)
        # notice here are some example API routes/ routes for crawl
        # hltv.org/results?startDate=2025-12-26&endDate=2026-01-26
        # the results are paginated aswell, checkout the following
        # hltv.org/results?offset=100&startDate=2025-12-26&endDate=2026-01-26
        # we need to change the offset for pagination
        # we also don't need to set the offset to being a multiple of 100, we can do 115 as an offset for example
        # other routes are the following
        # hltv.org/startDate=2025-10-25&endDate=2026-01-26&starts=1&matchType=Lan&map=de_train&team={team_id}
        #  Lot's of really cool filter for the api
        # you can also do things like the following
        # hltv.org/matches?archive

        #(1) INPUT VALIDATION: check that start_date and end_date are in range        
        url = f'https://www.hltv.org/results?startDate={str(start_date)}&endDate={str(end_date)}'
        print(url)
        print(self.scraper.get(url).text)

    def crawl_teams(self, start_date: date, end_date: date) -> list[str]:
        pass

    def crawl_team_rankings(self, start_date) -> list[str]:
        pass

    def crawl_tournaments(self, start_date: date, end_date: date) -> list[str]:
        pass


if __name__ == "__main__":
    crawler = HLTVCrawler()
    crawler.crawl_results(date(2026, 1, 20), date(2026, 1, 26))