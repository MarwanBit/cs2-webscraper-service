from datetime import datetime
from http.client import HTTPResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from playwright.sync_api import sync_playwright
import time
import random
from playwright_stealth import Stealth
import asyncio

class HLTVClient:

    def __init__(self):
        #HLTV settings
        self.base_url = 'https://www.hltv.org'

        # Browser settings
        self.browser_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
        self.user_agent = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
        )
        self.viewport = {"width": 1280, "height": 800}
        self.locale = "en-US"

        # timeouts
        self.timeout = 60000

        # Setting up the browser
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False, args=self.browser_args)
        self.context = self.browser.new_context(
            user_agent = self.user_agent,
            viewport = self.viewport,
            locale = self.locale
        )
        self.page = self.context.new_page()

    def _fetch_page(self, url: str, selector: str, debug_file: str) -> str:
        # Sleep in order to maintain timing/ rate limit
        sleep_duration = random.randint(4,10)
        time.sleep(sleep_duration)
        self.page.goto(url, wait_until="domcontentloaded") #domcontentloaded
        # print(self.page.content())
        sleep_duration = random.randint(4,10)
        time.sleep(sleep_duration)
        self.page.wait_for_selector(selector, timeout = self.timeout)
        html = self.page.content()
        sleep_duration = random.randint(4,10)
        time.sleep(sleep_duration)
        if debug_file:
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write(html)
        return html

    def get_match(self, match_id: str, match_name: str) -> HTTPResponse:
        url = f"{self.base_url}/matches/{match_id}/{match_name}"
        return self._fetch_page(url, '.match-page', 'debug_hltv_matches.html')
       
    def get_result(self, match_id: str, match_name: str) -> HTTPResponse:
        # same as get_match with some error handling
        # we should do some verification on the match to ensure that it has a valid result
        return self.get_match(match_id, match_name)

    def get_team(self, team_id: str, team_name: str) -> HTTPResponse:
        url = f"{self.base_url}/team/{team_id}/{team_name}"
        return self._fetch_page(url, '.teamProfile', 'debug_hltv_team.html')

    def get_team_ranking(self, year: str, month: str, day: str, team_id: str, ranking_type: str) -> HTTPResponse:
        # year is numerical: 2026
        # month is lowercase: january, febuary, etc.
        # day is numerial: 24
        # ranking_type is one of : 'valve-ranking', 'ranking', their are others like regional but we don't support them
        # regional addes another argument such as /ranking/teams/2026/january/19/country/United%States?teamid=11124
        url = f"{self.base_url}/{ranking_type}/teams/{year}/{month}/{day}/?teamid={team_id}"
        return self._fetch_page(url, '.hltv-logo-container', 'debug_htlv_tournament_ranking.html')

    def get_tournament(self, tournament_id: str, tournament_name: str) -> HTTPResponse:
        url = f"{self.base_url}/events/{tournament_id}/{tournament_name}"
        print("getting the url")
        return self._fetch_page(url, '.event-hub', 'debug_hltv_tournament.html')

if __name__ == "__main__":
    hltv_client = HLTVClient()
    hltv_client.get_match('2389280', 'paravision-vs-furia-blast-bounty-2026-season-1-finals')
    hltv_client.get_team('9565', 'vitality')
    hltv_client.get_tournament('8575', 'iem-krakw-2026-stage-1')
    # this is vitality team_ranking (valve ranking)
    hltv_client.get_team_ranking("2026", "january", '24', '95665', 'valve-ranking')