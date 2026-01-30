import json, time
from datetime import date, datetime, timedelta
from datetime import datetime
from http.client import HTTPResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
# from .client import HLTVClient
import asyncio
import random
import nodriver as uc


def random_delay(min_sec=0.5, max_sec=1.5):
    return random.uniform(min_sec, max_sec)

class HLTVCrawler:

    async def __init__(self):
        # noting
        self.browser = await uc.start(sandbox=False)


    async def crawl_matches(self, start_date: date, end_date: date) -> list[str]:
        # Need to verify that the matches are at the current day or after (matches must occur in the future)
        pass

    async def crawl_results(self, start_date: date, end_date: date, offset: int) -> list[str]:
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
        # offset should be a multiple of 100

        #(1) INPUT VALIDATION: check that start_date and end_date are in range        
        url = f'https://www.hltv.org/results?startDate={str(start_date)}&endDate={str(end_date)}&offset={offset}'
        page = await self.browser.get(url)
        await page
        await asyncio.sleep(random_delay(3, 5))

    async def crawl_teams(self, start_date: date, end_date: date) -> list[str]:
        pass

    async def crawl_team_rankings(self, start_date) -> list[str]:
        pass

    async def crawl_tournaments(self, start_date: date, end_date: date) -> list[str]:
        pass


if __name__ == "__main__":
    crawler = HLTVCrawler()
    crawler.crawl_results(date(2026, 1, 20), date(2026, 1, 26))