import json, time
from datetime import date, datetime, timedelta
from datetime import datetime
from http.client import HTTPResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from .client import HLTVClient
import asyncio
import random
import nodriver as uc
import re


def random_delay(min_sec=0.5, max_sec=1.5):
    return random.uniform(min_sec, max_sec)

class HLTVCrawler:

    def __init__(self):
        # noting
        self.hltv_client = None

    @classmethod
    async def create(cls):
        instance = cls()
        instance.hltv_client = await HLTVClient.create()
        return instance
    
    async def crawl_matches(self, date: date) -> list[str]:
        # Need to verify that the matches are at the current day or after (matches must occur in the future)
        url = f'{self.hltv_client.base_url}/matches?selectedDate={date.year}-{date.month}-{date.day}'
        html = await self.hltv_client._fetch_page(url, '.matches', 'hltv_matches.html')

        soup = BeautifulSoup(html, 'html.parser')
        res = []
        # Notice these matches use non-relative links unlike results
        pattern = re.compile(r"^https://www.hltv.org/matches/(?P<match_id>[^/]+)/(?P<match_name>[^/]+)$")
        for result in soup.find_all(class_="match"):
            a_tag = result.find("a")
            link = a_tag['href']
            m = pattern.match(link)
            if m:
                match_id = m.group("match_id")
                match_name = m.group("match_name")
                res.append({
                    "match_id": match_id,
                    "match_name": match_name
                })
        print(res)
        return res

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
        url = f'{self.hltv_client.base_url}/results?startDate={str(start_date)}&endDate={str(end_date)}&offset={offset}'
        html = await self.hltv_client._fetch_page(url, '.results', 'hltv_result.html')

        soup = BeautifulSoup(html, 'html.parser')

        res = []
        pattern = re.compile(r"^/matches/(?P<match_id>[^/]+)/(?P<match_name>[^/]+)$")
        for result in soup.find_all(class_="result-con"):
            a_tag = result.find(class_="a-reset")
            link = a_tag['href']
            m = pattern.match(link)
            if m:
                match_id = m.group("match_id")
                match_name = m.group("match_name")
                res.append({
                    "match_id": match_id,
                    "match_name": match_name
                })
        print(res)
        return res

    async def crawl_teams(self, year: str, month: str, day: str) -> list[str]:
        '''
        maybe we also want to add some sort of navigation here, since you only have rankings available
        every week or so on specific dates, so not every year, month, day combo works.

        valve-raking has it available each day though, so this could be helpful, additional api endpoints 
        are the following

        http://hltv.org/2026/january/5/region/Europe
        '''
        url = f'{self.hltv_client.base_url}/valve-ranking/teams/{year}/{month}/{day}'
        html_content = await self.hltv_client._fetch_page(url, '.teams', 'hltv_teams.html')
        
        soup = BeautifulSoup(html_content, 'html.parser')
        res = []
        pattern = re.compile(r"^https://www.hltv.org/team/(?P<team_id>[^/]+)/(?P<team_name>[^/]+)$")
        for result in soup.find_all(class_="ranked-team standard-box"):
            line_up = result.find(class_="lineup-con hidden")
            team_link = line_up.find(class_="more").find(class_="moreLink")['href']
            m = pattern.match(team_link)
            if m:
                team_id = m.group("team_id")
                team_name = m.group("team_name")
                res.append({
                    "team_id": team_id,
                    "team_name": team_name
                })
        print(res)
        return res

    async def crawl_team_rankings(self, year: str, month: str, day: str, ranking_type: str) -> list[str]:
        url = f'{self.hltv_client.base_url}/valve-rankings/teams/{year}/{month}/{day}'
        res = await self.hltv_client._fetch_page(url, '.regional-ranking-header', 'hltv_team_rankings.html')
        pass

    async def crawl_tournaments(self, start_date: date, end_date: date) -> list[str]:
        # We want to scrape the upcoming tournaments so we'll ignore start and end date for now
        # example of the API end points
        # for upcoming and future events they are all on the following endpoint:
        # https://www.hltv.org/events
        # for historical events you have to go to the following
        # https://www.hltv.org/events/archive?startDate={start_date}&endDate={end_date}&eventType={EVENT_TYPE}&prizeMin&prizeMax&player={playerId}
        # &valveRanked=RANKED
        url = f'{self.hltv_client.base_url}/events'
        res = await self.hltv_client._fetch_page(url, '.events', 'hltv_events.html')
        return res


if __name__ == "__main__":
    async def main():
        crawler = await HLTVCrawler.create()
        await crawler.crawl_results(date(2026, 1, 20), date(2026, 1, 26), 0)
    uc.loop().run_until_complete(main())