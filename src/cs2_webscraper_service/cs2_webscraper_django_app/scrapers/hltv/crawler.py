from datetime import date, datetime, timedelta
from datetime import datetime
from http.client import HTTPResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from playwright.sync_api import sync_playwright
from .client import HLTVClient


class HLTVCrawler:

    def __init__(self):
        self.base_url = 'https://www.hltv.org'
        self.hltv_client = HLTVClient()

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
        url = f'{self.hltv_client.base_url}/results?startDate={str(start_date)}&endDate={str(end_date)}'
        resp = self.hltv_client._fetch_page(url, '.sidebar-headline', 'debug_hltv_result.html')

        # Now that we have our response we want to go through each .result tag and get their link content
        # notice reach .result has a parent a tage which has the href which is the link to the match
        # what we can do is then get this link, extract the match_id and match_name using regex matching
        bs = BeautifulSoup(resp, 'html.parser')
        print(bs.find('.result').parent.href)

    def crawl_teams(self, start_date: date, end_date: date) -> list[str]:
        pass

    def crawl_team_rankings(self, start_date) -> list[str]:
        pass

    def crawl_tournaments(self, start_date: date, end_date: date) -> list[str]:
        pass


if __name__ == "__main__":
    crawler = HLTVCrawler()
    crawler.crawl_results(date(2026, 1, 20), date(2026, 1, 26))