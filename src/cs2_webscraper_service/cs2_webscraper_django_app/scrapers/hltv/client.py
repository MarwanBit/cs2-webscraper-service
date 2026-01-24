from datetime import datetime
from http.client import HTTPResponse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from playwright.sync_api import sync_playwright

class HLTVClient:

    def __init__(self):
        self.base_url = 'https://www.hltv.org'
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


    def get_match(self, match_id: str, match_name: str) -> HTTPResponse:
        url = self.base_url + '/matches' + '/' + match_id + '/' + match_name
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=self.browser_args)
            context = browser.new_context(
                user_agent = self.user_agent,
                viewport = self.viewport,
                locale = self.locale
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector(".match-page", timeout=60000)
            html = page.content()
            with open("debug_hltv_matches.html", "w", encoding="utf-8") as f:
                f.write(html)
            browser.close()

    def get_result(self, match_id: str, match_name: str) -> HTTPResponse:
        # same as get_match with some error handling
        pass

    def get_team(self, team_id: str, team_name: str) -> HTTPResponse:
        url = self.base_url + '/team' + '/' + team_id + '/' + team_name
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=self.browser_args)
            context = browser.new_context(
                user_agent = self.user_agent,
                viewport = self.viewport,
                locale = self.locale
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector(".teamProfile", timeout=60000)
            html = page.content()
            with open("debug_hltv_team.html", "w", encoding="utf-8") as f:
                f.write(html)
            browser.close()

    def get_team_ranking(self, team_id: str, date: datetime) -> HTTPResponse:
        pass

    def get_tournament(self, tournament_id: str) -> HTTPResponse:
        pass

if __name__ == "__main__":
    hltv_client = HLTVClient()
    hltv_client.get_team('9565', 'vitality')