import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scrapers.base import BaseClient
from playwright.sync_api import sync_playwright
"""HTTP client for making requests to HLTV.org with rate limiting and error handling."""
class HLTVClient(BaseClient):
    def __init__(self):
        self.base_url = "https://www.hltv.org/stats/"

    def get_top_50_teams(self):
        current_date = datetime.now()
        last_three_months = current_date - relativedelta(months=3)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            url = self.base_url + "teams?startDate=" + last_three_months.strftime("%Y-%m-%d") + "&endDate=" + current_date.strftime("%Y-%m-%d") + "&rankingFilter=Top50"

            page.goto(url, timeout=60000)

            page.wait_for_selector("table.stats-table.player-ratings-table", timeout=60000)

            teams = page.query_selector_all("table.stats-table.player-ratings-table tbody tr")

            for row in teams:
                name = row.query_selector("td.teamCol-teams-overview").inner_text()
                print(name)

            browser.close()

client = HLTVClient()
print(client.get_top_50_teams())