from datetime import datetime
from http.client import HTTPResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import random
import asyncio
import nodriver as uc


def random_delay(min_sec=0.5, max_sec=1.5):
    return random.uniform(min_sec, max_sec)

class HLTVClient:

    def __init__(self):
        #HLTV settings
        self.base_url = 'https://www.hltv.org'
        self.browser = None

    @classmethod
    async def create(cls):
        instance = cls()
        instance.browser = await uc.start(sandbox=False)
        return instance

    async def _fetch_page(self, url: str, selector: str, debug_file: str) -> str:
        # Sleep in order to maintain timing/ rate limit
        sleep_duration = random.randint(4,10)
        time.sleep(sleep_duration)

        page = await self.browser.get(url)
        sleep_duration = random.randint(4,10)
        time.sleep(sleep_duration)

        html = await page.get_content()
        sleep_duration = random.randint(4,10)
        time.sleep(sleep_duration)

        if debug_file:
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write(html)
        return html

    async def get_match(self, match_id: str, match_name: str) -> HTTPResponse:
        url = f"{self.base_url}/matches/{match_id}/{match_name}"
        res = await self._fetch_page(url, '.match-page', 'debug_hltv_matches.html')
        return res
       
    async def get_result(self, match_id: str, match_name: str) -> HTTPResponse:
        # same as get_match with some error handling
        # we should do some verification on the match to ensure that it has a valid result
        res = await self.get_match(match_id, match_name)
        return res
        
    async def get_team(self, team_id: str, team_name: str) -> HTTPResponse:
        url = f"{self.base_url}/team/{team_id}/{team_name}"
        res = await self._fetch_page(url, '.teamProfile', 'debug_hltv_team.html')
        return res

    async def get_team_ranking(self, year: str, month: str, day: str, team_id: str, ranking_type: str) -> HTTPResponse:
        # year is numerical: 2026
        # month is lowercase: january, febuary, etc.
        # day is numerial: 24
        # ranking_type is one of : 'valve-ranking', 'ranking', their are others like regional but we don't support them
        # regional addes another argument such as /ranking/teams/2026/january/19/country/United%States?teamid=11124
        url = f"{self.base_url}/{ranking_type}/teams/{year}/{month}/{day}/?teamid={team_id}"
        res = await self._fetch_page(url, '.hltv-logo-container', 'debug_hltv_tournament_ranking.html')
        return res

    async def get_tournament(self, tournament_id: str, tournament_name: str) -> HTTPResponse:
        url = f"{self.base_url}/events/{tournament_id}/{tournament_name}"
        print("getting the url")
        res = await self._fetch_page(url, '.event-hub', 'debug_hltv_tournament.html')
        return res

if __name__ == "__main__":
    async def main():
        hltv_client = await HLTVClient.create()
        await hltv_client.get_match('2389280', 'paravision-vs-furia-blast-bounty-2026-season-1-finals')
        await hltv_client.get_team('9565', 'vitality')
        await hltv_client.get_tournament('8575', 'iem-krakw-2026-stage-1')
        # this is vitality team_ranking (valve ranking)
        await hltv_client.get_team_ranking("2026", "january", '24', '95665', 'valve-ranking')
    uc.loop().run_until_complete(main())